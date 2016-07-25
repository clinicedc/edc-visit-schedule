from edc_base.views import EdcBaseViewMixin
from django.views.generic.base import TemplateView
from .visit_schedules import site_visit_schedules


class HomeView(EdcBaseViewMixin, TemplateView):

    template_name = 'example/home.html'

    def __init__(self, *args, **kwargs):
        super(HomeView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit_schedule = site_visit_schedules.visit_schedules.get('Example Visit Schedule')
        print(">>>>>>>>>>>", visit_schedule.membership_forms)
        context.update({'membership_forms': visit_schedule.membership_forms.get('schedule-1').get('example.subjectconsent')})
        form = visit_schedule.membership_forms.get('schedule-1').get('example.subjectconsent')
        return context
