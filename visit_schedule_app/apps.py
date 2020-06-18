from django.apps import AppConfig as DjangoAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig


class AppConfig(DjangoAppConfig):
    name = "visit_schedule_app"


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {"visit_schedule_app.subjectvisit": "reason"}
