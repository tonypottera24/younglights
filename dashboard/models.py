from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chinese_name = models.CharField(max_length=128, default="")

    school = models.CharField(max_length=100, null=True, blank=True, default='')
    college = models.CharField(max_length=100, null=True, blank=True, default='')
    major = models.CharField(max_length=100, null=True, blank=True, default='')
    
    phone = models.CharField(max_length=100, null=True, blank=True, default='')
    qq = models.CharField(max_length=100, null=True, blank=True, default='')
    wechat = models.CharField(max_length=100, null=True, blank=True, default='')

    research_field = models.TextField(max_length=1000, null=True, blank=True, default='')
    research_experience = models.TextField(max_length=10000, null=True, blank=True, default='')
    thesis_experience = models.TextField(max_length=10000, null=True, blank=True, default='')
    def save( self, *args, **kw ):
        self.chinese_name = self.user.last_name + self.user.first_name
        super( UserProfile, self ).save( *args, **kw )
    def __str__(self):
        if len(self.user.groups.all()) > 0:
            return self.chinese_name + " " + self.user.groups.first().name
        return self.chinese_name

    class Meta:
        permissions = (
            ("view_administrator", "Can view administrator"),
            ("add_administrator", "Can add administrator"),
            ("change_administrator", "Can change administrator"),
            ("delete_administrator", "Can delete administrator"),
            ("view_teacher", "Can view teacher"),
            ("add_teacher", "Can add teacher"),
            ("change_teacher", "Can change teacher"),
            ("delete_teacher", "Can delete teacher"),
            ("view_student", "Can view student"),
            ("add_student", "Can add student"),
            ("change_student", "Can change student"),
            ("delete_student", "Can delete student"),
        )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class MentoringRelationship(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MentoringRelationship_teacher")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MentoringRelationship_student")

    STATUS_CHOICES = (
            ('辅导中', '辅导中'),
            ('辅导完成', '辅导完成'),
            )
    relationship_status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    SCORE_CHOICES = (
            (-1, '未评分'),
            (5, '五颗星'),
            (4, '四颗星'),
            (3, '三颗星'),
            (2, '两颗星'),
            (1, '一颗星'),
            )
    teacher_score = models.IntegerField(choices=SCORE_CHOICES, default=SCORE_CHOICES[0][0])
    student_score = models.IntegerField(choices=SCORE_CHOICES, default=SCORE_CHOICES[0][0])

    administrator_comment = models.TextField(max_length=1000, default='')
    teacher_comment = models.TextField(max_length=1000, default='')
    student_comment = models.TextField(max_length=1000, default='')
    
    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "导生关系：%s（导师）、%s（学生）" % (self.teacher.userprofile.chinese_name, self.student.userprofile.chinese_name)

    class Meta:
        permissions = (
            ("view_mentoringrelationship", "Can view mentoring relationship"),
        )

class MentoringRecord(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MentoringRecord_teacher")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MentoringRecord_student")

    #teacher_record = models.TextField(max_length=1000)
    #student_record = models.TextField(max_length=1000)
    content = models.TextField(max_length=1000, default='')

    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    TIME_CHOICES = (
            (datetime.time(0, 30), '00:30'),
            (datetime.time(1, 0), '01:00'),
            (datetime.time(1, 30), '01:30'),
            (datetime.time(2, 0), '02:00'),
            (datetime.time(2, 30), '02:30'),
            (datetime.time(3, 0), '03:00'),
            (datetime.time(3, 30), '03:30'),
            (datetime.time(4, 0), '04:00'),
            (datetime.time(4, 30), '04:30'),
            (datetime.time(5, 0), '05:00'),
            (datetime.time(5, 30), '05:30'),
            )
    mentoring_date = models.DateField('mentoring date')
    #mentoring_time = models.TimeField('mentoring time')
    mentoring_time = models.TimeField(choices=TIME_CHOICES)

    def __str__(self):
        return "辅导纪录：%s（导师）、%s（学生）" % (self.teacher.userprofile.chinese_name, self.student.userprofile.chinese_name)

    class Meta:
        permissions = (
            ("view_mentoringrecord", "Can view mentoring record"),
        )

class Mission(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Mission_teacher")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Mission_student")

    title = models.CharField(max_length=15, default='')
    content = models.TextField(max_length=5000, default='')

    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    end_date = models.DateField('end date')

    def __str__(self):
        return "任务：%s（导师）、%s（学生）：%s" % (self.teacher.userprofile.chinese_name, self.student.userprofile.chinese_name, self.content)

    class Meta:
        permissions = (
            ("view_mission", "Can view mission"),
        )

class ApplyDegreeType(models.Model):
    name = models.CharField(max_length=64)
    chinese_name = models.CharField(max_length=64)

    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.name, self.chinese_name)

class ApplyMajor(models.Model):
    name = models.CharField(max_length=64)
    chinese_name = models.CharField(max_length=64)

    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.name, self.chinese_name)

    class Meta:
        permissions = (
            ("view_applymajor", "Can view apply major"),
        )

class ApplyCollege(models.Model):
    name = models.CharField(max_length=64)
    chinese_name = models.CharField(max_length=64)

    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.name, self.chinese_name)

    class Meta:
        permissions = (
            ("view_applycollege", "Can view apply college"),
        )

class ApplySchool(models.Model):
    name = models.CharField(max_length=64)
    chinese_name = models.CharField(max_length=64)

    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.name, self.chinese_name)

    class Meta:
        permissions = (
            ("view_applyschool", "Can view apply school"),
        )

class ApplyCountry(models.Model):
    name = models.CharField(max_length=64)
    chinese_name = models.CharField(max_length=64)

    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.name, self.chinese_name)

    class Meta:
        permissions = (
            ("view_applycountry", "Can view apply country"),
        )

class ApplySemester(models.Model):
    name = models.CharField(max_length=64)
    chinese_name = models.CharField(max_length=64)

    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.name, self.chinese_name)

class ApplyGRESubject(models.Model):
    name = models.CharField(max_length=64)
    chinese_name = models.CharField(max_length=64)

    added_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.name, self.chinese_name)

class ApplyDegree(models.Model):
    apply_country = models.ForeignKey(ApplyCountry, on_delete=models.CASCADE)
    apply_school = models.ForeignKey(ApplySchool, on_delete=models.CASCADE)
    apply_college = models.ForeignKey(ApplyCollege, on_delete=models.CASCADE)
    apply_major = models.ForeignKey(ApplyMajor, on_delete=models.CASCADE)
    apply_degree_type = models.ManyToManyField(ApplyDegreeType)

    apply_semester = models.ManyToManyField(ApplySemester)
    deadline = models.DateField()
    tuition = models.IntegerField(default = 0)

    usnews_rank = models.IntegerField(default = 0)
    
    gpa = models.FloatField(default = 0)
    gpa_required = models.BooleanField(default=False)
    toefl = models.FloatField(default = 0)
    toefl_required = models.BooleanField(default=False)
    ielts = models.FloatField(default = 0)
    ielts_required = models.BooleanField(default=False)
    gre = models.FloatField(default = 0)
    gre_required = models.BooleanField(default=False)
    gre_subject = models.ManyToManyField(ApplyGRESubject, blank=True)
    gmat = models.FloatField(default = 0)
    gmat_required = models.BooleanField(default=False)

    apply_comment = MarkdownxField(max_length = 5000, blank=True, default = '')
    @property
    def apply_comment_markdown(self):
        return markdownify(self.apply_comment)
    apply_curriculum = MarkdownxField(max_length = 5000, blank=True, default = '')
    @property
    def apply_curriculum_markdown(self):
        return markdownify(self.apply_curriculum)
    apply_link = MarkdownxField(max_length = 5000, blank=True, default = '')
    @property
    def apply_link_markdown(self):
        return markdownify(self.apply_link)

    added_datetime = models.DateTimeField(auto_now_add = True)
    updated_datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return ("%s %s %s %s " % (self.apply_country.chinese_name, self.apply_school.chinese_name, self.apply_college.chinese_name, self.apply_major.chinese_name)) + " ".join(i.chinese_name for i in self.apply_degree_type.all())

    class Meta:
        permissions = (
            ("view_applydegree", "Can view apply degree"),
        )
