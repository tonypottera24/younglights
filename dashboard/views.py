from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import MentoringRelationship, MentoringRecord, Mission
from .models import ApplyCountry, ApplySchool, ApplyCollege, ApplyMajor, ApplyDegree, ApplyDegreeType, ApplySemester
from .user_forms import AdministratorCreationForm, AdministratorChangeForm
from .user_forms import TeacherCreationForm, TeacherChangeForm
from .user_forms import StudentCreationForm, StudentChangeForm
from .forms import MentoringRelationshipCreationForm, MentoringRecordCreationForm, MissionCreationForm
from .forms import SchoolApplicationCountryCreationForm, SchoolApplicationSchoolCreationForm, SchoolApplicationCollegeCreationForm, SchoolApplicationMajorCreationForm, SchoolApplicationDegreeCreationForm
from django.db.models import Q
from django.http import Http404
from django.utils.translation import gettext as _
import datetime
import json

# Create your views here.

def overview(request):
    return redirect(reverse('dashboard:MissionListView'))

class SchoolApplicationDegreeListView(ListView):
    page_title = "院校申请信息"
    page_subtitle = "列表"
    page_tab = "学位比较"
    template_name = "dashboard/school_application_degree_list.html"
    page_add = reverse_lazy('dashboard:SchoolApplicationDegreeCreationView')
    success_url = reverse_lazy('dashboard:SchoolApplicationDegreeListView')
    model = ApplyDegree
    paginate_by = 20
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
        apply_degree_type_ids = self.get_apply_ids('apply_degree_type_id')
        apply_semester_ids = self.get_apply_ids('apply_semester_id')
        apply_degree = ApplyDegree.objects.all()
        if len(apply_country_ids) > 0:
            apply_degree = apply_degree.filter(apply_country__id__in = apply_country_ids)
        if len(apply_school_ids) > 0:
            apply_degree = apply_degree.filter(apply_school__id__in = apply_school_ids)
        if len(apply_college_ids) > 0:
            apply_degree = apply_degree.filter(apply_college__id__in = apply_college_ids)
        if len(apply_major_ids) > 0:
            apply_degree = apply_degree.filter(apply_major__id__in = apply_major_ids)
        if len(apply_degree_type_ids) > 0:
            apply_degree = apply_degree.filter(apply_degree_type__id__in = apply_degree_type_ids)
        if len(apply_semester_ids) > 0:
            apply_degree = apply_degree.filter(apply_semester__id__in = apply_semester_ids)
        return apply_degree
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationDegreeListView, self).get_context_data(**kwargs)
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
        context['apply_degree_type_id'] = self.get_apply_ids('apply_degree_type_id')
        context['apply_semester_id'] = self.get_apply_ids('apply_semester_id')
        context['query_apply_country'] = ApplyCountry.objects.all()
        context['query_apply_school'] = ApplySchool.objects.all()
        context['query_apply_college'] = ApplyCollege.objects.all()
        context['query_apply_major'] = ApplyMajor.objects.all()
        context['query_apply_degree_type'] = ApplyDegreeType.objects.all()
        context['query_apply_semester'] = ApplySemester.objects.all()
        return context
    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'usnews_rank')
        new_context = self.get_apply_degree().order_by(order_by)
        return new_context

class SchoolApplicationDegreeCreationView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "增加"
    page_tab = "学位比较"
    template_name = "dashboard/school_application_form.html"
    form_class = SchoolApplicationDegreeCreationForm
    success_url = reverse_lazy('dashboard:SchoolApplicationDegreeListView')
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationDegreeCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationDegreeCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationDegreeCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationDegreeUpdateView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "编辑"
    page_tab = "学位比较"
    form_class = SchoolApplicationDegreeCreationForm
    template_name = "dashboard/school_application_form.html"
    success_url = reverse_lazy('dashboard:SchoolApplicationDegreeListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplyDegree.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(SchoolApplicationDegreeUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationDegreeUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationDegreeUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationDegreeUpdateView, self).get_form_kwargs()
        r = ApplyDegree.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationDegreeDetailView(DetailView):
    page_title = "院校申请信息"
    page_subtitle = "详细信息"
    page_tab = "学位探索"
    success_url = reverse_lazy('dashboard:SchoolApplicationDegreeListView')
    model = ApplyDegree
    template_name = "dashboard/school_application_degree_detail.html"
    def dispatch(self, *args, **kwargs):
        if int(self.kwargs['pk']) == 0:
            return redirect(reverse_lazy('dashboard:SchoolApplicationDegreeDetailView', kwargs={'pk': ApplyDegree.objects.first().pk}))
        ad = ApplyDegree.objects.all()
        try:
            a =ad.get(id=self.kwargs['pk'])
        except ad.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ad.model._meta.verbose_name})
        return super(SchoolApplicationDegreeDetailView, self).dispatch(*args, **kwargs)
    def get_apply_degree_json(self):
        current_apply_degree = ApplyDegree.objects.get(id = self.kwargs['pk'])
        data = []
        apply_countries = ApplyCountry.objects.all()
        apply_schools = ApplySchool.objects.all()
        apply_colleges = ApplyCollege.objects.all()
        apply_majors = ApplyMajor.objects.all()
        for apply_country in apply_countries:
            if len(ApplyDegree.objects.filter(apply_country = apply_country)) > 0:
                d_country = {}
                d_country['title'] = apply_country.chinese_name
                d_country['type'] = 'folder'
                if apply_country == current_apply_degree.apply_country:
                    d_country['attr'] = {'id': 'apply_country_' + str(current_apply_degree.id)}
                d_country['child'] = []
                for apply_school in apply_schools:
                    if len(ApplyDegree.objects.filter(apply_country = apply_country, apply_school = apply_school)) > 0:
                        d_school = {}
                        d_school['title'] = apply_school.chinese_name
                        d_school['type'] = 'folder'
                        if apply_school == current_apply_degree.apply_school:
                            d_school['attr'] = {'id': 'apply_school_' + str(current_apply_degree.id)}
                        d_school['child'] = []
                        for apply_college in apply_colleges:
                            if len(ApplyDegree.objects.filter(apply_country = apply_country, apply_school = apply_school, apply_college = apply_college)) > 0:
                                d_college = {}
                                d_college['title'] = apply_college.chinese_name
                                d_college['type'] = 'folder'
                                if apply_college == current_apply_degree.apply_college:
                                    d_college['attr'] = {'id': 'apply_college_' + str(current_apply_degree.id)}
                                d_college['child'] = []
                                for apply_major in apply_majors:
                                    apply_degrees = ApplyDegree.objects.filter(apply_country = apply_country, apply_school = apply_school, apply_college = apply_college, apply_major = apply_major)
                                    if len(apply_degrees) > 0:
                                        d_major = {}
                                        d_major['title'] = apply_major.chinese_name
                                        d_major['type'] = 'folder'
                                        if apply_major == current_apply_degree.apply_major:
                                            d_major['attr'] = {'id': 'apply_major_' + str(current_apply_degree.id)}
                                        d_major['child'] = []
                                        for apply_degree in apply_degrees:
                                            d_degree = {}
                                            d_degree['title'] = " ".join(a.chinese_name for a in apply_degree.apply_degree_type.all())
                                            d_degree['type'] = 'item'
                                            d_degree['attr'] = {'id': 'apply_degree_' + str(apply_degree.id)}
                                            d_major['child'].append(d_degree)
                                        d_college['child'].append(d_major)
                                d_school['child'].append(d_college)
                        d_country['child'].append(d_school)
                data.append(d_country)
        return str(json.dumps(data))
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationDegreeDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        context['apply_degree_json'] = self.get_apply_degree_json()
        return context

class SchoolApplicationDegreeDeleteView(DeleteView):
    page_title = "院校申请信息"
    page_subtitle = "删除"
    page_tab = "学位比较"
    success_url = reverse_lazy('dashboard:SchoolApplicationDegreeListView')
    model = ApplyDegree
    template_name = "dashboard/school_application_panel.html"
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationDegreeDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class SchoolApplicationCountryListView(ListView):
    page_title = "院校申请信息"
    page_subtitle = "列表"
    page_tab = "国家"
    template_name = "dashboard/school_application_country_list.html"
    page_add = reverse_lazy('dashboard:SchoolApplicationCountryCreationView')
    success_url = reverse_lazy('dashboard:SchoolApplicationCountryListView')
    model = ApplyCountry
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationCountryListView, self).get_context_data(**kwargs)
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

class SchoolApplicationCountryCreationView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "增加"
    page_tab = "国家"
    template_name = "dashboard/school_application_form.html"
    form_class = SchoolApplicationCountryCreationForm
    success_url = reverse_lazy('dashboard:SchoolApplicationCountryListView')
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationCountryCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationCountryCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationCountryCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationCountryUpdateView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "编辑"
    page_tab = "国家"
    form_class = SchoolApplicationCountryCreationForm
    template_name = "dashboard/school_application_form.html"
    success_url = reverse_lazy('dashboard:SchoolApplicationCountryListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplyCountry.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(SchoolApplicationCountryUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationCountryUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationCountryUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationCountryUpdateView, self).get_form_kwargs()
        r = ApplyCountry.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationCountryDeleteView(DeleteView):
    page_title = "院校申请信息"
    page_subtitle = "删除"
    page_tab = "国家"
    success_url = reverse_lazy('dashboard:SchoolApplicationCountryListView')
    model = ApplyCountry
    template_name = "dashboard/school_application_panel.html"
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationCountryDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class SchoolApplicationSchoolListView(ListView):
    page_title = "院校申请信息"
    page_subtitle = "列表"
    page_tab = "学校"
    template_name = "dashboard/school_application_school_list.html"
    page_add = reverse_lazy('dashboard:SchoolApplicationSchoolCreationView')
    success_url = reverse_lazy('dashboard:SchoolApplicationSchoolListView')
    model = ApplySchool
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationSchoolListView, self).get_context_data(**kwargs)
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

class SchoolApplicationSchoolCreationView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "增加"
    page_tab = "学校"
    template_name = "dashboard/school_application_form.html"
    form_class = SchoolApplicationSchoolCreationForm
    success_url = reverse_lazy('dashboard:SchoolApplicationSchoolListView')
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationSchoolCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationSchoolCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationSchoolCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationSchoolUpdateView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "编辑"
    page_tab = "学校"
    form_class = SchoolApplicationSchoolCreationForm
    template_name = "dashboard/school_application_form.html"
    success_url = reverse_lazy('dashboard:SchoolApplicationSchoolListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplySchool.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(SchoolApplicationSchoolUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationSchoolUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationSchoolUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationSchoolUpdateView, self).get_form_kwargs()
        r = ApplySchool.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationSchoolDeleteView(DeleteView):
    page_title = "院校申请信息"
    page_subtitle = "删除"
    page_tab = "学校"
    success_url = reverse_lazy('dashboard:SchoolApplicationSchoolListView')
    model = ApplySchool
    template_name = "dashboard/school_application_panel.html"
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationSchoolDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class SchoolApplicationCollegeListView(ListView):
    page_title = "院校申请信息"
    page_subtitle = "列表"
    page_tab = "学院"
    template_name = "dashboard/school_application_college_list.html"
    page_add = reverse_lazy('dashboard:SchoolApplicationCollegeCreationView')
    success_url = reverse_lazy('dashboard:SchoolApplicationCollegeListView')
    model = ApplyCollege
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationCollegeListView, self).get_context_data(**kwargs)
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

class SchoolApplicationCollegeCreationView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "增加"
    page_tab = "学院"
    template_name = "dashboard/school_application_form.html"
    form_class = SchoolApplicationCollegeCreationForm
    success_url = reverse_lazy('dashboard:SchoolApplicationCollegeListView')
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationCollegeCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationCollegeCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationCollegeCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationCollegeUpdateView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "编辑"
    page_tab = "学院"
    form_class = SchoolApplicationCollegeCreationForm
    template_name = "dashboard/school_application_form.html"
    success_url = reverse_lazy('dashboard:SchoolApplicationCollegeListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplyCollege.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(SchoolApplicationCollegeUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationCollegeUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationCollegeUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationCollegeUpdateView, self).get_form_kwargs()
        r = ApplyCollege.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationCollegeDeleteView(DeleteView):
    page_title = "院校申请信息"
    page_subtitle = "删除"
    page_tab = "学院"
    success_url = reverse_lazy('dashboard:SchoolApplicationCollegeListView')
    model = ApplyCollege
    template_name = "dashboard/school_application_panel.html"
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationCollegeDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class SchoolApplicationMajorListView(ListView):
    page_title = "院校申请信息"
    page_subtitle = "列表"
    page_tab = "专业"
    template_name = "dashboard/school_application_major_list.html"
    page_add = reverse_lazy('dashboard:SchoolApplicationMajorCreationView')
    success_url = reverse_lazy('dashboard:SchoolApplicationMajorListView')
    model = ApplyMajor
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationMajorListView, self).get_context_data(**kwargs)
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

class SchoolApplicationMajorCreationView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "增加"
    page_tab = "专业"
    template_name = "dashboard/school_application_form.html"
    form_class = SchoolApplicationMajorCreationForm
    success_url = reverse_lazy('dashboard:SchoolApplicationMajorListView')
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationMajorCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationMajorCreationView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationMajorCreationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationMajorUpdateView(FormView):
    page_title = "院校申请信息"
    page_subtitle = "编辑"
    page_tab = "专业"
    form_class = SchoolApplicationMajorCreationForm
    template_name = "dashboard/school_application_form.html"
    success_url = reverse_lazy('dashboard:SchoolApplicationMajorListView')
    def dispatch(self, *args, **kwargs):
        ac = ApplyMajor.objects.all()
        try:
            a = ac.get(id = self.kwargs['pk'])
        except ac.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': ac.model._meta.verbose_name})
        return super(SchoolApplicationMajorUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationMajorUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        form.save()
        return super(SchoolApplicationMajorUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(SchoolApplicationMajorUpdateView, self).get_form_kwargs()
        r = ApplyMajor.objects.get(id = self.kwargs['pk'])
        kwargs['instance'] = r
        kwargs['request'] = self.request
        return kwargs

class SchoolApplicationMajorDeleteView(DeleteView):
    page_title = "院校申请信息"
    page_subtitle = "删除"
    page_tab = "专业"
    success_url = reverse_lazy('dashboard:SchoolApplicationMajorListView')
    model = ApplyMajor
    template_name = "dashboard/school_application_panel.html"
    def get_context_data(self, **kwargs):
        context = super(SchoolApplicationMajorDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_tab'] = self.page_tab
        context['page_cancel'] = self.success_url
        return context

class MentoringRelationshipListView(ListView):
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

class MentoringRelationshipCreationView(FormView):
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

class MentoringRelationshipUpdateView(FormView):
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

class MentoringRelationshipDeleteView(DeleteView):
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

class MentoringRecordListView(ListView):
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

class MentoringRecordCreationView(FormView):
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

class MentoringRecordUpdateView(FormView):
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

class MentoringRecordDeleteView(DeleteView):
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

class MissionListView(ListView):
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

class MissionCreationView(FormView):
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

class MissionUpdateView(FormView):
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

class MissionDetailView(DetailView):
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

class MissionDeleteView(DeleteView):
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
