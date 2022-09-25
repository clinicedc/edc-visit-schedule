from __future__ import annotations

import re
from decimal import Decimal

from django.apps import apps as django_apps
from django.core.management.color import color_style

from ..site_visit_schedules import SiteVisitScheduleError, site_visit_schedules
from ..subject_schedule import (
    NotOnScheduleError,
    NotOnScheduleForDateError,
    SubjectSchedule,
    SubjectScheduleError,
)
from ..visit import Visit
from .visit_collection import VisitCollection
from .window import Window

style = color_style()


class ScheduleNameError(Exception):
    pass


class AlreadyRegisteredVisit(Exception):
    pass


class VisitTimepointError(Exception):
    pass


class Schedule:
    """A class that represents a "schedule" of visits.

    Is contained by a "visit schedule".

    Contains an ordered dictionary of visit instances and the onschedule
    and offschedule models used to get on and off the schedule.
    """

    name_regex = r"[a-z0-9\_\-]+$"
    visit_cls = Visit
    visit_collection_cls = VisitCollection
    subject_schedule_cls = SubjectSchedule
    window_cls = Window

    def __init__(
        self,
        name=None,
        verbose_name: str = None,
        onschedule_model: str = None,
        offschedule_model: str = None,
        loss_to_followup_model: str = None,
        consent_model: str = None,
        appointment_model: str | None = None,
        offstudymedication_model: str | None = None,
        sequence: str | None = None,
        base_timepoint: float | Decimal | None = None,
    ):
        self._subject = None
        if isinstance(base_timepoint, (float,)):
            base_timepoint = Decimal(str(base_timepoint))
        elif isinstance(base_timepoint, (int,)):
            base_timepoint = Decimal(str(base_timepoint) + ".0")
        self.base_timepoint = base_timepoint or Decimal("0.0")
        self.visits = self.visit_collection_cls()
        if not name or not re.match(r"[a-z0-9_\-]+$", name):
            raise ScheduleNameError(
                f"Invalid name. Got '{name}'. May only contains numbers, "
                "lower case letters and '_'."
            )
        else:
            self.name = name
        self.verbose_name = verbose_name or name
        self.sequence = sequence or name

        self.appointment_model = appointment_model.lower() or "edc_appointment.appointment"
        self.consent_model = consent_model.lower()
        self.offschedule_model = offschedule_model.lower()
        self.onschedule_model = onschedule_model.lower()
        self.loss_to_followup_model = (
            None if loss_to_followup_model is None else loss_to_followup_model.lower()
        )
        self.offstudymedication_model = (
            None if offstudymedication_model is None else offstudymedication_model.lower()
        )

    def check(self):
        warnings = []
        try:
            self.subject.check()
        except (SiteVisitScheduleError, SubjectScheduleError) as e:
            warnings.append(f"{e} See schedule '{self.name}'.")
        return warnings

    def __repr__(self):
        return f"Schedule({self.name})"

    def __str__(self):
        return self.name

    def add_visit(self, visit=None, **kwargs):
        """Adds a unique visit to the schedule."""
        visit = visit or self.visit_cls(**kwargs)
        if visit.timepoint < self.base_timepoint:
            raise VisitTimepointError(
                "Visit timepoint cannot be less than this schedule's base_timepoint. "
                f"See {visit}. Got visit.timepoint={visit.timepoint}."
            )

        for attr in ["code", "title", "timepoint", "rbase"]:
            if getattr(visit, attr) in [getattr(v, attr) for v in self.visits.values()]:
                raise AlreadyRegisteredVisit(
                    f"Visit already registered. Got visit={visit} "
                    f"(offending attr='{attr}'). "
                    f"See schedule '{self}'"
                )
        if not self.visits and visit.timepoint != self.base_timepoint:
            raise VisitTimepointError(
                f"First visit timepoint should be {self.base_timepoint}. Set schedule"
                f".base_timepoint if not using default base_timepoint of 0. See {visit}. "
                f"Got visit.timepoint={visit.timepoint}."
            )
        visit.base_timepoint = self.base_timepoint
        self.visits.update({visit.code: visit})
        return visit

    @property
    def field_value(self):
        return self.name

    def crf_required_at(self, label_lower: str) -> list:
        """Returns a list of visit codes where the CRF is required
        by default.
        """
        visit_codes = []
        for visit_code, visit in self.visits.items():
            if label_lower in [form.model for form in visit.crfs if form.required]:
                visit_codes.append(visit_code)
        return visit_codes

    def requisition_required_at(self, requisition_panel) -> list:
        """Returns a list of visit codes where the requisition is
        required by default.

        A requisition is found by its panel.
        """
        visit_codes = []
        for visit_code, visit in self.visits.items():
            if requisition_panel in [
                form.panel for form in visit.requisitions if form.required
            ]:
                visit_codes.append(visit_code)
        return visit_codes

    @property
    def subject(self):
        """Returns a SubjectSchedule instance.

        Note: SubjectSchedule puts a subject on to a schedule or takes a subject
        off of a schedule.
        """
        if not self._subject:
            visit_schedule, schedule = site_visit_schedules.get_by_onschedule_model(
                self.onschedule_model
            )
            if schedule.name != self.name:
                raise ValueError(
                    f"Site visit schedules return the wrong schedule object. "
                    f"Expected {repr(self)} for onschedule_model={self.onschedule_model}. "
                    f"Got {repr(schedule)}."
                )
            self._subject = self.subject_schedule_cls(
                visit_schedule=visit_schedule, schedule=self
            )
        return self._subject

    def put_on_schedule(self, **kwargs):
        """Wrapper method to puts a subject onto this schedule."""
        self.subject.put_on_schedule(**kwargs)

    def refresh_schedule(self, **kwargs):
        """Resaves the onschedule model to, for example, refresh
        appointments.
        """
        self.subject.resave(**kwargs)

    def take_off_schedule(self, offschedule_datetime=None, **kwargs):
        self.subject.take_off_schedule(offschedule_datetime=offschedule_datetime, **kwargs)

    def is_onschedule(self, **kwargs):
        try:
            self.subject.onschedule_or_raise(compare_as_datetimes=True, **kwargs)
        except (NotOnScheduleError, NotOnScheduleForDateError):
            return False
        return True

    def datetime_in_window(self, **kwargs):
        return self.window_cls(name=self.name, visits=self.visits, **kwargs).datetime_in_window

    @property
    def onschedule_model_cls(self):
        return self.subject.onschedule_model_cls

    @property
    def offschedule_model_cls(self):
        return self.subject.offschedule_model_cls

    @property
    def loss_to_followup_model_cls(self):
        return django_apps.get_model(self.loss_to_followup_model)

    @property
    def ltfu_model_cls(self):
        return self.loss_to_followup_model_cls

    @property
    def history_model_cls(self):
        return self.subject.history_model_cls

    @property
    def appointment_model_cls(self):
        return self.subject.appointment_model_cls

    @property
    def visit_model_cls(self):
        return self.subject.visit_model_cls

    @property
    def consent_model_cls(self):
        return self.subject.consent_model_cls

    def to_dict(self):
        return {k: v.to_dict() for k, v in self.visits.items()}
