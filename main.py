import os
import shutil
from config import Config
from pathlib import Path


class File_manager:
    def __init__(self):
        self.c = Config()
        self.home_dir = f'{os.getcwd()}/work_folder'  # полный путь до домашней директории
        self.__changecfg__()
        self.home_dir_Path = Path(self.home_dir)
        os.chdir(f'{self.home_dir}')
        self.commands = ['crdr', 'rmdr', 'chdr', 'crf', 'fillf', 'chf', 'rmf', 'cof', 'mof', 'ref', 'exit', 'list',
                         'path', 'help', 'chcfg']  # команды на ввод
        self.name = ''  # используется для запоминания команды (надо бы убрать и исправить те места, где она нужна)
        self.line = ''  # переменная для приема команды из консоли
        self.flag = True  # переменная-флаг, чтобы заканчивать цикл
        self.command = None  # нужна для определения самой команды
        self.listcom = '''1. Создание папки(crdr);
2. Удаление папки по имени(rmdr);
3. Перемещение между папками (в пределах рабочей папки) - заход в папку по имени, выход на уровень вверх(chdr);
4. Создание пустых файлов с указанием имени(crf);
5. Запись текста в файл(fillf);
6. Просмотр содержимого текстового файла(chf); 
7. Удаление файлов по имени(rmf);
8. Копирование файлов из одной папки в другую(cof);
9. Перемещение файлов(mof);
10. Переименование файлов(ref);
11. Для выхода из программы(exit);
12. Для просмотра списка файлов и папок в директории(list);
13. Чтобы получить путь до файла(path);
14. Чтобы получить список команд(help);
15. Изменить конфиг'''  # возможности файлового менеджера

    def main(self):
        while self.flag:
            self.line = input('Введите команду: ').split()
            self.command = self.commands.index(self.line[0]) + 1
            if not (1 <= self.command <= 15):
                print('Вы ввели неправильную команду!')
                return 1
            elif self.command == 11:
                self.flag = False
                return 1
            elif self.command == 1:
                return self.__createDirectory__()
            elif self.command == 2:
                return self.__removeDirectory__()
            elif self.command == 3:
                return self.__cd__()
            elif self.command == 4:
                return self.__touch__()
            elif self.command == 5:
                return self.__nano__()
            elif self.command == 6:
                return self.__cat__()
            elif self.command == 7:
                return self.__removeFile__()
            elif self.command == 8:
                return self.__copyFile__()
            elif self.command == 9:
                return self.__movingFile__()
            elif self.command == 10:
                return self.__renameFile__()
            elif self.command == 12:
                print("\n".join(i for i in os.listdir()), end='\n\n')
            elif self.command == 13:
                print(self.__getPath__())
            elif self.command == 14:
                print(self.__getInfo__())
            elif self.command == 15:
                return self.__changecfg__()

    def __createDirectory__(self):
        self.name = self.line[1]
        if self.name == self.home_dir[self.home_dir.rfind('/') + 1:]:
            print(f'You are not allowed to create drectory with such name ({self.name})')
            return 1
        try:
            return os.mkdir(f'{self.home_dir}/{self.name}')
        except FileExistsError:
            print(f'FileExistsError: directory with name {self.name} is already exists\nПапка с именем {self.name} '
                  'уже существует')
            return 1

    def __removeDirectory__(self):
        self.name = self.line[1]
        if self.name == self.home_dir[self.home_dir.rfind('/') + 1:]:
            print(f'You are not allowed to remove drectory with such name ({self.name})')
            return 1
        try:
            return os.rmdir(f'{self.home_dir}/{self.name}')
        except OSError:
            print('OSError: directory is not empty OR there is no such directory\nПапка не пустая ИЛИ такой папки не '
                  'существует')
            return 1

    def __cd__(self):
        self.name = self.line[1]
        if self.name.lower() in ['выход на уровень вверх', '../', 'up', 'back', '<-']:
            path = os.getcwd()
            if path == self.home_dir:
                print('Нельзя выйти из корневой папки!\n')
                return 0
            return os.chdir('../')
        return os.chdir(self.name)

    def __touch__(self):  # try except IndexError
        for i in self.line[1:]:
            open(f'./{i}', 'a').close()
        return 1

    def __nano__(self):
        self.name = self.line[1]
        fd = os.open(self.name, os.O_RDWR)
        text = input('Введите текст, который хотите записать в файл\n').encode()
        os.write(fd, text)
        os.close(fd)
        return 1

    def __cat__(self):
        self.name = self.line[1]
        try:
            with open(self.name, "r") as file:
                for line in file:
                    print(line)
            return 1
        except IsADirectoryError:
            print('Вы пытаетесь прочитать папку(буууээээээ). Если хотите узнать содержимое папки, то воспользуйтесь '
                  'командой под номером 12\nЧтобы выйти из этого действия нажмите пробел')
            if input() == ' ':
                return 1
            return 1

    def __removeFile__(self):
        self.name = self.line[1]
        try:
            os.remove(self.name)
        except PermissionError:
            print('Вы пытаетесь удалить папку(буууээээээ). Если хотите удалить папку, то воспользуйтесь '
                  'командой под номером 2\nЧтобы выйти из этого действия нажмите пробел')
            if input() == ' ':
                return 1
            return 1

    def __copyFile__(self):
        os.chdir(self.home_dir)
        self.name = self.line[1]
        path1 = self.name
        self.name = self.line[2]
        path2 = self.name
        try:
            if self.__check_Path__(path2):
                return shutil.copy(f'{self.home_dir}/{path1}', f'{self.home_dir}/{path2}')
            else:
                print(f'Вы пытаетесь скопировать файл {path1} за пределы рабочей папки!')
        except FileExistsError:
            print(f'Файл {path1} не найден!')

    def __movingFile__(self):
        os.chdir(self.home_dir)
        self.name = self.line[1]
        path1 = self.name
        self.name = self.line[2]
        path2 = self.name
        try:
            if self.__check_Path__(path2):
                return shutil.move(f'{self.home_dir}/{path1}', f'{self.home_dir}/{path2}')
            else:
                print(f'Вы пытаетесь переместить файл {path1} за пределы рабочей папки!')
        except FileExistsError:
            print(f'Файл {path1} не найден!')

    def __renameFile__(self):
        try:
            oldname = self.line[1]
            self.name = self.line[2]
            return os.rename(f'{self.home_dir}/{oldname}', f'{self.home_dir}/{self.name}')
        except IndexError:
            print('List index out of range. Try again!')
            return 1

    def __getPath__(self):
        return os.getcwd()

    def __getInfo__(self):
        return self.listcom

    def __changecfg__(self):
        print(f'Your\'s work directory is a {Config().work_folder}')
        self.name = input('Do you want to change it (you must change it if you do not use OSX)? (y/n): ')
        if self.name.lower() == 'y':
            self.name = input('Type the full path to the directory, which you want work with: ')
            self.c.set_folder(self.name)
            return self.__setHomedir__(self.name)
        elif self.name.lower() == 'n':
            return 1

    def __setHomedir__(self, path):
        self.home_dir = path

    def __check_Path__(self, dest):
        if os.path.abspath(dest) in self.home_dir_Path:
            return True
        else:
            return False


a = File_manager()
a.main()
