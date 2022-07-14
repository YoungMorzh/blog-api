# Blog API

### Требования к системе.

- python3

```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10

```

- virtualenv

```bash
python3 -m pip install --user virtualenv
```

### Установка

В корневой директории выполнить:

```bash
chmod a+x install.sh
./ install.sh
chmod a+x run.sh
```

### Запуск.

```bash

./run.sh

```

### Api Documentation.

#### Авторизация.

Креды: user `admin`, password `password`

Все ресурсы защищены BasicAuth.

#### Модели.

##### Post

```
{
  "id": int,                    // Идентификационный номер поста.
  "author": str,                // автор поста.
  "title": str,                 // оглавление поста.
  "short_description": str,     // краткое описание поста.
  "content": str,               // контент поста.
}
```

##### Short_posts

```
{
    "author": str,                // автор поста.
    "title": str,                 // оглавление поста.
    "short_description": str,     // краткое описание поста.
}
```
##### Short_post

```
{
    "author": str,                // автор поста.
    "title": str,                 // оглавление поста.
    "content": str,               // контент поста.
}
```
#### Ресурсы.

##### Все посты.

URL: `http://localhost:5000/blog/api/v1.0/posts`

Method: `GET`

Response:

```
{
  "posts": [Short_posts]
}
```

##### Получение поста.

URl: `http://localhost:5000/blog/api/v1.0/tasks/<int:post_id>`

Method: `GET`

Response:

```
{
    "post": [Short_post]
}
```

Errors:

`404` Задача не найдена.

##### Добавление нового поста.

URL: `http://localhost:5000/blog/api/v1.0/posts`

Method: `POST`

Data:

```
{
  "author": str,                // автор поста, не пустая строка, обязательное поле.
  "title": str,                 // название поста, не пустая строка, обязательное поле.
  "short_description": str,     // краткое описание поста, не пустая строка , не обязательное поле.
  "content": str,               // контент статьи, не пустая строка, обязательное поле.
}
```

Response:

```
{
  "post": [post]  // добавленный пост.
}
```

Errors:

`400` - Невалидные данные.

##### Изменение поста.

URl: `http://localhost:5000/blog/api/v1.0/posts/<int:post_id>`

Method: `PUT`

Data:

```
{
  "author" str,             // изменённый автор поста, не пустая строка, обязательное поле.
  "title": str,             // изменённое оглавление поста, не пустая строка, обязательное поле.
  "short_description": str, // изменённое краткое описание, не обязательное поле.
  "content": str,           // изменённый контент поста, не пустая строка, обязательное поле.
}
```

Response:

```
{
    "post": [post]  // изменённый пост.
}
```

Errors:

`404` пост не найден.

`400` Невалидные данные.

##### Удаление поста.

URl: `http://localhost:5000/blog/api/v1.0/posts/<int:post_id>`

Method: `DELETE`

Response:

```
{
    "result": true
}
```

Errors:

`404` Пост не найден.