from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# local imports
from . import models


class RuleListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = models.Rule
    paginate_by = 10

    def get_queryset(self):
        return models.Rule.objects.filter(created_by=self.request.user)


class RuleCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = models.Rule
    fields = ['name', 'type', 'value']
    template_name = 'rule/rule_form.html'
    success_url = '/rule'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(RuleCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RuleCreate, self).get_context_data(**kwargs)
        context['form_name'] = "Add Rule"

        return context


class RuleUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = models.Rule
    fields = ['name', 'type', 'value']
    template_name = 'rule/rule_form.html'
    success_url = '/rule'

    def get_context_data(self, **kwargs):
        context = super(RuleUpdate, self).get_context_data(**kwargs)
        context['form_name'] = "Edit Rule"

        return context


class RuleDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = models.Rule
    success_url = '/rule'
