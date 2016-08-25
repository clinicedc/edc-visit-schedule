from django.db import models

from edc_appointment.model_mixins import AppointmentModelMixin, CreateAppointmentsMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_meta_data.managers import CrfMetaDataManager
from edc_meta_data.mixins import CrfMetaDataMixin
from edc_registration.model_mixins import RegisteredSubjectModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin, PreviousVisitModelMixin, VisitModelMixin
from edc_meta_data.model_mixins import CrfMetaDataModelMixin, RequisitionMetaDataModelMixin
from edc_consent.model_mixins import ConsentModelMixin
from edc_consent.models.fields.bw.identity_fields_mixin import IdentityFieldsMixin
from edc_consent.models.fields import ReviewFieldsMixin, PersonalFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'example'


class SubjectConsent(ConsentModelMixin, CreateAppointmentsMixin, IdentityFieldsMixin, ReviewFieldsMixin,
                     PersonalFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject)

    class Meta:
        app_label = 'example'


class Appointment(AppointmentModelMixin, BaseUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject)

    class Meta:
        app_label = 'example'


class SubjectVisit(CrfMetaDataMixin, PreviousVisitModelMixin, VisitModelMixin, BaseUuidModel):

    appointment = models.OneToOneField(Appointment)

    class Meta:
        app_label = 'example'


class CrfOne(CrfModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    f1 = models.CharField(max_length=10, default='erik')

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        app_label = 'example'


class CrfTwo(CrfModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    f1 = models.CharField(max_length=10, default='erik')

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        app_label = 'example'


class CrfThree(CrfModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    f1 = models.CharField(max_length=10, default='erik')

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        app_label = 'example'


class CrfFour(CrfModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    f1 = models.CharField(max_length=10, default='erik')

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        app_label = 'example'


class CrfFive(CrfModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    f1 = models.CharField(max_length=10, default='erik')

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        app_label = 'example'


class CrfSix(CrfModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    f1 = models.CharField(max_length=10, default='erik')

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        app_label = 'example'


class RequisitionOne(CrfModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    panel_name = models.CharField(max_length=25, null=True)

    f1 = models.CharField(max_length=10, default='erik')

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        app_label = 'example'


class RequisitionTwo(CrfModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    panel_name = models.CharField(max_length=25, null=True)

    f1 = models.CharField(max_length=10, default='erik')

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        app_label = 'example'


class CrfMetaData(CrfMetaDataModelMixin, BaseUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject)

    appointment = models.ForeignKey(Appointment, related_name='+')

    class Meta:
        app_label = 'example'


class RequisitionMetaData(RequisitionMetaDataModelMixin, BaseUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject)

    appointment = models.ForeignKey(Appointment, related_name='+')

    class Meta:
        app_label = 'example'
