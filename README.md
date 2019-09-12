Local OVAL repository managment tool.
Author: Denis Yablochkin <denis-yablochkin.ib@yandex.ru>
https://github.com/CISecurity/OVALRepo/

It is a wrapper for several OVALRepo modules (see additional info in COPYRIGHT.md):
oval_decomposition.py
build_oval_definitions_file.py

Allows to run local OVAL repository by creating false git environment for it. Every time when you need to build xml-files the wrapper creates git-repo in ScriptsEnvironment and then makes an initial commit with empty .init file. 



Утилита является обёрткой для стандартных модулей OVALRepo (дополнительная информация в COPYRIGHT.md):
oval_decomposition.py
build_oval_definitions_file.py

Позволяет вести локальный репозиторий сущностей OVAL (объектов,определений, тестов) без оглядки на глобальный репозиторий. Это достигается путём создания ложного git-репозитория в окружении скриптов ScriptsEnvironment каждый раз, когда нужно собрать xml-файл.



Known bug:

Exception: '' is not a parseable date
This means that <oval_repository> tag is not exists or corrupted:

```xml
<oval_repository>
    <dates>
        <submitted date="YYYY-MM-DDTHH:MM:SS.000+00:00">
            <contributor organization="ORGANISATION">JOHN WICK</contributor>
        </submitted>
    </dates>
</oval_repository>
```

