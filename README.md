# Массовая загрузка набора данных Open Images Dataset V6

![PyPI](https://img.shields.io/pypi/v/oidv6)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oidv6)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/oidv6)
![PyPI - Status](https://img.shields.io/pypi/status/oidv6)
![PyPI - License](https://img.shields.io/pypi/l/oidv6)

## [История релизов](https://github.com/DmitryRyumin/pkgs/blob/master/oidv6/NOTES.md)

## Установка

```shell script
pip install oidv6
```

## Обновление

```shell script
pip install --upgrade oidv6
```

## Зависимости

| Пакеты | Минимальная версия | Текущая версия |
| ------ | ------------------ | -------------- |
`requests` | `2.23.0` | ![PyPI](https://img.shields.io/pypi/v/requests) |
`numpy` | `1.18.4` | ![PyPI](https://img.shields.io/pypi/v/numpy) |
`pandas` | `1.0.4` | ![PyPI](https://img.shields.io/pypi/v/pandas) |
`progressbar2` | `3.51.3` | ![PyPI](https://img.shields.io/pypi/v/progressbar2) |
`opencv-contrib-python` | `4.2.0.34` | ![PyPI](https://img.shields.io/pypi/v/opencv-contrib-python) |
`awscli` | `1.18.69` | ![PyPI](https://img.shields.io/pypi/v/awscli) |

## [Класс для массовой загрузки набора данных Open Images Dataset V6 (OIDv6)](https://github.com/DmitryRyumin/OIDv6/blob/master/oidv6/OIDv6.py)

### Аргументы командной строки

| Аргумент | Тип | Описание | Допустимые значения |
| -------------------------- | ---  | -------- | ------------------- |
| command | str | Команда загрузки | `downloader` |
| --dataset | str | Корневая директория для сохранения OIDv6 | - |
| --type_data | str | Набор данных | `train`<br>`validation`<br>`test`<br>`all` |
| --classes | str | Последовательность названий классов или текстовый файл | - |
| --multi_classes | bool | Загрузка классов в одну директорию | Без значений |
| --limit | int | Лимит загрузки изображений | От `0` (нет лимита) до `\221E` |
| --yes | bool | Автоматическая загрузка служебных файлов | Без значений |
| --no_labels | bool | Автоматическая загрузка служебных файлов | Без значений |
| --hide_metadata | bool | Вывод метаданных | Без значений |
| --no_clear_shell | bool | Не очищать консоль перед выполнением | Без значений |

<h4 align="center"><span style="color:#EC256F;">Примеры</span></h4>

##### В разработке ...