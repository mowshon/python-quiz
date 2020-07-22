from pathlib import Path
from glob import glob
import json
import hashlib
import telebot
from database import config
from database import Question as DBQ
from time import time
import os
from highlight import Highlight


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
    short_code_filepath = None
    start_comment_with = ''
    show_title_in_code = False
    language = 'python'

    def __init__(self, question_filepath, code_filepath):
        self.code_filepath = code_filepath
        self.short_code_filepath = '/'.join(self.code_filepath.split('/')[-2:])
        super().__init__(question_filepath)

        # Символ с которого нужно начинать комментарий
        if 'start_comment_with' in self.structure.keys():
            self.start_comment_with = self.structure['start_comment_with']
        else:
            self.start_comment_with = config.get('highlight').get('start_comment_with')

        # Добавить заголовок вопроса в качестве первого комментария над кодом?
        if 'show_title_in_code' in self.structure.keys():
            self.show_title_in_code = self.structure['show_title_in_code']
        else:
            self.show_title_in_code = config.get('highlight').get('show_title_in_code')

        # Язык программирования
        if 'language' in self.structure.keys():
            self.language = self.structure['language']
        else:
            self.language = config.get('highlight').get('language')

        self.code = self.load_code(code_filepath)
        self.checksum = hashlib.md5(f"{self.short_filepath}{self.file_content}{self.code}".encode()).hexdigest()

    def load_from_json(self):
        super().load_from_json()
        self.is_code = True

    @staticmethod
    def load_code(code_filepath):
        with open(code_filepath) as f:
            code = f.readlines()

        return code

    def code_highlight(self):
        """
        Стилизуем код из файла.
        :return: Изображение в бинарном виде.
        """
        code2image = Highlight(
            self.language,
            style=config.get('highlight').get('style'),
            line_numbers=config.get('highlight').get('show_line_numbers'),
            font_size=config.get('highlight').get('font_size'),
            font_name=config.get('highlight').get('font_name'),
            line_pad=config.get('highlight').get('line_pad'),
            background_color=config.get('highlight').get('background_color'),
            highlight_color=config.get('highlight').get('highlight_color'),
            window_frame_color=config.get('highlight').get('window_frame_color'),
            bg_from_color=tuple(config.get('highlight').get('bg_from_color')),
            bg_to_color=tuple(config.get('highlight').get('bg_to_color')),
            close_circle=config.get('highlight').get('close_circle'),
            maximize_circle=config.get('highlight').get('maximize_circle'),
            minimize_circle=config.get('highlight').get('minimize_circle')
        )

        image = code2image.to_macos_frame(
            code2image.prepare_code(
                self.code,
                fake_line_numbers=config.get('highlight').get('show_fake_line_numbers'),
                show_title_in_code=self.show_title_in_code,
                title=self.title,
                comment_char=self.start_comment_with
            )
        )

        return code2image.to_bytes(image)


class Quiz:
    def __init__(self):
        self.simple_questions = Path.cwd() / "questions"
        self.questions_with_code = Path.cwd() / "coding"
        self.telebot = telebot.TeleBot(config.get('telegram').get('token'))
        self.chat_id = config.get('telegram').get('chat_id')

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

        edit_question_html = self.edit_this_question(question)

        if question.is_code:
            """
            Для вопроса с кодом, мы отправим две сообщения, одну с изображением кода другую с опросом.
            """
            send_image = self.telebot.send_photo(
                chat_id=self.chat_id,
                photo=question.code_highlight(),
                caption=f'{question.title}\n\n{edit_question_html}',
                parse_mode='html'
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

        if not question.is_code:
            edit = self.telebot.send_message(
                chat_id=self.chat_id, text=edit_question_html, parse_mode='html', disable_web_page_preview=True
            )
            messages_id.append(str(edit.message_id))

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

    @staticmethod
    def edit_this_question(question):
        github = config.get('telegram').get('github')
        if question.is_code:
            edit_question = f'{github}/tree/master/coding/{question.short_filepath}'
            edit_code = f'{github}/tree/master/coding/{question.short_code_filepath}'
            return f'<b>Заметили ошибку? Редактировать:</b> <a href="{edit_question}">вопрос</a> '\
                   f'или <a href="{edit_code}">код</a>'
        else:
            edit_question = f'{github}/tree/master/{question.short_filepath}'
            return f'👆 <b>Заметили ошибку?</b> <a href="{edit_question}">Редактировать вопрос</a>'
