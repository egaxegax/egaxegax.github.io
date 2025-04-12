<!--2022-01-03 01:46:05-->
## Просмотр заряда батареи ноутбука в консоли Linux
Печатаем заряд батареи *BAT1* в ваттах и процентах

    cat /sys/class/power_supply/BAT1/energy_full
    cat /sys/class/power_supply/BAT1/energy_now
    cat /sys/class/power_supply/BAT1/capacity
    cat /sys/class/power_supply/BAT1/status

Вывод

    28390000
    26360000
    92
    Discharging
    