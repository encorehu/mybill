# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0020_auto_20161022_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('tx_date', models.DateTimeField(auto_now_add=True)),
                ('from_account', models.ForeignKey(related_name='from_account_set', to='mybill.Account')),
                ('from_category', models.ForeignKey(related_name='from_category_set', blank=True, to='mybill.AccountCategory', null=True)),
                ('from_item', models.ForeignKey(related_name='from_item_set', editable=False, to='mybill.AccountItem')),
                ('to_account', models.ForeignKey(related_name='to_account_set', to='mybill.Account')),
                ('to_category', models.ForeignKey(related_name='to_category_set', blank=True, to='mybill.AccountCategory', null=True)),
                ('to_item', models.ForeignKey(related_name='to_item_set', editable=False, to='mybill.AccountItem')),
            ],
            options={
                'verbose_name': '\u8f6c\u8d26\u6761\u76ee',
                'verbose_name_plural': '\u8f6c\u8d26\u6761\u76ee',
            },
        ),
    ]
