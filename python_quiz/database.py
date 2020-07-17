from pathlib import Path, PurePath

from peewee import SqliteDatabase, Model
from peewee import IntegerField, CharField, PrimaryKeyField, TimestampField

from config_reader import get_config

config: dict = get_config()

db_file_path = Path(config.get("app")['db_path']) / config.get("app")['db_filename']
db = SqliteDatabase(db_file_path)


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
