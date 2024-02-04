<!--2020-03-21 16:11:37-->
### git tag push Работа с тагами в git
Добавление тага в локальный репозиторий *git*

    git tag <tag_name>

Добавление в удаленный репозиторий

    git push <tag_name>

Удаление тага в локальном и удаленном репозиториях *git*

    git tag -d <tag_name>
    git push origin :refs/tags/<tag_name>

Другой вариант

    git push --delete origin <tag_name>
    git tag -d <tag_name>
