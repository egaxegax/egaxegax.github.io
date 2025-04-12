<!--2013-01-16 20:20:27-->
## Перекодировка файлов из Windows в Linux
При копировании файлов с кириллицей из *Windows* в *Linux* их содержимое может быть не читабельным. Конвертим их, например, в *utf8*:

    #!/bin/bash
    # 
    # Конвертим рекурсивно файлы из кодировки Windows в Юникод из каталога $1
    
    export TMP_F=`mktemp`
    
    trap "rm -f $TMP_F" EXIT
    
    find "$1" -name \*.txt -print|while read x
    do 
        echo $x
        iconv -f cp1251 -t utf8 "$x">$TMP_F && cat $TMP_F > "$x"
    done