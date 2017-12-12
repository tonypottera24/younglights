from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from younglights import settings
from .myforms import MyBasicField

class MyUserCreationForm(UserCreationForm):
    phone = MyBasicField.phone
    qq = MyBasicField.qq
    wechat = MyBasicField.wechat
    class Meta:
        fields = []
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        MyBasicField.add_field_info(self, None)
class AdministratorCreationForm(MyUserCreationForm):
    class Meta:
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'password1', 'password2', 
            'email', 'phone', 'qq', 'wechat',
        )
class TeacherCreationForm(MyUserCreationForm):
    school = MyBasicField.school
    college = MyBasicField.college
    major = MyBasicField.major
    research_field = MyBasicField.research_field
    research_experience = MyBasicField.research_experience
    thesis_experience = MyBasicField.thesis_experience
    class Meta:
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'password1', 'password2', 
            'email', 'phone', 'qq', 'wechat',
            'school', 'college', 'major', 
            'research_field', 'research_experience', 'thesis_experience',
        )
class StudentCreationForm(MyUserCreationForm):
    school = MyBasicField.school
    college = MyBasicField.college
    major = MyBasicField.major
    class Meta:
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'password1', 'password2', 
            'email', 'phone', 'qq', 'wechat',
            'school', 'college', 'major', 
        )

class MyUserChangeForm(UserChangeForm):
    password = None
    new_password1 = MyBasicField.new_password1
    new_password2 = MyBasicField.new_password2
    phone = MyBasicField.phone
    qq = MyBasicField.qq
    wechat = MyBasicField.wechat
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    class Meta:
        model = User
        fields = []
    def __init__(self, *args, **kwargs):
        user = None
        if 'instance' in kwargs:
            user = kwargs['instance']
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        MyBasicField.add_field_info(self, user)
    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return new_password2
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('new_password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('new_password2', error)
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('new_password2')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
class AdministratorChangeForm(MyUserChangeForm):
    class Meta:
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'new_password1', 'new_password2', 
            'email', 'phone', 'qq', 'wechat',
        )
class TeacherChangeForm(MyUserChangeForm):
    school = MyBasicField.school
    college = MyBasicField.college
    major = MyBasicField.major
    research_field = MyBasicField.research_field
    research_experience = MyBasicField.research_experience
    thesis_experience = MyBasicField.thesis_experience
    class Meta:
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'new_password1', 'new_password2', 
            'email', 'phone', 'qq', 'wechat',
            'school', 'college', 'major', 
            'research_field', 'research_experience', 'thesis_experience',
        )
class StudentChangeForm(MyUserChangeForm):
    school = MyBasicField.school
    college = MyBasicField.college
    major = MyBasicField.major
    class Meta:
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'new_password1', 'new_password2', 
            'email', 'phone', 'qq', 'wechat',
            'school', 'college', 'major', 
        )
