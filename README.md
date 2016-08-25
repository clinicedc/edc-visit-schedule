# edc-visit-schedule

Add a data collection schedule to your app.

###Installation


###Usage

A `Visit Schedule` lives in your app in the module `visit_schedules`. Each app can declare on or more visit schedules and they will be loaded when `autodiscover` is called from `AppConfig`.

A `VisitSchedule` contains `Schedules` which contain `Visits` which contain `Crfs` and `Requisitions`.

A subject is enrolled to a schedule by an enrollment model. In the example below we use the informed consent, `SubjectConsent`.

See the example app for the complete code.

First, create a file `visit_schedules.py` in the root of your app where the code below will live.

Next, declare lists of `Crfs` and `Requisitions` to be completed during each visit. In this case we assume that every visit has the same data collection requirement.

    from example.models import SubjectVisit, SubjectConsent

    from edc_visit_schedule.site_visit_schedules import site_visit_schedules
    from edc_visit_schedule.visit_schedule import VisitSchedule
    from edc_visit_schedule.visit import Crf, Requisition
    from edc_visit_schedule.schedule import Schedule
    
    
    crfs = (
        Crf(show_order=10, app_label='example', model_name='CrfOne'),
        Crf(show_order=20, app_label='example', model_name='CrfTwo'),
        Crf(show_order=30, app_label='example', model_name='CrfThree'),
        Crf(show_order=40, app_label='example', model_name='CrfFour'),
        Crf(show_order=50, app_label='example', model_name='CrfFive'),
    )
    
    requisitions = (
        Requisition(
            show_order=10, app_label='example', model_name='RequisitionOne',
            panel_name='Research Blood Draw', panel_type='TEST', aliqout_type_alpha_code='WB'),
        Requisition(
            show_order=20, app_label='example', model_name='RequisitionTwo',
            panel_name='Viral Load', panel_type='TEST', aliqout_type_alpha_code='WB'),
    )

Create a schedule:

    schedule = Schedule(name='schedule-1', enrollment_model=SubjectConsent)

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
        visit_model=SubjectVisit,
    )

Add the schedule to your visit schedule:

    schedule = subject_visit_schedule.add_schedule(schedule)

Register the visit schedule with the site registry:

    site_visit_schedules.register(subject_visit_schedule)

When Django loads, the visit schedule class will be available in the global `site_visit_schedules`.

Note that the `schedule` above was declared with the enrollment model `SubjectConsent`. An enrollment model uses the `CreateAppointmentsMixin` from `edc_appointment`. On `subject_consent.save()` the method `subject_consent.prepare_appointments` is called. This method uses the visit schedule information to create the appointments as per the visit data in the schedule.
