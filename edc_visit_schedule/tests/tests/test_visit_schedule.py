from datetime import date

from dateutil.relativedelta import relativedelta
from django.test import TestCase, override_settings
from edc_appointment.models import Appointment
from edc_consent.consent_definition import ConsentDefinition
from edc_consent.exceptions import NotConsentedError
from edc_consent.site_consents import site_consents
from edc_constants.constants import FEMALE, MALE
from edc_facility.import_holidays import import_holidays
from edc_protocol.research_protocol_config import ResearchProtocolConfig
from edc_registration.models import RegisteredSubject
from edc_registration.utils import RegisteredSubjectDoesNotExist
from edc_sites.tests import SiteTestCaseMixin
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED

from edc_visit_schedule.constants import ON_SCHEDULE
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.site_visit_schedules import (
    SiteVisitScheduleError,
    site_visit_schedules,
)
from edc_visit_schedule.subject_schedule import (
    InvalidOffscheduleDate,
    NotOnScheduleError,
)
from edc_visit_schedule.utils import check_visit_schedule_models
from edc_visit_schedule.visit import Crf, FormsCollection, FormsCollectionError, Visit
from edc_visit_schedule.visit_schedule import (
    AlreadyRegisteredSchedule,
    VisitSchedule,
    VisitScheduleNameError,
)
from visit_schedule_app.consents import consent_v1
from visit_schedule_app.models import (
    OffSchedule,
    OnSchedule,
    OnScheduleThree,
    SubjectConsent,
    SubjectVisit,
)


@override_settings(
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=get_utcnow() - relativedelta(years=5),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=get_utcnow() + relativedelta(years=1),
    SITE_ID=30,
)
class TestVisitSchedule(SiteTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()

    def setUp(self):
        super().setUp()
        consent_v1 = ConsentDefinition(
            "visit_schedule_app.subjectconsentv1",
            version="1",
            start=ResearchProtocolConfig().study_open_datetime,
            end=ResearchProtocolConfig().study_close_datetime,
            age_min=18,
            age_is_adult=18,
            age_max=64,
            gender=[MALE, FEMALE],
        )
        site_consents.registry = {}
        site_consents.register(consent_v1)

    def test_visit_schedule_name(self):
        """Asserts raises on invalid name."""
        self.assertRaises(
            VisitScheduleNameError,
            VisitSchedule,
            name="visit &&&& schedule",
            verbose_name="Visit Schedule",
            offstudy_model="visit_schedule_app.deathreport",
            death_report_model="visit_schedule_app.deathreport",
            locator_model="edc_locator.subjectlocator",
        )

    def test_visit_schedule_repr(self):
        """Asserts repr evaluates correctly."""
        v = VisitSchedule(
            name="visit_schedule",
            verbose_name="Visit Schedule",
            offstudy_model="visit_schedule_app.deathreport",
            death_report_model="visit_schedule_app.deathreport",
            locator_model="edc_locator.subjectlocator",
        )
        self.assertTrue(v.__repr__())

    def test_visit_schedule_validates(self):
        visit_schedule = VisitSchedule(
            name="visit_schedule",
            verbose_name="Visit Schedule",
            offstudy_model="visit_schedule_app.subjectoffstudy",
            death_report_model="visit_schedule_app.deathreport",
            locator_model="edc_locator.subjectlocator",
        )
        errors = check_visit_schedule_models(visit_schedule)
        if errors:
            self.fail("visit_schedule.check() unexpectedly failed")


@override_settings(
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=get_utcnow() - relativedelta(years=5),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=get_utcnow() + relativedelta(years=1),
    SITE_ID=30,
)
class TestVisitSchedule2(SiteTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()

    def setUp(self):
        site_consents.registry = {}
        site_consents.register(consent_v1)

        self.visit_schedule = VisitSchedule(
            name="visit_schedule",
            verbose_name="Visit Schedule",
            offstudy_model="visit_schedule_app.subjectoffstudy",
            death_report_model="visit_schedule_app.deathreport",
            locator_model="edc_locator.subjectlocator",
        )

        self.schedule = Schedule(
            name="schedule",
            onschedule_model="visit_schedule_app.onschedule",
            offschedule_model="visit_schedule_app.offschedule",
            appointment_model="edc_appointment.appointment",
            consent_definitions=consent_v1,
        )

        self.schedule2 = Schedule(
            name="schedule_two",
            onschedule_model="visit_schedule_app.onscheduletwo",
            offschedule_model="visit_schedule_app.offscheduletwo",
            appointment_model="edc_appointment.appointment",
            consent_definitions=consent_v1,
        )

        self.schedule3 = Schedule(
            name="schedule_three",
            onschedule_model="visit_schedule_app.onschedulethree",
            offschedule_model="visit_schedule_app.offschedulethree",
            appointment_model="edc_appointment.appointment",
            consent_definitions=consent_v1,
        )

    def test_visit_schedule_add_schedule(self):
        try:
            self.visit_schedule.add_schedule(self.schedule)
        except AlreadyRegisteredSchedule:
            self.fail("AlreadyRegisteredSchedule unexpectedly raised.")

    def test_visit_schedule_add_schedule_with_appointment_model(self):
        self.visit_schedule.add_schedule(self.schedule3)
        for schedule in self.visit_schedule.schedules.values():
            self.assertEqual(schedule.appointment_model, "edc_appointment.appointment")

    def test_visit_already_added_to_schedule(self):
        self.visit_schedule.add_schedule(self.schedule)
        self.assertRaises(
            AlreadyRegisteredSchedule, self.visit_schedule.add_schedule, self.schedule
        )

    def test_visit_schedule_get_schedules(self):
        self.visit_schedule.add_schedule(self.schedule)
        self.assertIn(self.schedule, self.visit_schedule.schedules.values())
        self.visit_schedule.add_schedule(self.schedule3)
        self.assertIn(self.schedule3, self.visit_schedule.schedules.values())

    def test_crfs_unique_show_order(self):
        self.assertRaises(
            FormsCollectionError,
            FormsCollection,
            Crf(show_order=10, model="edc_example.CrfOne"),
            Crf(show_order=20, model="edc_example.CrfTwo"),
            Crf(show_order=20, model="edc_example.CrfThree"),
        )


@override_settings(
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=get_utcnow() - relativedelta(years=5),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=get_utcnow() + relativedelta(years=1),
    SITE_ID=30,
)
class TestVisitSchedule3(SiteTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()

    def setUp(self):
        self.visit_schedule = VisitSchedule(
            name="visit_schedule",
            verbose_name="Visit Schedule",
            offstudy_model="visit_schedule_app.subjectoffstudy",
            death_report_model="visit_schedule_app.deathreport",
        )

        self.schedule = Schedule(
            name="schedule",
            onschedule_model="visit_schedule_app.onschedule",
            offschedule_model="visit_schedule_app.offschedule",
            appointment_model="edc_appointment.appointment",
            consent_definitions=consent_v1,
            base_timepoint=1,
        )

        visit = Visit(
            code="1000",
            rbase=relativedelta(days=0),
            rlower=relativedelta(days=0),
            rupper=relativedelta(days=6),
            timepoint=1,
        )
        self.schedule.add_visit(visit)
        self.visit_schedule.add_schedule(self.schedule)
        site_visit_schedules._registry = {}
        site_visit_schedules.register(self.visit_schedule)

        site_consents.registry = {}
        for cdef in self.schedule.consent_definitions:
            site_consents.register(cdef)
        cdef = self.schedule.consent_definitions[0]
        self.subject_consent = cdef.model_cls.objects.create(
            subject_identifier="12345",
            consent_datetime=get_utcnow() - relativedelta(years=1),
            dob=date(1995, 1, 1),
            identity="11111",
            confirm_identity="11111",
            version=cdef.version,
        )
        self.subject_identifier = self.subject_consent.subject_identifier

    def test_put_on_schedule_creates_history(self):
        self.schedule.put_on_schedule(
            subject_identifier=self.subject_identifier, onschedule_datetime=get_utcnow()
        )
        self.assertEqual(
            SubjectScheduleHistory.objects.filter(
                subject_identifier=self.subject_identifier
            ).count(),
            1,
        )

    def test_onschedule_creates_history(self):
        onschedule_model_obj = OnSchedule.objects.create(
            subject_identifier=self.subject_identifier, onschedule_datetime=get_utcnow()
        )
        self.assertEqual(
            SubjectScheduleHistory.objects.filter(
                subject_identifier=self.subject_identifier
            ).count(),
            1,
        )
        history_obj = SubjectScheduleHistory.objects.get(
            subject_identifier=self.subject_identifier
        )
        self.assertIsNone(history_obj.__dict__.get("offschedule_datetime"))
        self.assertEqual(
            history_obj.__dict__.get("onschedule_datetime"),
            onschedule_model_obj.onschedule_datetime,
        )
        self.assertEqual(history_obj.__dict__.get("schedule_status"), ON_SCHEDULE)

    def test_can_create_offschedule_with_onschedule(self):
        # signal puts on schedule
        OnSchedule.objects.create(
            subject_identifier=self.subject_identifier, onschedule_datetime=get_utcnow()
        )
        try:
            OffSchedule.objects.create(
                subject_identifier=self.subject_identifier,
                offschedule_datetime=get_utcnow(),
            )
        except Exception as e:
            self.fail(f"Exception unexpectedly raised. Got {e}.")

    def test_creates_appointments(self):
        # signal puts on schedule
        onschedule_datetime = get_utcnow() - relativedelta(months=6)
        OnSchedule.objects.create(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=onschedule_datetime,
        )
        self.assertGreater(Appointment.objects.all().count(), 0)

    def test_creates_appointments_starting_with_onschedule_datetime(self):
        """Will pass as long as this is not a holiday"""
        onschedule_datetime = self.subject_consent.consent_datetime + relativedelta(days=28)
        _, schedule = site_visit_schedules.get_by_onschedule_model(
            "visit_schedule_app.onschedule"
        )
        schedule.put_on_schedule(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=onschedule_datetime,
        )
        appointment = Appointment.objects.all().order_by("appt_datetime").first()
        self.assertEqual(appointment.appt_datetime, onschedule_datetime)

    def test_cannot_create_offschedule_without_onschedule(self):
        self.assertEqual(
            OnSchedule.objects.filter(subject_identifier=self.subject_identifier).count(),
            0,
        )
        self.assertRaises(
            NotOnScheduleError,
            OffSchedule.objects.create,
            subject_identifier=self.subject_identifier,
        )

    def test_cannot_create_offschedule_before_onschedule(self):
        onschedule_datetime = self.subject_consent.consent_datetime + relativedelta(days=28)
        OnSchedule.objects.create(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=onschedule_datetime,
        )
        self.assertRaises(
            InvalidOffscheduleDate,
            OffSchedule.objects.create,
            subject_identifier=self.subject_identifier,
            offschedule_datetime=onschedule_datetime - relativedelta(days=1),
        )

    def test_cannot_create_offschedule_before_last_visit(self):
        onschedule_datetime = self.subject_consent.consent_datetime + relativedelta(days=10)
        _, schedule = site_visit_schedules.get_by_onschedule_model(
            "visit_schedule_app.onschedule"
        )
        schedule.put_on_schedule(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=onschedule_datetime,
        )
        appointments = Appointment.objects.all()
        SubjectVisit.objects.create(
            appointment=appointments[0],
            subject_identifier=self.subject_identifier,
            report_datetime=appointments[0].appt_datetime,
            reason=SCHEDULED,
        )
        self.assertRaises(
            InvalidOffscheduleDate,
            schedule.take_off_schedule,
            subject_identifier=self.subject_identifier,
            offschedule_datetime=appointments[0].appt_datetime - relativedelta(days=1),
        )

    def test_cannot_put_on_schedule_if_visit_schedule_not_registered_subject(self):
        onschedule_datetime = self.subject_consent.consent_datetime + relativedelta(days=10)
        _, schedule = site_visit_schedules.get_by_onschedule_model(
            "visit_schedule_app.onschedule"
        )
        RegisteredSubject.objects.all().delete()
        self.assertRaises(
            RegisteredSubjectDoesNotExist,
            schedule.put_on_schedule,
            subject_identifier=self.subject_identifier,
            onschedule_datetime=onschedule_datetime,
        )

    def test_cannot_put_on_schedule_if_visit_schedule_not_consented(self):
        onschedule_datetime = self.subject_consent.consent_datetime + relativedelta(days=10)
        _, schedule = site_visit_schedules.get_by_onschedule_model(
            "visit_schedule_app.onschedule"
        )
        SubjectConsent.objects.all().delete()
        self.assertRaises(
            NotConsentedError,
            schedule.put_on_schedule,
            subject_identifier=self.subject_identifier,
            onschedule_datetime=onschedule_datetime,
        )

    def test_cannot_put_on_schedule_if_schedule_not_added(self):
        self.assertRaises(SiteVisitScheduleError, OnScheduleThree.objects.create)
