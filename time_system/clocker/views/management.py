from django.views.generic.base import TemplateView


class ManageView(TemplateView):
    '''
    ' Generic view that renders a template for the chucho tables to be placed in.
    '''

    template_name = "management.html"
    app = None
    model = None

    def get_context_data(self, **kwargs):
        context = super(ManageView, self).get_context_data(**kwargs)
        context['app'] = self.app
        context['model'] = self.model
        return context

