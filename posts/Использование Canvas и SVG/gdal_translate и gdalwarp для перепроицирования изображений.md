<!--2014-04-06 19:44:46-->
### gdal_translate и gdalwarp для перепроицирования изображений
В составе проекта [GDAL](http://gdal.org) есть полезные утилиты для работы с изображениями через консоль

* gdal_translate
* gdalwarp

В среде Windows они доступны, например, в сборке программ [MS4W](http://www.ms4w.com/download.html#download).

Для своего проекта dbCartajs мне потребовались изображения для разных проекций. Изображения я хочу вывести на канвас вместе с векторными данными. Для этого цели из программы Orbitron я позаимствовал картинку с плоской картой Земли в небольшом разрешении.

![worldmap.jpg](http://img-fotki.yandex.ru/get/9802/136640652.0/0_e0110_1d7bbe1b_XL.jpg)

Она отлично подходит для экспериментов, но как быть с другими проекциями - меркатор, сфера? Я нашел несколько картинок в разных проекциях, но все они оказались в разных цветовых сочетаниях и разрешениях, поэтому решил попробовать самостоятельно преобразовать исходную картинку с помощью утилит gdal, используя их описание и примеры.

Сначала, преобразуем исходную картинку в формат tiff - родной формат gdal - и задаем координаты привязки изображения.

    gdal_translate -of Gtiff -co "TFW=YES" -a_ullr -180 90 180 -90 worldmap.png worldmap.tif

Для проекции Меркатора нужно ограничить размеры на полюсах (80-85 градусов).

    gdal_translate -of Gtiff -projwin -180 84 180 -84 worldmap.tif worldmap-1.tif

Теперь формируем изображение в проекции Меркатора в формате tiff.

    gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3857 worldmap-1.tif worldmap-merc.tif 

Браузер не работают с tiff, поэтому переводим его в jpeg.

    gdal_translate -of JPEG worldmap-merc.tif worldmap-merc.jpg

Вот результат

![worldmap-merc.jpg](http://img-fotki.yandex.ru/get/9802/136640652.0/0_e0111_1a993774_XL.jpg)

Аналогично получаем картинки для других проекций, например ortho.

    gdalwarp -s_srs EPSG:4326 -t_srs "+proj=ortho +lon_0=0 +lat_0=0" worldmap-1.tif worldmap-ortho.tif
    gdal_translate -of JPEG worldmap-ortho.tif worldmap-ortho.jpg

![worldmap-ortho.jpg](http://img-fotki.yandex.ru/get/9816/136640652.0/0_e0112_e8d7e76f_L.jpg)