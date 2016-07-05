from collections import OrderedDict
from edc_constants.constants import REQUIRED, NOT_ADDITIONAL
from edc_visit_schedule.visit_schedule_configuration import (
    VisitScheduleConfiguration, CrfTuple, RequisitionPanelTuple, MembershipFormTuple, ScheduleTuple)
from example.models import SubjectVisit, SubjectConsent
from edc_visit_schedule.site_visit_schedules import site_visit_schedules


entries = (
    CrfTuple(10, u'example', u'CrfOne', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(20, u'example', u'CrfTwo', REQUIRED, NOT_ADDITIONAL),
)

requisitions = ()
# requisitions = (
#     RequisitionPanelTuple(
#         10, u'example', u'RequisitionOne', 'Research Blood Draw', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
#     RequisitionPanelTuple(
#         20, u'edc_testing', u'RequisitionTwo', 'Viral Load', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
# )


class VisitSchedule(VisitScheduleConfiguration):
    """A visit schedule class for tests."""
    name = 'Test Visit Schedule'
    app_label = 'example'
    # panel_model = TestPanel
    # aliquot_type_model = TestAliquotType

    membership_forms = OrderedDict({
        'schedule-1': MembershipFormTuple('schedule-1', SubjectConsent, True),
    })

    schedules = OrderedDict({
        'schedule-1': ScheduleTuple('schedule-1', 'schedule-1', None, None),
    })

    visit_definitions = OrderedDict(
        {'1000': {
            'title': '1000',
            'time_point': 0,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': 'group1',
            'visit_tracking_model': SubjectVisit,
            'schedule': 'schedule-1',
            'instructions': None,
            'requisitions': requisitions,
            'entries': entries},
         '2000': {
             'title': '2000',
             'time_point': 1,
             'base_interval': 0,
             'base_interval_unit': 'D',
             'window_lower_bound': 0,
             'window_lower_bound_unit': 'D',
             'window_upper_bound': 0,
             'window_upper_bound_unit': 'D',
             'grouping': 'group1',
            'visit_tracking_model': SubjectVisit,
             'schedule': 'schedule-1',
             'instructions': None,
            'requisitions': requisitions,
            'entries': entries},
         },
    )
site_visit_schedules.register(VisitSchedule)
