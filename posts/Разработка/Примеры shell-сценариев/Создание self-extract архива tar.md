<!--2012-11-11 19:47:05-->
## Создание self-extract архива tar
Скрипт запуска *extract.sh*

    #!/bin/bash
    echo ""
    echo "Self Extracting Installer"
    echo ""
    
    export TMPDIR=`mktemp -d /tmp/selfextract.XXXXXX`
    
    ARCHIVE=`awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }' $0`
    
    tail -n+$ARCHIVE $0 | tar -xzv - -C $TMPDIR
    
    CDIR=`pwd`
    cd $TMPDIR
    ./installer
    
    cd $CDIR
    rm -rf $TMPDIR
    
    exit 0
    
    # newline after
    __ARCHIVE_BELOW__

Пакуем скрипт запуска и архив tar.gz в bundle

    cat extract.sh a.tar.gz > installer.run

Запускаем

    sh installer.run