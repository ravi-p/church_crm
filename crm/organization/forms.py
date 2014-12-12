from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models import Q
import re
from django.core.validators import validate_email
from organization.models import Person, Address, Designation, Organization, OrganizationType,Phone,Phone,VisitingCards

from django.forms import ModelChoiceField, ModelMultipleChoiceField

class TypeCreateForm(ModelForm):
    """
    ModelForm to create new organization type.
    """
    org = forms.IntegerField(widget=forms.HiddenInput())
    class  Meta:
        model = OrganizationType

class OrgCreateForm(ModelForm):
    """
    To create new organization
    """
    designations = ModelMultipleChoiceField(Designation.objects.filter(~Q(title="Individual")))

    def __init__(self, *args, **kwargs):
        """
        while form instantiation,
        required fields=['administrator','phone','types']
        altered the order of field
        """
        super(OrgCreateForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['types'].required = True
        self.fields.keyOrder = ['name','administrator','types','designations','phone','description']
    class  Meta:
        model = Organization
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        fields = ['name','administrator','designations','phone','description','types']


    def clean_phone(self):
        """
        Phone number validation
        """
        phone = self.cleaned_data['phone']
        p = re.compile('(^[+0-9]{1,3})*([0-9]{10,11}$)')
        if p.match(phone)!= None :
            return phone
        else:
            raise forms.ValidationError('Please enter a valid phone number')


class OrgProfileUpdateForm(ModelForm):
    """
    while form instantiation,
    required fields=['phone']
    altered the order of field
    """
    def __init__(self, *args, **kwargs):
        super(OrgProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields.keyOrder = ['name','administrator','types','designations','phone','description']

    class  Meta:
        model = Organization
        exclude = ('address',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_phone(self):
        """
        Phone number validation
        """
        phone = self.cleaned_data['phone']
        p = re.compile('(^[+0-9]{1,3})*([0-9]{10,11}$)')
        if p.match(phone)!= None :
            return phone
        else:
            raise forms.ValidationError('Please enter a valid phone number')


class DesignationCreateForm(forms.ModelForm):
    class Meta:
        model = Designation
        exclude = ('address',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class UserForm(UserCreationForm):
    """
    To create new User
    """
    class Meta:
        """
        exluding user name and password field
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        exclude = ('user', 'password')

class ChangeUserForm(ModelForm):
    """
    To  alter User infomation
    """

    class Meta:
        """
        fields = ['username', 'first_name', 'last_name', 'email']
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password(self):
            return ""
    def is_valid_email(self):
        """
        Validating email field using Validate_email
        from django.core.validators import validate_email
        """
        email=self.cleaned_data['email']
        return validate_email(email)

class UserProfileForm(ModelForm):
    """
    Update user profile by admin
    """
    org = ModelChoiceField(Organization.objects.all())
    designations = ModelMultipleChoiceField(Designation.objects.all())
    class Meta:
        """
        exclude = ['user', 'address']
        """
        model = Person
        exclude = ['user', 'address']

class AddressForm(ModelForm):
    """
    AddressForm
    all fields=['city','state','zip','street','apartment']
    """
    class Meta:
        model = Address

class UploadFileForm(forms.Form):
    """ file upload form """
    file  = forms.FileField() #: FileField

class PersonForm(forms.ModelForm):
    """
    person form
    """
    class Meta:
        """
        exclude = ['user','address','prefix','suffix']
        """
        model=Person
        exclude = ['user','address','prefix','suffix']
    def clean_phone(self):
        """
        phone number validation
        """
        phone = self.cleaned_data['phone']
        p = re.compile('(^[+0-9]{1,3})*([0-9]{10,11}$)')
        if p.match(phone)!= None :
            return phone
        else:
            raise forms.ValidationError('Please enter a valid phone number')





class PhoneForm(ModelForm):
    class Meta:
        model=Phone
        exclude = ['phone_type']

class PhoneTypeForm(ModelForm):
    class Meta:
        exclude = ['description']


class VisitingCardUpdateForm(ModelForm):
    """
    VisitingCardUpdateForm

    """
    class Meta:
        """
        exclude = ['address',]
        """
        model = VisitingCards
        exclude = ['address',]
        fields = ['designation', 'organization', 'user', 'email']

    def __init__(self, *args, **kwargs):
        super(VisitingCardUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields.keyOrder = ['organization','designation','user','email']
    def clean_email(self):
        """
        Validating email field using Validate_email
        from django.core.validators import validate_email
        """
        email=self.cleaned_data['email']
        validate_email(email)
        return email
