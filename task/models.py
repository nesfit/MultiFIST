from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.postgres.fields import JSONField
import ast
import os

# third party imports
import django_apscheduler.models as aps_models
import humanfriendly

# local imports
from rule import models as rule_models


class WebPage(models.Model):
    url = models.URLField(blank=False, null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='created_by')

    def __str__(self):
        return f"{self.url}"

    class Meta:
        unique_together = (("url", "created_by"),)


class Task(models.Model):
    name = models.CharField(max_length=100,
                            unique=True)

    interval = models.IntegerField(blank=False,
                                   null=False)

    job = models.OneToOneField(aps_models.DjangoJob,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    web_pages = models.ManyToManyField('WebPage')

    rules = models.ManyToManyField(rule_models.Rule)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('task', kwargs={'pk': self.id})

    def get_resume_url(self):
        return reverse('task_resume', kwargs={'name': self.name})

    def get_pause_url(self):
        return reverse('task_pause', kwargs={'name': self.name})

    def get_edit_url(self):
        return reverse('task_edit', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('task_delete', kwargs={'pk': self.id})

    def get_readable_interval(self):
        return humanfriendly.format_timespan(self.interval * 60)

    class Meta:
        unique_together = (("name", "created_by"),)


class WebArchive(models.Model):
    location = models.FilePathField()
    archive_hash = models.TextField()
    accessed_time = models.DateTimeField()
    web_page = models.ForeignKey('WebPage',
                                 on_delete=models.CASCADE,
                                 related_name='web_page')
    task = models.ForeignKey('Task',
                             on_delete=models.CASCADE)
    scraped_data = JSONField()

    class Meta:
        ordering=["-accessed_time"]

    def get_absolute_url(self):
        return reverse('web_archive_detail',
                       kwargs={'task_pk': self.task.id,
                               'pk': self.id}
                       )

    def get_scraped_data(self):
        try:
            scraped_data_dict = ast.literal_eval(self.scraped_data)
        except Exception:
            return {}
        else:
            return scraped_data_dict

    def get_web_archive_filename(self):
        return os.path.basename(self.location)