[![Build Status](https://travis-ci.org/clinicedc/edc-visit-schedule.svg?branch=develop)](https://travis-ci.org/clinicedc/edc-visit-schedule)
[![Coverage Status](https://coveralls.io/repos/clinicedc/edc-visit-schedule/badge.svg)](https://coveralls.io/r/clinicedc/edc-visit-schedule)


# edc-visit-schedule

Add data collection schedules to your app.

## Installation

Get the latest version:

    pip install git+https://github.com/clinicedc/edc-visit-schedule@develop#egg=edc_visit_schedule

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

A subject is put on a `schedule` by the schedule's `onschedule` model and taken off by the schedule's `offschedule` model. In the example below we use models `OnSchedule` and `OffSchedule` to do this for schedule `schedule1`.

## Usage

First, create a file `visit_schedules.py` in the root of your app where the visit schedule code below will live.

Next, declare lists of data `Crfs` and laboratory `Requisitions` to be completed during each visit. For simplicity, we assume that every visit has the same data collection requirement (not usually the case).

    from myapp.models import SubjectVisit, OnSchedule, OffSchedule, SubjectDeathReport, SubjectOffstudy

    from edc_visit_schedule.site_visit_schedules import site_visit_schedules
    from edc_visit_schedule.schedule import Schedule
    from edc_visit_schedule.visit import Crf, Requisition, FormsCollection
    from edc_visit_schedule.visit_schedule import VisitSchedule
    
    
    crfs = FormsCollection(
        Crf(show_order=10, model='myapp.crfone'),
        Crf(show_order=20, model='myapp.crftwo'),
        Crf(show_order=30, model='myapp.crfthree'),
        Crf(show_order=40, model='myapp.crffour'),
        Crf(show_order=50, model='myapp.crffive'),
    )
    
    requisitions = FormsCollection(
        Requisition(
            show_order=10, model='myapp.subjectrequisition', panel_name='Research Blood Draw'),
        Requisition(
            show_order=20, model='myapp.subjectrequisition', panel_name='Viral Load'),
    )

Create a new visit schedule:

    subject_visit_schedule = VisitSchedule(
        name='subject_visit_schedule',
        verbose_name='My Visit Schedule',
        death_report_model=SubjectDeathReport,
        offstudy_model=SubjectOffstudy,
        visit_model=SubjectVisit)


Visit schedules contain `Schedules` so create a schedule:

    schedule = Schedule(
        name='schedule1',
        onschedule_model='myapp.onschedule',
        offschedule_model='myapp.offschedule')

Schedules contains visits, so decalre some visits and add to the `schedule`:

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

> __Note:__ The `schedule` above was declared with `onschedule_model=OnSchedule`. An on-schedule model uses the `CreateAppointmentsMixin` from `edc_appointment`. On `onschedule.save()` the method `onschedule.create_appointments` is called. This method uses the visit schedule information to create the appointments as per the visit data in the schedule. See also `edc_appointment`.

### OnSchedule and OffSchedule models

Two models_mixins are available for the the on-schedule and off-schedule models, `OnScheduleModelMixin` and `OffScheduleModelMixin`. OnSchedule/OffSchedule models are specific to a `schedule`. The `visit_schedule_name` and `schedule_name` are declared on the model's `Meta` class attribute `visit_schedule_name`.

For example:

    class OnSchedule(OnScheduleModelMixin, CreateAppointmentsMixin, RequiresConsentModelMixin, BaseUuidModel):
        
        class Meta(EnrollmentModelMixin.Meta):
            visit_schedule_name = 'subject_visit_schedule.schedule1'
            consent_model = 'myapp.subjectconsent'
    
    
    class OffSchedule(OffScheduleModelMixin, RequiresConsentModelMixin, BaseUuidModel):
    
        class Meta(OffScheduleModelMixin.Meta):
            visit_schedule_name = 'subject_visit_schedule.schedule1'
            consent_model = 'myapp.subjectconsent'
