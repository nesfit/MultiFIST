from django.db import models
from django.conf import settings
from django.urls import reverse


# Create your models here.


class Rule(models.Model):
    RULE_TYPES = (
        ('r', 'regex'),
    )

    name = models.CharField(
        max_length=50,
        unique=True,
        blank=False)

    type = models.CharField(
        max_length=1,
        choices=RULE_TYPES,
        default='regex',
        blank=False)

    value = models.TextField(
        help_text="Rule searching attribute (regex, string, xpath)")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('rule_update', kwargs={'pk': self.id})

    class Meta:
        ordering = ['name']
        unique_together = (("name", "created_by"),)
