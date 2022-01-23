<!--2012-11-14 19:59:57-->
Примеры как работать с индексами таблиц для ускорения выборки данных. Для примера возьмем таблицу "grade" (данные по классам учеников школ) с 2,5 млн. записей. Тесты проводились на PostgreSQL 7.4.1.

Структура таблицы и индекса:

    ::::sql
    CREATE TABLE "grade" 
    (
      "id_school" integer,
      "id_class" integer,
      "sum_count" integer,
      "year_num" integer,
      "male_ratio" double precision,
      "avg_score" double precision
    )
    WITH OIDS;
     
    CREATE INDEX "grade_index" 
      ON "grade" 
      USING btree
      ("id_class", "id_school", "sum_count", "year_num", "male_ratio");

Запросы к таблице. Работает или нет индекс определяем по `explain`:

    ::::sql
    --индекс работает - время < 0.5 сек - ~ 300 тыс. строк
    select * from "grade" where "id_class"=14 and "id_school"=1 and "sum_count"=14;
    --индекс не работает - время > 2 сек - ~ 600 тыс. строк
    select * from "grade" where "id_class"=14 and "id_school"=1;
    select * from "grade" where "id_class"=14;
     
    --индекс работает
    select * from "grade" where 
        (id_class=14 and id_school=14 and year_num>0 and sum_count=14) or
        (id_class=1 and id_school=1 and year_num>2000 and sum_count=14) or
        (id_class=14 and id_school=2 and year_num>2000 and sum_count=14) 
    and male_ratio between 1 and 200 limit 100;
    
    --индекс не работает
    select * from "grade" where 
        (id_class=14 and id_school=14 and year_num>0 and sum_count>0);

Индекс работает на равно (=) когда число полей в запросе больше половины числа полей в индексе. Чувствителен к операциям множеств (>,<,BETWEEN) и конструкции IN (ее нужно заменить на комбинацию с OR).