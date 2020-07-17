from quiz import Quiz
from database import Question as DBQ
from time import time


if __name__ == '__main__':
    quiz = Quiz()

    for q in quiz.check_for_new_quiz():
        last_checksum = DBQ.get_or_none(DBQ.json_file == q.short_filepath)

        if last_checksum is None:
            print(f'Create: {q.title}')
            DBQ.create(**{
                'title': q.title,
                'last_checksum': q.checksum,
                'json_file': q.short_filepath,
                'created_on': int(time())
            })