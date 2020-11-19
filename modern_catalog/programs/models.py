from django.db import models
from django.db.models import JSONField


class Program(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Section(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    overview_image = models.URLField(blank=True)
    order_index = models.IntegerField(null=True)
    programs = models.ManyToManyField(Program)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order_index', )


class Activity(models.Model):
    name = models.CharField(max_length=100)
    choices = JSONField(blank=True, null=True, default=None)
    content = models.TextField(blank=True, null=True)
    sections = models.ManyToManyField(Section)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
