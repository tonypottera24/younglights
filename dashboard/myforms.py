from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from younglights import settings

class MyBasicField():
    new_password1 = forms.CharField(widget=forms.PasswordInput, strip=False, required = False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, strip=False, required = False)

    phone = forms.CharField(max_length = 100, required = True)
    qq = forms.CharField(max_length = 100, required = False) 
    wechat = forms.CharField(max_length = 100, required = False)

    school = forms.CharField(max_length = 100, required = False)
    college = forms.CharField(max_length = 100, required = False)
    major = forms.CharField(max_length = 100, required = False)

    research_field = forms.CharField(max_length=1000, required=False)
    research_experience = forms.CharField(max_length=10000, required=False)
    thesis_experience = forms.CharField(max_length=10000, required=False)
    def add_field_info(self, user):
        if 'username' in self.fields:
            self.fields['username'].widget.attrs['placeholder'] = '请输入亲的用户名 / Username'
            self.fields['username'].label = '用户名 / Username'
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs['placeholder'] = '请输入亲的密码 / Password'
            self.fields['password1'].label = '密码 / Password'
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs['placeholder'] = '请再次输入亲的密码 / Password confirm'
            self.fields['password2'].label = '密码确认 / Password confirm'
        if 'new_password1' in self.fields:
            self.fields['new_password1'].widget.attrs['placeholder'] = '请输入亲的新密码 / New Password'
            self.fields['new_password1'].label = '新密码 / New Password'
        if 'new_password2' in self.fields:
            self.fields['new_password2'].widget.attrs['placeholder'] = '请再次输入亲的新密码 / New Password confirm'
            self.fields['new_password2'].label = '新密码确认 / New Password confirm'
        if 'last_name' in self.fields:
            self.fields['last_name'].widget.attrs['placeholder'] = '请输入亲的姓氏 / Last name'
            self.fields['last_name'].label = '姓氏 / Last name'
            self.fields['last_name'].required = True
        if 'first_name' in self.fields:
            self.fields['first_name'].widget.attrs['placeholder'] = '请输入亲的名字 / First name'
            self.fields['first_name'].label = '名字 / First name'
            self.fields['first_name'].required = True
        if 'email' in self.fields:
            self.fields['email'].widget.attrs['placeholder'] = '请输入亲的电子邮件地址 / Email address'
            self.fields['email'].label = '电子邮件地址 / Email address'
            self.fields['email'].required = True
        if 'phone' in self.fields:
            self.fields['phone'].widget.attrs['placeholder'] = '请输入亲的电话号码 / Phone'
            self.fields['phone'].label = '电话号码 / Phone'
            self.fields['phone'].required = True
        if 'qq' in self.fields:
            self.fields['qq'].widget.attrs['placeholder'] = '请输入亲的QQ号码 / QQ'
            self.fields['qq'].label = 'QQ号码 / QQ'
            self.fields['qq'].required = False
        if 'wechat' in self.fields:
            self.fields['wechat'].widget.attrs['placeholder'] = '请输入亲的微信 / WeChat'
            self.fields['wechat'].label = '微信 / WeChat'
            self.fields['wechat'].required = False
        if 'school' in self.fields:
            self.fields['school'].widget.attrs['placeholder'] = '请输入亲的学校 / School'
            self.fields['school'].label = '学校 / School'
            self.fields['school'].required = False
        if 'college' in self.fields:
            self.fields['college'].widget.attrs['placeholder'] = '请输入亲的学院 / College'
            self.fields['college'].label = '学院 / College'
            self.fields['college'].required = False
        if 'major' in self.fields:
            self.fields['major'].widget.attrs['placeholder'] = '请输入亲的专业 / Major'
            self.fields['major'].label = '专业 / Major'
            self.fields['major'].required = False
        if 'research_field' in self.fields:
            self.fields['research_field'].widget = forms.Textarea(attrs = {'placeholder': '请输入亲的研究领域 / Research Field'})
            self.fields['research_field'].label = '研究领域 / Research Field'
            self.fields['research_field'].required = False
        if 'research_experience' in self.fields:
            self.fields['research_experience'].widget = forms.Textarea(attrs = {'placeholder': '请输入亲的研究经验 / Research Experience'})
            self.fields['research_experience'].label = '研究经验 / Research Experience'
            self.fields['research_experience'].required = False
        if 'thesis_experience' in self.fields:
            self.fields['thesis_experience'].widget = forms.Textarea(attrs = {'placeholder': '请输入亲的论文经验 / Thesis Experience'})
            self.fields['thesis_experience'].label = '论文经验 / Thesis Experience'
            self.fields['thesis_experience'].required = False
        if 'teacher' in self.fields:
            self.fields['teacher'].widget.attrs['data-am-selected']="{searchBox: 1}"
            self.fields['teacher'].widget.attrs['placeholder'] = '请选择导师 / Teacher'
            self.fields['teacher'].label = '导师 / Teacher'
            self.fields['teacher'].required = True
        if 'student' in self.fields:
            self.fields['student'].widget.attrs['data-am-selected']="{searchBox: 1}"
            self.fields['student'].widget.attrs['placeholder'] = '请选择学生 / Student'
            self.fields['student'].label = '学生 / Student'
            self.fields['student'].required = True
        if 'start_date' in self.fields:
            self.fields['start_date'].widget.attrs['class'] = 'datepicker'
            self.fields['start_date'].widget.attrs['data-am-datepicker'] = "{format: 'yyyy/mm/dd'}"
            self.fields['start_date'].label = '开始日期 / start_date'
            self.fields['start_date'].required = True
        if 'end_date' in self.fields:
            self.fields['end_date'].widget.attrs['class'] = 'datepicker'
            self.fields['end_date'].widget.attrs['data-am-datepicker'] = "{format: 'yyyy/mm/dd'}"
            self.fields['end_date'].label = '结束日期 / end_date'
            self.fields['end_date'].required = True
        if 'mentoring_date' in self.fields:
            self.fields['mentoring_date'].widget.attrs['placeholder'] = '请选择亲的辅导日期 / Mentoring Date'
            self.fields['mentoring_date'].widget.attrs['class'] = 'datepicker'
            self.fields['mentoring_date'].widget.attrs['data-am-datepicker'] = "{format: 'yyyy/mm/dd'}"
            self.fields['mentoring_date'].label = '辅导日期 / Mentoring Date'
            self.fields['mentoring_date'].required = True
        if 'mentoring_time' in self.fields:
            self.fields['mentoring_time'].widget.attrs['placeholder'] = '请选择亲的辅导时长'
            self.fields['mentoring_time'].widget.attrs['data-am-selected']="{searchBox: 1}"
            self.fields['mentoring_time'].label = '辅导时长 / Mentoring time'
            self.fields['mentoring_time'].required = True
        if 'title' in self.fields:
            self.fields['title'].widget.attrs['placeholder'] = '请输入标题 / Title'
            self.fields['title'].label = '标题 / Title'
            self.fields['title'].required = True
        if 'relationship_status' in self.fields:
            self.fields['relationship_status'].widget.attrs['data-am-selected'] = ""
            self.fields['relationship_status'].label = '輔導状态 / Relationship Status'
            self.fields['relationship_status'].required = True
        if 'content' in self.fields:
            self.fields['content'].widget.attrs['placeholder'] = '请输入内容 / Content'
            self.fields['content'].label = '内容 / Content'
            self.fields['content'].required = True
        if 'comment' in self.fields:
            self.fields['comment'].widget.attrs['placeholder'] = '请输入备注 / Comment'
            self.fields['comment'].label = '备注 / Comment'
            self.fields['comment'].required = True
