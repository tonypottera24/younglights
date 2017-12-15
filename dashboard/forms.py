from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .myforms import MyBasicField
from .models import MentoringRelationship, MentoringRecord, Mission

class MentoringRelationshipCreationForm(ModelForm):
    class Meta:
        model = MentoringRelationship
        fields = ['teacher', 'student', 'relationship_status', 'comment']
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            self.old_instance = kwargs['instance']
        else:
            self.old_instance = None
        super(MentoringRelationshipCreationForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.filter(groups__name="导师")
        self.fields['student'].queryset = User.objects.filter(groups__name="学生")
        MyBasicField.add_field_info(self, None)
    def clean_student(self):
        teacher = self.cleaned_data.get("teacher")
        student = self.cleaned_data.get("student")
        if teacher and student:
            if self.old_instance:
                if teacher == self.old_instance.teacher and student == self.old_instance.student:
                    return student
            rs = MentoringRelationship.objects.all()
            try:
                r = rs.get(teacher = teacher, student = student)
                raise forms.ValidationError("导生关系已存在")
            except rs.model.DoesNotExist:
                pass
        return student

class MentoringRecordCreationForm(ModelForm):
    class Meta:
        model = MentoringRecord
        fields = ['teacher', 'student', 'mentoring_date', 'mentoring_time', 'content']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(MentoringRecordCreationForm, self).__init__(*args, **kwargs)
        teachers = User.objects.filter(groups__name="导师")
        students = User.objects.filter(groups__name="学生")
        if self.request.user.groups.first().name == "导师":
            rs = MentoringRelationship.objects.filter(teacher__id = self.request.user.id)
            self.fields['teacher'].queryset = teachers.filter(id = self.request.user.id)
            self.fields['student'].queryset = students.filter(MentoringRelationship_student__in = rs)
        elif self.request.user.groups.first().name == "管理员":
            self.fields['teacher'].queryset = teachers.filter(groups__name="导师")
            self.fields['student'].queryset = students.filter(groups__name="学生")
        MyBasicField.add_field_info(self, None)
    def clean_student(self):
        teacher = self.cleaned_data.get("teacher")
        student = self.cleaned_data.get("student")
        if teacher and student:
            rs = MentoringRelationship.objects.all()
            try:
                r = rs.get(teacher = teacher, student = student)
            except rs.model.DoesNotExist:
                raise forms.ValidationError("导师与学生无导生关系")
        return student

class MissionCreationForm(ModelForm):
    class Meta:
        model = Mission
        fields = ['teacher', 'student', 'end_date', 'title', 'content']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(MissionCreationForm, self).__init__(*args, **kwargs)
        teachers = User.objects.filter(groups__name="导师")
        students = User.objects.filter(groups__name="学生")
        if self.request.user.groups.first().name == "导师":
            rs = MentoringRelationship.objects.filter(teacher__id = self.request.user.id)
            self.fields['teacher'].queryset = teachers.filter(id = self.request.user.id)
            self.fields['student'].queryset = students.filter(MentoringRelationship_student__in = rs)
        elif self.request.user.groups.first().name == "管理员":
            self.fields['teacher'].queryset = teachers.filter(groups__name="导师")
            self.fields['student'].queryset = students.filter(groups__name="学生")
        MyBasicField.add_field_info(self, None)
    def clean_student(self):
        teacher = self.cleaned_data.get("teacher")
        student = self.cleaned_data.get("student")
        if teacher and student:
            rs = MentoringRelationship.objects.all()
            try:
                r = rs.get(teacher = teacher, student = student)
            except rs.model.DoesNotExist:
                raise forms.ValidationError("导师与学生无导生关系")
        return student
