from django.urls.conf import path

from .admin_site import visit_schedule_app_admin

app_name = "visit_schedule_app"

urlpatterns = [path("admin/", visit_schedule_app_admin.urls)]
