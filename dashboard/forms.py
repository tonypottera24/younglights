from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .myforms import MyBasicField
from .models import ChannelRelationship, MentoringRelationship, MentoringRecord, Mission
from .models import ApplyCountry, ApplySchool, ApplyCollege, ApplyMajor, ApplyDegree

class SchoolApplicationDegreeCreationForm(ModelForm):
    class Meta:
        model = ApplyDegree
        fields = ['apply_country', 'apply_school', 'apply_college', 'apply_major', 'apply_degree_type', 'apply_semester', 'deadline', 'tuition', 'usnews_rank',
                'gpa_required', 'gpa', 'toefl_required', 'toefl', 'gre_required', 'gre', 'gre_subject', 'ielts_required', 'ielts', 'gmat_required', 'gmat', 
                'apply_comment', 'apply_curriculum', 'apply_link']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        if 'instance' in kwargs:
            self.old_instance = kwargs['instance']
        else:
            self.old_instance = None
        super(SchoolApplicationDegreeCreationForm, self).__init__(*args, **kwargs)
        MyBasicField.add_field_info(self, None)
        self.fields['apply_country'].queryset = self.fields['apply_country'].queryset.order_by('-updated_datetime')
        self.fields['apply_school'].queryset = self.fields['apply_school'].queryset.order_by('-updated_datetime')
        self.fields['apply_college'].queryset = self.fields['apply_college'].queryset.order_by('-updated_datetime')
        self.fields['apply_major'].queryset = self.fields['apply_major'].queryset.order_by('-updated_datetime')

    def clean_apply_degree_type(self):
        apply_country = self.cleaned_data.get("apply_country")
        apply_school = self.cleaned_data.get("apply_school")
        apply_college = self.cleaned_data.get("apply_college")
        apply_major = self.cleaned_data.get("apply_major")
        apply_degree_type = self.cleaned_data.get("apply_degree_type")
        if apply_country and apply_school and apply_college and apply_major and apply_degree_type:
            if self.old_instance:
                if apply_country == self.old_instance.apply_country and apply_school == self.old_instance.apply_school and apply_college == self.old_instance.apply_college and apply_major == self.old_instance.apply_major and set(apply_degree_type.all()) == set(self.old_instance.apply_degree_type.all()):
                    return apply_degree_type
            dg = ApplyDegree.objects.all()
            for adt in apply_degree_type:
                d = dg.filter(apply_country = apply_country, apply_school = apply_school, apply_college = apply_college, apply_major = apply_major, apply_degree_type = adt)
                if len(d) > 0:
                    raise forms.ValidationError("已存在")
        return apply_degree_type

class SchoolApplicationCountryCreationForm(ModelForm):
    class Meta:
        model = ApplyCountry
        fields = ['name', 'chinese_name']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        if 'instance' in kwargs:
            self.old_instance = kwargs['instance']
        else:
            self.old_instance = None
        super(SchoolApplicationCountryCreationForm, self).__init__(*args, **kwargs)
        MyBasicField.add_field_info(self, None)
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            if self.old_instance:
                if name == self.old_instance.name:
                    return name
            ac = ApplyCountry.objects.all()
            try:
                a = ac.get(name = name)
                raise forms.ValidationError("已存在")
            except ac.model.DoesNotExist:
                pass
        return name
    def clean_chinese_name(self):
        chinese_name = self.cleaned_data.get("chinese_name")
        if chinese_name:
            if self.old_instance:
                if chinese_name == self.old_instance.chinese_name:
                    return chinese_name
            ac = ApplyCountry.objects.all()
            try:
                a = ac.get(chinese_name = chinese_name)
                raise forms.ValidationError("已存在")
            except ac.model.DoesNotExist:
                pass
        return chinese_name

class SchoolApplicationSchoolCreationForm(ModelForm):
    class Meta:
        model = ApplySchool
        fields = ['name', 'chinese_name']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        if 'instance' in kwargs:
            self.old_instance = kwargs['instance']
        else:
            self.old_instance = None
        super(SchoolApplicationSchoolCreationForm, self).__init__(*args, **kwargs)
        MyBasicField.add_field_info(self, None)
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            if self.old_instance:
                if name == self.old_instance.name:
                    return name
            ac = ApplySchool.objects.all()
            try:
                a = ac.get(name = name)
                raise forms.ValidationError("已存在")
            except ac.model.DoesNotExist:
                pass
        return name
    def clean_chinese_name(self):
        chinese_name = self.cleaned_data.get("chinese_name")
        if chinese_name:
            if self.old_instance:
                if chinese_name == self.old_instance.chinese_name:
                    return chinese_name
            ac = ApplySchool.objects.all()
            try:
                a = ac.get(chinese_name = chinese_name)
                raise forms.ValidationError("已存在")
            except ac.model.DoesNotExist:
                pass
        return chinese_name

class SchoolApplicationCollegeCreationForm(ModelForm):
    class Meta:
        model = ApplyCollege
        fields = ['name', 'chinese_name']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        if 'instance' in kwargs:
            self.old_instance = kwargs['instance']
        else:
            self.old_instance = None
        super(SchoolApplicationCollegeCreationForm, self).__init__(*args, **kwargs)
        MyBasicField.add_field_info(self, None)
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            if self.old_instance:
                if name == self.old_instance.name:
                    return name
            ac = ApplyCollege.objects.all()
            try:
                a = ac.get(name = name)
                raise forms.ValidationError("已存在")
            except ac.model.DoesNotExist:
                pass
        return name
    def clean_chinese_name(self):
        chinese_name = self.cleaned_data.get("chinese_name")
        if chinese_name:
            if self.old_instance:
                if chinese_name == self.old_instance.chinese_name:
                    return chinese_name
            ac = ApplyCollege.objects.all()
            try:
                a = ac.get(chinese_name = chinese_name)
                raise forms.ValidationError("已存在")
            except ac.model.DoesNotExist:
                pass
        return chinese_name

class SchoolApplicationMajorCreationForm(ModelForm):
    class Meta:
        model = ApplyMajor
        fields = ['name', 'chinese_name']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        if 'instance' in kwargs:
            self.old_instance = kwargs['instance']
        else:
            self.old_instance = None
        super(SchoolApplicationMajorCreationForm, self).__init__(*args, **kwargs)
        MyBasicField.add_field_info(self, None)
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            if self.old_instance:
                if name == self.old_instance.name:
                    return name
            ac = ApplyMajor.objects.all()
            try:
                a = ac.get(name = name)
                raise forms.ValidationError("已存在")
            except ac.model.DoesNotExist:
                pass
        return name
    def clean_chinese_name(self):
        chinese_name = self.cleaned_data.get("chinese_name")
        if chinese_name:
            if self.old_instance:
                if chinese_name == self.old_instance.chinese_name:
                    return chinese_name
            ac = ApplyMajor.objects.all()
            try:
                a = ac.get(chinese_name = chinese_name)
                raise forms.ValidationError("已存在")
            except ac.model.DoesNotExist:
                pass
        return chinese_name

class ChannelRelationshipCreationForm(ModelForm):
    class Meta:
        model = ChannelRelationship
        fields = ['channel', 'student']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        if 'instance' in kwargs:
            self.old_instance = kwargs['instance']
        else:
            self.old_instance = None
        super(ChannelRelationshipCreationForm, self).__init__(*args, **kwargs)
        self.fields['channel'].queryset = User.objects.filter(groups__name="渠道")
        self.fields['student'].queryset = User.objects.filter(groups__name="学生")
        MyBasicField.add_field_info(self, None)
    def clean_student(self):
        channel = self.cleaned_data.get("channel")
        student = self.cleaned_data.get("student")
        if channel and student:
            if self.old_instance:
                if channel == self.old_instance.channel and student == self.old_instance.student:
                    return student
            cr = ChannelRelationship.objects.all()
            try:
                r = cr.get(channel = channel, student = student)
                raise forms.ValidationError("渠道关系已存在")
            except cr.model.DoesNotExist:
                pass
        return student

class MentoringRelationshipCreationForm(ModelForm):
    class Meta:
        model = MentoringRelationship
        fields = ['teacher', 'student', 'relationship_status', 'teacher_score', 'student_score', 'administrator_comment', 'teacher_comment', 'student_comment']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        if 'instance' in kwargs:
            self.old_instance = kwargs['instance']
        else:
            self.old_instance = None
        super(MentoringRelationshipCreationForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.filter(groups__name="导师")
        self.fields['student'].queryset = User.objects.filter(groups__name="学生")
        MyBasicField.add_field_info(self, None)
        if self.request.user.groups.first().name == "导师":
            self.fields['teacher'].disabled = True
            self.fields['student'].disabled = True
            self.fields['relationship_status'].disabled = True
            self.fields['teacher_score'].disabled = True
            self.fields.pop('teacher_score')
            self.fields['administrator_comment'].disabled = True
            self.fields.pop('administrator_comment')
            self.fields['student_comment'].disabled = True
            self.fields.pop('student_comment')
        if self.request.user.groups.first().name == "学生":
            self.fields['teacher'].disabled = True
            self.fields['student'].disabled = True
            self.fields['relationship_status'].disabled = True
            self.fields['student_score'].disabled = True
            self.fields.pop('student_score')
            self.fields['administrator_comment'].disabled = True
            self.fields.pop('administrator_comment')
            self.fields['teacher_comment'].disabled = True
            self.fields.pop('teacher_comment')
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
