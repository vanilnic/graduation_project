# HotelHaven Дипломный проект
Веб-приложение для учета и управления бронированием в сфере гостеприимства

## Функциональность
* регистрация и авторизация пользователей;
* поиск и фильтрация номеров; 
* сохранение/удаление отеля в «Избранное»;
* бронирование номера;
* просмотр истории поездок;
* написание отзыва.

## Стек технологий
- **Backend:** Django  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **База данных:** MySQL  

## Старт проекта
1) Клонирование репозитория
```bash
git clone https://github.com/vanilnic/graduation_project.git
cd Hotel
```
2) Создание и активация venv
```bash
python -m venv .venv
.venv\Scipts\Activate.ps1
```
3) Настройка settings.py
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'your_host',
        'PORT': 'your_port'
    }
}
```
4) Установка библиотек
```bash
pip install -r requirements.txt
```
5) Загрузка базы данных
* Запустить скрипт из файла DB.sql в MySQL Workbench
7) Запуск проекта
```bash
cd Hotel
python manage.py runserver
```
