from peewee import SqliteDatabase, Model
from peewee import IntegerField, CharField, PrimaryKeyField, TimestampField
from pathlib import Path
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini", encoding="utf-8")

db = SqliteDatabase(Path.cwd() / config.get('database', 'file'))


class BaseModel(Model):
    class Meta:
        database = db


class Question(BaseModel):
    id = PrimaryKeyField(null=False)
    # Заголовок вопроса
    title = CharField()
    # Последний MD5 из содержимого вопроса и кода (если есть)
    last_checksum = CharField()
    # Путь к JSON файлу вопроса
    json_file = CharField()
    # Путь к сгенерированной изображении с кодом
    image = CharField()
    # ID сообщения в Telegram
    message_id = IntegerField()
    created_on = TimestampField()

    class Meta:
        db_table = 'questions'


db.connect()
if not Question.table_exists():
    Question.create_table()
