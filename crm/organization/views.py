from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.views import login
from django.db.models import Q
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from django.dispatch import receiver
from django.utils.decorators import method_decorator

from django.conf import settings
from organization.models import Organization, OrganizationType, Designation, Person, OrganizationType, VisitingCards, Address,Phone,PhoneType

from organization.forms import AddressForm, DesignationCreateForm, OrgCreateForm, UserForm, ChangeUserForm, UploadFileForm, PersonForm,VisitingCardUpdateForm

from django.http import StreamingHttpResponse,HttpResponseBadRequest,HttpResponseServerError
from organization.forms import OrgProfileUpdateForm
import pdb
import json
from django.core.mail import send_mass_mail,send_mail
import threading
import thread
from django.template import Context
from django.template.loader import get_template
import logging
logger = logging.getLogger(__name__)


def custom_login(request, **kwargs):
    """
    will authenticate user and redirect home page if user is valid
    """
    if request.user and request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        return login(request, **kwargs)

class OrgTypeList(ListView):
    """
    to display list of organization
    """
    model = OrganizationType
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(OrgTypeList, self).get_context_data(**kwargs)
        context['sort_on'] = self.temp
        context['srt_ord'] = self.sort_ordr
        return context

    def get_queryset(self):
        """
        will get 'search' or 'sort_by' parameter from request,
        based on that objects list is return to template
        """

        search_str = self.request.GET.get('search', None)
        col_nm = self.request.GET.get('sort_by', "name")
        self.temp=col_nm
        sort_order = self.request.GET.get('sort_order', "ASC")
        self.sort_ordr=sort_order
        if search_str:
            a = Q(name__icontains = search_str)
            b = Q(description__icontains = search_str)
            objects = self.model.objects.filter(a | b).distinct()

        else:
            objects = OrganizationType.objects.filter().extra(
                select = {col_nm:'lower('+col_nm+')'}).order_by(col_nm)

            if sort_order == "DESC":
                objects = objects.reverse()
        return objects

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            srch=self.request.GET.get('search', None)
            if srch:
                results = []
                search_q = OrganizationType.objects.filter(name__startswith=srch).values('name')
                results = [i['name'] for i in search_q]
                search_q=OrganizationType.objects.filter(description__startswith=srch).values('description')
                temp = [i['description'] for i in search_q]
                results=results+temp

                resp = self.request.REQUEST['callback'] + '(' + json.dumps(results) + ');'
                return HttpResponse(resp, content_type='application/json')
        return super(OrgTypeList, self).dispatch(*args, **kwargs)

class OrgTypeCreate(CreateView):
    """
    class based generic view (CreateView) to create new organization
    """
    model = OrganizationType
    template_name = 'create_type.html'
    success_url = "/org/orgtype/list"

    def form_valid(self, form):
        """
        Called when a form is valid. will display success message after adding org
        """
        response = super(OrgTypeCreate, self).form_valid(form)
        messages.success(
                self.request, "Organization Type, '%s', added successfully" % self.object.name
        )
        return response
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrgTypeCreate, self).dispatch(*args, **kwargs)

class OrgTypeUpdate(UpdateView):
    """
    The view which will update organization type
    """
    model = OrganizationType
    template_name = 'add_edit.html'
    success_url = "/org/orgtype/list"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrgTypeUpdate, self).dispatch(*args, **kwargs)


class OrgTypeDelete(DeleteView):
    """
    The view which will delete organization type
    """
    model = OrganizationType
    success_url = "/org/orgtype/list"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrgTypeDelete, self).dispatch(*args, **kwargs)

class OrgCreate(SuccessMessageMixin, CreateView):
    """
    Mixin view which will create new organization
    """
    model = Organization
    template_name = 'create_org.html'
    form_class = OrgCreateForm
    success_url = "/org/list/"
    success_message = "Organization \"%(name)s\" was created successfully"

    def post(self, request, *args, **kwargs):
        super(OrgCreate, self).post(request, *args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        print form.is_valid()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Called if a form is valid, and will save new instance to database
        """
        self.object = form.save(commit=False)
        self.object.administrator = self.request.user
        form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        request = self.request
        #if not request.user.is_superuser:
        #    messages.error(request, "Permission Error")
        #    return HttpResponseRedirect("/org/list/")

        return super(OrgCreate, self).dispatch(*args, **kwargs)

class OrgUpdate(UpdateView):
    """
    class based generic view(Updateview), for site admin to update organization
    """
    model = Organization
    template_name = 'create_org.html'
    form_class = OrgCreateForm
    success_url = "/org/list/"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrgUpdate, self).dispatch(*args, **kwargs)

class OrgProfileUpdate(UpdateView):
    """
    class based generic view(Updateview), for organization admin to update his organization profile
    """
    model = Organization
    template_name = 'edit_org_profile.html'
    form_class = OrgProfileUpdateForm
    success_url = "/org/list/"

   # def get_form(formclass,request):
   #     if formclass.exclude:
   #         if not request.user.is_superuser:
   #             formclass.exclude.append('administrator')
   #     return super(OrgProfileUpdate,self).get_form(formclass, request)


    def get(self, request, *args, **kwargs):
        """
        HTTP method that will pickup organization profile instance to update,
        if user is not a site admin,administrator field will be excluded.
        because only site admin have rights to alter organization admin.
        """

        self.object = self.get_object()
        formclass = self.get_form_class()
        opform = self.get_form(formclass)
        if not request.user.is_superuser:
            del opform.fields['administrator']
        addrform = AddressForm(instance=self.object.address)
        return self.render_to_response(
            self.get_context_data(
                form=opform,
                address_form=addrform,
            )
        )

    def post(self, request, *args, **kwargs):
        """
        HTTP method which accept the data filled  and call validation method
        """
        self.object = self.get_object()
        formclass = self.get_form_class()
        opform = self.get_form(formclass)
        if not request.user.is_superuser:
            del opform.fields['administrator']
        addrform = AddressForm(data=self.request.POST,
                instance=self.object.address)
        self.types = self.request.POST.getlist('types')
        self.desigs = self.request.POST.getlist('designations')
        if opform.is_valid() and addrform.is_valid():
            return self.form_valid(opform, addrform)
        else:
            return self.form_invalid(opform, addrform)

    def form_valid(self, form, address_form):
        addr = address_form.save()
        """
        Called if a form is valid. and update existing instance
        """
        org = form.save(commit=False)
        # Clear current types
        org.types.clear()
        # Add selected types
        new_types = OrganizationType.objects.filter(pk__in=self.types)
        map(org.types.add, new_types)
        if not org.address:
            org.address = addr

        # Check if designations changed
        current_desigs = org.designations.values_list('pk', flat=True)
        new_desigs = map(int, self.desigs)
        del_desigs = list(set(current_desigs) - set(new_desigs))
        add_desigs = list(set(new_desigs) - set(current_desigs))

        # for each del_desig remove all the visiting cards as well.
        VisitingCards.objects.filter(organization=org, designation__in=del_desigs).delete()

        # Add new desigs if any
        map(org.designations.remove, del_desigs)
        map(org.designations.add, add_desigs)

        org.save()
        messages.success(self.request, "Update Successfully")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, address_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """

        return self.render_to_response(self.get_context_data(form=form,
                                  address_form=address_form))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        Permission checking before update organization profile.
        """
        request = self.request
        user = request.user
        self.object = self.get_object()
        if not self.object in Organization.objects.filter(administrator=user):
            messages.error(request, "Permission Error")
            return HttpResponseRedirect("/org/list/")

        return super(OrgProfileUpdate, self).dispatch(*args, **kwargs)

class OrgList(ListView):
    model = Organization
    paginate_by = 10
    template_name = 'organization/organization_list.html'

    def get_context_data(self, **kwargs):
        context = super(OrgList, self).get_context_data(**kwargs)
        context['sort_on'] = self.temp
        context['srt_ord'] = self.sort_ordr
        return context

    def get_queryset(self):
        """
        will get 'search' or 'sort_by' parameter from request,
        based on that objects list is return to template
        """
        search_str = self.request.GET.get('search')
        col_nm = self.request.GET.get('sort_by', "name")
        self.temp=col_nm
        sort_order = self.request.GET.get('sort_order', "ASC")
        self.sort_ordr=sort_order

        if search_str:
            search_str = self.request.GET.get('search', None)
            a = Q(name__icontains=search_str)
            b = Q(administrator__first_name__icontains = search_str)
            c = Q(administrator__last_name__icontains = search_str)
            d = Q(administrator__username__icontains = search_str)
            e = Q(types__name__icontains = search_str)
            f = Q(description__icontains = search_str)
            objects = Organization.objects.filter(a | b | c | d | e | f).distinct()

        else: # SORTING BY COL_NM
            if col_nm in ['name', 'description'] :
                objects = Organization.objects.filter().extra(
                    select = {col_nm:'lower('+col_nm+')'}).order_by(col_nm)

                if sort_order == "DESC":
                    objects = objects.reverse()
            elif col_nm =='administrator__first_name':
                objects=Organization.objects.filter().order_by(col_nm)
                if sort_order == "DESC":
                    objects = objects.reverse()
            else:
                objects=Organization.objects.extra(select=
                    {'name':'lower(name)'}).order_by('name')


        return objects

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            srch=self.request.REQUEST['search']
            if srch:
                results = []
                search_q1 = Organization.objects.filter(name__startswith=srch).values('name')
                results = [i['name'] for i in search_q1]
                search_q2 = OrganizationType.objects.filter(name__startswith=srch).values('name')
                temp=[i['name'] for i in search_q2]
                results=results+temp
                search_q4 = Organization.objects.filter(
                        description__startswith=srch).values('description')
                temp=[i['description'] for i in search_q4]
                results=results+temp
                search_q3 = User.objects.filter(first_name__startswith=srch).values('first_name')
                temp=[i['first_name'] for i in search_q3]
                results=results+temp

                resp = self.request.REQUEST['callback'] + '(' + json.dumps(results) + ');'
                return HttpResponse(resp, content_type='application/json')
        return super(OrgList, self).dispatch(*args, **kwargs)


class OrgDelete(SuccessMessageMixin, DeleteView):
    """
    The view which will delete organization,
    org admin and site admin can delete the orgnanization.
    """
    model = Organization
    success_url = "/org/list"
    success_message = "Organization deleted successfully"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        request = self.request
        return super(OrgDelete, self).dispatch(*args, **kwargs)

class DesignationList(ListView):
    model = Designation
    paginate_by = 10
    description='description'

    def get_context_data(self, **kwargs):
        context = super(DesignationList, self).get_context_data(**kwargs)
        context['temp'] =self.temp
        context['sort_on'] =self.temp
        context['srt_ord'] =self.sort_ordr
        return context

    def get_queryset(self):
        """
        will get 'search' or 'sort_by' parameter from request,
        based on that objects list is return to template
        """
        search_str = self.request.GET.get('search', None)
        col_nm = self.request.GET.get('sort_by', 'title')
        self.temp=col_nm
        sort_order = self.request.GET.get('sort_order', 'ASC')
        self.sort_ordr=sort_order
        if search_str:
            search_str = self.request.GET.get('search', None)
            a = Q(title__icontains = search_str)
            b = Q(description__icontains = search_str)
            objects = Designation.objects.filter(a | b).distinct()
        else: # SORTING BY COL_NM
            objects = Designation.objects.filter().extra(
                select = {col_nm:'lower('+col_nm+')'}).order_by(col_nm)

            if sort_order == "DESC":
                objects = objects.reverse()
        return objects



    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            srch=self.request.REQUEST['search']
            if srch:
                results = []
                search_q = Designation.objects.filter(title__startswith=srch).values('title')
                results = [i['title'] for i in search_q]
                search_q=Designation.objects.filter(description__startswith=srch).values('description')
                temp = [i['description'] for i in search_q]
                results=results+temp

                resp = self.request.REQUEST['callback'] + '(' + json.dumps(results) + ');'
                return HttpResponse(resp, content_type='application/json')
        return super(DesignationList, self).dispatch(*args, **kwargs)

class DesignationUpdate(UpdateView):
    """
    class based generic view(Updateview), for site admin to update designation
    """
    model = Designation
    template_name = 'add_edit_org.html'
    form_class = DesignationCreateForm
    success_url = "/org/designation/list/"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DesignationUpdate, self).dispatch(*args, **kwargs)

class DesignationCreate(CreateView):
    """
    class based generic view(CreateView), for create new designation
    """
    template_name = 'create_designation.html'
    model = Designation
    form_class = DesignationCreateForm
    success_url = "/org/designation/list/"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DesignationCreate, self).dispatch(*args, **kwargs)

class DesignationDelete(DeleteView):
    """
    class based generic view(DeleteView), for delete designation
    """
    model = Designation
    success_url = "/org/designation/list/"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DesignationDelete, self).dispatch(*args, **kwargs)

class PersonList(ListView):
    """
    A List view to display list of user in system
    """
    model = Person
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PersonList, self).get_context_data(**kwargs)
        context['sort_on'] =self.col
        context['srt_ord'] =self.sort_ordr
        return context
    def get_queryset(self):
        """
        will get 'search' or 'sort_by' parameter from request,
        based on that objects list is return to template
        """
        search_str = self.request.GET.get('search', None)
        col_nm = self.request.GET.get('sort_by', "user__username")
        self.col=col_nm
        pg = self.request.GET.get('page', None)
        self.request.session['pg_no']=pg
        sort_order = self.request.GET.get('sort_order', "ASC")
        self.sort_ordr=sort_order

        if search_str:
            a = Q(user__first_name__icontains = search_str)
            b = Q(user__last_name__icontains = search_str)
            c = Q(user__username__icontains = search_str)
            d = Q(user__email__icontains = search_str)
            e = Q(title__icontains = search_str)
            objects = Person.objects.filter(a | b | c | d | e).distinct()
        elif col_nm:
            objects = Person.objects.filter().order_by(col_nm)
            #if pg:
            #    print self.paginator_class
            #    if self.request.session['pg_no']==pg:
            #        p=self.paginator_class(objects,5)
            #        page1=p.page(pg)
            #        print page1.object_list
            #        return page1.object_list

            if sort_order == "DESC":
                objects = objects.reverse()
        return objects

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            srch=self.request.REQUEST['search']
            if srch:
                results = []
                search_q1 = Person.objects.filter(title__startswith=srch).values('title')
                results = [i['title'] for i in search_q1]
                search_q2 = User.objects.filter(email__startswith=srch).values('email')
                temp=[i['email'] for i in search_q2]
                results=results+temp
                search_q3 = User.objects.filter(first_name__startswith=srch).values('first_name')
                temp=[i['first_name'] for i in search_q3]
                search_q4 = User.objects.filter(last_name__startswith=srch).values('last_name')
                temp=[i['last_name'] for i in search_q4]
                results=results+temp
                results=list(set(results))
                resp = self.request.REQUEST['callback'] + '(' + json.dumps(results) + ');'
                return HttpResponse(resp, content_type='application/json')
        return super(PersonList, self).dispatch(*args, **kwargs)

class UserCreate(CreateView):
    """
    View to create new user,
    only site admin have right to add new user.
    """
    model = User
    template_name = "create_user.html"
    form_class = UserForm
    success_url = '/org/user/list'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserCreate, self).dispatch(*args, **kwargs)

class UserUpdate(UpdateView): # for each user by admin
    """
    View to delete user,
    only site admin have right to update user.
    """
    model = Person
    template_name = "edit_user_profile.html"
    form_class = PersonForm
    success_url = '/org/user/list'

    def get_object(self,pk):
       """
       overridden method to get instance of person insted of user
       """
       # return Person.objects.get(user=self.request.user)
       p,c = Person.objects.get_or_create(user_id=pk)
       return p

    def get(self, request,pk, *args, **kwargs):
        self.object = self.get_object(pk)
        formclass = self.get_form_class()
        ppform = self.get_form(formclass)
        addrform = AddressForm(instance=self.object.address)
        cuform = ChangeUserForm(instance=self.object.user)
        return self.render_to_response(
            self.get_context_data(ppform=ppform,address_form=addrform,cuform=cuform))

    def post(self, request,pk, *args, **kwargs):
        """
        HTTP method which accept the data filled  and call validation method
        """
        self.object = self.get_object(pk)
        formclass = self.get_form_class()
        ppform = self.get_form(formclass)
        addrform = AddressForm(data=self.request.POST,
            instance=self.object.address)
        cuform = ChangeUserForm(data=self.request.POST,
            instance=self.object.user)

        if ppform.is_valid() and addrform.is_valid() and cuform.is_valid():
            return self.form_valid(ppform, addrform, cuform)
        else:
            return self.form_invalid(ppform, addrform,cuform)

    def form_valid(self, ppform, address_form,cuform):
        addr = address_form.save()
        cuformo = cuform.save()
        ppform.save()
        self.object.address = addr
        self.object.user = cuformo
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, ppform, address_form,cuform):
        """
        Called if a form is invalid.
        """
        return self.render_to_response(self.get_context_data(ppform=ppform,
            address_form=address_form,cuform=cuform))


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdate, self).dispatch(*args, **kwargs)

class UserDelete(DeleteView):
    """
    class based generic view(DeleteView), for delete user
    only site admin have right to delete user.
    """
    model = User
    success_url = "/org/user/list"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDelete, self).dispatch(*args, **kwargs)

class VCardList(ListView):
    """
    Listview to display VisitingCards
    """

    model = VisitingCards
    paginate_by = 10
    template_name = 'organization/visitingcards_list.html'

    def get_context_data(self,**kwargs):
        context=super(VCardList,self).get_context_data(**kwargs)
        context['sort_on'] =self.temp
        context['srt_ord'] =self.sort_ordr
        return context
    def get_queryset(self):

        """
        will get 'search'  parameter from request,
        based on that objects list is return to template
        """
        search_str = self.request.GET.get('search', None)
        col_nm = self.request.GET.get('sort_by', "user")
        self.temp=col_nm
        sort_order = self.request.GET.get('sort_order', "ASC")
        self.sort_ordr=sort_order
        if search_str:
            a = Q(user__first_name__icontains = search_str)
            b = Q(user__last_name__icontains = search_str)
            c = Q(user__username__icontains = search_str)
            d = Q(organization__name__icontains = search_str)
            e = Q(designation__title__icontains = search_str)
            objects = self.model.objects.filter(a | b | c | d | e).distinct()
        else:
            objects=VisitingCards.objects.all().order_by(col_nm)
            if sort_order == "DESC":
                objects = objects.reverse()

        return objects

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            srch=self.request.REQUEST['search']
            if srch:
                results = []
                search_q1 = Designation.objects.filter(title__startswith=srch)
                search_q2 = User.objects.filter(first_name__startswith=srch)
                search_q3 = Organization.objects.filter(name__startswith=srch)
                for r in search_q1:
                    results.append(r.title)
                for r in search_q2:
                    results.append(r.first_name)
                for r in search_q3:
                    results.append(r.name)
                resp = self.request.REQUEST['callback'] + '(' + json.dumps(results) + ');'
                return HttpResponse(resp, content_type='application/json')
        return super(VCardList, self).dispatch(*args, **kwargs)

class VCardUpdate(UpdateView):
    """
    View to update visiting card,
    only site admin and org admin have right to update update visiting card
    """

    model = VisitingCards
    template_name = 'add_edit.html'
    form_class = VisitingCardUpdateForm
    success_url = "/org/vcard/list"

    #def get_queryset(self):
    #    organization=Organization.objects.filter(administrator=self.request.user)
    #    return VisitingCards.objects.filter(organization=organization)

    def get(self, request,pk, *args, **kwargs):
        if request.is_ajax():
            print 'ajax Get'
        self.object = self.get_object()
        formclass = self.get_form_class()
        form = self.get_form(formclass)
        return self.render_to_response(self.get_context_data(form=form,pk=pk))

    def post(self, request,pk, *args, **kwargs):
        if request.is_ajax():
            print 'ajax Post'
            self.object = self.get_object()
            formclass = self.get_form_class()
            form = self.get_form(formclass)

            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form,pk)
        else:
            print 'no ajax call'
            self.object = self.get_object()
            formclass = self.get_form_class()
            form = self.get_form(formclass)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self,form):
        form.save()
        update_dict={}
        desig = self.object.designation.title
        org = self.object.organization.name
        usr = self.object.user.get_full_name()
        u_id = self.object.user.id
        id = self.object.id
        update_dict={'org':org,'desig':desig,'usr':usr,'u_id':u_id,'id':id}
        return HttpResponse(json.dumps(update_dict))
        #return HttpResponse(self.object.id)

    def form_invalid(self,form,pk):
        #return self.render_to_response(self.get_context_data(form=form,pk=pk))
        errors_dict = {}
        if form.errors:
            for error in form.errors:
                e = form.errors[error]
                errors_dict[error] = unicode(e)
        #return HttpResponseBadRequest(json.dumps(errors_dict))
        return HttpResponseServerError(json.dumps(errors_dict))


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        request = self.request
        user = request.user
        self.object = self.get_object()

        if not self.object.organization in \
            Organization.objects.filter(administrator=user):
            messages.error(request, "Permission Error")
            return HttpResponseRedirect("/org/list/")

        return super(VCardUpdate, self).dispatch(*args, **kwargs)


#def VCardUpdate(request,pk):
#    if request.method == "GET":
#        vcard=VisitingCards.objects.get(pk=pk)
#        organization = Organization.objects.filter(administrator=request.user)
#        desig_list = organization.values_list('designations', flat=True)
#        designation = Designation.objects.filter(pk__in=desig_list)
#        return render_to_response('organization/vcardupdate.html',
#            {'organization': organization,'designation':designation},
#            context_instance=RequestContext(request))
#


class VCardDelete(DeleteView):
    """
    View to delete card,
    only site admin and org admin have right to delete visiting card
    """
    model = VisitingCards
    success_url = "/org/vcard/list/"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        request = self.request
        user = request.user
        self.object = self.get_object()
        if not self.object.organization in \
            Organization.objects.filter(administrator=user):
            messages.error(request, "Permission Error")
            return HttpResponseRedirect("/org/list/")

        return super(VCardDelete, self).dispatch(*args, **kwargs)

@login_required
def employee_add(request, user_id):
    """
    function based view,
    organization admin can add users as emp to his organizations
    """

    if request.method == "GET":
        employee = User.objects.get(pk=user_id)
        orgs = Organization.objects.filter(administrator=request.user)

        #desig_list = orgs.values_list('designations', flat=True)
        #designations = Designation.objects.filter(pk__in=desig_list)

        return render_to_response('organization/employee_add1.html',
            {'employee':employee, 'orgs': orgs},
            context_instance=RequestContext(request))

    user_id = request.POST.get('employee_id')
    org = request.POST.get('add2orgs') # id of selected org
    designations_list = request.POST.getlist('designations2add')#list of ids of selected designation

    try:
        user = User.objects.get(pk=user_id)# emp obj to add
        org = Organization.objects.get(pk=org)#selected org objects
        designations = Designation.objects.filter(pk__in=designations_list)#convert desig id in obj
    except Exception, e:
        # log this error
        print str(e)
        messages.error(request, str(e))
        user = org = designations = None

    if not (user and designations.count()):
        # add error message.
        messages.error(request, "Select atleast one Organization and its Designation")
        # redirect to the same page.
        return HttpResponseRedirect(request.path)

    #def send_email():
    #    template = get_template('organization/confirmation_email.txt')
    #    context = Context({'user':user,'org':o.organization,'desig':desig})
    #    subject = u'confirmation email'
    #    message = template.render(context)
    #    send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,['ravirajmca12@gmail.com'])

    # create  visiting card(s) for the employee
    try:
        l=[]
        for desig in designations:
            if desig in org.designations.all():
                o,c = VisitingCards.objects.get_or_create(organization=org,
                    designation=desig, user=user)

                if c:
                    #send_email()
                    template = get_template('organization/confirmation_email.txt')
                    context = Context({'user':user,'org':o.organization,'desig':desig})
                    subject = u'confirmation email'
                    message = template.render(context)
                    msg = (subject,message,settings.DEFAULT_FROM_EMAIL, ['ravirajmca12@gmail.com'])
                    l.append(msg)
                    #t=threading.Thread(target=send_email)
                    #t.start()
                    messages.success(request,"Employee Added Succefully..!")
                else:
                    messages.info(request," %s Already Added ..!" % user.username)
            else:
                messages.error(request,"%s Doesnt have selected designation %s .!" %(orgs, desig))
                raise Exception()
        if c:
            tupl=tuple(l)
            threading.Thread(send_mass_mail(tupl, fail_silently=False)).start()
            messages.success(request,"Employee Added Succefully..!")



    except:
        messages.error(request,"something went wroung ")
        return HttpResponseRedirect(request.path)

    return HttpResponseRedirect("/org/user/list")






@login_required
def user_details(request, user_id):
    """
    function based view to display user profile and visiting cards the user has
    """
    user = User.objects.get(pk=user_id)
    maps = VisitingCards.objects.filter(user=user).filter(~Q(designation__title='Individual'))
    orgs = [m.organization for m in maps]
    designations = [m.designation for m in maps]

    # Remove None objects
    from operator import is_not
    from functools import partial
    designations = filter(partial(is_not, None),designations)
    orgs = list(set(orgs))

    return render_to_response('organization/user_details.html',
        {"orgs": orgs, "maps": maps, "designations": designations, "puser": user},
        context_instance=RequestContext(request))

@login_required
def org_details(request, org_id):
    """
    function based view to display org profile and available visiting cards in organization
    """
    org = Organization.objects.get(pk=org_id)
    maps = VisitingCards.objects.filter(organization=org)
    designations = [m.designation for m in maps]
    users = [m.user for m in maps]
    # Remove None objects
    from operator import is_not
    from functools import partial
    designations = filter(partial(is_not, None),designations)
    users = filter(partial(is_not, None),users)

    return render_to_response('organization/details.html',
        {"org": org, "maps": maps, "designations": designations, "users":users},
        context_instance=RequestContext(request))

@login_required
def user_upload(request):
    """
    To add multiple users at once using cvs file
    only site admin have right to add user
    """

    if not request.user.is_superuser:

        HttpResponseRedirect(reverse('login'))

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            _handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('user_list'))
        else:
            messages.error(request, "Invalid file %s" % str(form.errors))

    return render_to_response('upload_file.html', {"form": UploadFileForm()},
        context_instance=RequestContext(request))

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)
        designation = Designation.objects.get(pk=1)
        VisitingCards.objects.create(designation=designation, user=instance)

@receiver(post_delete, sender=Organization)
def delete_org_address(sender, instance, using, **kwargs):
    try:
        if instance.address:
            instance.address.delete()
    except Exception, e:
        messages.error(request, "Error deleting address associated to org <br/>%s" % str(e))

def _handle_uploaded_file(f):
    def gen_password():
        # set username as the password
        return record["username"]

    def check_record():
        for header in ['username']:
            if record[header] == '':
                raise Exception("Invalid record")

    ufile = '/tmp/user_list.txt'
    with open(ufile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    destination.close()

    import csv
    with open(ufile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        headers = [x.lower() for x in spamreader.next()]

        for row in spamreader:
            record = dict(zip(headers, row))
            # check if required files are populated.
            try:
                check_record()
                # create random password
                record["password"] = gen_password()
            except:
                # need to handle this error
                # move to next record.
                continue

            print record
            try:
                username = record.pop("username")
                email = record.pop("email")
                password = record.pop("password")
                user = User.objects.create_user(username, email, password, **record)
                user.save()
            except:
                continue



class my_contact_page(UpdateView):
    """
    class based generic view.
    user can update his profile
    """
    model = Person
    template_name = 'edit_user_profile.html'
    success_url = "/org/list"
    form_class = PersonForm

    def get_object(self):
       """
       overridden get_object method to get instance of person
       """
       # return Person.objects.get(user=self.request.user)
       p,c = Person.objects.get_or_create(user=self.request.user)
       return p

    def get(self, request, *args, **kwargs):
        """
        HTTP get method to get profile instance of logged in user
        """
        self.object = self.get_object()
        formclass = self.get_form_class()
        ppform = self.get_form(formclass)
        addrform = AddressForm(instance=self.object.address)
        cuform = ChangeUserForm(instance=self.object.user)
        return self.render_to_response(
            self.get_context_data(ppform=ppform,address_form=addrform,cuform=cuform))

    def post(self, request, *args, **kwargs):
        """
        HTTP method which accept the data filled  and call validation method
        """
        self.object = self.get_object()
        formclass = self.get_form_class()
        ppform = self.get_form(formclass)
        addrform = AddressForm(data=self.request.POST,
            instance=self.object.address)
        cuform = ChangeUserForm(data=self.request.POST,
            instance=self.object.user)

        if ppform.is_valid() and addrform.is_valid() and cuform.is_valid():
            return self.form_valid(ppform, addrform,cuform)
        else:
            return self.form_invalid(ppform, addrform,cuform)


    def form_valid(self, ppform, address_form,cuform):
        """
        Called if a form is valid. and update existing instance
        """
        addr = address_form.save()
        cuformo = cuform.save()
        ppform.save()
        self.object.address = addr
        self.object.user = cuformo
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, ppform, address_form,cuform):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(self.get_context_data(ppform=ppform,
            address_form=address_form,cuform=cuform))
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(my_contact_page, self).dispatch(*args, **kwargs)







def autocompleteModel(request):
    search_qs = Designation.objects.filter(title__startswith=request.REQUEST['search'])
    results = []
    for r in search_qs:
        results.append(r.title)
    resp = request.REQUEST['callback'] + '(' + json.dumps(results) + ');'
    return HttpResponse(resp, content_type='application/json')




def myfunction():
    logger.debug("this is a debug message!")

def myotherfunction():
    logger.error("this is an error message!!")






