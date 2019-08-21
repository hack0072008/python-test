# Generated by Django 2.2.3 on 2019-08-19 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_classlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlist',
            name='tech_teachers',
            field=models.ManyToManyField(blank=True, limit_choices_to={'depart__title__in': ['python部']}, related_name='teach_classes', to='web.UserInfo', verbose_name='任课老师'),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('qq', models.CharField(help_text='QQ号/微信/手机号', max_length=64, unique=True, verbose_name='联系方式')),
                ('status', models.IntegerField(choices=[(1, '已报名'), (2, '未报名')], default=2, verbose_name='状态')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('source', models.SmallIntegerField(choices=[(1, 'qq群'), (2, '内部转介绍'), (3, '官方网站'), (4, '百度推广'), (5, '360推广'), (6, '搜狗推广'), (7, '腾讯课堂'), (8, '广点通'), (9, '高校宣讲'), (10, '渠道代理'), (11, '51cto'), (12, '智汇推'), (13, '网盟'), (14, 'DSP'), (15, 'SEO'), (16, '其它')], default=1, verbose_name='客户来源')),
                ('education', models.IntegerField(blank=True, choices=[(1, '重点大学'), (2, '普通本科'), (3, '独立院校'), (4, '民办本科'), (5, '大专'), (6, '民办专科'), (7, '高中'), (8, '其他')], null=True, verbose_name='学历')),
                ('graduation_school', models.CharField(blank=True, max_length=64, null=True, verbose_name='毕业学校')),
                ('major', models.CharField(blank=True, max_length=64, null=True, verbose_name='所学专业')),
                ('experience', models.IntegerField(blank=True, choices=[(1, '在校生'), (2, '应届毕业'), (3, '半年以内'), (4, '半年至一年'), (5, '一年至三年'), (6, '三年至五年'), (7, '五年以上')], null=True, verbose_name='工作经验')),
                ('work_status', models.IntegerField(blank=True, choices=[(1, '在职'), (2, '无业')], default=1, null=True, verbose_name='职业状态')),
                ('company', models.CharField(blank=True, max_length=64, null=True, verbose_name='目前就职公司')),
                ('salary', models.CharField(blank=True, max_length=64, null=True, verbose_name='当前薪资')),
                ('date', models.DateField(auto_now_add=True, verbose_name='咨询日期')),
                ('last_consult_date', models.DateField(auto_now_add=True, verbose_name='最后跟进日期')),
                ('consultant', models.ForeignKey(blank=True, limit_choices_to={'depart__title': '销售部'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultant', to='web.UserInfo', verbose_name='课程顾问')),
                ('course', models.ManyToManyField(to='web.Course', verbose_name='咨询课程')),
                ('referral_from', models.ForeignKey(blank=True, help_text='若此客户是转介绍自内部学员,请在此处选择内部学员姓名', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='internal_referral', to='web.Customer', verbose_name='转介绍自学员')),
            ],
        ),
    ]
