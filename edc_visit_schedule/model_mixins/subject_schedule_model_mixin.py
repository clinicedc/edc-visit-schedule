from typing import Any

from django.db import models

from ..subject_schedule import SubjectSchedule


class SubjectScheduleModelMixin(models.Model):
    """A mixin for CRF models to add the ability to determine
    if the subject is on/off schedule.
    """

    # If True, compares report_datetime and offschedule_datetime as datetimes
    # If False, (Default) compares report_datetime and
    # offschedule_datetime as dates
    offschedule_compare_dates_as_datetimes = False
    subject_schedule_cls = SubjectSchedule

    def validate_subject_schedule_status(self: Any):
        visit_schedule = self.related_visit.appointment.visit_schedule
        schedule = self.related_visit.appointment.schedule
        subject_identifier = self.related_visit.subject_identifier
        subject_schedule = self.subject_schedule_cls(
            visit_schedule=visit_schedule, schedule=schedule
        )
        subject_schedule.onschedule_or_raise(
            subject_identifier=subject_identifier,
            report_datetime=self.related_visit.report_datetime,
            compare_as_datetimes=self.offschedule_compare_dates_as_datetimes,
        )

    def save(self, *args, **kwargs):
        self.validate_subject_schedule_status()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
