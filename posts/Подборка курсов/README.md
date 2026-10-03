<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><p>Задача довольно проста: у нас есть число и слово в трех склонениях, надо выбрать верно склонение в зависимости от числа.<br> Например: <code>1 дерево, 2 дерева, 15 деревьев</code></p> <script src="https://gist.github.com/m5wdev/03bce6f8875b922255451883290238a1.js"></script></div>
  <p class="titl"><a href="http://dev-ed.ru/blog/rus-plural-words-python/">Склонение слов во множественном числе с помощью Python</a></p>
</div><!--n:DevEducation/Склонение слов во множественном числе с помощью Python:s:0:e:684-->
<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><pre> uv --version uv self update </pre></div>
  <p class="titl"><a href="http://dev-ed.ru/blog/update-uv-in-win11/">Как обновить uv Python  в Windows 11?</a></p>
</div><!--n:DevEducation/Как обновить uv Python в Windows 11:s:812:e:270-->
<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><pre> from urllib.request import urlopen, Request url = 'https://jsonplaceholder.typicode.com/posts' # url = 'https://google.com' http_request = Request(url) with urlopen(http_request) as response: print(response.status) print(response.read().decode()) </pre></div>
  <p class="titl"><a href="http://dev-ed.ru/blog/how-to-fetch-url-without-requests-module/">Как получить данные из url без модуля requests в Python</a></p>
</div><!--n:DevEducation/Как получить данные из url без модуля requests в Python:s:1164:e:546-->
<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><p>Предположим что вы используете несколько баз данных в вашем проекте, одна из них основная, другая уже содержит какие-то данные.</p> <p>При работе с основной БД вы часто будете использовать команды:</p> <pre> …</div>
  <p class="titl"><a href="http://dev-ed.ru/blog/django-models-managed-false/">Что означает managed=False в models.py Django?</a></p>
</div><!--n:DevEducation/Что означает managed False в models.py Django:s:1830:e:619-->
<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><p>Docker по-умолчанию сохраняет логи ваших контейнеров в /var/lib/docker/containers/</p> <p>Узнать их размер можно с помощью:</p> <pre> du -sh /var/lib/docker/containers/* </pre> <p>Очистить логи:</p> <pre> sudo find /var/lib/docker/containers/ -name "*-json.log" -exec truncate -s …</div>
  <p class="titl"><a href="http://dev-ed.ru/blog/clear-logs-docker/">Команды для очистки логов в контейнерах Docker</a></p>
</div><!--n:DevEducation/Команды для очистки логов в контейнерах Docker:s:2542:e:626-->
<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><pre> sudo apt update sudo apt install docker.io docker-compose-v2 docker-buildx -y sudo systemctl enable --now docker sudo hash -r </pre> <p>Проверьте версии:</p> <pre> docker version docker compose version </pre></div>
  <p class="titl"><a href="http://dev-ed.ru/blog/how-to-install-docker-compose-v2-ubuntu/">Как установить Docker Compose V2 на Ubuntu</a></p>
</div><!--n:DevEducation/Как установить Docker Compose V2 на Ubuntu:s:3284:e:488-->
<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><p>Установите npm-check-updates:</p> <pre> npm i -g npm-check-updates </pre> <p>Далее будут доступны команды:</p> <pre> ncu -u npm install </pre> <p>Стандартный способ:</p> <pre> npm outdated npm update </pre></div>
  <p class="titl"><a href="http://dev-ed.ru/blog/update-node-packages/">Как обновить все пакеты в Node.js?</a></p>
</div><!--n:DevEducation/Как обновить все пакеты в Node.js:s:3865:e:499-->
<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><script src="https://gist.github.com/m5wdev/9ff36b765f650d26fe8376e8dc8ee28d.js"></script></div>
  <p class="titl"><a href="http://dev-ed.ru/blog/flatten-list-iterative-python/">Как "сжать" список любой вложенность итеративно в Python?</a></p>
</div><!--n:DevEducation/Как сжать список любой вложенность итеративно в Python:s:4454:e:380-->
<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><p>Иногда возникают проблемы при установке ПО на Win 11 через стандартный installer. Поэтому проще воспользоваться winget.</p> <p>Рассмотрим на примере NodeJS:</p> <pre> winget source reset --force winget install OpenJS.NodeJS.LTS --version 24.14.1 …</div>
  <p class="titl"><a href="http://dev-ed.ru/blog/install-software-with-winget/">Установка программ с помощью winget</a></p>
</div><!--n:DevEducation/Установка программ с помощью winget:s:4965:e:604-->
<!----><!--2026-10-01 20:28:06-->
<div class="yb">
  <div class="rss mw_f scroll dev_ed"><p class="codepen" data-height="430" data-default-tab="js,result" data-slug-hash="MWNvoJd" data-pen-title="Untitled" data-user="m5dev" style="height: 425.142822265625px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border: 2px solid; margin: 1em 0; padding: 1em;"> <span>See the Pen <a href="https://codepen.io/m5dev/pen/MWNvoJd"> …</div>
  <p class="titl"><a href="http://dev-ed.ru/blog/js-copy-text-to-clipboard/">Копировать текст в буфер обмена с помощью JS</a></p>
</div><!--n:DevEducation/Копировать текст в буфер обмена с помощью JS:s:5665:e:641-->
