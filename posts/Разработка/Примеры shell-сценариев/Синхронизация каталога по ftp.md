<!--2020-09-04 16:37:08-->
## Синхронизация каталога по ftp
Синхронизация файлов каталогов с помощью утилиты *ltfp*

    #!/bin/bash
    sudo mkdir -p files
    cd files
    lftp -c mirror ftp://192.168.0.4/home/user/serv
    lftp -c mirror ftp://192.168.0.4/home/user/images
    sudo chmod -R 777 .
