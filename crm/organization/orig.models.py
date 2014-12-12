from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('org_update', kwargs={'pk': self.pk})


class OrganizationType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, )
    orgs = models.ManyToManyField(Organization, related_name="types", null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('orgtype_update', kwargs={'pk': self.pk})


class Contact(models.Model):
    fname = models.CharField(max_length=255, )
    lname = models.CharField(max_length=255, )
    title = models.CharField(max_length=255, )
    phone = models.CharField(max_length=255, null=True, blank=True)
    fax = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, )
    email = models.EmailField(max_length=255, )

    user = models.ForeignKey(User)
    orgs = models.ManyToManyField(Organization, null=True, blank=True)


    def __unicode__(self):
        return self.fname + " " + self.lname

    def get_absolute_url(self):
        return reverse('contact_update', kwargs={'pk': self.pk})

    def set_password(self, pwd):
        #this is dummy method to work with inherited userform
        return

