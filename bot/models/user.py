from peewee import Model, SqliteDatabase, CharField, TextField, ForeignKeyField, DateTimeField

db = SqliteDatabase('bot.db')

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = CharField(unique=True)
    username = CharField(null=True)

    class Meta:
        database = db
        table_name = 'users'  # Явное указание имени таблицы

class History(BaseModel):
    user = ForeignKeyField(User, backref='history')
    command = CharField()
    result = TextField()
    timestamp = DateTimeField()  # Исправлено с CharField на DateTimeField

    class Meta:
        table_name = 'history'

# Создаем таблицы при первом запуске
db.connect()
db.create_tables([User, History], safe=True)
db.close()
