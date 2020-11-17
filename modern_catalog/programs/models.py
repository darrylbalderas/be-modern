from django.db import models


class Program(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    overview_image = models.URLField(blank=True)
    order_index = models.IntegerField(null=True)
    program = models.ForeignKey(Program,
                                related_name="sections",
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    section = models.ForeignKey(Section,
                                related_name="activities",
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name
