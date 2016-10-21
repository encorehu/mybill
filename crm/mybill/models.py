# -*- coding=utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.

ACCOUNT_TYPE=(
	(1, u'现金'), #资产Cash
	(2, u'存款'), #资产Bank
	(3, u'负债'), #应付债务
    (4, u'权益'), #应收债权, 报销款
)

class Account(models.Model):
	number = models.CharField(max_length=20)
	account_type = models.CharField(max_length=10, null=True, blank=True, default='')
	name = models.CharField(max_length=20, null=True, blank=True, default='')
	display_name = models.CharField(max_length=20, null=True, blank=True, default='')

	class Meta:
		verbose_name = u'科目（账户）'
		verbose_name_plural =u'科目（账户）'
		ordering = ('number', 'id')


	def __str__(self):
		return self.__unicode__().encode('utf-8')

	def __unicode__(self):
		return u'({0}){1}'.format(self.number, self.name)

TX_TYPE=(
	(1, u'收入'),
	(0, u'支出')
)

class AccountCategory(models.Model):
	account	= models.ForeignKey(Account, null=True, blank=True, default=None, related_name='category_account_set')
	name =  models.CharField(max_length=255, blank=True)
	display_name = models.CharField(max_length=255, null=True, blank=True, default=u'')
	parent = models.ForeignKey('self', null=True, blank=True, related_name='child_category_set')
	tx_type =  models.IntegerField(u'收支类型', default=0, choices=TX_TYPE)
	class Meta:
		verbose_name = u'收支分类'
		verbose_name_plural =u'收支分类'
		ordering = ('account', )

	def __str__(self):
		return self.__unicode__().encode('utf-8')

	def __unicode__(self):
		return u'{0}: {1}: {2}'.format(self.account, self.get_tx_type_display(), self.name)

class AccountItem(models.Model):
	account = models.ForeignKey(Account, related_name='account_set')
	title =  models.CharField(max_length=255, null=True, blank=True, default=u'')
	summary =  models.CharField(max_length=255, null=True, blank=True, default=u'餐费')
	category =  models.ForeignKey(AccountCategory, related_name='account_category_item_set', null=True)
	category_verbosename =  models.CharField(max_length=255, null=True, blank=True, default=u'')
	#debit =   models.DecimalField(u'收入', max_digits=10, decimal_places=2, default=0.00)
	#credit =   models.DecimalField(u'支出', max_digits=10, decimal_places=2, default=0.00)
	#balance =   models.DecimalField(u'余额', max_digits=10, decimal_places=2, default=0.00)
	receipt =  models.CharField(u'票据号码', max_length=32, null=True, blank=True, default=u'')
	amount =   models.DecimalField(u'金额', max_digits=10, decimal_places=2, default=0.00)
	tx_date =  models.DateTimeField(u'交易日期', default=timezone.now)
	tx_type =  models.IntegerField(u'收支类型', default=0, choices=TX_TYPE)
	adding_type =  models.IntegerField(default=0, editable=False)
	adding_type_name =  models.CharField(max_length=20, default='manual', editable=False) #手工还是系统操作
	operator =  models.CharField(max_length=20, default='hcz', editable=False)
	transaction_id =  models.IntegerField(default=0, editable=False)
	class Meta:
		verbose_name = u'记账条目'
		verbose_name_plural =u'记账条目'
		ordering = ('tx_date', 'id')

	def __str__(self):
		return self.__unicode__().encode('utf-8')

	def __unicode__(self):
		if self.tx_type==1:
			return u'{0},{1},收入:{2}'.format(self.account, self.summary, self.amount)
		else:
			return u'{0},{1},支出:{2}'.format(self.account, self.summary, self.amount)
