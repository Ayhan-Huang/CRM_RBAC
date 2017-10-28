from django.db import models
from rbac.models import User as rbac_User


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称', max_length=16)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    员工表
    """
    # 与权限表建立一对一表关联，重复字段在这里剔除
    user = models.OneToOneField(verbose_name='账户', to=rbac_User)
    name = models.CharField(verbose_name='员工姓名', max_length=16, null=True, blank=True)
    # username = models.CharField(verbose_name='用户名', max_length=32, null=True, blank=True)
    # password = models.CharField(verbose_name='密码', max_length=64, null=True, blank=True)
    # email = models.EmailField(verbose_name='邮箱', max_length=64, null=True, blank=True)

    depart = models.ForeignKey(verbose_name='部门', to="Department", null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    课程表
    如：
        Linux基础
        Linux架构师
        Python自动化开发精英班
        Python自动化开发架构师班
    """
    name = models.CharField(verbose_name='课程名称', max_length=32)

    def __str__(self):
        return self.name


class School(models.Model):
    """
    校区表
    如：
        北京海淀校区
        北京昌平校区
        上海虹口校区
        广州白云山校区
    """
    title = models.CharField(verbose_name='校区名称', max_length=32)

    def __str__(self):
        return self.title


class ClassList(models.Model):
    """
    班级表
    如：
        Python全栈  面授班  5期  10000  2017-11-11  2018-5-11
    """
    school = models.ForeignKey(verbose_name='校区', to='School')
    course = models.ForeignKey(verbose_name='课程名称', to='Course')
    semester = models.IntegerField(verbose_name="班级(期)")
    price = models.IntegerField(verbose_name="学费")
    start_date = models.DateField(verbose_name="开班日期")
    graduate_date = models.DateField(verbose_name="结业日期", null=True, blank=True)
    memo = models.CharField(verbose_name='说明', max_length=256, blank=True, null=True, )
    teachers = models.ManyToManyField(verbose_name='任课老师', to='UserInfo', related_name='teach_classes')
    tutor = models.ForeignKey(verbose_name='班主任', to='UserInfo', related_name='classes')

    def __str__(self):
        tpl = '{course} {semester}期'.format(course=self.course.name, semester=self.semester)
        return tpl


class Customer(models.Model):
    """
    客户表
    """
    qq = models.CharField(verbose_name='qq', max_length=64, unique=True, help_text='QQ号必须唯一')

    name = models.CharField(verbose_name='学生姓名', max_length=16)
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

    education_choices = (
        (1, '重点大学'),
        (2, '普通本科'),
        (3, '独立院校'),
        (4, '民办本科'),
        (5, '大专'),
        (6, '民办专科'),
        (7, '高中'),
        (8, '其他')
    )
    education = models.IntegerField(verbose_name='学历', choices=education_choices, blank=True, null=True, )
    graduation_school = models.CharField(verbose_name='毕业学校', max_length=64, blank=True, null=True)
    major = models.CharField(verbose_name='所学专业', max_length=64, blank=True, null=True)

    experience_choices = [
        (1, '在校生'),
        (2, '应届毕业'),
        (3, '半年以内'),
        (4, '半年至一年'),
        (5, '一年至三年'),
        (6, '三年至五年'),
        (7, '五年以上'),
    ]
    experience = models.IntegerField(verbose_name='工作经验', blank=True, null=True, choices=experience_choices)
    work_status_choices = [
        (1, '在职'),
        (2, '无业')
    ]
    work_status = models.IntegerField(verbose_name="职业状态", choices=work_status_choices, default=1, blank=True,
                                      null=True)
    company = models.CharField(verbose_name="目前就职公司", max_length=64, blank=True, null=True)
    salary = models.CharField(verbose_name="当前薪资", max_length=64, blank=True, null=True)

    source_choices = [
        (1, "qq群"),
        (2, "内部转介绍"),
        (3, "官方网站"),
        (4, "百度推广"),
        (5, "360推广"),
        (6, "搜狗推广"),
        (7, "腾讯课堂"),
        (8, "广点通"),
        (9, "高校宣讲"),
        (10, "渠道代理"),
        (11, "51cto"),
        (12, "智汇推"),
        (13, "网盟"),
        (14, "DSP"),
        (15, "SEO"),
        (16, "其它"),
    ]
    source = models.SmallIntegerField('客户来源', choices=source_choices, default=1)
    referral_from = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name="转介绍自学员",
        help_text="若此客户是转介绍自内部学员,请在此处选择内部学员姓名",
        related_name="internal_referral"
    )
    course = models.ManyToManyField(verbose_name="咨询课程", to="Course")

    status_choices = [
        (1, "已报名"),
        (2, "未报名")
    ]
    status = models.IntegerField(
        verbose_name="状态",
        choices=status_choices,
        default=2,
        help_text=u"选择客户此时的状态"
    )
    consultant = models.ForeignKey(verbose_name="课程顾问", to='UserInfo', related_name='consultant')
    date = models.DateField(verbose_name="咨询日期", auto_now_add=True)
    last_consult_date = models.DateField(verbose_name="最后跟进日期", auto_now_add=True)

    def __str__(self):
        return self.name


class ConsultRecord(models.Model):
    """
    客户跟进记录
    """
    customer = models.ForeignKey(verbose_name="所咨询客户", to='Customer')
    consultant = models.ForeignKey(verbose_name="跟踪人", to='UserInfo')
    date = models.DateField(verbose_name="跟进日期", auto_now_add=True)
    note = models.TextField(verbose_name="跟进内容...")


class PaymentRecord(models.Model):
    """
    缴费记录
    """
    customer = models.ForeignKey(Customer, verbose_name="客户")

    class_list = models.ForeignKey(verbose_name="班级", to="ClassList", blank=True, null=True)

    pay_type_choices = [
        (1, "订金/报名费"),
        (2, "学费"),
        (3, "转班"),
        (4, "退学"),
        (5, "退款"),
    ]
    pay_type = models.IntegerField(verbose_name="费用类型", choices=pay_type_choices, default=1)
    paid_fee = models.IntegerField(verbose_name="费用数额", default=0)
    turnover = models.IntegerField(verbose_name="成交金额", blank=True, null=True)
    quote = models.IntegerField(verbose_name="报价金额", blank=True, null=True)
    note = models.TextField(verbose_name="备注", blank=True, null=True)
    date = models.DateTimeField(verbose_name="交款日期", auto_now_add=True)
    consultant = models.ForeignKey(verbose_name="负责老师", to='UserInfo', help_text="谁签的单就选谁")


class Student(models.Model):
    """
    学生表
    """
    customer = models.OneToOneField(verbose_name='客户信息', to='Customer')

    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    emergency_contract = models.CharField(max_length=32, blank=True, null=True, verbose_name='紧急联系人')
    class_list = models.ManyToManyField(verbose_name="已报班级", to='ClassList', blank=True)

    company = models.CharField(verbose_name='公司', max_length=128, blank=True)
    location = models.CharField(max_length=64, verbose_name='所在区域', blank=True)
    position = models.CharField(verbose_name='岗位', max_length=64, blank=True)
    salary = models.IntegerField(verbose_name='薪资', null=True, blank=True)
    welfare = models.CharField(verbose_name='福利', max_length=256, blank=True)
    date = models.DateField(verbose_name='入职时间', help_text='格式yyyy-mm-dd', null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=256, blank=True)

    def __str__(self):
        return self.username


class CourseRecord(models.Model):
    """
    上课记录表
    """
    course = models.ForeignKey(verbose_name="班级(课程)", to="ClassList")
    day_num = models.IntegerField(verbose_name="节次", help_text=u"此处填写第几节课或第几天课程...,必须为数字")
    teacher = models.ForeignKey(verbose_name="讲师", to='UserInfo')
    date = models.DateField(verbose_name="上课日期", auto_now_add=True)

    course_title = models.CharField(verbose_name='本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField(verbose_name='本节课程内容概要', blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField(verbose_name='本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField(verbose_name='作业描述', max_length=500, blank=True, null=True)
    exam = models.TextField(verbose_name='踩分点', max_length=300, blank=True, null=True)

    def __str__(self):
        name = '{0}{1}期'.format(self.course.course.name, self.course.semester)
        return '{name} 第{day_num}天 - {title}'.format(name=name, day_num=self.day_num, title=self.course_title)


class StudyRecord(models.Model):
    course_record = models.ForeignKey(verbose_name="第几天课程", to="CourseRecord")
    student = models.ForeignKey(verbose_name="学员", to='Student')
    record_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('noshow', "缺勤"),
                      ('leave_early', "早退"),
                      )
    record = models.CharField("上课纪录", choices=record_choices, default="checked", max_length=64)
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (70, 'B-'),
                     (60, 'C+'),
                     (50, 'C'),
                     (40, 'C-'),
                     (0, ' D'),
                     (-1, 'N/A'),
                     (-100, 'COPY'),
                     (-1000, 'FAIL'),
                     )
    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(verbose_name='作业评语', max_length=255,blank=True, null=True)
    note = models.CharField(verbose_name="备注", max_length=255, blank=True, null=True)

    homework = models.FileField(verbose_name='作业文件', blank=True, null=True, default=None)
    stu_memo = models.TextField(verbose_name='学员备注', blank=True, null=True)
    date = models.DateTimeField(verbose_name='提交作业日期', auto_now_add=True)


class Survery(models.Model):
    """
    问卷
    """
    name = models.CharField(verbose_name="调查问卷名称", max_length=128, unique=True)
    by_class = models.ForeignKey(ClassList, verbose_name=u"问卷调查班级")
    date = models.DateTimeField(auto_now_add=True, verbose_name=u"问卷创建日期")


class SurveryItem(models.Model):
    """
    问卷选项
    """
    survery = models.ForeignKey(verbose_name='问卷', to='Survery')
    name = models.CharField(u"调查问题", max_length=255, help_text=u"此处填写需要调查的问题...")
    date = models.DateField(auto_now_add=True)
    answer_type_choices = (('single', "单选"),
                           ('score', "打分"),
                           ('suggestion', "建议"),
                           )
    answer_type = models.CharField(u"问题类型", choices=answer_type_choices, default='score', max_length=32)


class SurveryChoices(models.Model):
    """
    问卷选项答案
    """
    question = models.ForeignKey(SurveryItem, verbose_name='问题')
    content = models.CharField(verbose_name='答案内容', max_length=256)
    points = models.IntegerField(verbose_name='分值', )


class SurveryRecord(models.Model):
    """
    问卷记录
    """
    survery = models.ForeignKey(Survery, verbose_name="问卷")
    student_name = models.ForeignKey(verbose_name="学员姓名", to="Student")
    survery_item = models.ForeignKey(verbose_name="调查项", to='SurveryItem')

    score = models.IntegerField(verbose_name="评分", blank=True, null=True)
    single = models.ForeignKey(verbose_name='单选', to='SurveryChoices', blank=True, null=True)

    suggestion = models.TextField(verbose_name="建议", max_length=1024, blank=True, null=True)

    date = models.DateTimeField(verbose_name="答题日期", auto_now_add=True)


class MeetingRome(models.Model):
    """
    会议室
    """
    title = models.CharField(max_length=64, verbose_name='会议室名称')


class Booking(models.Model):
    """
    会议室预定
    """
    room = models.ForeignKey(verbose_name='会议室', to='MeetingRome')
    user = models.ForeignKey(verbose_name='预订者', to='UserInfo')
    title = models.CharField(max_length=64, verbose_name='会议主题')

    start = models.DateTimeField(verbose_name='开始时间')
    end = models.DateTimeField(verbose_name='结束时间')
