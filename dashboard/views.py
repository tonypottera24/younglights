from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import MentoringRelationship, MentoringRecord, Mission
from .user_forms import AdministratorCreationForm, AdministratorChangeForm
from .user_forms import TeacherCreationForm, TeacherChangeForm
from .user_forms import StudentCreationForm, StudentChangeForm
from .forms import MentoringRelationshipCreationForm
from .forms import MentoringRecordCreationForm
from .forms import MissionCreationForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils.translation import gettext as _

# Create your views here.

@login_required
def overview(request):
    context = {}
    return render(request, 'dashboard/overview.html', context)

class MentoringRelationshipListView(LoginRequiredMixin, ListView):
    page_title = "导生关系"
    page_subtitle = "列表"
    template_name = "dashboard/mentoring_relationship_list.html"
    page_add = reverse_lazy('dashboard:MentoringRelationshipCreationView')
    success_url = reverse_lazy('dashboard:MentoringRelationshipListView')
    model = MentoringRelationship
    paginate_by = 10
    editable = True
    def get_context_data(self, **kwargs):
        context = super(MentoringRelationshipListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_add'] = self.page_add
        context['editable'] = self.editable
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', 'teacher')
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', 'teacher__username')
        query = Q(teacher__userprofile__chinese_name__icontains = search_text)
        query.add(Q(student__userprofile__chinese_name__icontains = search_text), Q.OR)
        query.add(Q(comment__icontains = search_text), Q.OR)
        new_context = MentoringRelationship.objects.filter(query).order_by(order_by)
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

class MentoringRelationshipUpdateView(LoginRequiredMixin, FormView):
    page_title = "导生关系"
    page_subtitle = "编辑"
    form_class = MentoringRelationshipCreationForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy('dashboard:MentoringRelationshipListView')
    def dispatch(self, *args, **kwargs):
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
        return kwargs

class MentoringRelationshipDeleteView(LoginRequiredMixin, DeleteView):
    page_title = "导生关系"
    page_subtitle = "删除"
    page_h1 = "请问亲是否确定要删除"
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
    editable = True
    def get_context_data(self, **kwargs):
        context = super(MentoringRecordListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_add'] = self.page_add
        context['editable'] = self.editable
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', '-mentoring_date')
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', '-mentoring_date')
        if self.request.user.groups.first().name == "导师":
            m = MentoringRecord.objects.filter(teacher = self.request.user)
        elif self.request.user.groups.first().name == "管理员":
            m = MentoringRecord.objects.all()
        query = Q(teacher__userprofile__chinese_name__icontains = search_text)
        query.add(Q(student__userprofile__chinese_name__icontains = search_text), Q.OR)
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
    page_h1 = "请问亲是否确定要删除"
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
    editable = True
    def get_context_data(self, **kwargs):
        context = super(MissionListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_add'] = self.page_add
        context['editable'] = self.editable
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
    page_h1 = "请问亲是否确定要删除"
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
