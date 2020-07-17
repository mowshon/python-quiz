from pathlib import Path
from glob import glob
import json
import hashlib


class Question:
    filepath = None
    short_filepath = None
    title = None
    is_anonymous = True
    options = []
    type = "quiz"
    correct_option_id = None
    explanation = ""
    checksum = None
    is_code = False
    image = ''
    code = ''

    def __init__(self, filepath):
        self.filepath = filepath
        self.question_file = open(filepath, 'r')
        self.load_from_json()
        self.question_file.close()

    def load_from_json(self):
        structure = json.loads(self.question_file.read())
        self.short_filepath = '/'.join(self.filepath.split('/')[-2:])
        self.title = structure['title']
        self.options = structure['options']
        self.correct_option_id = structure['correct_option_id']
        self.explanation = structure['explanation']
        self.checksum = hashlib.md5(f"{self.short_filepath}{self.question_file.read()}".encode()).hexdigest()


class QuestionWithCode(Question):

    def load_from_json(self):
        super().load_from_json()
        self.is_code = True


class Quiz:
    def __init__(self):
        self.simple_questions = Path.cwd() / "questions"
        self.questions_with_code = Path.cwd() / "coding"

    def check_for_new_quiz(self):
        return self.check_for_simple_quiz()

    def check_for_simple_quiz(self):
        result = []
        for filepath in glob(str(self.simple_questions / "*.json")):
            result.append(Question(filepath))

        return result
