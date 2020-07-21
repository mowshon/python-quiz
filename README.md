# Собеседование у Гвидо ван Россума
Источник вопросов и задач для канала "Собеседование у Гвидо ван Россума" https://t.me/ask_guido

# Как добавить свой вопрос?
На данный момент, вопрос можно создать только через pull-request.

### Вопросы разделены на две папки:
* https://github.com/mowshon/python-quiz/tree/master/questions - Обычные опросы с вариантами для ответа;
    - **nazvanie-dlea-oprosa.json** - Название файла должно быть уникальным и в транслите.
* https://github.com/mowshon/python-quiz/tree/master/coding - Тут содержаться папки с опросами вместе с кодом.
    - **question.json** - Структура опроса;
    - **code.py** - Пример кода (всегда использовать данное имя файла в папке вопроса).

### Структура question.json
```json
{
  "title": "Какой результат выведет функция calculate?",
  "options": [
    "20", "Вернет ошибку", "True", "30"
  ],
  "correct_option_id": 3,
  "explanation": "Небольшая аргументация для правильного ответа.",
  "language": "python",
  "start_comment_with": "#"
}
```

- **title** - заголовок вопроса;
- **options** - список вариантов для ответа;
- **correct_option_id** - аргументация правильного ответа;
- **language** - язык программирования (python, go, php, etc.);
- **start_comment_with** - начало комментария в коде в зависимости от языка программирования (для Python это #, для C++ это //).


### Файл конфигурации config.ini
```ini
[database]
file = quiz.db

[telegram]
token = ENTER-HERE
chat_id = -100

[highlight]
code_bg = #243036
img_bg = #5b81e3
show_line_numbers = 1
shadow_dt = 1
shadow_color = #111111
start_comment_with = #
```