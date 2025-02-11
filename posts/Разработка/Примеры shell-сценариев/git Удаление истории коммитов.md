<!--2025-02-09 00:54:01-->
### git Удаление истории репозитория

Очистка всей истории репозитория гита.

Создаем временный бранч

    $ git checkout --orphan temp_branch

Коммит во временный бранч

    $ git add -A
    $ git commit -am "Новый первый коммит"

Удаляем бранч *master*

    $ git branch -D master

Переименовываем временный бранч в *master*

    $ git branch -m master

Принудительно обновляем удаленный репо

    $ git push -f origin master
