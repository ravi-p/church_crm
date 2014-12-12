# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
#from django.dispatch import receiver
from django.db.models import Q

from django.db.models import Manager
from django.db.models.query import QuerySet

def get_full_name(self):
    """
    Return full name of user,if it not added then user name will be return
    """
    full_name = ''
    if self.first_name:
        full_name += self.first_name + ' '
    if self.last_name:
        full_name += self.last_name

    if full_name == '':
        full_name = self.username

    return full_name
User.full_name = property(get_full_name)
class Address(models.Model):
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=25, blank=True)
    zipcode = models.CharField(max_length=15, blank=True)
    street = models.CharField(max_length=250, blank=True)
    apartment = models.CharField(max_length=250, blank=True)
    class Meta:
        db_table = 'address'
        verbose_name_plural = 'addresses'

    def __unicode__(self):
        return ','.join([self.city, self.state, self.zipcode,self.street,self.apartment])

class Person(models.Model):
    user = models.OneToOneField(User)
    title = models.CharField(max_length=250, blank=True)
    prefix = models.CharField(max_length=20, blank=True)
    suffix = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.ForeignKey(Address, blank=True, null=True)
    class Meta:
        db_table = 'person'

class OrganizationType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=10000, blank=True)
    class Meta:
        db_table = 'organization_type'

    def __unicode__(self):
        return self.name

class Designation(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=10000, blank=True)
    class Meta:
        db_table = 'designation'

    #def delete(self):
        #VisitingCards.objects.filter(designation=self).delete()
        #super(Designation, self).delete()

    def __unicode__(self):
        return self.title


class OrgNameManager(models.Manager):
    """
    Model manager class
    """
    use_for_related_fields = True
    def get_queryset(self):
        """
        return objects in case insensitive order
        """
        org = super(OrgNameManager, self).get_queryset().filter().extra(
            select = {'lower_name':'lower(administrator)'}).order_by('lower_name')
        return org

class OrgAdminManager(models.Manager):
    def insensitive(self):
        """
        return objects in case insensitive order
        """
        org = self.objects.raw('select * from organization o,auth_user a on o.administrator_id=a.id order by a.username COLLATE NOCASE ASC')[:]


        return org


class OrganizationManager(models.Manager):
    use_for_related_fields = True
    def get_queryset(self):
        return super(OrganizationManager,self).get_queryset().all().order_by('administrator')

class Organization(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=10000, blank=True)
    administrator = models.ForeignKey(User, blank=True, null=True,
                      related_name='OrgAdmin')
    address = models.ForeignKey(Address, blank=True, null=True)
    types = models.ManyToManyField(OrganizationType, blank=True, null=True)
    designations = models.ManyToManyField(Designation, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    #pho = models.ForeignKey('Phone', blank=True, null=True)
    class Meta:
        db_table = 'organization'
        ordering = ['name','administrator']

    objects = models.Manager() # The default manager.
    cobjects = OrganizationManager()
    nm_objects = OrgNameManager() # The case insensitive name manager
    org_objects = OrgAdminManager()


    def __unicode__(self):
        return self.name
    @property
    def details( self ):
        return repr( dict( address=self.address,administrator=self.administrator ) )

#class VCManager(models.Manager):
#    use_for_related_fields = True
#    def get_queryset(self):
#        return super(VCManager, self).get_queryset().filter(
#            organization=Organization.objects.filter(administrator=self.request.user)
#            )

class VisitingCards(models.Model):
    designation = models.ForeignKey(Designation, related_name='orgusermap')
    organization = models.ForeignKey(Organization, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True)
    address = models.ForeignKey(Address, blank=True, null=True)
    public = models.BooleanField(default=True)

    #objects = VCManager()
    #objects = models.Manager()
    class Meta:
        db_table = 'visiting_cards'


class Phone(models.Model):
    phone_number = models.CharField(max_length=50)
    phone_type = models.ForeignKey('PhoneType', db_column='phone_type')
    designation = models.ForeignKey(Designation, null=True, blank=True)
    def __str__(self):
        return self.number
    class Meta:
        db_table = 'phone'

class PhoneType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=10000, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'phone_type'

#######################################################################################################################
#################################           Signals Zone             ##################################################
#######################################################################################################################

#def create_login(sender, **kwargs):
#    person = kwargs['instance']
#    if person.auth_user == None:
#        print('=============================')
#        print("Auth_user doesn't exist")
#        print('=============================')
#        login = AuthUser()
#        #login.username = person.
#        login.save()
#        login.first_name = person.first_name
#        login.last_name = person.last_name
#        person.administrator = login
#    print('=====================================')
#    print('Admin saved!!')
#    print('=====================================')
#
#def create_admin(sender, **kwargs):
#    savingObject = kwargs['instance']
#    if savingObject.administrator == None:
#        admin = Administrator()
#        admin.name = 'Administrator for ' + savingObject.name
#        admin.save()
#        savingObject.administrator = admin


#######################################################################################################################
#################################       Connect Signals Zone         ##################################################
#######################################################################################################################
#pre_save.connect(create_admin, sender=Organization)

#######################################################################################################################
#################################         End Signals Zone           ##################################################
#######################################################################################################################
