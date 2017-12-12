from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .myforms import MyBasicField
from .models import MentoringRelationship, MentoringRecord, Mission

class MentoringRelationshipCreationForm(ModelForm):
    class Meta:
        model = MentoringRelationship
        fields = ['teacher', 'student', 'comment']
    def __init__(self, *args, **kwargs):
        super(MentoringRelationshipCreationForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.filter(groups__name="导师")
        self.fields['student'].queryset = User.objects.filter(groups__name="学生")
        MyBasicField.add_field_info(self, None)
    """
    def clean_end_date(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("结束日期不得早于开始日期")
        return end_date
    """

class MentoringRecordCreationForm(ModelForm):
    class Meta:
        model = MentoringRecord
        fields = ['teacher', 'student', 'mentoring_date', 'mentoring_time', 'teacher_record', 'student_record']
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
