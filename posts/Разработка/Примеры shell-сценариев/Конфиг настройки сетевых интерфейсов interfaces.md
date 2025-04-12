<!--2020-04-06 11:44:11-->
## Конфиг настройки сетевых интерфейсов interfaces
Конфиг настройки локальной сети */etc/networking/interfaces*
    
    auto lo eth0 eth1
    iface lo inet loopback
    
    iface eth0 inet static
        address 172.16.0.126
        netmask 255.255.252.0
        gateway 172.16.0.1
        broadcast 172.16.0.255
    
    iface eth1 inet static
        address 172.16.2.126
        netmask 255.255.252.0
        gateway 172.16.2.1
        broadcast 172.16.2.255
    