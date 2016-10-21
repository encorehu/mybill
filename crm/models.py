from peewee import *

database = SqliteDatabase('db.sqlite3', **{})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class AuthGroup(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'auth_group'

class DjangoContentType(BaseModel):
    app_label = CharField()
    model = CharField()

    class Meta:
        db_table = 'django_content_type'

class AuthPermission(BaseModel):
    codename = CharField()
    content_type = ForeignKeyField(db_column='content_type_id', rel_model=DjangoContentType, to_field='id')
    name = CharField()

    class Meta:
        db_table = 'auth_permission'

class AuthGroupPermissions(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')

    class Meta:
        db_table = 'auth_group_permissions'

class AuthUser(BaseModel):
    date_joined = DateTimeField()
    email = CharField()
    first_name = CharField()
    is_active = BooleanField()
    is_staff = BooleanField()
    is_superuser = BooleanField()
    last_login = DateTimeField(null=True)
    last_name = CharField()
    password = CharField()
    username = CharField(unique=True)

    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(BaseModel):
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_user_permissions'

class DjangoAdminLog(BaseModel):
    action_flag = IntegerField()
    action_time = DateTimeField()
    change_message = TextField()
    content_type = ForeignKeyField(db_column='content_type_id', null=True, rel_model=DjangoContentType, to_field='id')
    object = TextField(db_column='object_id', null=True)
    object_repr = CharField()
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'django_admin_log'

class DjangoMigrations(BaseModel):
    app = CharField()
    applied = DateTimeField()
    name = CharField()

    class Meta:
        db_table = 'django_migrations'

class DjangoSession(BaseModel):
    expire_date = DateTimeField(index=True)
    session_data = TextField()
    session_key = CharField(primary_key=True)

    class Meta:
        db_table = 'django_session'

class MybillAccount(BaseModel):
    account_type = CharField(null=True)
    display_name = CharField(null=True)
    name = CharField(null=True)
    number = CharField()

    class Meta:
        db_table = 'mybill_account'

class MybillAccountbook(BaseModel):
    balance = DecimalField()
    balance_cash = DecimalField()
    balance_deposit = DecimalField()
    name = CharField(null=True)

    class Meta:
        db_table = 'mybill_accountbook'

class MybillAccountcategory(BaseModel):
    account = ForeignKeyField(db_column='account_id', null=True, rel_model=MybillAccount, to_field='id')
    display_name = CharField(null=True)
    name = CharField()
    parent = ForeignKeyField(db_column='parent_id', null=True, rel_model='self', to_field='id')
    tx_type = IntegerField()

    class Meta:
        db_table = 'mybill_accountcategory'

class MybillAccountitem(BaseModel):
    account = ForeignKeyField(db_column='account_id', rel_model=MybillAccount, to_field='id')
    adding_type = IntegerField()
    adding_type_name = CharField()
    amount = DecimalField()
    category = ForeignKeyField(db_column='category_id', rel_model=MybillAccountcategory, to_field='id')
    category_verbosename = CharField(null=True)
    operator = CharField()
    receipt = CharField(null=True)
    summary = CharField(null=True)
    title = CharField(null=True)
    transaction = IntegerField(db_column='transaction_id')
    tx_date = DateTimeField()
    tx_type = IntegerField()

    class Meta:
        db_table = 'mybill_accountitem'

class MybillAccountitemdetail(BaseModel):
    accountitem = ForeignKeyField(db_column='accountitem_id', rel_model=MybillAccountitem, to_field='id')
    amount = DecimalField()
    operator = CharField()
    summary = CharField(null=True)
    tx_date = DateTimeField()
    tx_type = IntegerField()

    class Meta:
        db_table = 'mybill_accountitemdetail'

class MybillAccountstat(BaseModel):
    account = ForeignKeyField(db_column='account_id', null=True, rel_model=MybillAccount, to_field='id')
    amount = DecimalField()
    day = IntegerField()
    display_name = CharField(null=True)
    level = IntegerField()
    levelname = CharField()
    month = IntegerField()
    name = CharField()
    tx_type = IntegerField()
    year = IntegerField()

    class Meta:
        db_table = 'mybill_accountstat'

class MybillAccounttype(BaseModel):
    code = CharField()
    credit_symbol = CharField()
    debit_increase = BooleanField()
    debit_symbol = CharField()
    name = CharField()

    class Meta:
        db_table = 'mybill_accounttype'

class SqliteSequence(BaseModel):
    name = UnknownField(null=True)  # 
    seq = UnknownField(null=True)  # 

    class Meta:
        db_table = 'sqlite_sequence'

