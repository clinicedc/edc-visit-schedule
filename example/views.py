from edc_base.views import EdcBaseViewMixin
from django.views.generic.base import TemplateView


class HomeView(EdcBaseViewMixin, TemplateView):

    template_name = 'example/home.html'

    def __init__(self, *args, **kwargs):
        super(HomeView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context.update()
        return context
