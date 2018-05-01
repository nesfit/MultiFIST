from django import forms


from . import models


class WebArchiveSearchForm(forms.Form):
    url = forms.CharField(required=False)
    data = forms.CharField(required=False)
    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        self.task = kwargs.pop('task')
        super(WebArchiveSearchForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['class'] = "form-control rounded-0"
        self.fields['url'].widget.attrs['placeholder'] = "URL Address"
        self.fields['url'].label = "URL address"

        self.fields['data'].widget.attrs['class'] = "form-control rounded-0 border-right-0"
        self.fields['data'].widget.attrs['placeholder'] = "Data"

        self.fields['from_date'].widget.attrs['class'] = "form-control rounded-0"
        self.fields['from_date'].widget.attrs['data-toggle'] = "datepicker"
        self.fields['from_date'].label = "From"

        self.fields['to_date'].widget.attrs['class'] = "form-control rounded-0 border-left-0"
        self.fields['to_date'].widget.attrs['data-toggle'] = "datepicker"
        self.fields['to_date'].label = "To"

    def search(self):
        web_archives = self.task.webarchive_set.all()

 

        return web_archives



class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['name', 'interval', 'rules']

    INTERVAL_CHOICES = (
        (1, "Every minute"),
        (60, "Every hour"),
        (1440, "Every day"),
        (10080, "Every week"),
    )

    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Task name'
            })
    )

    interval = forms.ChoiceField(
        choices=INTERVAL_CHOICES,
        label="Interval",
        initial="Every minute",
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(TaskForm, self).save(commit=False)
        instance.created_by = self.user

        if commit:
            instance.save()

        return instance


class TaskUpdateForm(forms.ModelForm):
    pass


class WebPageForm(forms.ModelForm):
    class Meta:
        model = models.WebPage
        fields = ['url']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WebPageForm, self).__init__(*args, **kwargs)
        self.fields['url'].required = True

    def save(self, commit=True):
        instance = self.__get_instance()
        instance.created_by = self.user

        if commit:
            instance.save()
        return instance

    def __get_instance(self):
        try:
            instance = models.WebPage.objects.get(
                url=self.cleaned_data['url'], created_by=self.user)
        except models.WebPage.DoesNotExist:
            return super(WebPageForm, self).save(commit=False)
        else:
            return instance


class BaseWebPageFormSet(forms.BaseFormSet):
    def clean(self):

        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        url_list = []
        for form in self.forms:
            try:
                url = form.cleaned_data['url']
            except KeyError:
                raise forms.ValidationError("Please remove or fulfill empty URL field[s]")

            if url in url_list:
                raise forms.ValidationError("Web Pages in a set must have distinct URL addresses.")
            url_list.append(url)


WebPageFormSet = forms.formset_factory(WebPageForm, formset=BaseWebPageFormSet)
