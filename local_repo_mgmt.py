"""
    Утилита управления локальным репозиторием OVAL.

    Утилита является обёрткой для стандартных модулей OVALRepo:
    oval_decomposition.py
    build_oval_definitions_file.py

    Позволяет вести локальный репозиторий сущностей OVAL (объектов, 
    определений, тестов) без оглядки на глобальный репозиторий.
    Это достигается путём создания ложного git-репозитория в окружении
    скриптов ScriptsEnvironment каждый раз, когда нужно собрать xml-файл.

    Автор: Денис Яблочкин <denis-yablochkin.ib@yandex.ru>
    For english reference see README.md file.
"""
import os, shutil, sys
from git import Repo

def decomposition():
    """
        Вызов модуля oval_decomposition.py для разложения OVAL xml на
        составные части - определения, объекты и т.д.

        Для вывода help конкретного модуля:
        local_repo_mgmt.py -d -h

        Для корректного сбора модулем build необходима следующая секция
        внутри каждого исходного <definition>:
        <oval_repository>
            <dates>
                <submitted date="YYYY-MM-DDTHH:MM:SS.000+00:00">
                    <contributor organization="ORGANISATION">JOHN WICK</contributor>
                </submitted>
            </dates>
        </oval_repository>
        
    """
    oval_decomposition.main()



def build():
    """
        Вызов модуля build_oval_definitions_file.py для сбора OVAL xml
        на основе репозитория.

        Для вывода help конкретного модуля:
        local_repo_mgmt.py -b -h

        Для корректного сбора модулем build необходима следующая секция
        внутри каждого исходного <definition>:
        <oval_repository>
            <dates>
                <submitted date="YYYY-MM-DDTHH:MM:SS.000+00:00">
                    <contributor organization="ORGANISATION">JOHN WICK</contributor>
                </submitted>
            </dates>
        </oval_repository>
    """
    try:
        shutil.rmtree(os.path.abspath('./ScriptsEnvironment/.git'))
    except:
        pass
    
    open(os.path.abspath('./ScriptsEnvironment/.init'), 'w').close()
    repo = Repo.init(os.path.abspath('./ScriptsEnvironment'))
    index = repo.index
    index.add( [ '.init' ] )
    index.commit("init")
    build_oval_definitions_file.main()

    try:
        shutil.rmtree(os.path.abspath('./ScriptsEnvironment/.git'))
        os.remove(os.path.abspath('./ScriptsEnvironment/.init'))
    except:
        pass


def clear():
    """
        Очищает окружение ScriptsEnvironment от файлов, необходимых для
        построения репозитория (каталог .git и файл .init). Если таких файлов
        нет - выводит соответствующее сообщение.
        Файлы репозиториев и скриптов остаются нетронутыми в любом случае.
    """
    try:
        shutil.rmtree(os.path.abspath('./ScriptsEnvironment/.git'))
    except Exception as e:
        print(str(e))
    try:
        os.remove(os.path.abspath('./ScriptsEnvironment/.init'))
    except Exception as e:
        print(str(e))


def main(args):
    """
        Утилита управления локальным репозиторием OVAL.

        Утилита является обёрткой для стандартных модулей OVALRepo:
        oval_decomposition.py
        build_oval_definitions_file.py

        Позволяет вести локальный репозиторий сущностей OVAL (объектов, 
        определений, тестов) без оглядки на глобальный репозиторий.
        Это достигается путём создания ложного git-репозитория в окружении
        скриптов ScriptsEnvironment каждый раз, когда нужно собрать xml-файл.

        ИСПОЛЬЗОВАНИЕ
        Передача управления модулю декомпозиции (разобра) xml-файла:
        local_repo_mgmt.py -d

        Передача управления модулю построения xml-файла:
        local_repo_mgmt.py -b

        Очистка окружения скриптов ScriptsEnvironment:
        local_repo_mgmt.py -c

        Для вывода help конкретного модуля:
        local_repo_mgmt.py -d -h
        local_repo_mgmt.py -b -h

    """
    try:
        if args[1]=='-d':
            args.pop(1) 
            decomposition()

        elif args[1]=='-b':
            args.pop(1)
            build()

        elif args[1] == '-c':
            clear()

        elif args[1] == '-h':
            help(main)
            help(decomposition)
            help(build)
            help(clear)

    except IndexError:
        help(main)
        help(decomposition)
        help(build)
        help(clear)



sys.path.insert(1,'./ScriptsEnvironment/scripts')
import oval_decomposition
import build_oval_definitions_file
import build_all_oval_definitions






main(sys.argv)

