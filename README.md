Local OVAL repository managment tool.
Author: Denis Yablochkin <denis-yablochkin.ib@yandex.ru>

It is a wrapper for several OVALRepo modules:
oval_decomposition.py
build_oval_definitions_file.py

Allows to run local OVAL repository by creating false git environment for it. Every time when you need to build xml-files the wrapper creates git-repo in ScriptsEnvironment and then makes an initial commit with empty .init file. 




Утилита является обёрткой для стандартных модулей OVALRepo:
oval_decomposition.py
build_oval_definitions_file.py

Позволяет вести локальный репозиторий сущностей OVAL (объектов,определений, тестов) без оглядки на глобальный репозиторий. Это достигается путём создания ложного git-репозитория в окружении скриптов ScriptsEnvironment каждый раз, когда нужно собрать xml-файл.

Причины для разработки обёртки:
Инструменты OVALRepo, созданные сообществом, позволяют удобно поддерживать сущности OVAL, разбирая файлы на составляющие - определения, объекты, состояния, переменные и тесты. Например, если несколько файлов используют один и тот же объект (версию продукта), то можно хранить лишь один файл для него.

Однако, эти инструменты в основном предназначены для работы с глобальным общим репозиторием. При работе с файлами происходит обращение к git-окружению, вырезать которое из огромного количества кода не представляется возможным. 

Разбор файла OVAL модулем oval_decomposition просто раскладывает файл на составляющие в окружении OVAL - в папку repository. 

Сбор модулем build_oval_definitions_file.py использует окружение git. Для имитации его работы был использован каталог ScriptsEnvironment. На время работы модуля build_oval_definitions_file.py инициализируется новый git-репозиторий и делается коммит с пустым файлом .init. После этого модуль срабатывает как нужно, а элементы окружения (.git и .init) удаляются. На случай проблем предусмотрен флаг -c, выполняющий удаление автоматически.