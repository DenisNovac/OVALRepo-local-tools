# Использование lrm.py

Инструменты сообщества, представленные в репозитории CISecurity OVALRepo, обладают полезными возможностями для управления большим количеством определений OVAL (особенно если эти определения используют одни и те же ресурсы - объекты, переменные). Однако, эти инструменты предназначены для подготовки определений и их составляющих к загрузке в репозиторий, поэтому осуществлять управление через ними напрямую невозможно. Например, невозможно сделать сборку одного репозитория несколько раз (собрать из репозитория все определения для WinCC, а потом сразу же все определения для MasterSCADA). 

Для решения этих проблем используется обёртка Local repository management, позволяющая не только разбирать и собирать определения неограниченное количество раз, но и расширяющая возможности стандартных скриптов.

## Состав

Обёртка использует следующие модули оригинальной библиотеки CISecurity:

- build_oval_definitions_file.py

- oval_decomposition.py

- lib_git.py

- lib_oval.py

- lib_repo.py

- lib_search.py

- lib_xml.py

Поэтому она требует все те же библиотеки (смотри requirements.txt), что и оригинальный набор инструментов. Для Windows имеется bat-скрипт для установки требуемых библиотек из PIP.

Кроме того, в обёртке используется несколько модулей (папка modules, для каждого модуля существует команда). Список модулей представлен ниже:

- decompose_definition и build_definition - собственно модули обёртки. Представляют из себя вызов соответствующих модулей из оригинальной библиотеки с предварительной обработкой - подстановкой аргументов командной строки, созданием git-окружения и т.д.;

- clear_repository - модуль очистки репозитория. Удаляет временные папки от Python и git;

- list_repository - модуль вывода списка файлов в репозитории. Для определений выводит поле `<title>`;

- timestamp_definition - модуль вставки временной отметки в определения. Создаёт валидный блок `<oval_repository>` с временной отметкой, необходимый для работы с репозиторием;

- validate_definition - модуль валидации. Проводит валидацию файла по заданному каталогу схем (см. каталог schemas).

Список подмодулей:

- read_title.py - модуль для вычитки поля title из определения, используется при выводе списка определений в репозитории;

- RecursiveXMLSearcher.py - модуль для поиска xml-тегов в файле. Является классом с приватными рекурсивными методами (их использовать руками не надо) и публичными методами search_one и search_all. Оба модуля возвращают ссылки на нужные теги. Модуль используется в timestamp_definition.py;

- Validator.py - модуль, используемый при валидации. Для папки схем создаёт общую схему, по которой и делает проверку.

## Принцип работы

Папка ScriptsEnvironment содержит папку scripts с модулями. Управление этим модулям передаётся в зависимости от ключа (d для oval_decomposition и b для build_oval_definitions_file). При работе с ними в каталоге ScriptsEnvironment создаётся временный репозиторий git, необходимый для корректной работы. Разобранные файлы помещаются в каталоге repository. При каждой операции build репозиторий пересоздаётся, что позволяет сбор определений несколько раз подряд.

## Пример использования

Предположим, на руках имеется некоторое определение (файл example1.xml):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<oval_definitions
    xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5"
    xmlns:oval="http://oval.mitre.org/XMLSchema/oval-common-5"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://oval.mitre.org/XMLSchema/oval-common-5 oval-common-schema.xsd http://oval.mitre.org/XMLSchema/oval-definitions-5 oval-definitions-schema.xsd">

    <generator>
        <oval:product_name>CIS OVAL Repository</oval:product_name>
        <oval:product_version>0.1</oval:product_version>
        <oval:schema_version>5.10.1</oval:schema_version>
        <oval:timestamp>2019-09-16T06:47:34</oval:timestamp>
    </generator>

    <definitions>        <definition xmlns:oval-def="http://oval.mitre.org/XMLSchema/oval-definitions-5" class="inventory" id="oval:datapk.ussc.ru-masterscada:def:2019001" version="1">
          <metadata>
            <title>MasterSCADA установлена</title>
            <description>MasterSCADA installed on the computer</description>
            <oval_repository>
              <dates>
                <submitted date="2019-08-20T14:55:00.000+05:00">
                  <contributor organization="USSC">Denis Yablochkin</contributor>
                </submitted>
              </dates>
            </oval_repository>
            <affected family="windows">
              <product>masterscada</product>
              <product>MasterSCADA</product>
            </affected>
          </metadata>
          <criteria>
            <criterion test_ref="oval:datapk.ussc.ru-masterscada:tst:2019001" />
          </criteria>
        </definition>

    </definitions>

    <tests>        <registry_test xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows" check="at least one" check_existence="at_least_one_exists" comment="Check if MasterSCADA installed" id="oval:datapk.ussc.ru-masterscada:tst:2019001" version="1">
          <object object_ref="oval:datapk.ussc.ru-masterscada:obj:2019001" />
        </registry_test>

    </tests>

    <objects>        <registry_object xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows" comment="x64 and x32 registry paths" id="oval:datapk.ussc.ru-masterscada:obj:2019001" version="1">
          <set set_operator="UNION">
            <object_reference>oval:datapk.ussc.ru-masterscada:obj:2019101</object_reference>
            <object_reference>oval:datapk.ussc.ru-masterscada:obj:2019102</object_reference>
            <filter action="include">oval:datapk.ussc.ru-masterscada:ste:2019001</filter>
          </set>
        </registry_object>

        <registry_object xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows" comment="MasterSCADA in wow6432node uninstall" id="oval:datapk.ussc.ru-masterscada:obj:2019101" version="1">
          <behaviors windows_view="64_bit" />
          <hive>HKEY_LOCAL_MACHINE</hive>
          <key operation="pattern match">^SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\.*$</key>
          <name>DisplayName</name>
        </registry_object>

        <registry_object xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows" comment="MasterSCADA in uninstall" id="oval:datapk.ussc.ru-masterscada:obj:2019102" version="1">
          <hive>HKEY_LOCAL_MACHINE</hive>
          <key operation="pattern match">^SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\.*$</key>
          <name>DisplayName</name>
        </registry_object>

    </objects>

    <states>        
        <registry_state xmlns="http://oval.mitre.org/XMLSchema/oval-definitions-5#windows" id="oval:datapk.ussc.ru-masterscada:ste:2019001" version="1">
          <value operation="pattern match">(?i)(.*MasterSCADA.*)$</value>
        </registry_state>

    </states>


</oval_definitions>
```

**Обратите особое внимание на теги:**

```xml
<oval_repository>
 <dates>
     <submitted date="2019-08-20T14:55:00.000+05:00">
         <contributor organization="USSC">Denis Yablochkin</contributor>
     </submitted>    
 </dates>
 </oval_repository> 
```

**Эти теги не проверяются интерпретаторами вроде OVALdi (это означает, что на этапе тестирования определений интерпретаторы в них ошибок не увидят), но НЕОБХОДИМЫ для корректного функционирования всех инструментов. Для автоматической вставки таких тегов в любой файл имеется опция t в обёртке.**

Для разбора определения на составляющие требуется выполнить команду:

```batch
python lrm.py d --o "-f .\example1.xml"

Decomposing example1.xml ... Success
```


Полученное сообщение означает, что конфиг был успешно разобран на составляющие. Его содержимое теперь находится в ScriptsEnvironment/repository. Можно заметить, что каждая составляющая (объект, состояние, переменная и т.п.) теперь является отдельным файлом с названиями, соответствующими их id. **Такие файлы, в случае совпадения id, будут заменяться без предупреждения.** (через флаг -v внутри поля опций можно наблюдать каждую замену). Это означает, что если, например, три определения используют один и тот же объект, то он будет представлен в репозитории в единственном экземпляре. Если в нём содержится опечатка, её можно исправить в этом экземпляре либо собрать одно из определений, исправить там, а затем разложить определение обратно в репозиторий (файл с опечаткой заменится на новый).

Что произошло при вызове команды? Ключ d означает, что управление передаётся в модуль oval_decomposition.py. Поле опций --o "..." - это то поле, которое передаётся непосредственно в оригинальный модуль. Всего существует две операции, которые требуют такое поле: d (разборка) и b (сборка). Содержимое поля опций подставляется в аргументы командной строки и передаётся оригинальным модулям. В обоих случаях поле --o можно опустить, тогда будет вызван help из **оригинального файла**: 

```batch
python.exe .\lrm.py d
usage: [-h] -f FILE [-v]

Separates an OVAL file into its component parts and saves them to the
repository.

optional arguments:
  -h, --help            show this help message and exit

options:
  -f FILE, --file FILE  The name of the source file
  -v, --verbose         Enable more verbose messages
```

Вывод содержимого репозитория:

```batch
python.exe .\lrm.py l --m a
definitions:
        \inventory\oval:datapk.ussc.ru-masterscada:def:2019001   MasterSCADA установлена
objects:
        \windows\registry_object\2019000\oval:datapk.ussc.ru-masterscada:obj:2019001
        \windows\registry_object\2019000\oval:datapk.ussc.ru-masterscada:obj:2019101
        \windows\registry_object\2019000\oval:datapk.ussc.ru-masterscada:obj:2019102
states:
        \windows\registry_state\2019000\oval:datapk.ussc.ru-masterscada:ste:2019001
tests:
        \windows\registry_test\2019000\oval:datapk.ussc.ru-masterscada:tst:2019001
Total: 6
```

Название, выводимое рядом с определением  берётся напрямую из тега title в нём. Следует обратить внимание, что этот вывод обработан для удобства (например, чтобы скопировать id). Дело в том, что на самом деле файлы имеют несколько другие названия. Для отключения обработки вывода можно воспользоваться командой:

```batch
python.exe .\lrm.py l --m a --f f

ScriptsEnvironment\repository\definitions\inventory\oval_datapk.ussc.ru-masterscada_def_2019001.xml
ScriptsEnvironment\repository\objects\windows\registry_object\2019000\oval_datapk.ussc.ru-masterscada_obj_2019001.xml
ScriptsEnvironment\repository\objects\windows\registry_object\2019000\oval_datapk.ussc.ru-masterscada_obj_2019101.xml
ScriptsEnvironment\repository\objects\windows\registry_object\2019000\oval_datapk.ussc.ru-masterscada_obj_2019102.xml
ScriptsEnvironment\repository\states\windows\registry_state\2019000\oval_datapk.ussc.ru-masterscada_ste_2019001.xml
ScriptsEnvironment\repository\tests\windows\registry_test\2019000\oval_datapk.ussc.ru-masterscada_tst_2019001.xml
Total: 6
```

Можно заметить, что при разборе двоеточие заменяется на землю. Символ '_' в id запрещён и будет создавать проблемы при сборке (см. известные ошибки).

Стоит также помнить, что указание команды l без дополнительных аргументов выводит только список определений в репозитории. Команда имеет ключи для любого типа файлов и несколько дополнительных режимов работы:

```batch
--m {a,d,t,o,s,v}, --mode {a,d,t,o,s,v}
                        Output mode: all, definitions, tests, objects, states
                        or variables. Default: only definitions.
--f {f,l,h}, --format {f,l,h}
                        Format options: full paths, count files in every
                        category, hide definitions name
```


Теперь нужно собрать определение обратно. Для этого используется ключ b:

```batch
python.exe .\lrm.py b
usage: lrm.py [-h] -o OUTFILE [-v] [-s] [-t TEMPDIR]
                          [--definition_id [OVAL_ID [OVAL_ID ...]]]
                          [--title [PHRASE [PHRASE ...]]]
                          [--description [PHRASE [PHRASE ...]]]
                          [--class [CLASS [CLASS ...]]]
                          [--status [STATUS [STATUS ...]]]
                          [--family [FAMILY [FAMILY ...]]]
                          [--platform [PLATFORM [PLATFORM ...]]]
                          [--product [PRODUCT [PRODUCT ...]]]
                          [--contributor [NAME [NAME ...]]]
                          [--organization [NAME [NAME ...]]]
                          [--reference_id [REFERENCE_ID [REFERENCE_ID ...]]]
                          [--max_schema_version [SCHEMA_VERSION]]
                          [--all_definitions] [--from [YYYYMMDD]]
                          [--to [YYYYMMDD]]
lrm.py: error: the following arguments are required: -o/--outfile
```

**При возникновении проблем с этим модулем следует запустить команду очистки окружения (опция c).**

Он имеет множество параметров. Самыми полезными для сборки являются параметры:

- product - при разработке определений под один и тот же продукт (например, MasterSCADA), следует указывать одинаковые теги `<product>`. Благодаря им затем можно собирать наборы определений под конкретные продукты;

- max_schema_version - позволяет указать версию 5.10.1, поддерживаемую OVALdi. Тогда OVALdi будет обрабатывать собранные определения "из коробки" без проблем;

- all_definitions - позволяет собрать все определения, что есть. Однако, не поддерживает никакие фильтры, в т.ч. max_schema_version (можно руками поменять в теге generator. Это работает, если не используются объекты, отсутствующие в этой версии).

- definition_id - полезно для сборки конкретных определений;

- reference_id - позволяет указать идентификатор типа CVE-2019-12345 для поиска определения. Конечно, этот идентификатор должен быть указан в определении OVAL в соответствующем поле.

Пример сборки:

```batch
python.exe .\lrm.py b --o '--product masterscada --max_schema_version 5.10.1 -o out.xml'

INFO: Rebuilding oval_definitions index completed (1 definitions)
INFO: Found 1 matching OVAL definitions
INFO: Finding downstream OVAL ids for all definitions
INFO: Rebuilding oval_elements index completed (6 elements)
INFO: Found 5 downstream OVAL ids
INFO: Finding paths for 6 OVAL elements
INFO: Generating OVAL definition file with 6 elements
INFO: Writing OVAL definitions to out.xml
INFO: Completed in 00:00:01
```

Таким образом будет получен тот же файл example1.xml с небольшими отступлениями (явно указан неймспейс oval-def в определении).

## Дополнительные функции

Обёртка по сравнению с оригинальными модулями обладает некоторым расширенным функционалом. 

Например, возможно выполнять **декомпозицию каталога**:

```batch
python.exe .\lrm.py d --o '-f .\example\'
Decomposing example\example2.xml ... Success
Decomposing example\example3.xml ... Success
```

Декомпозиция выполняется в алфавитном порядке, как видно из примера. 

Кроме того, возможен **перенос декомпозированных файлов в каталог .decomposed** для удобства автозаполнения (сам каталог перемещён не будет, только содержимое). Для этого используется ключ --r в команде d:

```batch
python.exe .\lrm.py d --r --o '-f .\example\'

Decomposing example\example2.xml ... Success
Decomposing example\example3.xml ... Success

dir .\.decomposed\

Name
----
1568619391.282225 example2.xml

1568619391.293443 example3.xml
```

К именам файлов приписывается временная отметка для защиты от случайной замены нужного файла.

Наконец, существует команда очистки окружения скриптов на случай, если что-то пошло не так:

```batch
python.exe .\lrm.py c
[WinError 2] Не удается найти указанный файл: 'ScriptsEnvironment\\.git'
[WinError 2] Не удается найти указанный файл: 'ScriptsEnvironment\\.init'
Removed ScriptsEnvironment\scripts\__pycache__
Removed ScriptsEnvironment\scripts\__index__
Removed modules\__pycache__
Removed modules\submodules\__pycache__
```

Ошибки для несуществующих файлов - это нормально, т.к. при штатной работе некоторые временные файлы удаляются автоматически.

## Известные ошибки

### Exception: '' is not a parseable date

Если теги oval_repository, dates, submitted (с атрибутом date в правильном формате) и contributor повреждены или отсутствуют, при сборке будет получено следующее сообщение:

```batch
INFO: Rebuilding oval_definitions index completed (1 definitions)
Process SubWriterTask-1:
Traceback (most recent call last):
  File "C:\Users\dyablochkin\AppData\Local\Programs\Python\Python37\lib\multiprocessing\process.py", line 297, in _bootstrap
    self.run()
  File "C:\Users\dyablochkin\AppData\Local\Programs\Python\Python37\lib\site-packages\whoosh\multiproc.py", line 113, in run
    self._process_file(*jobinfo)
  File "C:\Users\dyablochkin\AppData\Local\Programs\Python\Python37\lib\site-packages\whoosh\multiproc.py", line 149, in _process_file
    writer.add_document(**args)
  File "C:\Users\dyablochkin\AppData\Local\Programs\Python\Python37\lib\site-packages\whoosh\writing.py", line 750, in add_document
    for tbytes, freq, weight, vbytes in items:
  File "C:\Users\dyablochkin\AppData\Local\Programs\Python\Python37\lib\site-packages\whoosh\fields.py", line 669, in index
    yield (self.to_bytes(num, shift), 1, 1.0, emptybytes)
  File "C:\Users\dyablochkin\AppData\Local\Programs\Python\Python37\lib\site-packages\whoosh\fields.py", line 840, in to_bytes
    x = self.prepare_datetime(x)
  File "C:\Users\dyablochkin\AppData\Local\Programs\Python\Python37\lib\site-packages\whoosh\fields.py", line 819, in prepare_datetime
    x = self._parse_datestring(x)
  File "C:\Users\dyablochkin\AppData\Local\Programs\Python\Python37\lib\site-packages\whoosh\fields.py", line 872, in _parse_datestring
    raise Exception("%r is not a parseable date" % qstring)
Exception: '' is not a parseable date
INFO: Found 0 matching OVAL definitions
INFO: Writing OVAL definitions to out.xml
INFO: Completed in 00:00:01!
```

Правильный формат:

```xml
<oval_repository>
    <dates>
      <submitted date="2019-08-20T14:55:00.000+05:00">
        <contributor organization="USSC">Denis Yablochkin</contributor>
      </submitted>
    </dates>
</oval_repository>
```

Автоматически такой блок в определения можно вставить, использовав ключ t в основной программе.

### Invalid OVAL id

Символ "_" запрещено использовать в ID. Это служебный символ, используемый для расположения файлов на диске (на него заменяются : в id). В итоге выходит путаница:

```batch
py.exe .\lrm.py b --o '--definition_id oval:datapk.us____________sc.ru-wincc:def:2018001 -o out.xml'
INFO: Rebuilding oval_definitions index completed (17 definitions)
INFO: Found 1 matching OVAL definitions
INFO: Finding downstream OVAL ids for all definitions
INFO: Rebuilding oval_elements index completed (71 elements)
INFO: Found 12 downstream OVAL ids
INFO: Finding paths for 13 OVAL elements
INFO: Generating OVAL definition file with 13 elements
Invalid OVAL id: oval:datapk.us::::::::::::sc.ru-wincc:def:2018001
```
