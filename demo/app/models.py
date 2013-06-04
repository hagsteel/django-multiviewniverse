from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Person, related_name='pets')

    def __unicode__(self):
        return self.name
