# Generated by Django 2.2.3 on 2019-08-19 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20190819_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='跟进内容')),
                ('date', models.DateField(auto_now_add=True, verbose_name='跟进日期')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo', verbose_name='跟踪人')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Customer', verbose_name='所咨询客户')),
            ],
        ),
    ]
