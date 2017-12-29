from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import MentoringRelationship, MentoringRecord, Mission
from .models import ApplyCountry, ApplySchool, ApplyCollege, ApplyMajor, ApplyDegree
from .user_forms import AdministratorCreationForm, AdministratorChangeForm
from .user_forms import TeacherCreationForm, TeacherChangeForm
from .user_forms import StudentCreationForm, StudentChangeForm
from .forms import MentoringRelationshipCreationForm, MentoringRecordCreationForm, MissionCreationForm
from .forms import ApplyManagementCountryCreationForm, ApplyManagementSchoolCreationForm, ApplyManagementCollegeCreationForm, ApplyManagementMajorCreationForm, ApplyManagementDegreeCreationForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils.translation import gettext as _
import datetime

# Create your views here.

@login_required
def overview(request):
    return redirect(reverse('dashboard:MissionListView'))

class ApplyManagementDegreeListView(LoginRequiredMixin, ListView):
    page_title = "院校申请信息管理"
    page_subtitle = "列表"
    page_tab = "学位"
    template_name = "dashboard/apply_management_degree_list.html"
    page_add = reverse_lazy('dashboard:ApplyManagementDegreeCreationView')
    success_url = reverse_lazy('dashboard:ApplyManagementDegreeListView')
    model = ApplyDegree
    paginate_by = 40
    def try_list_int(self, l):
        for i in l:
            if i != 'cancel':
                try:
                    int(i)
                except ValueError:
                    raise Http404("id格式错误")
    def get_apply_ids(self, id_str):
        ids = self.request.GET.getlist(id_str)
        self.try_list_int(ids)
        if 'cancel' in ids:
            return []
        else:
            return ids
    def get_apply_degree(self):
        apply_country_ids = self.get_apply_ids('apply_country_id')
        apply_school_ids = self.get_apply_ids('apply_school_id')
        apply_college_ids = self.get_apply_ids('apply_college_id')
        apply_major_ids = self.get_apply_ids('apply_major_id')
        apply_degree = ApplyDegree.objects.all()
        if len(apply_country_ids) > 0:
            apply_degree = apply_degree.filter(apply_country__id__in = apply_country_ids)
        if len(apply_school_ids) > 0:
            apply_degree = apply_degree.filter(apply_school__id__in = apply_school_ids)
        if len(apply_college_ids) > 0:
            apply_degree = apply_degree.filter(apply_college__id__in = apply_college_ids)
        if len(apply_major_ids) > 0:
            apply_degree = apply_degree.filter(apply_major__id__in = apply_major_ids)
        return apply_degree
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementDegreeListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_add'] = self.page_add
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', 'name')
        context['apply_country_id'] = self.get_apply_ids('apply_country_id')
        context['apply_school_id'] = self.get_apply_ids('apply_school_id')
        context['apply_college_id'] = self.get_apply_ids('apply_college_id')
        context['apply_major_id'] = self.get_apply_ids('apply_major_id')
        context['query_apply_country'] = ApplyCountry.objects.all()
        context['query_apply_school'] = ApplySchool.objects.all()
        context['query_apply_college'] = ApplyCollege.objects.all()
        context['query_apply_major'] = ApplyMajor.objects.all()
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', 'usnews_rank')
        c = self.get_apply_degree()
        query = Q(apply_country__chinese_name__icontains = search_text)
        query.add(Q(apply_school__chinese_name__icontains = search_text), Q.OR)
        new_context = c.filter(query).order_by(order_by)
        return new_context

class ApplyManagementDegreeCreationView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "增加"
    page_tab = "学位"
    template_name = "dashboard/apply_management_form.html"
    form_class = ApplyManagementDegreeCreationForm
    success_url = reverse_lazy('dashboard:ApplyManagementDegreeListView')
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementDegreeCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementDegreeCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementDegreeCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementDegreeUpdateView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "编辑"
    page_tab = "学位"
    form_class = ApplyManagementDegreeCreationForm
    template_name = "dashboard/apply_management_form.html"
    success_url = reverse_lazy('dashboard:ApplyManagementDegreeListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplyDegree.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(ApplyManagementDegreeUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementDegreeUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementDegreeUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementDegreeUpdateView, self).get_form_kwargs()
        r = ApplyDegree.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementDegreeDetailView(LoginRequiredMixin, DetailView):
    page_title = "院校申请信息管理"
    page_subtitle = "详细信息"
    page_tab = "学位"
    success_url = reverse_lazy('dashboard:ApplyManagementDegreeListView')
    model = ApplyDegree
    template_name = "dashboard/apply_management_degree_detail.html"
    def dispatch(self, *args, **kwargs):
        ad = ApplyDegree.objects.all()
        try:
            a =ad.get(id=self.kwargs['pk'])
        except ApplyDegree.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ApplyDegree.model._meta.verbose_name})
        return super(ApplyManagementDegreeDetailView, self).dispatch(*args, **kwargs)
    def get_apply_degree_json(self):
        country = ApplyCountry.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ApplyManagementDegreeDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        context['apply_degree_json'] = self.get_apply_degree_json()
        return context

class ApplyManagementDegreeDeleteView(LoginRequiredMixin, DeleteView):
    page_title = "院校申请信息管理"
    page_subtitle = "删除"
    page_tab = "学位"
    success_url = reverse_lazy('dashboard:ApplyManagementDegreeListView')
    model = ApplyDegree
    template_name = "dashboard/apply_management_panel.html"
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementDegreeDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class ApplyManagementCountryListView(LoginRequiredMixin, ListView):
    page_title = "院校申请信息管理"
    page_subtitle = "列表"
    page_tab = "国家"
    template_name = "dashboard/apply_management_country_list.html"
    page_add = reverse_lazy('dashboard:ApplyManagementCountryCreationView')
    success_url = reverse_lazy('dashboard:ApplyManagementCountryListView')
    model = ApplyCountry
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementCountryListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_add'] = self.page_add
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', 'name')
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', 'name')
        c = ApplyCountry.objects.all()
        query = Q(name__icontains = search_text)
        query.add(Q(chinese_name__icontains = search_text), Q.OR)
        new_context = c.filter(query).order_by(order_by)
        return new_context

class ApplyManagementCountryCreationView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "增加"
    page_tab = "国家"
    template_name = "dashboard/apply_management_form.html"
    form_class = ApplyManagementCountryCreationForm
    success_url = reverse_lazy('dashboard:ApplyManagementCountryListView')
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementCountryCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementCountryCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementCountryCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementCountryUpdateView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "编辑"
    page_tab = "国家"
    form_class = ApplyManagementCountryCreationForm
    template_name = "dashboard/apply_management_form.html"
    success_url = reverse_lazy('dashboard:ApplyManagementCountryListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplyCountry.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(ApplyManagementCountryUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementCountryUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementCountryUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementCountryUpdateView, self).get_form_kwargs()
        r = ApplyCountry.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementCountryDeleteView(LoginRequiredMixin, DeleteView):
    page_title = "院校申请信息管理"
    page_subtitle = "删除"
    page_tab = "国家"
    success_url = reverse_lazy('dashboard:ApplyManagementCountryListView')
    model = ApplyCountry
    template_name = "dashboard/apply_management_panel.html"
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementCountryDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class ApplyManagementSchoolListView(LoginRequiredMixin, ListView):
    page_title = "院校申请信息管理"
    page_subtitle = "列表"
    page_tab = "学校"
    template_name = "dashboard/apply_management_school_list.html"
    page_add = reverse_lazy('dashboard:ApplyManagementSchoolCreationView')
    success_url = reverse_lazy('dashboard:ApplyManagementSchoolListView')
    model = ApplySchool
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementSchoolListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_add'] = self.page_add
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', 'name')
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', 'name')
        c = ApplySchool.objects.all()
        query = Q(name__icontains = search_text)
        query.add(Q(chinese_name__icontains = search_text), Q.OR)
        new_context = c.filter(query).order_by(order_by)
        return new_context

class ApplyManagementSchoolCreationView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "增加"
    page_tab = "学校"
    template_name = "dashboard/apply_management_form.html"
    form_class = ApplyManagementSchoolCreationForm
    success_url = reverse_lazy('dashboard:ApplyManagementSchoolListView')
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementSchoolCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementSchoolCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementSchoolCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementSchoolUpdateView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "编辑"
    page_tab = "学校"
    form_class = ApplyManagementSchoolCreationForm
    template_name = "dashboard/apply_management_form.html"
    success_url = reverse_lazy('dashboard:ApplyManagementSchoolListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplySchool.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(ApplyManagementSchoolUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementSchoolUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementSchoolUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementSchoolUpdateView, self).get_form_kwargs()
        r = ApplySchool.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementSchoolDeleteView(LoginRequiredMixin, DeleteView):
    page_title = "院校申请信息管理"
    page_subtitle = "删除"
    page_tab = "学校"
    success_url = reverse_lazy('dashboard:ApplyManagementSchoolListView')
    model = ApplySchool
    template_name = "dashboard/apply_management_panel.html"
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementSchoolDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class ApplyManagementCollegeListView(LoginRequiredMixin, ListView):
    page_title = "院校申请信息管理"
    page_subtitle = "列表"
    page_tab = "学院"
    template_name = "dashboard/apply_management_college_list.html"
    page_add = reverse_lazy('dashboard:ApplyManagementCollegeCreationView')
    success_url = reverse_lazy('dashboard:ApplyManagementCollegeListView')
    model = ApplyCollege
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementCollegeListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_add'] = self.page_add
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', 'name')
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', 'name')
        c = ApplyCollege.objects.all()
        query = Q(name__icontains = search_text)
        query.add(Q(chinese_name__icontains = search_text), Q.OR)
        new_context = c.filter(query).order_by(order_by)
        return new_context

class ApplyManagementCollegeCreationView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "增加"
    page_tab = "学院"
    template_name = "dashboard/apply_management_form.html"
    form_class = ApplyManagementCollegeCreationForm
    success_url = reverse_lazy('dashboard:ApplyManagementCollegeListView')
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementCollegeCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementCollegeCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementCollegeCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementCollegeUpdateView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "编辑"
    page_tab = "学院"
    form_class = ApplyManagementCollegeCreationForm
    template_name = "dashboard/apply_management_form.html"
    success_url = reverse_lazy('dashboard:ApplyManagementCollegeListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplyCollege.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(ApplyManagementCollegeUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementCollegeUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementCollegeUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementCollegeUpdateView, self).get_form_kwargs()
        r = ApplyCollege.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementCollegeDeleteView(LoginRequiredMixin, DeleteView):
    page_title = "院校申请信息管理"
    page_subtitle = "删除"
    page_tab = "学院"
    success_url = reverse_lazy('dashboard:ApplyManagementCollegeListView')
    model = ApplyCollege
    template_name = "dashboard/apply_management_panel.html"
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementCollegeDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class ApplyManagementMajorListView(LoginRequiredMixin, ListView):
    page_title = "院校申请信息管理"
    page_subtitle = "列表"
    page_tab = "专业"
    template_name = "dashboard/apply_management_major_list.html"
    page_add = reverse_lazy('dashboard:ApplyManagementMajorCreationView')
    success_url = reverse_lazy('dashboard:ApplyManagementMajorListView')
    model = ApplyMajor
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementMajorListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_add'] = self.page_add
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', 'name')
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', 'name')
        c = ApplyMajor.objects.all()
        query = Q(name__icontains = search_text)
        query.add(Q(chinese_name__icontains = search_text), Q.OR)
        new_context = c.filter(query).order_by(order_by)
        return new_context

class ApplyManagementMajorCreationView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "增加"
    page_tab = "专业"
    template_name = "dashboard/apply_management_form.html"
    form_class = ApplyManagementMajorCreationForm
    success_url = reverse_lazy('dashboard:ApplyManagementMajorListView')
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementMajorCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementMajorCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementMajorCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementMajorUpdateView(LoginRequiredMixin, FormView):
    page_title = "院校申请信息管理"
    page_subtitle = "编辑"
    page_tab = "专业"
    form_class = ApplyManagementMajorCreationForm
    template_name = "dashboard/apply_management_form.html"
    success_url = reverse_lazy('dashboard:ApplyManagementMajorListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplyMajor.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(ApplyManagementMajorUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementMajorUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(ApplyManagementMajorUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ApplyManagementMajorUpdateView, self).get_form_kwargs()
        r = ApplyMajor.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class ApplyManagementMajorDeleteView(LoginRequiredMixin, DeleteView):
    page_title = "院校申请信息管理"
    page_subtitle = "删除"
    page_tab = "专业"
    success_url = reverse_lazy('dashboard:ApplyManagementMajorListView')
    model = ApplyMajor
    template_name = "dashboard/apply_management_panel.html"
    def get_context_data(self, **kwargs):
        context = super(ApplyManagementMajorDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class MentoringRelationshipListView(LoginRequiredMixin, ListView):
    page_title = "导生关系"
    page_subtitle = "列表"
    template_name = "dashboard/mentoring_relationship_list.html"
    page_add = reverse_lazy('dashboard:MentoringRelationshipCreationView')
    success_url = reverse_lazy('dashboard:MentoringRelationshipListView')
    model = MentoringRelationship
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(MentoringRelationshipListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_add'] = self.page_add
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', 'teacher')
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', 'teacher__username')
        m = MentoringRelationship.objects.all()
        if self.request.user.groups.first().name == "导师":
            m = MentoringRelationship.objects.filter(teacher__id = self.request.user.id)
        if self.request.user.groups.first().name == "学生":
            m = MentoringRelationship.objects.filter(student__id = self.request.user.id)
        query = Q(teacher__userprofile__chinese_name__icontains = search_text)
        query.add(Q(student__userprofile__chinese_name__icontains = search_text), Q.OR)
        query.add(Q(administrator_comment__icontains = search_text), Q.OR)
        query.add(Q(teacher_comment__icontains = search_text), Q.OR)
        new_context = m.filter(query).order_by(order_by)
        return new_context

class MentoringRelationshipCreationView(LoginRequiredMixin, FormView):
    page_title = "导生关系"
    page_subtitle = "增加"
    template_name = "dashboard/form.html"
    form_class = MentoringRelationshipCreationForm
    success_url = reverse_lazy('dashboard:MentoringRelationshipListView')
    def get_context_data(self, **kwargs):
        context = super(MentoringRelationshipCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(MentoringRelationshipCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(MentoringRelationshipCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class MentoringRelationshipUpdateView(LoginRequiredMixin, FormView):
    page_title = "导生关系"
    page_subtitle = "编辑"
    form_class = MentoringRelationshipCreationForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy('dashboard:MentoringRelationshipListView')
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.first().name == "学生":
            rs = MentoringRelationship.objects.filter(student = self.request.user)
        elif self.request.user.groups.first().name == "导师":
            rs = MentoringRelationship.objects.filter(teacher = self.request.user)
        elif self.request.user.groups.first().name == "管理员":
            rs = MentoringRelationship.objects.all()
        try:
            r = rs.get(id = self.kwargs['pk'])
        except rs.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': rs.model._meta.verbose_name})
        return super(MentoringRelationshipUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(MentoringRelationshipUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(MentoringRelationshipUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(MentoringRelationshipUpdateView, self).get_form_kwargs()
        r = MentoringRelationship.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class MentoringRelationshipDeleteView(LoginRequiredMixin, DeleteView):
    page_title = "导生关系"
    page_subtitle = "删除"
    success_url = reverse_lazy('dashboard:MentoringRelationshipListView')
    model = MentoringRelationship
    template_name = "dashboard/panel.html"
    def get_context_data(self, **kwargs):
        context = super(MentoringRelationshipDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context

class MentoringRecordListView(LoginRequiredMixin, ListView):
    page_title = "辅导纪录"
    page_subtitle = "列表"
    template_name = "dashboard/mentoring_record_list.html"
    page_add = reverse_lazy('dashboard:MentoringRecordCreationView')
    success_url = reverse_lazy('dashboard:MentoringRecordListView')
    model = MentoringRecord
    paginate_by = 10
    def get_mentoring_record(self):
        teacher_id = self.request.GET.get('teacher_id', 'all')
        if teacher_id != 'all':
            try:
                int(teacher_id)
            except ValueError:
                raise Http404("教师id格式错误")
        student_id = self.request.GET.get('student_id', 'all')
        if student_id != 'all':
            try:
                int(student_id)
            except ValueError:
                raise Http404("学生id格式错误")

        teachers = User.objects.filter(groups__name="导师")
        students = User.objects.filter(groups__name="学生")
        if self.request.user.groups.first().name == "导师":
            m = MentoringRecord.objects.filter(teacher = self.request.user)
            if student_id != 'all':
                mr = MentoringRelationship.objects.filter(teacher__id = self.request.user.id)
                try:
                    student = students.get(MentoringRelationship_student__in = mr, id = student_id)
                    m = m.filter(student__id = student.id)
                except students.model.DoesNotExist:
                    raise Http404(_("No %(verbose_name)s found matching the query") %
                                {'verbose_name': students.model._meta.verbose_name})
        elif self.request.user.groups.first().name == "管理员":
            m = MentoringRecord.objects.all()
            if teacher_id != 'all':
                try:
                    teacher = teachers.get(id = teacher_id)
                    m = m.filter(teacher__id = teacher.id)
                except teachers.model.DoesNotExist:
                    raise Http404(_("No %(verbose_name)s found matching the query") %
                                {'verbose_name': teachers.model._meta.verbose_name})
            if student_id != 'all':
                try:
                    student = students.get(id = student_id)
                    m = m.filter(student__id = student.id)
                except students.model.DoesNotExist:
                    raise Http404(_("No %(verbose_name)s found matching the query") %
                                {'verbose_name': students.model._meta.verbose_name})
        return m
    def get_context_data(self, **kwargs):
        context = super(MentoringRecordListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_add'] = self.page_add
        context['search_text'] = self.request.GET.get('search_text', '')
        context['teacher_id'] = self.request.GET.get('teacher_id', 'all')
        context['student_id'] = self.request.GET.get('student_id', 'all')
        context['orderby'] = self.request.GET.get('orderby', '-mentoring_date')
        teachers = User.objects.filter(groups__name="导师")
        students = User.objects.filter(groups__name="学生")
        if self.request.user.groups.first().name == "导师":
            mr = MentoringRelationship.objects.filter(teacher__id = self.request.user.id)
            teachers = teachers.filter(id = self.request.user.id)
            students = students.filter(MentoringRelationship_student__in = mr)
        context['query_teachers'] = teachers
        context['query_students'] = students
        mr = self.get_mentoring_record()
        time_sum = datetime.timedelta(0, 0, 0)
        for m in mr:
            t = m.mentoring_time
            dt = datetime.timedelta(0, t.second, 0, 0, t.minute, t.hour)
            time_sum += dt
        s = time_sum.seconds
        hour = s // 3600
        s -= hour * 3600
        minute = s // 60
        context['query_mentoring_time'] = "%02d:%02d" % (hour, minute)
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', '-mentoring_date')
        query = Q(teacher__userprofile__chinese_name__icontains = search_text)
        query.add(Q(student__userprofile__chinese_name__icontains = search_text), Q.OR)
        query.add(Q(content__icontains = search_text), Q.OR)
        m = self.get_mentoring_record()
        new_context = m.filter(query).order_by(order_by)
        return new_context

class MentoringRecordCreationView(LoginRequiredMixin, FormView):
    page_title = "辅导纪录"
    page_subtitle = "增加"
    template_name = "dashboard/form.html"
    form_class = MentoringRecordCreationForm
    success_url = reverse_lazy('dashboard:MentoringRecordListView')
    def get_context_data(self, **kwargs):
        context = super(MentoringRecordCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(MentoringRecordCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(MentoringRecordCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class MentoringRecordUpdateView(LoginRequiredMixin, FormView):
    page_title = "辅导纪录"
    page_subtitle = "编辑"
    form_class = MentoringRecordCreationForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy('dashboard:MentoringRecordListView')
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.first().name == "导师":
            mr = MentoringRecord.objects.filter(teacher = self.request.user)
        elif self.request.user.groups.first().name == "管理员":
            mr = MentoringRecord.objects.all()
        try:
            m = mr.get(id=self.kwargs['pk'])
        except mr.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': mr.model._meta.verbose_name})
        return super(MentoringRecordUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(MentoringRecordUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(MentoringRecordUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(MentoringRecordUpdateView, self).get_form_kwargs()
        r = MentoringRecord.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class MentoringRecordDeleteView(LoginRequiredMixin, DeleteView):
    page_title = "辅导纪录"
    page_subtitle = "删除"
    success_url = reverse_lazy('dashboard:MentoringRecordListView')
    model = MentoringRecord
    template_name = "dashboard/panel.html"
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.first().name == "导师":
            mr = MentoringRecord.objects.filter(teacher = self.request.user)
        elif self.request.user.groups.first().name == "管理员":
            mr = MentoringRecord.objects.all()
        try:
            m = mr.get(id=self.kwargs['pk'])
        except mr.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': mr.model._meta.verbose_name})
        return super(MentoringRecordDeleteView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(MentoringRecordDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context

class MissionListView(LoginRequiredMixin, ListView):
    page_title = "任务"
    page_subtitle = "列表"
    template_name = "dashboard/mission_list.html"
    page_add = reverse_lazy('dashboard:MissionCreationView')
    success_url = reverse_lazy('dashboard:MissionListView')
    model = Mission
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(MissionListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_add'] = self.page_add
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', '-end_date')
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', '-end_date')
        if self.request.user.groups.first().name == "学生":
            m = Mission.objects.filter(student = self.request.user)
        elif self.request.user.groups.first().name == "导师":
            m = Mission.objects.filter(teacher = self.request.user)
        elif self.request.user.groups.first().name == "管理员":
            m = Mission.objects.all()
        query = Q(teacher__userprofile__chinese_name__icontains = search_text)
        query.add(Q(student__userprofile__chinese_name__icontains = search_text), Q.OR)
        query.add(Q(title__icontains = search_text), Q.OR)
        query.add(Q(content__icontains = search_text), Q.OR)
        new_context = m.filter(query).order_by(order_by)
        return new_context

class MissionCreationView(LoginRequiredMixin, FormView):
    page_title = "任务"
    page_subtitle = "增加"
    template_name = "dashboard/form.html"
    form_class = MissionCreationForm
    success_url = reverse_lazy('dashboard:MissionListView')
    def get_context_data(self, **kwargs):
        context = super(MissionCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(MissionCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(MissionCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class MissionUpdateView(LoginRequiredMixin, FormView):
    page_title = "任务"
    page_subtitle = "编辑"
    form_class = MissionCreationForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy('dashboard:MissionListView')
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.first().name == "导师":
            missions = Mission.objects.filter(teacher = self.request.user)
        elif self.request.user.groups.first().name == "管理员":
            missions = Mission.objects.all()
        try:
            mission = missions.get(id=self.kwargs['pk'])
        except missions.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': missions.model._meta.verbose_name})
        return super(MissionUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(MissionUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(MissionUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(MissionUpdateView, self).get_form_kwargs()
        r = Mission.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class MissionDetailView(LoginRequiredMixin, DetailView):
    page_title = "任务"
    page_subtitle = "详细信息"
    success_url = reverse_lazy('dashboard:MissionListView')
    model = Mission
    template_name = "dashboard/mission_detail.html"
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.first().name == "学生":
            missions = Mission.objects.filter(student = self.request.user)
        elif self.request.user.groups.first().name == "导师":
            missions = Mission.objects.filter(teacher = self.request.user)
        elif self.request.user.groups.first().name == "管理员":
            missions = Mission.objects.all()
        try:
            mission = missions.get(id=self.kwargs['pk'])
        except missions.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': missions.model._meta.verbose_name})
        return super(MissionDetailView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(MissionDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context

class MissionDeleteView(LoginRequiredMixin, DeleteView):
    page_title = "任务"
    page_subtitle = "删除"
    success_url = reverse_lazy('dashboard:MissionListView')
    model = Mission
    template_name = "dashboard/panel.html"
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.first().name == "导师":
            missions = Mission.objects.filter(teacher = self.request.user)
        elif self.request.user.groups.first().name == "管理员":
            missions = Mission.objects.all()
        try:
            mission = missions.get(id=self.kwargs['pk'])
        except missions.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': missions.model._meta.verbose_name})
        return super(MissionDeleteView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(MissionDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
