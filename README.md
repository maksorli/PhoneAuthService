# PhoneAuthService
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python)![Django](https://img.shields.io/badge/Django-5.1.3-green)![DRF](https://img.shields.io/badge/DRF-3.15%2B-red?logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-20.10-blue?style=flat&logo=docker)![Nginx Status](https://img.shields.io/badge/Nginx-active-brightgreen?logo=nginx&logoColor=white)![Gunicorn Status](https://img.shields.io/badge/Gunicorn-active-brightgreen?logo=gunicorn&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue?logo=postgresql&logoColor=white)

### PhoneAuthService — это REST API сервис для аутентификации пользователей по номеру телефона с использованием проверочных кодов (OTP) и системы инвайт-кодов. Проект разработан на фреймворке Django REST Framework и развернут с использованием Docker и Docker Compose.

### Функциональные возможности
Отправка кода подтверждения на указанный номер телефона.
- Проверка кода подтверждения и выдача токена аутентификации.
- Получение профиля пользователя, включая информацию об инвайт-кодах.
- Активация инвайт-кода, предоставленного другим пользователем.
- Система рефералов, позволяющая отслеживать приглашенных пользователей.


 ## Установка и запуск
С использованием Docker
1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/maksorli/PhoneAuthService.git
2. Проверьте версию Docker и Docker Compose, либо установите:
    ```bash
    docker --version
    docker-compose --version

3. Запустите проект с помощью Docker Compose:
   ```bash
   docker-compose up --build

### API Эндпоинты
#### 1. Отправка кода подтверждения
URL: /api/send-code/
Метод: POST
Описание: Отправляет код подтверждения на указанный номер телефона.

Пример запроса:


    {
    "phone_number": "71234567890"
    }
Пример ответа:


    {
    "detail": "Код отправлен",
    "auth_code": "1234"
    }

Примечание: В ответе auth_code возвращается только в режиме разработки для целей тестирования.

#### 2. Проверка кода подтверждения
URL: /api/verify-code/
Метод: POST
Описание: Проверяет код подтверждения и выдает токен аутентификации.
Пример запроса:


    {
    "phone_number": "71234567890",
    "code": "1234"
    }
Пример ответа:


    {
    "token": "your_auth_token",
    "invite_code": "ABC123"
    }

#### 3. Получение профиля пользователя
URL: /api/profile/
Метод: GET
Требуется аутентификация:  (Token Authentication)
Описание: Возвращает информацию о пользователе, включая инвайт-код и список приглашенных пользователей.
Пример ответа:


    {
    "phone_number": "71234567890",
    "invite_code": "ABC123",
    "activated_invite_code": "XYZ789",
    "invited_users": ["79876543210", "79765432109"],
    "inviter": "79876543210"
    }

#### 4. Активация инвайт-кода
URL: /api/activate-invite/
Метод: POST
Требуется аутентификация: Да (Token Authentication)
Описание: Активирует инвайт-код, предоставленный другим пользователем.
Пример запроса:

    {
    "invite_code": "XYZ789"
    }
Пример ответа:


    {
    "detail": "Инвайт-код успешно активирован"
    }

### Безопасность
В данном проекте используется тестовое окружение.
