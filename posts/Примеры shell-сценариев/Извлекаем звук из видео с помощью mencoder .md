<!--2019-10-05 22:42:55-->
Извлекаем и обрезаем дорожку по времени от начала (-ss) с длительностью в сек (-endpos), а также увеличиваем громкость трека га 10 дб (-af volume=10:0)

    mencoder v.mp4 -ss 56 -endpos 190 -af volume=10:0 -of rawaudio -oac mp3lame -ovc copy -o a.mp3