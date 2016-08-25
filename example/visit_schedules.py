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

subject_visit_schedule = VisitSchedule(
    name='subject_visit_schedule',
    verbose_name='Example Visit Schedule',
    app_label='example',
    visit_model=SubjectVisit,
)

# add schedules
schedule = Schedule(name='schedule-1', enrollment_model=SubjectConsent)

# add visits to this schedule
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

schedule = subject_visit_schedule.add_schedule(schedule)

# register the visit_schedule
site_visit_schedules.register(subject_visit_schedule)
