# edc-visit-schedule

Add data collection schedules to your app.

## Installation

Get the latest version:

    pip install git+https://github.com/botswana-harvard/edc-visit-schedule@develop#egg=edc_visit_schedule

Add to settings:

    INSTALLED_APPS = [
        ...
        'edc_visit_schedule.apps.AppConfig',
        ...
    ]


## Overview

A `Visit Schedule` lives in your app in `visit_schedules.py`. Each app can declare and register one or more visit schedules in its `visit_schedules` module. Visit schedules are loaded when `autodiscover` is called from `AppConfig`.

A `VisitSchedule` contains `Schedules` which contain `Visits` which contain `Crfs` and `Requisitions`.

A `schedule` is effectively a "data collection schedule" where each contained `visit` represents a data collection timepoint.

A subject is enrolled to a `schedule` by the schedule's enrollment model and disenrolled by the schedule's disenrollment model. In the example below we use models `Enrollment` and `Disenrollment` to do this for schedule 'schedule1'.

## Usage

First, create a file `visit_schedules.py` in the root of your app where the visit schedule code below will live.

Next, declare lists of data `Crfs` and laboratory `Requisitions` to be completed during each visit. For simplicity, we assume that every visit has the same data collection requirement (not usually the case).

    from example.models import SubjectVisit, Enrollment, Disenrollment, SubjectDeathReport, SubjectOffstudy

    from edc_visit_schedule.site_visit_schedules import site_visit_schedules
    from edc_visit_schedule.schedule import Schedule
    from edc_visit_schedule.visit import Crf, Requisition, FormsCollection
    from edc_visit_schedule.visit_schedule import VisitSchedule
    
    
    crfs = FormsCollection(
        Crf(show_order=10, model='example.crfone'),
        Crf(show_order=20, model='example.crftwo'),
        Crf(show_order=30, model='example.crfthree'),
        Crf(show_order=40, model='example.crffour'),
        Crf(show_order=50, model='example.crffive'),
    )
    
    requisitions = FormsCollection(
        Requisition(
            show_order=10, model='SubjectRequisition', panel_name='Research Blood Draw'),
        Requisition(
            show_order=20, model='SubjectRequisition', panel_name='Viral Load'),
    )

Create a new visit schedule:

    subject_visit_schedule = VisitSchedule(
        name='subject_visit_schedule',
        verbose_name='Example Visit Schedule',
        death_report_model=SubjectDeathReport,
        offstudy_model=SubjectOffstudy,
        visit_model=SubjectVisit)


Visit schedules contain `Schedules` so create a schedule:

    schedule = Schedule(
        name='schedule1',
        enrollment_model='edc_example.enrollment',
        disenrollment_model='edc_example.disenrollment')

Schedules contains visits, so add visits to the `schedule`:

    visit0 = Visit(
        code='1000',
        title='Visit 1000',
        timepoint=0,
        rbase=relativedelta(days=0),
        requisitions=requisitions,
        crfs=crfs)

    visit1 = Visit(
        code='2000',
        title='Visit 2000',
        timepoint=1,
        rbase=relativedelta(days=28),
        requisitions=requisitions,
        crfs=crfs)

    schedule.add_visit(visit=visit0)
    schedule.add_visit(visit=visit1)


Add the schedule to your visit schedule:

    schedule = subject_visit_schedule.add_schedule(schedule)

Register the visit schedule with the site registry:

    site_visit_schedules.register(subject_visit_schedule)

When Django loads, the visit schedule class will be available in the global `site_visit_schedules`.

The `site_visit_schedules` has a number of methods to help query the visit schedule and some related data.

The `schedule` above was declared with the enrollment model `Enrollment`. An enrollment model uses the `CreateAppointmentsMixin` from `edc_appointment`. On `enrollment.save()` the method `enrollment.create_appointments` is called. This method uses the visit schedule information to create the appointments as per the visit data in the schedule.

### Enrollment and Disenrollment models

Two models_mixins are available for the the enrollment and disenrollment models, `EnrollmentModelMixin` and `DisenrollmentModelMixin`. Enrollment/disenrollment are specific to a `schedule`. The visit schedule name and schedule name are declared on the model's `Meta` class `visit_schedule_name` attribute.

For example:

    class Enrollment(EnrollmentModelMixin, CreateAppointmentsMixin, RequiresConsentMixin, BaseUuidModel):
    
        is_eligible = models.BooleanField(default=True)
    
        class Meta(EnrollmentModelMixin.Meta):
            visit_schedule_name = 'subject_visit_schedule.schedule1'
            consent_model = 'edc_example.subjectconsent'
            app_label = 'edc_example'
    
    
    class Disenrollment(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):
    
        class Meta(DisenrollmentModelMixin.Meta):
            visit_schedule_name = 'subject_visit_schedule.schedule1'
            consent_model = 'edc_example.subjectconsent'
            app_label = 'edc_example'


### Off study vs. Disenrolled from a schedule

Subjects may be disenrolled from a schedule while still considered to be "on study". Enrollment / Disenrollment is per schedule, not per study/protocol. On/Off study is study/protocol-wide. If a subject is "off study" further data collection is blocked for timepoints that come after the date the subject was taken "off study". See also `edc-offstudy`. 
