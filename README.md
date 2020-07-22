# Собеседование у Гвидо ван Россума
Источник вопросов и задач для канала "Собеседование у Гвидо ван Россума" https://t.me/ask_guido

![Preview](https://python-scripts.com/wp-content/uploads/2020/07/code-highlight.png)

# Как добавить свой вопрос?
На данный момент, вопрос можно создать только через pull-request.

### Вопросы разделены на две папки:
* https://github.com/mowshon/python-quiz/tree/master/questions - обычные опросы с вариантами для ответа;
    - **nazvanie-dlea-oprosa.json** - название файла должно быть уникальным и в транслите.
* https://github.com/mowshon/python-quiz/tree/master/coding - Тут содержаться папки с опросами вместе с кодом.
    - **question.json** - структура опроса;
    - **code.py** - пример кода (всегда использовать данное имя файла в папке вопроса).

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
- **correct_option_id** - id правильного ответа из списка (начало отсчета с 0 нуля);
- **explanation** - аргументация правильного ответа;
- **language** - язык программирования (python, go, php, etc.);
- **start_comment_with** - начало комментария в коде в зависимости от языка программирования (для Python это #, для C++ это //).


### Файл конфигурации config.toml
```toml
[database]
file = "quiz.db"

[telegram]
token = "1306699297:AAE_DWtRIagEpZDEyTggkOxw6UbyDywWbhQ"
chat_id = -1001399962208

[highlight]
background_color = ""
highlight_color = ""
show_line_numbers = true
show_fake_line_numbers = false
show_title_in_code = true
start_comment_with = "#"
font_size = 16
font_name = "Liberation Mono"
line_pad = 5
style = "manni"
language = "python"

window_frame_color = "#e2e1e3"
bg_from_color = [48, 113, 227]
bg_to_color = [27, 62, 122]
close_circle = "#fa4b4b"
maximize_circle = "#fab339"
minimize_circle = "#2fc242"
```
- **file** - файл базы данных SQLite;
- **token** - токен от телеграм бота;
- **chat_id** - ID чата где бот был добавлен;
- **background_color** - цвета фона для стиля от pygments;
- **highlight_color** - цвет ситаксиса для стиля от pygments;
- **show_line_numbers** - показать нумерацию строк кода (если строк в коде меньше чем 3, то данный параметр игнорируется и становится False, даже если он True);
- **show_fake_line_numbers** - вставляет нумерацию строк сразу в исходный код (желательно указать в **show_line_numbers** = false);
- **show_title_in_code** - вставить заголовок вопроса как первый комментарий в коде;
- **start_comment_with** - заголовок опроса (title) будет добавлен как первый комментарий над предоставленным кодом из code.py
- **font_size** - размер шрифта;
- **font_name** - название шрифта;
- **style** - название стиля для подсветки ситаксиса ([посмотреть все стили](https://github.com/pygments/pygments/tree/master/pygments/styles));
- **language** - язык программирования на котором написан код из примеров (python, php, go, java... [посмотреть все](https://github.com/pygments/pygments/tree/master/pygments/lexers));
- **window_frame_color** - цвет фона для рамки с кодом;
- **bg_from_color** - начальный цвет градиента фона для изображения на которой будет наложена изображение кода;
- **bg_to_color** - финальный цвет градиента фона для изображения на которой будет наложена изображение кода;
- **close_circle** - цвет фона иконки закрытия;
- **maximize_circle** - цвет фона иконки "развернуть";
- **minimize_circle** - цвет фона иконки "свернуть".