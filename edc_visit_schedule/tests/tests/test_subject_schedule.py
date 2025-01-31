from datetime import datetime
from zoneinfo import ZoneInfo

import time_machine
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings
from edc_consent.consent_definition import ConsentDefinition
from edc_consent.site_consents import site_consents
from edc_constants.constants import FEMALE, MALE
from edc_protocol.research_protocol_config import ResearchProtocolConfig
from edc_sites.tests import SiteTestCaseMixin
from edc_utils import get_utcnow

from edc_visit_schedule.exceptions import SubjectScheduleError
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_schedule.subject_schedule import SubjectSchedule
from edc_visit_schedule.visit_schedule import VisitSchedule
from visit_schedule_app.models import OffSchedule, OnSchedule, SubjectConsent


@time_machine.travel(datetime(2019, 4, 1, 8, 00, tzinfo=ZoneInfo("UTC")))
@override_settings(SITE_ID=30)
class TestSubjectSchedule(SiteTestCaseMixin, TestCase):
    def setUp(self):
        self.study_open_datetime = ResearchProtocolConfig().study_open_datetime
        self.study_close_datetime = ResearchProtocolConfig().study_close_datetime
        site_consents.registry = {}
        self.consent_v1 = ConsentDefinition(
            "visit_schedule_app.subjectconsentv1",
            version="1",
            start=self.study_open_datetime,
            end=self.study_close_datetime,
            age_min=18,
            age_is_adult=18,
            age_max=64,
            gender=[MALE, FEMALE],
        )
        site_consents.register(self.consent_v1)
        site_visit_schedules._registry = {}
        self.visit_schedule = VisitSchedule(
            name="visit_schedule",
            verbose_name="Visit Schedule",
            offstudy_model="visit_schedule_app.SubjectOffstudy",
            death_report_model="visit_schedule_app.DeathReport",
        )

        self.schedule = Schedule(
            name="schedule",
            onschedule_model="visit_schedule_app.OnSchedule",
            offschedule_model="visit_schedule_app.OffSchedule",
            appointment_model="edc_appointment.appointment",
            consent_definitions=[self.consent_v1],
            base_timepoint=1,
        )
        self.schedule3 = Schedule(
            name="schedule_three",
            onschedule_model="visit_schedule_app.OnScheduleThree",
            offschedule_model="visit_schedule_app.OffScheduleThree",
            appointment_model="edc_appointment.appointment",
            consent_definitions=[self.consent_v1],
            base_timepoint=1,
        )

        self.visit_schedule.add_schedule(self.schedule)
        self.visit_schedule.add_schedule(self.schedule3)
        site_visit_schedules.register(self.visit_schedule)

        self.visit_schedule_two = VisitSchedule(
            name="visit_schedule_two",
            verbose_name="Visit Schedule Two",
            offstudy_model="visit_schedule_app.SubjectOffstudy",
            death_report_model="visit_schedule_app.DeathReport",
        )

        self.schedule_two_1 = Schedule(
            name="schedule_two",
            onschedule_model="visit_schedule_app.OnScheduleTwo",
            offschedule_model="visit_schedule_app.OffScheduleTwo",
            appointment_model="edc_appointment.appointment",
            consent_definitions=[self.consent_v1],
        )
        self.schedule_two_2 = Schedule(
            name="schedule_four",
            onschedule_model="visit_schedule_app.OnScheduleFour",
            offschedule_model="visit_schedule_app.OffScheduleFour",
            appointment_model="edc_appointment.appointment",
            consent_definitions=[self.consent_v1],
        )

        self.visit_schedule_two.add_schedule(self.schedule_two_1)
        self.visit_schedule_two.add_schedule(self.schedule_two_2)
        site_visit_schedules.register(self.visit_schedule_two)
        self.subject_identifier: str = "111111"
        SubjectConsent.objects.create(subject_identifier=self.subject_identifier)

    def test_onschedule_updates_history(self):
        """Asserts returns the correct instances for the schedule."""
        traveller = time_machine.travel(self.study_open_datetime)
        traveller.start()
        for onschedule_model, schedule_name in [
            ("visit_schedule_app.onscheduletwo", "schedule_two"),
            ("visit_schedule_app.onschedulefour", "schedule_four"),
        ]:
            with self.subTest(onschedule_model=onschedule_model, schedule_name=schedule_name):
                visit_schedule, schedule = site_visit_schedules.get_by_onschedule_model(
                    onschedule_model
                )
                subject_schedule = SubjectSchedule(
                    self.subject_identifier,
                    visit_schedule=visit_schedule,
                    schedule=schedule,
                )
                subject_schedule.put_on_schedule(onschedule_datetime=get_utcnow())
                try:
                    SubjectScheduleHistory.objects.get(
                        subject_identifier=self.subject_identifier,
                        schedule_name=schedule_name,
                    )
                except ObjectDoesNotExist:
                    self.fail("ObjectDoesNotExist unexpectedly raised")
        traveller.stop()

    def test_multpile_consents(self):
        """Asserts does not raise if more than one consent
        for this subject
        """
        traveller = time_machine.travel(self.study_open_datetime)
        traveller.start()
        subject_identifier = "ABCDEF"
        SubjectConsent.objects.create(subject_identifier=subject_identifier, version="1")
        SubjectConsent.objects.create(subject_identifier=subject_identifier, version="2")
        visit_schedule, schedule = site_visit_schedules.get_by_onschedule_model(
            "visit_schedule_app.onscheduletwo"
        )
        subject_schedule = SubjectSchedule(
            subject_identifier, visit_schedule=visit_schedule, schedule=schedule
        )
        try:
            subject_schedule.put_on_schedule(onschedule_datetime=get_utcnow())
        except SubjectScheduleError:
            self.fail("SubjectScheduleError unexpectedly raised.")
        traveller.stop()

    def test_resave(self):
        """Asserts returns the correct instances for the schedule."""
        traveller = time_machine.travel(self.study_open_datetime)
        traveller.start()
        visit_schedule, schedule = site_visit_schedules.get_by_onschedule_model(
            "visit_schedule_app.onscheduletwo"
        )
        subject_schedule = SubjectSchedule(
            self.subject_identifier,
            visit_schedule=visit_schedule,
            schedule=schedule,
        )
        onschedule_datetime: datetime = get_utcnow()
        subject_schedule.put_on_schedule(onschedule_datetime)
        subject_schedule.put_on_schedule(onschedule_datetime)
        traveller.stop()

    def test_put_on_schedule(self):
        traveller = time_machine.travel(self.study_open_datetime)
        traveller.start()
        _, schedule = site_visit_schedules.get_by_onschedule_model(
            "visit_schedule_app.onschedule"
        )
        self.assertRaises(
            ObjectDoesNotExist,
            OnSchedule.objects.get,
            subject_identifier=self.subject_identifier,
        )
        schedule.put_on_schedule(
            subject_identifier=self.subject_identifier, onschedule_datetime=get_utcnow()
        )
        try:
            OnSchedule.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised")
        traveller.stop()

    def test_take_off_schedule(self):
        traveller = time_machine.travel(self.study_open_datetime)
        traveller.start()
        visit_schedule = site_visit_schedules.get_visit_schedule(
            visit_schedule_name="visit_schedule"
        )
        schedule = visit_schedule.schedules.get("schedule")
        schedule.put_on_schedule(self.subject_identifier, get_utcnow())
        schedule.take_off_schedule(self.subject_identifier, get_utcnow())
        try:
            OffSchedule.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised")
        traveller.stop()
