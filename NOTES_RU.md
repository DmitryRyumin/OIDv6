# Массовая загрузка набора данных Open Images Dataset V6

## 9 июня 2020 года

> `1.0.4` = `1.0.3`

<h4><span style="color:#DB534F;">Исправления</span></h4>

- Исправлены опечатки

> `1.0.3`

<h4><span style="color:#008000;">Что нового</span></h4>

- Добавлена поддержка английского языка (аргумент командной строки `en`)

<h4><span style="color:#247CB4;">Изменения</span></h4>

- Язык по умолчанию изменен с `русский` на `английский`

## 5 июня 2020 года

> `1.0.2`

<h4><span style="color:#DB534F;">Исправления</span></h4>

- Исправлены опечатки

> `1.0.1`

<h4><span style="color:#008000;">Что нового</span></h4>

- Добавлен [файл](https://github.com/DmitryRyumin/OIDv6/blob/master/oidv6/classes.txt) со списком всех классов, которые возможно загрузить

<h4><span style="color:#DB534F;">Исправления</span></h4>

- Исправлена ошибка в методе `download` класса [OIDv6](https://github.com/DmitryRyumin/OIDv6/blob/master/oidv6/OIDv6.py)

> `1.0.0`

<h4><span style="color:#008000;">Что нового</span></h4>

- Добавлена загрузка классов в одну директорию (флаг командной строки `--multi_classes`)
- Добавлен новый класс [Switch](https://github.com/DmitryRyumin/OIDv6/blob/master/oidv6/modules/core/switch.py)

<h4><span style="color:#247CB4;">Изменения</span></h4>

- Переработаны внутренние методы класса [OIDv6](https://github.com/DmitryRyumin/OIDv6/blob/master/oidv6/OIDv6.py) (возвращают код статуса ответа)

<h4><span style="color:#DB534F;">Исправления</span></h4>

- Исправлена ошибка в методе `_download_images` класса [OIDv6](https://github.com/DmitryRyumin/OIDv6/blob/master/oidv6/OIDv6.py)

## 2 июня 2020 года

> Первая версия пакета `1.0.0-rc7`
