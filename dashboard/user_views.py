from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import UserProfile
from .models import MentoringRelationship
from .user_forms import AdministratorCreationForm, AdministratorChangeForm
from .user_forms import TeacherCreationForm, TeacherChangeForm
from .user_forms import StudentCreationForm, StudentChangeForm
from django.db.models import Q
from django.utils.translation import gettext as _
from django.http import Http404

class MyUserListView(ListView):
    groups_name = ""
    page_subtitle = "列表"
    model = User
    paginate_by = 10
    editable = False
    def get_context_data(self, **kwargs):
        context = super(MyUserListView, self).get_context_data(**kwargs)
        context['page_title'] = self.groups_name
        context['page_subtitle'] = self.page_subtitle
        context['page_add'] = self.page_add
        context['page_cancel'] = self.success_url
        context['editable'] = self.editable
        context['search_text'] = self.request.GET.get('search_text', '')
        context['orderby'] = self.request.GET.get('orderby', 'user__username')
        return context
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        order_by = self.request.GET.get('order_by', 'username')
        users = User.objects.filter(groups__name = self.groups_name)
        if self.request.user.groups.first().name == "导师":
            rs = MentoringRelationship.objects.filter(teacher__id = self.request.user.id, relationship_status = '辅导中')
            users = users.filter(MentoringRelationship_student__in = rs)
        query = Q(username__icontains = search_text)
        query.add(Q(email__icontains = search_text), Q.OR)
        query.add(Q(userprofile__chinese_name__icontains = search_text), Q.OR)
        query.add(Q(userprofile__school__icontains = search_text), Q.OR)
        query.add(Q(userprofile__college__icontains = search_text), Q.OR)
        query.add(Q(userprofile__major__icontains = search_text), Q.OR)
        query.add(Q(userprofile__phone__icontains = search_text), Q.OR)
        query.add(Q(userprofile__qq__icontains = search_text), Q.OR)
        query.add(Q(userprofile__wechat__icontains = search_text), Q.OR)
        new_users = users.filter(query).order_by(order_by)
        return new_users
class AdministratorListView(MyUserListView):
    groups_name = "管理员"
    editable = True
    template_name = "dashboard/administrator_list.html"
    page_add = reverse_lazy('dashboard:AdministratorCreationView')
    success_url = reverse_lazy('dashboard:AdministratorListView')
class TeacherListView(MyUserListView):
    groups_name = "导师"
    editable = True
    template_name = "dashboard/teacher_list.html"
    page_add = reverse_lazy('dashboard:TeacherCreationView')
    success_url = reverse_lazy('dashboard:TeacherListView')
class StudentListView(MyUserListView):
    groups_name = "学生"
    editable = True
    template_name = "dashboard/student_list.html"
    page_add = reverse_lazy('dashboard:StudentCreationView')
    success_url = reverse_lazy('dashboard:StudentListView')

class StudentDetailView(DetailView):
    page_title = "学生"
    page_subtitle = "详细信息"
    success_url = reverse_lazy('dashboard:StudentListView')
    model = User
    template_name = "dashboard/student_detail.html"
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.first().name == "导师":
            try:
                rs = MentoringRelationship.objects.get(teacher = self.request.user, student__id = self.kwargs['pk'], relationship_status='辅导中')
            except MentoringRelationship.model.DoesNotExist:
                raise Http404(_("No %(verbose_name)s found matching the query") %
                            {'verbose_name': missions.model._meta.verbose_name})
        return super(StudentDetailView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context

class MyUserCreationView(FormView):
    groups_name = ""
    page_subtitle = "增加"
    template_name = "dashboard/form.html"
    def get_context_data(self, **kwargs):
        context = super(MyUserCreationView, self).get_context_data(**kwargs)
        context['page_title'] = self.groups_name
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()  # load the profile instance created by the signal
        user.userprofile.school = form.cleaned_data.get('school')
        user.userprofile.college = form.cleaned_data.get('college')
        user.userprofile.major = form.cleaned_data.get('major')
        user.userprofile.phone = form.cleaned_data.get('phone')
        user.userprofile.qq = form.cleaned_data.get('qq')
        user.userprofile.wechat = form.cleaned_data.get('wechat')
        user.userprofile.research_field = form.cleaned_data.get('research_field')
        user.userprofile.research_experience = form.cleaned_data.get('research_experience')
        user.userprofile.thesis_experience = form.cleaned_data.get('thesis_experience')
        g = Group.objects.get(name=self.groups_name) 
        g.user_set.add(user)
        user.save()
        return super(MyUserCreationView, self).form_valid(form)
class AdministratorCreationView(MyUserCreationView):
    groups_name = "管理员"
    form_class = AdministratorCreationForm
    success_url = reverse_lazy('dashboard:AdministratorListView')
class TeacherCreationView(MyUserCreationView):
    groups_name = "导师"
    form_class = TeacherCreationForm
    success_url = reverse_lazy('dashboard:TeacherListView')
class StudentCreationView(MyUserCreationView):
    groups_name = "学生"
    form_class = StudentCreationForm
    success_url = reverse_lazy('dashboard:StudentListView')

class MyUserUpdateView(FormView):
    self_pk = None
    groups_name = ""
    page_subtitle = "编辑"
    template_name = "dashboard/form.html"
    def dispatch(self, *args, **kwargs):
        if self.self_pk is None:
            self.self_pk = self.kwargs['pk']
        users = User.objects.filter(groups__name = self.groups_name)
        try:
            user = users.get(id=self.self_pk)
        except users.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': users.model._meta.verbose_name})
        return super(MyUserUpdateView, self).dispatch(*args, **kwargs)
    def form_valid(self, form):
        form.save()
        user = User.objects.get(id=self.self_pk)
        user.userprofile.school = form.cleaned_data.get('school')
        user.userprofile.college = form.cleaned_data.get('college')
        user.userprofile.major = form.cleaned_data.get('major')
        user.userprofile.phone = form.cleaned_data.get('phone')
        user.userprofile.qq = form.cleaned_data.get('qq')
        user.userprofile.wechat = form.cleaned_data.get('wechat')
        user.userprofile.research_field = form.cleaned_data.get('research_field')
        user.userprofile.research_experience = form.cleaned_data.get('research_experience')
        user.userprofile.thesis_experience = form.cleaned_data.get('thesis_experience')
        user.save()
        return super(MyUserUpdateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(MyUserUpdateView, self).get_form_kwargs()
        user = User.objects.get(id=self.self_pk)
        kwargs['instance'] = user
        kwargs['initial'] = {
                'school': user.userprofile.school,
                'college': user.userprofile.college,
                'major': user.userprofile.major,
                'phone': user.userprofile.phone,
                'qq': user.userprofile.qq,
                'wechat': user.userprofile.wechat,
                'research_field': user.userprofile.research_field,
                'research_experience': user.userprofile.research_experience,
                'thesis_experience': user.userprofile.thesis_experience,
        }
        return kwargs
    def get_context_data(self, **kwargs):
        context = super(MyUserUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = self.groups_name
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
class AdministratorUpdateView(MyUserUpdateView):
    groups_name = "管理员"
    form_class = AdministratorChangeForm
    success_url = reverse_lazy('dashboard:AdministratorListView')
class TeacherUpdateView(MyUserUpdateView):
    groups_name = "导师"
    form_class = TeacherChangeForm
    success_url = reverse_lazy('dashboard:TeacherListView')
class StudentUpdateView(MyUserUpdateView):
    groups_name = "学生"
    form_class = StudentChangeForm
    success_url = reverse_lazy('dashboard:StudentListView')
class SelfUpdateView(MyUserUpdateView):
    success_url = reverse_lazy('dashboard:overview')
    self_pk = None
    def dispatch(self, *args, **kwargs):
        self.self_pk = self.request.user.id
        self.groups_name = self.request.user.groups.first().name
        return super(SelfUpdateView, self).dispatch(*args, **kwargs)
    def get_form_class(self):
        if self.groups_name == "管理员":
            return AdministratorChangeForm
        elif self.groups_name == "导师":
            return TeacherChangeForm
        elif self.groups_name == "学生":
            return StudentChangeForm
    def get_context_data(self, **kwargs):
        context = super(SelfUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = "修改信息"
        return context

class MyUserDeleteView(DeleteView):
    groups_name = ""
    page_subtitle = "删除"
    page_h1 = "请问亲是否确定要删除"
    model = User
    template_name = "dashboard/panel.html"
    def dispatch(self, *args, **kwargs):
        users = User.objects.filter(groups__name = self.groups_name)
        try:
            user = users.get(id=self.kwargs['pk'])
        except users.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': users.model._meta.verbose_name})
        return super(MyUserDeleteView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(MyUserDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = self.groups_name
        context['page_subtitle'] = self.page_subtitle
        context['page_cancel'] = self.success_url
        return context
class AdministratorDeleteView(MyUserDeleteView):
    groups_name = "管理员"
    success_url = reverse_lazy('dashboard:AdministratorListView')
class TeacherDeleteView(MyUserDeleteView):
    groups_name = "导师"
    success_url = reverse_lazy('dashboard:TeacherListView')
class StudentDeleteView(MyUserDeleteView):
    groups_name = "学生"
    success_url = reverse_lazy('dashboard:StudentListView')
