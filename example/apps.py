from django.apps.config import AppConfig

from edc_consent.apps import EdcConsentAppConfig as EdcConsentAppConfigParent
from datetime import datetime
from dateutil.relativedelta import relativedelta
from edc_visit_schedule.apps import EdcVisitScheduleAppConfig as EdcVisitScheduleAppConfigParent


class ExampleAppConfig(AppConfig):
    name = 'example'


class EdcVisitScheduleAppConfig(EdcVisitScheduleAppConfigParent):
    pass
#     def ready(self):
#         pass


class EdcConsentAppConfig(EdcConsentAppConfigParent):

    consent_type_setup = [
        {'app_label': 'example',
         'model_name': 'subjectconsent',
         'start_datetime': datetime.today() + relativedelta(years=-1),
         'end_datetime': datetime.today() + relativedelta(years=+1),
         'version': '1'}
    ]
