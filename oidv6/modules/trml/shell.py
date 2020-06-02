#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Работа с Shell
"""

# ######################################################################################################################
# Импорт необходимых инструментов
# ######################################################################################################################
import subprocess  # Работа с процессами
import sys         # Доступ к некоторым переменным и функциям Python


# ######################################################################################################################
# Работа с Shell
# ######################################################################################################################
class Shell:
    """Класс для работы с Shell"""

    # ------------------------------------------------------------------------------------------------------------------
    #  Внешние методы
    # ------------------------------------------------------------------------------------------------------------------

    # Очистка консоли
    @staticmethod
    def clear():
        """
        Очистка консоли
        """

        command_shell = None  # Команда выполнения в Shell

        # linux или OS X
        if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
            command_shell = 'clear'
        # Windows
        elif sys.platform == "win32":
            command_shell = 'cls'

        if command_shell is not None:
            subprocess.call(command_shell, shell = True)  # Очистка Shell

    # Добавление линии во весь экран
    @staticmethod
    def add_line():
        """
        Добавление линии во весь экран
        """

        commands_shell = []  # Команды выполнения в Shell

        # linux или OS X
        if sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
            commands_shell.append("printf '%*s\n' \"${COLUMNS:-$(tput cols)}\" '' | tr ' ' -")
        # Windows
        elif sys.platform == 'win32':
            commands_shell.append("powershell -NoLogo -NoProfile -Command \"'-' * $Host.UI.RawUI.WindowSize.Width\"")

        if len(commands_shell) > 0:
            for command in commands_shell:
                subprocess.call(command, shell = True)  # Добавление линии в Shell
