<!--2013-07-02 20:51:25-->
## Заметки, отзывы, планы проекта карты dbCartajs
Идея проекта создать инструмент отображения географических объектов (имеющих координаты), который можно было бы использовать на любых платформах для отладки и разработки более сложных геоинформационных систем.

Демо и исходники доступны на [dbcartajs.appspot.com](http://dbcartajs.appspot.com).

dbCartajs для рисования использует объект Canvas, который доступен в новых версиях браузеров, поддерживающих разметку HTML5.

Для пересчета координат из одной проекции в другую используется код [Proj4js](http://trac.osgeo.org/proj4js/). В версии 1.0 доступны следующие проекции:

* merc (Меркатор)
* ortho (Ортографическая)
* laea (Азимутальная проекция Ламберта)

Проекции пересчитываются из плоских декартовых координат longlat. Если скрипты Proj4js не подключены доступна только плоская проекция longlat.