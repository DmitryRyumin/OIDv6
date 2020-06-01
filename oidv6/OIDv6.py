#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Массовая загрузка набора данных Open Images Dataset V6
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import os  # Взаимодействие с файловой системой
import requests  # Отправка HTTP запросов
import numpy as np  # Научные вычисления
import pandas as pd  # Обработка и анализ данных
import progressbar
import cv2  # Алгоритмы компьютерного зрения

from multiprocessing.dummy import Pool as ThreadPool  # Распараллелирование
from datetime import datetime  # Взаимодействие со временем
from pathlib import Path  # Работа с путями в файловой системе

# Персональные
from oidv6.modules.core import config as cfg  # Глобальный файл настроек
from oidv6.modules.trml.shell import Shell  # Работа с Shell


# ######################################################################################################################
# Сообщения
# ######################################################################################################################
class Messages(cfg.Messages):
    """Класс для сообщений"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._args_empty = '[{}{}{}] Словарь аргументов командной строки пуст ...'
        self._check_args_valid = '[{}] Проверка аргументов командной строки на валидность ...'
        self._create_dirs = '[{}] Создание каталогов для служебных файлов ...'
        self._download = '[{}] Загрузка "{}" ...'
        self._extract = '    Извлечение данных из "{}" ...'
        self._index_error = '    {}Категория "{}" не найдена, пропуск ... {}'
        self._missing_file = '    Отсутствует файл "{}" ...'
        self._automatic_download = '        Автоматическая загрузка ... '
        self._input = '        Скачать отсутствующий файл? [Y/n] '
        self._input_error = '        {}Скачать отсутствующий файл? [Y/n]{} '
        self._cancel_download = '[{}{}{}] Отмена загрузки ...'
        self._url_error = '        [{}{}{}] Не удалось скачать файл (ошибка {}) ...'
        self._already_downloaded = '        Все изображений были загружены ранее ...'
        self._all_images_in_class = '    Всего "{}" изображений {} ...'
        self._limit = ' из них будет скачано {} ...'
        self._labels = '    Формирование меток ... '
        self._photo_not_read = '        {}Изображение "{}" повреждено ...{}'
        self._headers = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                        'Chrome/83.0.4103.61 Safari/537.36'
        self._in_developing = '[{}{}{}] {} в разработке ...'


# ######################################################################################################################
# Воспроизведение фото/видео данных
# ######################################################################################################################
class OIDv6(Messages):
    """Класс для массовой загрузки набора данных Open Images Dataset V6"""

    # ------------------------------------------------------------------------------------------------------------------
    # Конструктор
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()  # Выполнение конструктора из суперкласса

        self._args = None  # Аргументы командной строки

        # Пути к набору данных Open Images Dataset разных версий
        self._oid_url = {
            'v5': 'https://storage.googleapis.com/openimages/v5/',
            'v6': 'https://storage.googleapis.com/openimages/v6/'
        }

        self._dir = 'OIDv6'  # Корневая директория по умолчанию
        self._commands = ['downloader']  # Команды
        # Подвыборка набора данных
        self._type_data = {
            'train': {
                'bbox': 'oidv6-train-annotations-bbox.csv',
                'url': self._oid_url['v6'],
                'df': None  # Таблица с подвыборкой из набора данных
            },
            'validation': {
                'bbox': 'validation-annotations-bbox.csv',
                'url': self._oid_url['v5'],
                'df': None
            },
            'test': {
                'bbox': 'test-annotations-bbox.csv',
                'url': self._oid_url['v5'],
                'df': None
            },
        }
        self._boxes = 'boxes'  # Директория для файлов с информацией
        self._metadata = 'metadata'  # Директория для метаданных
        self._lbls = 'labels'  # Директория для меток
        self._name_file_classes = 'class-descriptions-boxable.csv'  # Файл с названиями классов
        self._chunk_size = 512  # Размер загрузки за 1 шаг
        self._download_file_classes = 'y'  # Загрузка файлов CSV
        self._df_classes = None  # Таблица с названиями классов

        self._ext = '.jpg'  # Расширение изображений

    # ------------------------------------------------------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------------------------------------------------------

    # Получение команд
    @property
    def commands(self):
        return self._commands

    # Получение подвыборки набора данных
    @property
    def type_data(self):
        return self._type_data

    # Получение корневой директория по умолчанию
    @property
    def dir(self):
        return self._dir

    # ------------------------------------------------------------------------------------------------------------------
    # Внутренние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Проверка аргументов командной строки на валидность
    def _valid_args(self, args, out = True):
        """
        Проверка аргументов командной строки на валидность

        (dict [, bool]) -> bool

        Аргументы:
           args - Словарь из аргументов командной строки
           out  - Печатать процесс выполнения

        Возвращает: True если аргументы валидны, в обратном случае False
        """

        # Проверка аргументов
        if type(args) is not dict or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self._valid_args.__name__
                ))

            return False

        # Словарь аргументов командной строки пуст
        if len(args) == 0:
            # Вывод сообщения
            if out is True:
                print(self._args_empty.format(self.red, datetime.now().strftime(self._format_time), self.end))

            return False

        # Вывод сообщения
        if out is True:
            print(self._check_args_valid.format(datetime.now().strftime(self._format_time)))

        all_layer = 5  # Общее количество аргументов
        curr_valid_layer = 0  # Валидное количество аргументов

        # Проход по всем разделам конфигурационного файла
        for key, val in args.items():
            if key == 'command':
                # Проверка значения
                if type(val) is not str or not val:
                    continue

                if val == 'downloader' or val == 'visualizer':
                    curr_valid_layer += 1

            if key == 'dataset':
                # Проверка значения
                if type(val) is not str or not val:
                    continue

                curr_valid_layer += 1

            if key == 'type_data':
                # Проверка значения
                if type(val) is not str or not val:
                    continue

                if val == 'train' or val == 'test' or val == 'validation' or val == 'all':
                    curr_valid_layer += 1

            if key == 'classes':
                # Проверка значения
                if type(val) is not list or not val:
                    continue

                # Текстовый файл
                if val[0].endswith('.txt'):
                    if os.path.isfile(val[0]) is False or os.stat((val[0])).st_size == 0:
                        continue

                    # Чтение файла
                    with open(val[0], encoding = 'utf-8') as f:
                        args['classes'] = [x.strip().replace(' ', '_') for x in f.readlines()]  # Формирование списка

                if len(list(filter(None, args['classes']))) == 0:
                    continue

                args['classes'] = [x.lower() for x in args['classes']]  # Формирование списка

                curr_valid_layer += 1

            if key == 'limit':
                # Проверка значения
                if type(val) is not int or val < 0:
                    continue

                curr_valid_layer += 1

        # Сравнение общего количества разделов и валидных разделов в конфигурационном файле
        if all_layer != curr_valid_layer:
            # Вывод сообщения
            if out is True:
                print(self._invalid_args.format(
                    self.red, datetime.now().strftime(self._format_time), self.end
                ))

            return False

        self._args = args  # Аргументы командной строки

        return True  # Результат

    # Создание каталогов для категорий с файлами
    def _mkdirs(self, metadata_folder, boxes_folder, out = True):
        """
        Создание каталогов для категорий с файлами

        (str, str, list, str [, bool]) -> bool

        Аргументы:
           metadata_folder - Директория для медаданных
           boxes_folder    - Директория для файлов с информацией
           out             - Печатать процесс выполнения

        Возвращает: True если все директории успешно созданы, в обратном случае False
        """

        # Проверка аргументов
        if (type(metadata_folder) is not str or not metadata_folder
                or type(boxes_folder) is not str or not boxes_folder
                or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self._mkdirs.__name__
                ))

            return False

        # Вывод сообщения
        if out is True:
            print(self._create_dirs.format(datetime.now().strftime(self._format_time)))

        # Создание директорий
        for folder in [metadata_folder, boxes_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        return True

    # Проверка наличия необходимого файла CSV
    def _valid_csv(self, url, file, download_miss_f, out = True):
        """
        Проверка наличия необходимого файла CSV

        (str, bool [, bool]) -> bool

        Аргументы:
           url             - Полный путь к файлу
           file            - Файл CSV
           download_miss_f - Загрузка отсутствующего файла
           out             - Печатать процесс выполнения

        Возвращает: True если CSV файл загружен, в обратном случае False
        """

        # Проверка аргументов
        if type(url) is not str or not url or type(file) is not str or not file or type(download_miss_f) is not bool \
                or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self._valid_csv.__name__
                ))

            return False

        # Файл с общим названием классов не найден
        if not os.path.isfile(file):
            # Вывод сообщения
            if out is True:
                print(self._missing_file.format(os.path.basename(file)))

            cnt = 0

            while True:
                # Загрузка отсутствующих файлов
                if not download_miss_f:
                    try:
                        if cnt == 0:
                            self._download_file_classes = input(self._input)  # Вопрос
                        else:
                            self._download_file_classes = input(self._input_error.format(self.red, self.end))  # Вопрос
                    except UnicodeDecodeError:
                        cnt += 1

                        continue

                self._download_file_classes = self._download_file_classes.lower()

                if self._download_file_classes == 'y':
                    return self._download_file(url, file, out)  # Сохранение файла с названиями классов
                elif self._download_file_classes == 'n':
                    # Вывод сообщения
                    if out is True:
                        print(self._cancel_download.format(
                            self.red, datetime.now().strftime(self._format_time), self.end,
                            os.path.basename(file))
                        )

                    return False
                else:
                    cnt += 1

        return True

    # Загрузка файла из URL
    def _download_file(self, url, filename, out = True):
        """
        Загрузка файла из URL

        (str, str [, bool]) -> bool

        Аргументы:
           url      - Полный путь к файлу
           filename - Локальный файл с названиями классов
           out      - Печатать процесс выполнения

        Возвращает: True если файл загружен, в обратном случае False
        """

        # Проверка аргументов
        if type(url) is not str or not url or type(filename) is not str or not filename or type(out) is not bool:
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self._download_file.__name__
                ))

            return False

        # Отправка GET запроса для получения CSV файла
        r = requests.get(url, headers = {'user-agent': self._headers}, stream = True)

        # Ответ получен
        if r.status_code == 200:
            # Вывод сообщения
            if out is True:
                total_length = int(r.headers.get('content-length', 0))  # Длина файла

                num_bars = np.ceil(total_length / self._chunk_size)  # Количество загрузок

                # Прогресс бар
                bar = progressbar.ProgressBar(max_value = int(num_bars),
                                              prefix = self._automatic_download,
                                              widgets = [progressbar.SimpleProgress(
                                                  format = '%(value_s)s из %(max_value_s)s (%(percentage)1d%%)'
                                              )]).start()

            # Открытие файла для записи
            with open(filename, 'wb') as f:
                # Сохранение файла по частям
                for i, chunk in enumerate(r.iter_content(chunk_size = self._chunk_size)):
                    f.write(chunk)  # Запись в файл
                    f.flush()

                    # Вывод сообщения
                    if out is True:
                        bar.update(i + 1)

            # Вывод сообщения
            if out is True:
                bar.finish()

            return True
        else:
            # Вывод сообщения
            if out is True:
                print(self._url_error.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, r.status_code
                ))

            return False

    # Загрузка изображений
    def _download_images(self, type_data, class_name, class_code, threads = 20, out = True):
        """
        Загрузка изображений

        (str, str, str, int [, bool]) -> bool

        Аргументы:
           type_data  - Подвыборка набора данных
           class_name - Имя класса
           class_code - Код класса
           threads    - Количество потоков
           out        - Печатать процесс выполнения

        Возвращает: True если изображения загружены, в обратном случае False
        """

        # Проверка аргументов
        if (type(type_data) is not str or not type_data
                or type(class_name) is not str or not class_name
                or type(class_code) is not str or not class_code
                or type(threads) is not int or threads < 1
                or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self._download_images.__name__
                ))

            return False

        images_list = self._type_data[type_data]['df']['ImageID'][
            self._type_data[type_data]['df'].LabelName == class_code
        ].unique().tolist()  # Всего изображений

        all_images = len(images_list)

        if all_images < self._args['limit']:
            self._args['limit'] = all_images

        # Вывод сообщения
        if out is True:
            print(self._all_images_in_class.format(type_data, all_images) + (self._limit.format(self._args['limit']) if
                  self._args['limit'] > 0 else ''))

        # Лимит загрузки изображений
        if self._args['limit'] == 0:
            self._args['limit'] = all_images

        # Путь к изображениям
        download_dir = os.path.join(self._args['dataset'], type_data, class_name)

        commands = []

        # Проход по всем изображениям
        for i in range(0, self._args['limit']):
            # Изображение не сохранено ранее
            if Path(os.path.join(download_dir, images_list[i] + self._ext)).is_file() is False:
                path = type_data + '/' + str(images_list[i]) + '.jpg ' + '"' + download_dir + '"'
                command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/' + path

                commands.append(command)

        # Загрузка изображений
        if len(commands) > 0:

            # Вывод сообщения
            if out is True:
                i = self._args['limit'] - len(commands)  # Счетчик процесса загрузки

                # Прогресс бар
                bar = progressbar.ProgressBar(
                    max_value = self._args['limit'], prefix = self._automatic_download,
                    min_value = 0,
                    initial_value = i,
                    widgets = [progressbar.SimpleProgress(
                        format = '%(value_s)s из %(max_value_s)s (%(percentage)1d%%)'
                    )]).start()

            # Параллельная загрузка
            with ThreadPool(threads) as pool:
                # Загрузка
                for _ in pool.imap(os.system, commands):
                    # Вывод сообщения
                    if out is True:
                        i += 1
                        bar.update(i)

                pool.close()
                pool.join()

                # Вывод сообщения
                if out is True:
                    bar.finish()
        else:
            # Вывод сообщения
            if out is True:
                print(self._already_downloaded)

        return True

    # Формирование меток
    def _get_label(self, type_data, class_name, class_code, out = True):
        """
        Формирование меток

        (str, str, str [, bool]) -> bool

        Аргументы:
           type_data  - Подвыборка набора данных
           class_name - Имя класса
           class_code - Код класса
           out        - Печатать процесс выполнения

        Возвращает: True если все метки сформированы, в обратном случае False
        """

        # Проверка аргументов
        if (type(type_data) is not str or not type_data
                or type(class_name) is not str or not class_name
                or type(class_code) is not str or not class_code
                or type(out) is not bool):
            # Вывод сообщения
            if out is True:
                print(self._invalid_arguments.format(
                    self.red, datetime.now().strftime(self._format_time),
                    self.end, __class__.__name__ + '.' + self._get_label.__name__
                ))

            return False

        # Формирование меток
        if not self._args['no_labels']:
            # Путь к изображениям
            download_dir = os.path.join(self._args['dataset'], type_data, class_name)

            # Список загруженных изображений
            downloaded_images_list = [
                str(p.resolve()) for p in Path(download_dir).glob('*' + self._ext)
            ]

            # Вывод сообщения
            if out is True:
                # Прогресс бар
                bar = progressbar.ProgressBar(
                    max_value = len(downloaded_images_list), prefix = self._labels,
                    min_value = 0,
                    initial_value = 0,
                    widgets = [progressbar.SimpleProgress(
                        format = '%(value_s)s из %(max_value_s)s (%(percentage)1d%%)'
                    )]).start()

            # Группировка динных по ID изображениям
            groups = self._type_data[type_data]['df'][
                (self._type_data[type_data]['df'].LabelName == class_code)
            ].groupby(self._type_data[type_data]['df'].ImageID)

            # Путь к меткам
            labels_path = os.path.join(download_dir, self._lbls)

            # Создание директории
            if not os.path.exists(labels_path):
                os.makedirs(labels_path)

            # Проход по всем изображениям
            for i, img in enumerate(downloaded_images_list):
                curr_image = cv2.imread(img)  # Загрузка изображения

                basename = os.path.basename(img).split('.')[0]

                # Текущее изображение не получено
                if curr_image is None:
                    # Вывод сообщения
                    if out is True:
                        print(self._photo_not_read.format(self.red, basename, self.end))

                    continue

                boxes = groups.get_group(basename)[['XMin', 'XMax', 'YMin', 'YMax']].values.tolist()

                # Путь к текстовому файлу, куда будут сохранены координаты
                file_path = os.path.join(labels_path, basename + '.txt')

                # Открытие файла для записи
                with open(file_path, 'w') as f:
                    for box in boxes:
                        box[0] *= int(curr_image.shape[1])
                        box[1] *= int(curr_image.shape[1])
                        box[2] *= int(curr_image.shape[0])
                        box[3] *= int(curr_image.shape[0])

                        print(class_name, box[0], box[2], box[1], box[3], file = f)

                # Вывод сообщения
                if out is True:
                    bar.update(i + 1)

            # Вывод сообщения
            if out is True:
                bar.finish()

            return True

    # ------------------------------------------------------------------------------------------------------------------
    # Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    def download(self, args, out = True):
        """
        Массовая загрузка набора данных Open Images Dataset V6

        (argparse.Namespace [, bool]) -> bool

        Аргументы:
            args - Параметры командной строки
            out  - Печатать процесс выполнения

        Возвращает: True если все этапы загрузки выполнены, в обратном случае False
        """

        # Проверка аргументов командной строки на валидность
        if not self._valid_args(args, out):
            return False

        metadata_dir = os.path.join(args['dataset'], self._metadata)  # Директория для метаданных
        boxes_dir = os.path.join(args['dataset'], self._boxes)  # Директория для файлов с информацией

        # --------------------------------------------------------------------------------------------------------------
        # Загрузка данных из набора Open Images Dataset V6
        # --------------------------------------------------------------------------------------------------------------
        if args['command'] == 'downloader':
            # Скачивать классы отдельно
            if args['multi_classes'] is False:
                # Создание папок для категорий с файлами
                if self._mkdirs(metadata_dir, boxes_dir, out) is False:
                    return False

                # Вывод сообщения
                if out is True:
                    Shell.add_line()  # Добавление линии во весь экран

                # Проход по всем классам
                for class_name in args['classes']:
                    class_name_del = class_name.replace('_', ' ')  # Название класса с пробелом

                    # Вывод сообщения
                    if out is True:
                        print(self._download.format(datetime.now().strftime(self._format_time), class_name_del))

                    if self._download_file_classes == 'y':
                        url_class_descriptions = os.path.join(self._oid_url['v5'], self._name_file_classes)
                        path_class_descriptions = os.path.join(metadata_dir, self._name_file_classes)

                        # Проверка наличия необходимого файла CSV
                        if not self._valid_csv(url_class_descriptions, path_class_descriptions, args['yes'], out):
                            return False

                        # Таблица с названиями классов не заполнена
                        if self._df_classes is None:
                            self._df_classes = pd.read_csv(
                                os.path.join(metadata_dir, self._name_file_classes), header = None
                            )

                        try:
                            # Код класса
                            class_code = self._df_classes.loc[
                                self._df_classes[1].str.lower() == class_name_del
                            ].values[0][0]
                        except IndexError:
                            # Вывод сообщения
                            if out is True:
                                print(self._index_error.format(self.red, class_name_del, self.end))
                                Shell.add_line()  # Добавление линии во весь экран

                            continue

                        # Выборка из набора данных
                        if args['type_data'] not in self._type_data.keys():
                            type_data = self._type_data.keys()
                        else:
                            type_data = [args['type_data']]

                        # Проход по выбранным наборам данных
                        for curr_type_data in type_data:
                            # Каталог с категорией
                            curr_folder = os.path.join(self._args['dataset'], curr_type_data, class_name)

                            # Создание директории, куда будут сохранены изображения, если она не существует
                            if not os.path.exists(curr_folder):
                                os.makedirs(curr_folder)

                            url_annotations = os.path.join(
                                self._type_data[curr_type_data]['url'],
                                self._type_data[curr_type_data]['bbox']
                            )
                            curr_annotations = os.path.join(boxes_dir, self._type_data[curr_type_data]['bbox'])

                            # Проверка наличия необходимого файла CSV
                            if not self._valid_csv(url_annotations, curr_annotations, args['yes'], out):
                                return False

                            # Таблица с набором
                            if self._type_data[curr_type_data]['df'] is None:
                                # Вывод сообщения
                                if out is True:
                                    print(self._extract.format(self._type_data[curr_type_data]['bbox']))

                                self._type_data[curr_type_data]['df'] = pd.read_csv(curr_annotations)

                            # Загрузка изображений
                            if not self._download_images(curr_type_data, class_name, class_code, 20, out):
                                return False

                            #  Формирование меток
                            if not self._get_label(curr_type_data, class_name, class_code, out):
                                return False

                    Shell.add_line()  # Добавление линии во весь экран
            else:
                # TODO РАЗРАБОТКА

                # Вывод сообщения
                if out is True:
                    Shell.add_line()  # Добавление линии во весь экран

                    print(self._in_developing.format(
                        self.green, datetime.now().strftime(self._format_time), self.end,
                        'Функция "Загрузка всех классов в одну директорию"'
                    ))

                    Shell.add_line()  # Добавление линии во весь экран

        return True
