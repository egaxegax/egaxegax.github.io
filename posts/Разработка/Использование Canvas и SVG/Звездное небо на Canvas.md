<!--2013-08-10 19:13:59-->
## Звездное небо на Canvas
В этой статье я хочу более подробно рассказать о примере [Starry Sky](http://dbcartajs.appspot.com/starry.html) (Звездное Небо), реализованном с помощью скриптов [dbCartajs](http://dbcartajs.appspot.com). Starry Sky включает в себя идеи других "звездных" проектов, которые были портированы на JavaScript. Рассмотрим их подробнее. Алгоритм формирования звездного неба был позаимствован из проекта Marble KDE (плагин stars), расчет положения планет построен на основе замечательной статьи шведского астронома [Поля Шлетера](http://stjarnhimlen.se/comp/ppcomp.html), модель движения космических аппаратов SGP4/SDP4 предоставлена модулем satellite-js (проект в github), формулы солнечного терминатора (ночной зоны) взяты с [астрономического форума](http://www.astronomy.ru/forum/index.php/topic,70976.msg1145154.html). Вид орбит как эллипсов подсмотрен у Сelestia.

Пример имеет чисто технологическое назначение: вывести в заданное время точку положения космического аппарата при заданных орбитальных параметрах. В Canvas это получилось очень красиво и я решил подробнее написать об этом. Если нужно что-то поменять в выводе объектов, настройках не нужно перекомпилировать программу как Marble или Xephem (и соответственно устанавливать компилятор или среду разработки) достаточно иметь лишь браузер. В Mozilla или Chrome уже есть встроенные панели отладки, где можно посмотреть, скажем, массив точек траектории аппарата. Это гораздо удобнее чем "вытаскивать" их из C-й.

## Управление

Вращение Земли происходит по клику в любой точке глобуса. В демо предусмотрен авторежим с ускорением времени (1 сек~15 минут, кнопка play рядом с датой). Анимацию с суточным периодом можно посмотреть [здесь](http://img-fotki.yandex.ru/get/9115/136640652.0/0_bf3ec_c1eb0a8_orig), простой скриншот приведен ниже.

![Starry Sky](http://img-fotki.yandex.ru/get/9555/136640652.0/0_becbd_66ad485b_XL.png)