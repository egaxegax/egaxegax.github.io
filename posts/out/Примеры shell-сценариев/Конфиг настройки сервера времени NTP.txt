<!--2020-04-06 11:38:04-->
Конфиг */etc/ntp/ntp.conf*

    # master

    # server srv
    # server 127.127.1.0
    # fudge 127.127.1.0 stratum 10
    # restrict default kod noquery nomodify notrap
    # restrict 127.0.0.1 mask 255.255.255.255 
    # restrict 0.0.0.0 mask 255.255.0.0 
    # logconfig +syncall
    # broadcastdelay 4
    # broadcastclient
    # driftfile /var/lib/ntp/ntp.drift


    # client

    # server srv minpoll 6 maxpoll 10 version 4 prefer
    # server pc1 minpoll 6 maxpoll 10 version 4
    # restrict default
    # logconfig +syncall
    # broadcast 0.0.0.0 minpoll 6 version 4 ttl 127
    # broadcastclient
    # driftfile /var/lib/ntp/ntp.drift

Для запуска мастера (раздающего) нужно раскомментировать что ниже # master, для клиента (синхронизируемого) что ниже клиента и перезапустить сервер

    service ntp restart

или 

    systemctl restart ntpd
