<!--2013-10-01 20:22:22-->
Конвертор mp3-файлов в VBR-формат с хорошим качеством и небольшим размером.

Удобен для сжатия mp3-файлов с большим битрейтом (256, 320 Кб/с). Использует утилиты *lame* и *id3info*.

    #!/bin/bash
    #
    # Конвертор mp3-файлов в VBR-битрейт
    # Вызов: bash mp3conv [каталог_с_mp3]
    # egax
    
    parse_tag ()
    {
        retval=$(echo "$1" | grep -P "$2" | iconv -f CP1251 -t UTF-8)
        expr match "$retval" ".*:[ \\t]*\(.*\)"
    }
    
    cd "$1"
    for curfile in *.mp3; do
        tag=$(id3info "$curfile")
    
        # берем поля тага
        title=$(parse_tag "$tag" TIT2)
        artist=$(parse_tag "$tag" TPE1)
        track=$(parse_tag "$tag" TRCK)
        year=$(parse_tag "$tag" TYER)
        album=$(parse_tag "$tag" TALB)
    
        newfile="$curfile"
        # новое имя файла $artist - [$track_]$title.mp3
        if [ ! -z "$artist" ] && [ ! -z "$title" ]; then
            if [ ! -z $track ]; then
                [ $track -lt 10  ] && track=0"$track"
                title="$track"_"$title"
            fi
            newfile="$artist"" - "$title".mp3"
        fi
    
        dirname=1
        # имя папки для новых файлов [$year_]$album
        if [ ! -z "$album" ]; then
            [ -z $year ] || album="$year"_"$album"
            dirname="$album"
        fi
    
        # создаем папку если не создана
        [ -d "$dirname" ] || mkdir "$dirname"
        newfile="$dirname"/"$newfile"
    
        # конвертим файл с VBR-битрейдом и копируем таги v2 и v1
        lame --vbr-new -B 192 "$curfile" "$newfile"
        id3cp -2 "$curfile" "$newfile"
        id3cp -1 "$curfile" "$newfile"
    done