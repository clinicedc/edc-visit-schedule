import sys

from django.core.management.color import color_style

style = color_style()


def populate_visit_schedule(sender=None, **kwargs):
    from .models import VisitSchedule
    from .site_visit_schedules import site_visit_schedules

    sys.stdout.write(style.MIGRATE_HEADING("Populating visit schedule:\n"))
    VisitSchedule.objects.update(active=False)
    site_visit_schedules.to_model(VisitSchedule)
    sys.stdout.write("Done.\n")
    sys.stdout.flush()
