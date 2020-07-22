from peewee import SqliteDatabase, Model
from peewee import IntegerField, CharField, PrimaryKeyField, TimestampField
from pathlib import Path
import toml


config = toml.load("config.toml")
db = SqliteDatabase(Path.cwd() / config.get('database').get('file'))


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
    image = CharField(null=True)
    # ID сообщения в Telegram (если вопрос с кодом, то публикации будут две через запятую)
    message_id = CharField(null=True)
    created_on = TimestampField()

    class Meta:
        db_table = 'questions'


db.connect()
if not Question.table_exists():
    Question.create_table()
