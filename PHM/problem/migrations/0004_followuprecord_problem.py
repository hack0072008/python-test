# Generated by Django 2.2.3 on 2019-08-26 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0003_auto_20190826_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='followuprecord',
            name='problem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='follow_record_problem', to='problem.Problem', verbose_name='对应的问题'),
            preserve_default=False,
        ),
    ]
