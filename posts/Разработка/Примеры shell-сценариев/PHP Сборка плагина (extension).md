<!--2013-07-26 20:30:35-->
### PHP Сборка плагина (extension)
Краткая сводка действий для сборки плагина под PHP 5.2, 5.3, 5.4.

*Сборка под Linux*

PHP должен быть установлен в системе.

    phpize
    ./configure
    make
    make test
    make install (или скопировать вручную php_extension.so)

*Сборка под Windows*

Используем среду Visual Studio 2008.

Настройка php-sdk (поставляется отдельно от дистрибутива php):

    setenv /x86 /xp /release
    cd c:\php-sdk\
    bin\phpsdk_setvars.bat
    bin\phpsdk_buildtree.bat <php_src_dir>

Для PHP 5.2 также нужен win32build (ставится тоже отдельно):

    set INCLUDE=c:\win32build\include

Выставляем переменные окружения Visual Studio:

    c:\Program Files\Microsoft Visual Studio 9.0\VC\bin\vcvars32.bat

Собираем PHP через `configure.js` и `nmake`. В VS2008Express отсутствует компилятор сообщений mc.exe. Его можно взять из VS2010 добавив в Makefile строчку перед "MT = ...":

    MC=C:\Program Files\Microsoft SDKs\Windows\v7.0A\bin\mc.exe 
    MT=C:\Program Files\Microsoft SDKs\Windows\v6.0A\bin\mt.exe

Либо установить Windows SDK.

Инициализируем плагин:

1. php.exe ext_skel_win32.php --extname=myextension --proto=myprototypefile.dat
2. Раскомментарить ARG_ENABLE или ARG_WITH в config.w32

Собираем PHP 5.2 с плагином:

    buildconf.bat
    cscript /nologo configure.js --disable-zts --disable-cgi --disable-fastcgi --disable-path-info-check --disable-bcmath --disable-calendar --disable-com-dotnet --disable-ctype --disable-xmlreader --disable-zlib --disable-xmlwriter --disable-ftp --disable-filter --disable-ctype --disable-com-dotnet --enable-cli --without-xml --without-libxml --without-simplexml --disable-ipv6 --with-EXTENSION[=shared[,PATH]]
    nmake


Сборка PHP 5.3 с плагином:

    buildconf.bat
    cscript /nologo configure.js --disable-all --enable-cli --with-EXTENSION[=shared[,PATH]]
    nmake

Для компиляции через Visual Studio в настройках проекта нужно выставить флаг препроцессора _USE_32BIT_TIME_T.