<!--2016-11-30 20:26:58-->
Простой скрипт, использующий интерпретатор expect для удаленного подключения к хосту по *ssh* без ввода пароля. Подключается, выводит информацию о системе через *uname*, закрывает соединение.

    #!/usr/bin/expect -f
    
    set timeout 2
    set USER "agena"
    set HOST "3"
    set PASS "12345678"
    
    spawn ssh $USER@192.168.0.$HOST
    expect {
    "(yes/no)?*" {
    send "yes\r"
    }
    }
    expect "word:"
    send "$PASS\r"
    expect "$*"
    send "uname -a\r"
    expect "$*"
    send "exit\r"
    expect eof