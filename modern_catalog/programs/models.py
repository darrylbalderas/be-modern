from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100)
    program = models.ForeignKey(Program,
                                related_name="sections",
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section,
                                related_name="activities",
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name
