# edc-visit-schedule

Add data collection schedules to your app.

###Installation


###Usage

A `Visit Schedule` lives in your app in `visit_schedules.py`. Each app can declare and register one or more visit schedules in its `visit_schedules` module. Visit schedules are loaded when `autodiscover` is called from `AppConfig`.

A `VisitSchedule` contains `Schedules` which contain `Visits` which contain `Crfs` and `Requisitions`.

A `schedule` is effectively a "data collection schedule" where each contained `visit` represents a data collection timepoint.

A subject is enrolled to a `schedule` by an enrollment model and disenrolled by a disenrollment model. In the example below we use models `Enrollment` and `Disenrollment` to do this.


See the example app for the complete code.

First, create a file `visit_schedules.py` in the root of your app where the code below will live.

Next, declare lists of `Crfs` and `Requisitions` to be completed during each visit. For simplicity, we assume that every visit has the same data collection requirement (not usually the case).

    from example.models import SubjectVisit, Enrollment, Disenrollment, SubjectDeathReport, SubjectOffstudy

    from edc_visit_schedule.site_visit_schedules import site_visit_schedules
    from edc_visit_schedule.visit_schedule import VisitSchedule
    from edc_visit_schedule.visit import Crf, Requisition
    from edc_visit_schedule.schedule import Schedule
    
    
    crfs = (
        Crf(show_order=10, model='example.crfone'),
        Crf(show_order=20, model='example.crftwo'),
        Crf(show_order=30, model='example.crfthree'),
        Crf(show_order=40, model='example.crffour'),
        Crf(show_order=50, model='example.crffive'),
    )
    
    requisitions = (
        Requisition(
            show_order=10, app_label='example', model_name='SubjectRequisition',
            panel_name='Research Blood Draw', panel_type='TEST', aliqout_type_alpha_code='WB'),
        Requisition(
            show_order=20, app_label='example', model_name='SubjectRequisition',
            panel_name='Viral Load', panel_type='TEST', aliqout_type_alpha_code='WB'),
    )

Create a schedule:

    schedule = Schedule(name='schedule-1')

Add visits to the `schedule`:

    schedule.add_visit(
        code='1000',
        title='Visit 1000',
        timepoint=0,
        base_interval=0,
        requisitions=requisitions,
        crfs=crfs)
    schedule.add_visit(
        code='2000',
        title='Visit 2000',
        timepoint=1,
        base_interval=1,
        requisitions=requisitions,
        crfs=crfs)

Then create a new visit schedule:

    subject_visit_schedule = VisitSchedule(
        name='subject_visit_schedule',
        verbose_name='Example Visit Schedule',
        app_label='example',
        enrollment_model=Enrollment,
        disenrollment=Disenrollment,
        death_report_model=SubjectDeathReport,
        offstudy_model=SubjectOffstudy,
        visit_model=SubjectVisit,
    )

Add the schedule to your visit schedule:

    schedule = subject_visit_schedule.add_schedule(schedule)

Register the visit schedule with the site registry:

    site_visit_schedules.register(subject_visit_schedule)

When Django loads, the visit schedule class will be available in the global `site_visit_schedules`.

Note that the `schedule` above was declared with the enrollment model `Enrollment`. An enrollment model uses the `CreateAppointmentsMixin` from `edc_appointment`. On `enrollment.save()` the method `enrollment.create_appointments` is called. This method uses the visit schedule information to create the appointments as per the visit data in the schedule.

### Enrollment and Disenrollment models

Two models_mixins are available for the the enrollment and disenrollment models, `EnrollmentModelMixin` and `DisenrollmentModelMixin`. Enrollment/disenrollment models may be used for only one `visit_schedule`. The `visit_schedule_name` is declared in the model's `Meta` class. Each schedule contained in the `visit_schedule` uses the same enrollment/disenrollment models. The schedule name is saved with the model instance to make it possible to differentiate between enrollment/disenrollment to each schedule.  

For example:

    class Enrollment(EnrollmentModelMixin, CreateAppointmentsMixin, RequiresConsentMixin, BaseUuidModel):
    
        is_eligible = models.BooleanField(default=True)
    
        class Meta(EnrollmentModelMixin.Meta):
            visit_schedule_name = 'subject_visit_schedule'
            consent_model = 'edc_example.subjectconsent'
            app_label = 'edc_example'
    
    
    class Disenrollment(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):
    
        class Meta(DisenrollmentModelMixin.Meta):
            visit_schedule_name = 'subject_visit_schedule'
            consent_model = 'edc_example.subjectconsent'
            app_label = 'edc_example'


### Off study vs. Disenrolled from a schedule

Subjects may be disenrolled from a schedule while still considered to be "on study". Enrollment / Disenrollment is per schedule, not per study/protocol. On/Off study is study/protocol-wide. If a subject is "off study" further data collection is blocked for timepoints that come after the date the subject was taken "off study". See also `edc-offstudy`. 
