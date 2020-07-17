from pathlib import Path
from glob import glob
import json
import hashlib
import telebot
from database import config
from database import Question as DBQ
from time import time


class Question:
    filepath = None
    short_filepath = None
    title = None
    is_anonymous = True
    options = []
    q_type = "quiz"
    correct_option_id = None
    explanation = ""
    checksum = None
    is_code = False
    image = ''
    code = ''

    def __init__(self, filepath):
        self.filepath = filepath
        self.question_file = open(filepath, 'r')
        self.file_content = self.question_file.read().strip()
        self.load_from_json()
        self.question_file.close()

    def load_from_json(self):
        structure = json.loads(self.file_content)
        self.short_filepath = '/'.join(self.filepath.split('/')[-2:])
        self.title = structure['title']
        self.options = structure['options']
        self.correct_option_id = structure['correct_option_id']
        self.explanation = structure['explanation']
        self.checksum = hashlib.md5(f"{self.short_filepath}{self.file_content}".encode()).hexdigest()


class QuestionWithCode(Question):

    def load_from_json(self):
        super().load_from_json()
        self.is_code = True


class Quiz:
    def __init__(self):
        self.simple_questions = Path.cwd() / "questions"
        self.questions_with_code = Path.cwd() / "coding"
        self.telebot = telebot.TeleBot(config.get('telegram', 'token'))
        self.chat_id = config.get('telegram', 'chat_id')

    def check_for_new_quiz(self):
        return self.check_for_simple_quiz()

    def check_for_simple_quiz(self):
        result = []
        for filepath in glob(str(self.simple_questions / "*.json")):
            result.append(Question(filepath))

        return result

    def publish(self, question):
        messages_id = []

        if not question.is_code:
            post = self.telebot.send_poll(
                chat_id=self.chat_id,
                question=question.title,
                is_anonymous=question.is_anonymous,
                options=question.options,
                type=question.q_type,
                correct_option_id=question.correct_option_id,
                explanation=question.explanation
            )

            messages_id.append(str(post.message_id))

        DBQ.create(**{
            'title': question.title,
            'last_checksum': question.checksum,
            'json_file': question.short_filepath,
            'message_id': ','.join(messages_id),
            'created_on': int(time())
        })

    def delete_messages(self, messages):
        for message_id in messages.split(','):
            message_id = message_id.strip()
            self.telebot.delete_message(self.chat_id, message_id=message_id)