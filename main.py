from quiz import Quiz
from database import Question as DBQ
from time import time


if __name__ == '__main__':
    quiz = Quiz()

    for q in quiz.check_for_new_quiz():
        qdb = DBQ.get_or_none(DBQ.json_file == q.short_filepath)

        if qdb is None:
            quiz.publish(q)
        else:
            if q.checksum != qdb.last_checksum:
                quiz.delete_messages(qdb.message_id)
                qdb.delete_instance()
                quiz.publish(q)