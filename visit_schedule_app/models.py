from datetime import date

from django.db import models
from django.db.models.deletion import PROTECT
from edc_action_item.models import ActionItem
from edc_consent.managers import ConsentObjectsByCdefManager, CurrentSiteByCdefManager
from edc_crf.model_mixins import CrfModelMixin, CrfWithActionModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_list_data.model_mixins import ListModelMixin
from edc_model.models import BaseUuidModel
from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow
from edc_visit_tracking.model_mixins import SubjectVisitMissedModelMixin
from edc_visit_tracking.models import SubjectVisit

from edc_visit_schedule.model_mixins import OffScheduleModelMixin, OnScheduleModelMixin


class SubjectVisitMissedReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Subject Missed Visit Reasons"
        verbose_name_plural = "Subject Missed Visit Reasons"


class SubjectVisitMissed(
    SubjectVisitMissedModelMixin,
    CrfWithActionModelMixin,
    BaseUuidModel,
):
    action_item = models.ForeignKey(
        ActionItem, null=True, blank=True, on_delete=PROTECT, related_name="+"
    )

    subject_visit = models.OneToOneField(
        SubjectVisit, on_delete=models.PROTECT, related_name="+"
    )

    missed_reasons = models.ManyToManyField(
        SubjectVisitMissedReasons, blank=True, related_name="+"
    )

    class Meta(
        SubjectVisitMissedModelMixin.Meta,
        BaseUuidModel.Meta,
    ):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"


class SubjectScreening(
    SiteModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    BaseUuidModel,
):
    screening_identifier = models.CharField(max_length=50)

    screening_datetime = models.DateTimeField(default=get_utcnow)

    age_in_years = models.IntegerField(default=25)


class SubjectConsent(
    SiteModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    BaseUuidModel,
):
    consent_datetime = models.DateTimeField(default=get_utcnow)

    version = models.CharField(max_length=25, default="1")

    identity = models.CharField(max_length=25)

    confirm_identity = models.CharField(max_length=25)

    dob = models.DateField(default=date(1995, 1, 1))


class SubjectConsentV1(SubjectConsent):
    on_site = CurrentSiteByCdefManager()
    objects = ConsentObjectsByCdefManager()

    class Meta:
        proxy = True


class SubjectOffstudy(SiteModelMixin, OffstudyModelMixin, BaseUuidModel):
    objects = SubjectIdentifierManager()


class SubjectOffstudyFive(SiteModelMixin, OffstudyModelMixin, BaseUuidModel):
    objects = SubjectIdentifierManager()


class SubjectOffstudySix(SiteModelMixin, OffstudyModelMixin, BaseUuidModel):
    objects = SubjectIdentifierManager()


class SubjectOffstudySeven(SiteModelMixin, OffstudyModelMixin, BaseUuidModel):
    objects = SubjectIdentifierManager()


class DeathReport(SiteModelMixin, BaseUuidModel):
    subject_identifier = models.CharField(max_length=25, null=True)

    report_datetime = models.DateTimeField()


# visit_schedule


class OnSchedule(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffSchedule(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    class Meta(OffScheduleModelMixin.Meta):
        pass


class OnScheduleThree(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffScheduleThree(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    class Meta(OffScheduleModelMixin.Meta):
        pass


# visit_schedule_two


class OnScheduleTwo(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffScheduleTwo(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    pass


class OnScheduleFour(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffScheduleFour(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    pass


class OnScheduleFive(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffScheduleFive(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    offschedule_datetime_field_attr = "my_offschedule_datetime"

    my_offschedule_datetime = models.DateTimeField()

    class Meta(OffScheduleModelMixin.Meta):
        pass


class OnScheduleSix(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffScheduleSix(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    offschedule_datetime_field_attr = "my_offschedule_date"

    my_offschedule_date = models.DateField()

    class Meta(OffScheduleModelMixin.Meta):
        pass


class BadOffSchedule1(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    """Meta.OffScheduleModelMixin.offschedule_datetime_field
    is None"""

    offschedule_datetime_field_attr = None

    my_offschedule_date = models.DateField()

    class Meta(OffScheduleModelMixin.Meta):
        pass


class OnScheduleSeven(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffScheduleSeven(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    """Is Missing Meta.OffScheduleModelMixin"""

    class Meta:
        pass


class CrfOne(CrfModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT, related_name="+")

    report_datetime = models.DateTimeField(default=get_utcnow)

    f1 = models.CharField(max_length=50, null=True, blank=True)

    f2 = models.CharField(max_length=50, null=True, blank=True)

    f3 = models.CharField(max_length=50, null=True, blank=True)


class CrfTwo(CrfModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT, related_name="+")

    report_datetime = models.DateTimeField(default=get_utcnow)

    f1 = models.CharField(max_length=50, null=True, blank=True)


class CrfThree(CrfModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT, related_name="+")

    report_datetime = models.DateTimeField(default=get_utcnow)

    f1 = models.CharField(max_length=50, null=True, blank=True)


class CrfOneProxyOne(CrfOne):
    class Meta:
        proxy = True


class CrfOneProxyTwo(CrfOne):
    class Meta:
        proxy = True


class CrfOneProxyThree(CrfOne):
    class Meta:
        proxy = True


class CrfTwoProxyOne(CrfTwo):
    class Meta:
        proxy = True


class CrfTwoProxyTwo(CrfTwo):
    class Meta:
        proxy = True


class PrnOne(CrfModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT, related_name="+")

    report_datetime = models.DateTimeField(default=get_utcnow)

    f1 = models.CharField(max_length=50, null=True, blank=True)


class PrnTwo(CrfModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT, related_name="+")

    report_datetime = models.DateTimeField(default=get_utcnow)

    f1 = models.CharField(max_length=50, null=True, blank=True)


class PrnThree(CrfModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT, related_name="+")

    report_datetime = models.DateTimeField(default=get_utcnow)

    f1 = models.CharField(max_length=50, null=True, blank=True)
