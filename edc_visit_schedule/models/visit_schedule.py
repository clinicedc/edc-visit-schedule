from decimal import Decimal

from django.db import models
from edc_model import models as edc_models

from ..model_mixins import VisitScheduleMethodsModelMixin


class VisitScheduleManager(models.Manager):
    def get_by_natural_key(self, visit_schedule_name, schedule_name, visit_code):
        return self.get(
            visit_schedule_name=visit_schedule_name,
            schedule_name=schedule_name,
            visit_code=visit_code,
        )


class VisitSchedule(VisitScheduleMethodsModelMixin, edc_models.BaseUuidModel):
    visit_schedule_name = models.CharField(max_length=150)

    schedule_name = models.CharField(max_length=150)

    visit_code = models.CharField(max_length=150)

    visit_name = models.CharField(max_length=150)

    visit_title = models.CharField(max_length=150)

    timepoint = models.DecimalField(null=True, decimal_places=1, max_digits=6)

    active = models.BooleanField(default=False)

    objects = VisitScheduleManager()

    history = edc_models.HistoricalRecords()

    def __str__(self):
        return f"{self.visit_code}.0: {self.visit_title}"

    def natural_key(self):
        return (
            self.visit_schedule_name,
            self.schedule_name,
            self.visit_code,
        )

    def next_by_timepoint(self, timepoint: Decimal):
        for obj in self.objects.filter(timepoint__gt=timepoint):
            return obj
        return None

    class Meta(edc_models.BaseUuidModel.Meta):
        # ordering = ("visit_schedule_name", "schedule_name", "visit_code")
        unique_together = (
            ("visit_schedule_name", "schedule_name", "visit_code"),
            ("visit_schedule_name", "schedule_name", "timepoint"),
        )
        indexes = [
            models.Index(
                fields=[
                    "visit_schedule_name",
                    "schedule_name",
                    "visit_code",
                    "visit_name",
                    "visit_title",
                ]
            ),
            models.Index(fields=["visit_schedule_name", "schedule_name", "timepoint"]),
        ]
