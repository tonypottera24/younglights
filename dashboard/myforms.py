from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from younglights import settings

class MyBasicField():
    channel_name = forms.CharField(max_length=128, required = True)
    principal_name = forms.CharField(max_length=128, required = True)
    contact_name = forms.CharField(max_length=128, required = True)

    new_password1 = forms.CharField(widget=forms.PasswordInput, strip=False, required = False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, strip=False, required = False)

    phone = forms.CharField(max_length = 100, required = False)
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
        if 'channel_name' in self.fields:
            self.fields['channel_name'].widget.attrs['placeholder'] = '请输入亲的渠道名 / Channel name'
            self.fields['channel_name'].label = '渠道名 / Channel name'
        if 'principal_name' in self.fields:
            self.fields['principal_name'].widget.attrs['placeholder'] = '请输入亲的负责人姓名 / Principal name'
            self.fields['principal_name'].label = '负责人姓名 / Principal name'
        if 'contact_name' in self.fields:
            self.fields['contact_name'].widget.attrs['placeholder'] = '请输入亲的对接人姓名 / Contact name'
            self.fields['contact_name'].label = '对接人姓名 / Contact name'
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
            self.fields['email'].required = False
        if 'phone' in self.fields:
            self.fields['phone'].widget.attrs['placeholder'] = '请输入亲的电话号码 / Phone'
            self.fields['phone'].label = '电话号码 / Phone'
            self.fields['phone'].required = False
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
            self.fields['teacher'].widget.attrs['data-am-selected']="{searchBox: 1, btnWidth: '100%', maxHeight: 300}"
            self.fields['teacher'].widget.attrs['placeholder'] = '请选择导师 / Teacher'
            self.fields['teacher'].label = '导师 / Teacher'
            self.fields['teacher'].required = True
        if 'student' in self.fields:
            self.fields['student'].widget.attrs['data-am-selected']="{searchBox: 1, btnWidth: '100%', maxHeight: 300}"
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
        if 'deadline' in self.fields:
            self.fields['deadline'].widget.attrs['placeholder'] = '请选择Deadline'
            self.fields['deadline'].widget.attrs['class'] = 'datepicker'
            self.fields['deadline'].widget.attrs['data-am-datepicker'] = "{format: 'yyyy/mm/dd', viewMode: 'years'}"
            self.fields['deadline'].label = '截止日期 / Deadline'
            self.fields['deadline'].required = True
        if 'mentoring_date' in self.fields:
            self.fields['mentoring_date'].widget.attrs['placeholder'] = '请选择亲的辅导日期 / Mentoring Date'
            self.fields['mentoring_date'].widget.attrs['class'] = 'datepicker'
            self.fields['mentoring_date'].widget.attrs['data-am-datepicker'] = "{format: 'yyyy/mm/dd'}"
            self.fields['mentoring_date'].label = '辅导日期 / Mentoring Date'
            self.fields['mentoring_date'].required = True
        if 'mentoring_time' in self.fields:
            self.fields['mentoring_time'].widget.attrs['placeholder'] = '请选择亲的辅导时长'
            self.fields['mentoring_time'].widget.attrs['data-am-selected']="{searchBox: 1, btnWidth: '100%', maxHeight: 300}"
            self.fields['mentoring_time'].label = '辅导时长 / Mentoring time'
            self.fields['mentoring_time'].required = True
        if 'title' in self.fields:
            self.fields['title'].widget.attrs['placeholder'] = '请输入标题 / Title'
            self.fields['title'].label = '标题 / Title'
            self.fields['title'].required = True
        if 'relationship_status' in self.fields:
            self.fields['relationship_status'].widget.attrs['data-am-selected'] = "{btnWidth: '100%'}"
            self.fields['relationship_status'].label = '輔導状态 / Relationship Status'
            self.fields['relationship_status'].required = True
        if 'content' in self.fields:
            self.fields['content'].widget.attrs['placeholder'] = '请输入内容 / Content'
            self.fields['content'].label = '内容 / Content'
            self.fields['content'].required = True
        if 'teacher_score' in self.fields:
            self.fields['teacher_score'].widget.attrs['data-am-selected'] = "{btnWidth: '100%'}"
            self.fields['teacher_score'].label = '导师分数 / Teacher Score'
            self.fields['teacher_score'].required = True
        if 'student_score' in self.fields:
            self.fields['student_score'].widget.attrs['data-am-selected'] = "{btnWidth: '100%'}"
            self.fields['student_score'].label = '学生分数 / Student Score'
            self.fields['student_score'].required = True
        if 'administrator_comment' in self.fields:
            self.fields['administrator_comment'].widget.attrs['placeholder'] = '请输入管理员备注 / Administrator Comment'
            self.fields['administrator_comment'].label = '管理员备注 / Administrator Comment'
            self.fields['administrator_comment'].required = False
        if 'teacher_comment' in self.fields:
            self.fields['teacher_comment'].widget.attrs['placeholder'] = '请输入导师备注 / Teacher Comment'
            self.fields['teacher_comment'].label = '导师评语 / Teacher Comment'
            self.fields['teacher_comment'].required = False
        if 'student_comment' in self.fields:
            self.fields['student_comment'].widget.attrs['placeholder'] = '请输入学生备注 / Student Comment'
            self.fields['student_comment'].label = '学生评语 / Student Comment'
            self.fields['student_comment'].required = False
        if 'name' in self.fields:
            self.fields['name'].widget.attrs['placeholder'] = '请输入名称 / Name'
            self.fields['name'].label = '名称 / Name'
            self.fields['name'].required = True
        if 'chinese_name' in self.fields:
            self.fields['chinese_name'].widget.attrs['placeholder'] = '请输入中文名称 / Chinese Name'
            self.fields['chinese_name'].label = '中文名称 / Chinese Name'
            self.fields['chinese_name'].required = True
        if 'apply_country' in self.fields:
            self.fields['apply_country'].widget.attrs['data-am-selected']="{searchBox: 1, btnWidth: '100%', maxHeight: 300}"
            self.fields['apply_country'].widget.attrs['placeholder'] = '请选择国家 / Country'
            self.fields['apply_country'].label = '国家 / Country'
            self.fields['apply_country'].required = True
        if 'apply_school' in self.fields:
            self.fields['apply_school'].widget.attrs['data-am-selected']="{searchBox: 1, btnWidth: '100%', maxHeight: 300}"
            self.fields['apply_school'].widget.attrs['placeholder'] = '请选择学校 / School'
            self.fields['apply_school'].label = '学校 / School'
            self.fields['apply_school'].required = True
        if 'apply_college' in self.fields:
            self.fields['apply_college'].widget.attrs['data-am-selected']="{searchBox: 1, btnWidth: '100%', maxHeight: 300}"
            self.fields['apply_college'].widget.attrs['placeholder'] = '请选择学院 / College'
            self.fields['apply_college'].label = '学院 / College'
            self.fields['apply_college'].required = True
        if 'apply_major' in self.fields:
            self.fields['apply_major'].widget.attrs['data-am-selected']="{searchBox: 1, btnWidth: '100%', maxHeight: 300}"
            self.fields['apply_major'].widget.attrs['placeholder'] = '请选择专业 / Major'
            self.fields['apply_major'].label = '专业 / Major'
            self.fields['apply_major'].required = True
        if 'apply_degree_type' in self.fields:
            self.fields['apply_degree_type'].widget.attrs['data-am-selected']="{btnWidth: '100%'}"
            self.fields['apply_degree_type'].widget.attrs['placeholder'] = '请选择学位种类 / Degree Type'
            self.fields['apply_degree_type'].widget.attrs['multiple'] = ""
            self.fields['apply_degree_type'].label = '学位种类 / Degree Type'
            self.fields['apply_degree_type'].required = True
        if 'apply_type' in self.fields:
            self.fields['apply_type'].widget.attrs['data-am-selected']="{btnWidth: '100%'}"
            self.fields['apply_type'].widget.attrs['placeholder'] = '请选择种类 / Type'
            self.fields['apply_type'].label = '种类 / Type'
            self.fields['apply_type'].required = True
        if 'usnews_rank' in self.fields:
            self.fields['usnews_rank'].widget.attrs['placeholder'] = '请输入USNEWS排名'
            self.fields['usnews_rank'].label = 'USNEWS排名'
            self.fields['usnews_rank'].required = True
        if 'gpa_required' in self.fields:
            self.fields['gpa_required'].label = '要求GPA'
            self.fields['gpa_required'].required = False
        if 'gpa' in self.fields:
            self.fields['gpa'].widget.attrs['placeholder'] = '请输入GPA'
            self.fields['gpa'].label = 'GPA'
            self.fields['gpa'].required = True
        if 'toefl_required' in self.fields:
            self.fields['toefl_required'].label = '要求TOEFL成绩'
            self.fields['toefl_required'].required = False
        if 'toefl' in self.fields:
            self.fields['toefl'].widget.attrs['placeholder'] = '请输入TOEFL'
            self.fields['toefl'].label = 'TOEFL成绩'
            self.fields['toefl'].required = True
        if 'ielts_required' in self.fields:
            self.fields['ielts_required'].label = '要求IELTS成绩'
            self.fields['ielts_required'].required = False
        if 'ielts' in self.fields:
            self.fields['ielts'].widget.attrs['placeholder'] = '请输入IELTS'
            self.fields['ielts'].label = 'IELTS成绩'
            self.fields['ielts'].required = True
        if 'gre_required' in self.fields:
            self.fields['gre_required'].label = '要求GRE成绩'
            self.fields['gre_required'].required = False
        if 'gre' in self.fields:
            self.fields['gre'].widget.attrs['placeholder'] = '请输入GRE成绩'
            self.fields['gre'].label = 'GRE成绩'
            self.fields['gre'].required = True
        if 'gre_subject' in self.fields:
            self.fields['gre_subject'].widget.attrs['data-am-selected'] = "{btnWidth: '100%'}"
            self.fields['gre_subject'].widget.attrs['multiple'] = ""
            self.fields['gre_subject'].widget.attrs['placeholder'] = '无要求'
            self.fields['gre_subject'].label = 'GRE科目 / GRE Subject'
            self.fields['gre_subject'].required = False
        if 'gmat_required' in self.fields:
            self.fields['gmat_required'].label = '要求GMAT成绩'
            self.fields['gmat_required'].required = False
        if 'gmat' in self.fields:
            self.fields['gmat'].widget.attrs['placeholder'] = '请输入GMAT成绩'
            self.fields['gmat'].label = 'GMAT成绩'
            self.fields['gmat'].required = True
        if 'tuition' in self.fields:
            self.fields['tuition'].widget.attrs['placeholder'] = '请输入学费 / Tuition Fee'
            self.fields['tuition'].label = '学费 / Tuition Fee'
            self.fields['tuition'].required = True
        if 'apply_semester' in self.fields:
            self.fields['apply_semester'].widget.attrs['data-am-selected'] = "{btnWidth: '100%'}"
            self.fields['apply_semester'].widget.attrs['multiple'] = ""
            self.fields['apply_semester'].widget.attrs['placeholder'] = '请选择可申请学期 / Semester'
            self.fields['apply_semester'].label = '可申请学期 / Semester'
            self.fields['apply_semester'].required = True
        if 'apply_comment' in self.fields:
            self.fields['apply_comment'].widget.attrs['placeholder'] = '请输入申请说明 / Comment'
            self.fields['apply_comment'].label = '申请说明 / Comment'
            self.fields['apply_comment'].required = False
        if 'apply_curriculum' in self.fields:
            self.fields['apply_curriculum'].widget.attrs['placeholder'] = '请输入课程设置 / Curriculum'
            self.fields['apply_curriculum'].label = '课程设置 / Curriculum'
            self.fields['apply_curriculum'].required = False
        if 'apply_link' in self.fields:
            self.fields['apply_link'].widget.attrs['placeholder'] = '请输入相关连结 / Links'
            self.fields['apply_link'].label = '相关连结 / Links'
            self.fields['apply_link'].required = False
