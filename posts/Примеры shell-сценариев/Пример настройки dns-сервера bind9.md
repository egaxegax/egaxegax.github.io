<!--2018-01-28 08:28:19-->
### Пример настройки dns-сервера bind9
Настроим в локальной сети 192.168.x.x сервер разрешения имен dns. 
Создадим имена **srv**, **db**, **ftp** в домене dom на сервере 192.168.0.1.

Файл */etc/bind/dom/named.dom*

    $TTL    86400
    @       IN      SOA     srv.dom. root.srv.dom.  (
                                      20180128 ; Serial
                                      28800      ; Refresh
                                      14400      ; Retry
                                      3600000    ; Expire
                                      86400 )    ; Minimum
              IN      NS      srv.dom.

    srv     IN      A     192.168.0.1
    db    IN      A     192.168.2.2
    ftp     IN      A  192.168.0.127

>

Файл */etc/bind/dom/db.ftp* для настройки короткого имени **ftp** без домена dom.

    $TTL    86400
    @       IN      SOA     srv.dom. root.srv.dom.  (
                                      20180128 ; Serial
                                      28800      ; Refresh
                                      14400      ; Retry
                                      3600000    ; Expire
                                      86400 )    ; Minimum
              IN      NS      srv.dom.

          IN      A     192.168.0.127
>

Прописываем зоны в */etc/bind/named.conf*

    zone "dom" {
        type master;
        file "/etc/bind/dom/named.dom";
    };
    zone "ftp" {
        type master;
        file "/etc/bind/dom/db.ftp";
    };

>

Запускаем **bind** на сервере **srv**

    sudo /etc/init.d/bind9 restart

Теперь создаем файл */etc/resolv.conf* на всех машинах с которых нужно обращаться по именам

    search dom
    nameserver 192.168.0.1

Пробуем

    ping ftp
    ping ftp.dom
    ping db.dom