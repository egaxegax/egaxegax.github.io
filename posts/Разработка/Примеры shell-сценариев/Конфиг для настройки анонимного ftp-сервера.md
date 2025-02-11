<!--2017-11-22 21:13:41-->
### Конфиг для настройки анонимного ftp-сервера
Конфиг */etc/vsftpd.conf*

    listen=yes
    tcp_wrappers=yes

    write_enable=yes
    anon_root=/
    anon_mkdir_write_enable=yes
    anon_other_write_enable=yes
    anon_upload_enable=yes
    anon_umask=000

    #seccomp_sandbox=NO
