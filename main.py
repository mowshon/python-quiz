from quiz import Quiz
from database import Question as DBQ


if __name__ == '__main__':
    quiz = Quiz()

    for q in quiz.get_all_quiz():
        qdb = DBQ.get_or_none(DBQ.json_file == q.short_filepath)

        if qdb is None:
            quiz.publish(q)
        else:
            if q.checksum != qdb.last_checksum:
                # Удаляем сообщения из канала
                quiz.delete_messages(qdb.message_id)
                # Удаляем запись из БД
                qdb.delete_instance()
                quiz.publish(q)