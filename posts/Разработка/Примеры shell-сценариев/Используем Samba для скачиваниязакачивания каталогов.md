<!--2012-11-12 19:51:55-->
## Используем Samba для скачиваниязакачивания каталогов
Чтобы "скачать" каталог файлов по сети с машины под *Windows* (*Samba*-сервером под *linux*) удобно воспользоваться утилитой *smbclient* из пакета *samba*.
Например.

Список доступных сетевых папок  

    smbclient -L 192.168.0.9 -U Администратор

Подключаемся

    smbclient //192.168.0.9/E$ -U Администратор

В оболочке *Samba* вводим команды для "скачивания" рекурсивно папки в текущий каталог  

    smb:/> recurse
    smb:/> prompt
    smb:/> mget Документы

Аналогично можно закачать папку из текущего каталога 

    smb:/> recurse
    smb:/> prompt
    smb:/> mput home

Текущим путем является текущий путь в терминале, в котором был выполнен *smbclient* 