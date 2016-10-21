from models import *
import datetime
from decimal import Decimal

txt=open('data.txt','r').read().decode('gb18030')
# specify the account
account, created = MybillAccount.get_or_create(id=1, number='')

#
# each line
# created_at, category, summary, income, outcome
# split by tab key
#

for line in txt.split('\n'):
    #line =  line.strip()
    data=line.split('\t')
    created_at, category, summary, income, outcome=(None,)*5

    if len(data)==4:
        created_at, category, summary, income=data
        outcome=0
    elif len(data)==5:
        created_at, category, summary, income, outcome=data
    if created_at:
        created_at=datetime.datetime.strptime(created_at,'%Y-%m-%d')
    else:
        print line
        print 'created_at is empty'
        break

    if income and outcome:
        print line
        print 'ERROR single record cannot have income and outcome value'
        break
    else:
        tx_type=1 if income else 0

    if category:
        category, created=MybillAccountcategory.get_or_create(account=account, name=category, tx_type=tx_type)
        #print category, tx_type, income, outcome
        pass
    else:
        print line
        print 'category is empty'
        break

    if income:
        income=Decimal(income)
    else:
        income=Decimal(0.0)

    if outcome:
        outcome=Decimal(outcome)
    else:
        outcome=Decimal(0.0)

    amount = income if income else outcome

    print created_at, category.name, summary.strip('"'), tx_type, amount
    summary=summary.strip('"')
    kwargs=dict(account=account,
             adding_type=1,
             adding_type_name='python',
             operator='hcz',
             tx_date=created_at,
             tx_type=tx_type,
             category=category,
             amount=amount,
             summary=summary,
             transaction=0,
             )

    #print kwargs
    MybillAccountitem.create(**kwargs)
