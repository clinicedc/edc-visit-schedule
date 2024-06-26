from django.contrib.admin import SimpleListFilter

__all__ = ["ScheduleStatusListFilter"]

from django.db.models import Count

from ..models import SubjectScheduleHistory


class ScheduleStatusListFilter(SimpleListFilter):
    title = "Schedule status"
    parameter_name = "schedule_status"

    def lookups(self, request, model_admin):
        names = []
        qs = (
            SubjectScheduleHistory.objects.values(
                "schedule_name", "onschedule_model", "offschedule_model"
            )
            .order_by("schedule_name", "onschedule_model", "offschedule_model")
            .annotate(cnt=Count("schedule_name"))
        )
        for obj in qs:
            names.append(
                (f"{obj.get('schedule_name')}__on", f"On: {obj.get('schedule_name')}")
            )
        for obj in qs:
            names.append(
                (f"{obj.get('schedule_name')}__off", f"Off: {obj.get('schedule_name')}")
            )
        return tuple(names)

    @property
    def subject_identifiers(self):
        schedule_name, status = self.value().split("__")
        return SubjectScheduleHistory.objects.filter(
            schedule_name=schedule_name, offschedule_datetime__isnull=status == "on"
        ).values_list("subject_identifier", flat=True)

    def queryset(self, request, queryset):
        if self.value() and self.value() != "none":
            queryset = queryset.filter(subject_identifier__in=self.subject_identifiers)
        return queryset
