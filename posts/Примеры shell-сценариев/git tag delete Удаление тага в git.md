<!--2020-03-21 16:11:37-->
Удаление тага (с названием mytag) в локальном и удаленном репозиториях git

    git tag -d mytag
    git push origin :refs/tags/mytag

Другой вариант

    git push --delete origin mytag
    git tag -d mytag