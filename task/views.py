from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, FormView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
import logging

# third party imports
from django_filters.views import FilterView
from multifist.apscheduler import APScheduler
from django_apscheduler import models as aps_models

# local imports
from . import models
from . import forms
from . import filters
from . import tasks


def test_job():
    print("I'm a test job!")


def resume(request, name):
    APScheduler.get_job(name).resume()
    return redirect('tasks')


def pause(request, name):
    APScheduler.get_job(name).pause()
    return redirect('tasks')


class TaskListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = models.Task
    paginate_by = 10

    def get_queryset(self):
        return models.Task.objects.filter(created_by=self.request.user)


class TaskDetailView(LoginRequiredMixin, FilterView):
    login_url = '/login'
    template_name = 'task/task_detail.html'
    filterset_class = filters.WebArchiveSearchFilter

    def get(self, request, *args, **kwargs):
        task = models.Task.objects.get(pk=self.kwargs.get("pk"))

        self.__check_user_permission(task)

        web_archive_qs = models.WebArchive.objects.filter(task=task)
        filterset = self.filterset_class(request.GET, queryset=web_archive_qs)

        return render(request, self.template_name, {'task': task, 'filter': filterset})

    def __check_user_permission(self, task):
        if task.created_by != self.request.user:
            raise Http404


class TaskCreate(LoginRequiredMixin, FormView):
    login_url = '/login'
    template_name = 'task/task_form.html'
    success_url = '/task'

    def get(self, request, *argv, **kwargs):
        form = forms.TaskForm(user=request.user)
        formset = forms.WebPageFormSet(form_kwargs={'user': request.user})
        return self.render_to_response(
                self.get_context_data(form=form, formset=formset, form_name="New Task"))

    def post(self, *argv, **kwargs):
        form = forms.TaskForm(self.request.POST, user=self.request.user)
        formset = forms.WebPageFormSet(self.request.POST, form_kwargs={'user': self.request.user})

        if form.is_valid() and formset.is_valid():
            task = self.__create_task_from(form, formset)

            try:
                tasks.create_task_job(task)
            except Exception as e:
                logging.exception(e)
                self.__task_roll_back(task)


            return redirect('tasks')

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset, form_name="New Task"))

    @staticmethod
    def __create_task_from(form, formset):
        task = form.save()
        form.save_m2m()

        web_pages = [url_form.save() for url_form in formset if url_form.is_valid()]
        task.web_pages.add(*web_pages)
        task.save()

        return task

    @staticmethod
    def __task_roll_back(task):
        job = aps_models.DjangoJob.objects.filter(name=task.name)

        if job:
            job.delete()

        task.delete()


class TaskUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    template_name = 'task/task_form.html'
    success_url = '/task'
    model = models.Task
    fields = ['interval', 'rules']

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context['form_name'] = f"Edit Task - {self.object}"
        return context


class TaskDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = models.Task
    success_url = '/task'

    def delete(self, request, *args, **kwargs):
        task = models.Task.objects.get(pk=self.kwargs.get("pk"))
        models.WebArchive.objects.filter(task=task).delete()

        if task.job is not None:
            task.job.delete()

        task.delete()

        return HttpResponseRedirect(reverse('tasks'))


class WebArchiveDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    template_name = 'task/web_archive_detail.html'
    model = models.WebArchive
