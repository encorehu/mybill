# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0005_accountitem_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('display_name', models.CharField(default='', max_length=255, null=True, blank=True)),
                ('tx_type', models.IntegerField(default=0, verbose_name='\u6536\u652f\u7c7b\u578b', choices=[(1, '\u6536\u5165'), (0, '\u652f\u51fa')])),
                ('parent', models.ForeignKey(related_name='child_category_set', blank=True, to='mybill.AccountCategory', null=True)),
            ],
            options={
                'verbose_name': '\u6536\u652f\u5206\u7c7b',
                'verbose_name_plural': '\u6536\u652f\u5206\u7c7b',
            },
        ),
        migrations.AlterModelOptions(
            name='accountitem',
            options={'ordering': ('tx_date', 'id'), 'verbose_name': '\u8bb0\u8d26\u6761\u76ee', 'verbose_name_plural': '\u8bb0\u8d26\u6761\u76ee'},
        ),
    ]
