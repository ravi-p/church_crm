import autocomplete_light
from models import VisitingCards,Organization,Designation
from django.contrib.auth.models import User
class VCardsAutocomplete(autocomplete_light.AutocompleteModelBase):
    choices = (
        User.objects.all(),
        Organization.objects.all(),
        Designation.objects.all(),
    )

    search_fields = (
        ('first_name',),
        ('name',),
        ('title',),

    )
    #search_fields = ['organization']
autocomplete_light.register(VCardsAutocomplete)


class DesignationAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']
    autocomplete_js_attributes={'placeholder': 'Other model name ?',},
autocomplete_light.register(Designation, DesignationAutocomplete)



class OsAutocomplete(autocomplete_light.AutocompleteListBase):
    choices = ['Linux', 'BSD', 'Minix']
    autocomplete_template = 'designation_list.html'
autocomplete_light.register(OsAutocomplete)
