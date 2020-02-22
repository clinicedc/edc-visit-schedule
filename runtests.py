#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings
from os.path import abspath, dirname

app_name = 'edc_visit_schedule'
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    EDC_NAVBAR_DEFAULT="edc_visit_schedule",
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django_crypto_fields.apps.AppConfig',
        'django_revision.apps.AppConfig',
        'edc_appointment.apps.AppConfig',
        'edc_registration.apps.AppConfig',
        'edc_device.apps.AppConfig',
        'edc_identifier.apps.AppConfig',
        'edc_timepoint.apps.AppConfig',
        "edc_offstudy.apps.AppConfig",
        'edc_metadata.apps.AppConfig',
        'edc_sites.apps.AppConfig',
        'edc_visit_tracking.apps.AppConfig',
        'edc_visit_schedule.apps.EdcFacilityAppConfig',
        "edc_visit_schedule.apps.EdcProtocolAppConfig",
        'edc_visit_schedule.apps.AppConfig',
        'visit_schedule_app.apps.AppConfig',
    ],
    add_dashboard_middleware=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split('=')[1] for t in sys.argv if t.startswith('--tag')]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests(
        [f'{app_name}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
