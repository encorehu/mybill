# -*- coding=utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.
class Account(models.Model):
	number = models.CharField(max_length=20)
	account_type = models.CharField(max_length=10, null=True, blank=True)
	name = models.CharField(max_length=20, null=True, blank=True)
	display_name = models.CharField(max_length=20, null=True, blank=True)

	class Meta:
		verbose_name = u'科目（账户）'
		verbose_name_plural =u'科目（账户）'


	def __str__(self):
		return self.__unicode__().encode('utf-8')

	def __unicode__(self):
		return u'{0}({1})'.format(self.name, self.number)

class AccountItem(models.Model):
	account = models.ForeignKey(Account, related_name='account_set')
	title =  models.CharField(max_length=255, null=True, blank=True, default=u'')
	summary =  models.CharField(max_length=255, null=True, blank=True, default=u'餐费')
	#debit =   models.DecimalField(u'收入', max_digits=10, decimal_places=2, default=0.00)
	#credit =   models.DecimalField(u'支出', max_digits=10, decimal_places=2, default=0.00)
	#balance =   models.DecimalField(u'余额', max_digits=10, decimal_places=2, default=0.00)
	tx_date =  models.DateTimeField(u'交易日期', default=timezone.now)
	adding_type =  models.IntegerField(default=0, editable=False)
	adding_type_name =  models.CharField(max_length=20, default='manual', editable=False)
	operator =  models.CharField(max_length=20, default='hcz', editable=False)
	transaction_id =  models.IntegerField(default=0, editable=False)
	class Meta:
		verbose_name = u'记账条目'
		verbose_name_plural =u'记账条目'
		ordering = ('tx_date', )

	def __str__(self):
		return self.__unicode__().encode('utf-8')

	def __unicode__(self):
		return u'{0},{1},收入:{2}, 支出:{3}'.format(self.account, self.summary, self.debit, self.credit)
