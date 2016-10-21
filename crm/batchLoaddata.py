from models import *
import datetime
from decimal import Decimal

txt=open('data.txt','r').read().decode('gb18030')
# specify the account
account, created = MybillAccount.get_or_create(id=1, number='0011')

#
# each line 7 column
# created_at, category, title, summary, income, outcome, txtype(in or out)
# split by tab key
#

for line in txt.split('\n'):
    #line =  line.strip()
    data=map(lambda s:s.strip(), line.split('\t'))
    created_at, category, title, summary, income, outcome, txtype=(None,)*7

    if len(data)==7:
        created_at, category, title, summary, income, outcome, txtype=data
    else:
        print line
        print repr(line)
        print 'unrecognize'
        continue

    if created_at:
        created_at=datetime.datetime.strptime(created_at,'%Y-%m-%d')
    else:
        print line
        print repr(line)
        print 'created_at is empty'
        break

    if income and outcome:
        print line
        print repr(line)
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
             title=title,
             amount=amount,
             summary=summary,
             transaction=0,
             )

    #print kwargs
    MybillAccountitem.create(**kwargs)
