from pathlib import Path
from glob import glob
import json
import hashlib
import telebot
from database import config
from database import Question as DBQ
from time import time
import os
from code2image.cls import Code2ImageBackground
from io import BytesIO


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
    code = ''

    def __init__(self, filepath):
        self.filepath = filepath
        question_file = open(filepath, 'r')
        self.file_content = question_file.read().strip()
        self.structure = json.loads(self.file_content)
        self.load_from_json()
        question_file.close()

    def load_from_json(self):
        self.short_filepath = '/'.join(self.filepath.split('/')[-2:])
        self.title = self.structure['title']
        self.options = self.structure['options']
        self.correct_option_id = self.structure['correct_option_id']
        self.explanation = self.structure['explanation']
        self.checksum = hashlib.md5(f"{self.short_filepath}{self.file_content}".encode()).hexdigest()


class QuestionWithCode(Question):

    code_filepath = None

    def __init__(self, question_filepath, code_filepath):
        self.code_filepath = code_filepath
        super().__init__(question_filepath)
        self.code = self.load_code(code_filepath)
        self.checksum = hashlib.md5(f"{self.short_filepath}{self.file_content}{self.code}".encode()).hexdigest()

    def load_from_json(self):
        super().load_from_json()
        self.is_code = True

    @staticmethod
    def load_code(code_filepath):
        with open(code_filepath) as f:
            code = f.read()

        return code

    def code_highlight(self):
        """
        Стилизуем код из файла.
        :return: Изображение в бинарном виде.
        """
        c2i = Code2ImageBackground(
            code_bg=config.get('highlight', 'code_bg'),
            img_bg=config.get('highlight', 'img_bg'),
            shadow_dt=int(config.get('highlight', 'shadow_dt')),
            shadow_color=config.get('highlight', 'shadow_color'),
        )

        # Добавление нумерации строк
        if int(config.get('highlight', 'show_line_numbers')):
            content = self.add_line_number()
        else:
            content = self.code

        with BytesIO() as output:
            img = c2i.highlight(content)
            img.save(output, format='PNG')
            data = output.getvalue()

        return data

    def add_line_number(self) -> str:
        content = ''
        with open(self.code_filepath) as f:
            lines = f.readlines()

        total_numbers = len(str(len(lines)))
        for n, line in enumerate(lines, start=1):
            spaces = ' ' * (total_numbers - len(str(n)))
            content += f'{spaces}{n}| {line}'

        return content


class Quiz:
    def __init__(self):
        self.simple_questions = Path.cwd() / "questions"
        self.questions_with_code = Path.cwd() / "coding"
        self.telebot = telebot.TeleBot(config.get('telegram', 'token'))
        self.chat_id = config.get('telegram', 'chat_id')

    def get_all_quiz(self) -> list:
        """
        Получаем список всех вопросов которые есть.
        :return: Получаем список всех вопросов которые есть.
        """
        return self.checking_for_simple_quiz() + self.checking_for_quiz_with_code()

    def checking_for_simple_quiz(self) -> list:
        """
        Проверяем только обычные опросы из папки questions
        :return: Получаем список обычных опросов.
        """
        result = []
        for filepath in glob(str(self.simple_questions / "*.json")):
            result.append(Question(filepath))

        return result

    def checking_for_quiz_with_code(self) -> list:
        """
        Проверяем наличие опросов с кодом.
        :return: Список вопросов с примером кода.
        """
        result = []
        for folder in glob(str(self.questions_with_code / "*")):
            question_file = os.path.join(folder, 'question.json')
            file_with_code = glob(os.path.join(folder, 'code.*'))[0]

            if os.path.exists(question_file) and os.path.exists(file_with_code):
                result.append(QuestionWithCode(question_file, file_with_code))

        return result

    def publish(self, question) -> None:
        """
        Публикуем данные из объекта Question в Telegram и сохраняем запись в SQLite базу данных.
        :param question: объект Question или QuestionWithCode
        :return: None
        """
        # ID всех опубликованных сообщений в Telegram которые связаны с данным опросом.
        messages_id = []

        if question.is_code:
            """
            Для вопроса с кодом, мы отправим две сообщения, одну с изображением кода другую с опросом.
            """
            send_image = self.telebot.send_photo(
                chat_id=self.chat_id,
                photo=question.code_highlight(),
                caption=question.title
            )

            messages_id.append(str(send_image.message_id))

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
        """
        Если это был вопрос с кодом, тогда будут два ID сообщений т.к. первый ID это отправленное изображение
        второй ID сам опрос.
        :param messages: Строка с ID опубликованных сообщений из Telegram
        :return: void
        """
        for message_id in messages.split(','):
            message_id = message_id.strip()
            self.telebot.delete_message(self.chat_id, message_id=message_id)