<!--2016-06-06 21:49:40-->
### PostgreSQL Репликация кластера
Про настройку репликации мастер-слэйв в Postgresql написано много и довольно давно. Выделю лишь [этот](https://habrahabr.ru/post/106872/) пост на Хабре для примера. Важно различать, что репликация и "горячий бэкап" настраиваются и работают отдельно. Репликация - это синхронизация данных серверов слэйвов с мастером в режиме одновременной работы. В случае запуска слэйва после длительной остановки (достаточно 2-3 часов при активных изменениях на мастере) синхронизация с мастером прекращается, поскольку требуемые файлы изменений (транзакций) на мастере уже были удалены и возникает ощибка чтения на слэйве. В этом случае потребуется выполнить полное копирование кластера с мастера на слэйв (выполнить перебазирование) и перезапустить слэйв для старта репликации.

Для избежания этого нужна настройка "горячего резерва" - каталога, где будут храниться все файлы изменений на мастере (WAL-файлы) и откуда они будут считываться в случае прерывания репликации на слэйве.

Включение "горячего" резерва на мастере в *postgresql.conf*.

    archive_mode=on
    archive_command=cp '%p /mnt/disk/home/wal_arc/%f'

Ниже приведен текст скрипта для Ubuntu создания зеркала (на слэйве) для базы данных на мастере. 

	#!/bin/bash
	#
	# Создаем кластер для репликации на слэйве
	#
	# На мастере нужно внести правки в postgresql.conf
	#   wal_level = hot_standby
	#   max_wal_senders = 2
	#   wal_keep_segments = 32
	#   checkpoint_segments = 16
	# В pg_hba.conf добавить
	#   host    replication     postgres        0.0.0.0/0            md5
	#
	# На слэйве внести в postgresql.conf
	#   hot_standby = on

	export PGUSER=postgres
	export PGPASSWORD=postgres

	service postgresql stop

	pgconf=/etc/postgresql/9.3/main/postgresql.conf

	cat $pgconf | sed -e 's/^\#\(hot_standby =\) off/\1 on/' > $pgconf.tmp
	[ -s $pgconf.tmp ] && { 
	    mv $pgconf.tmp $pgconf
	    chown postgres:postgres $pgconf
	    chmod 640 $pgconf
	}

	rm -fr /home/pgrepl
	pg_basebackup --host=192.168.0.5 -R -P -D /home/pgrepl || exit 1

	chown -R postgres:postgres /home/pgrepl

	clusterdir="/var/lib/postgresql/9.3/main"
	[ -d "$clusterdir" ] && mv $clusterdir $clusterdir.0

	ln -s /home/pgrepl $clusterdir

	service postgresql start

Базы данных на созданном кластере на слэйве будут доступны только на чтение и синхронно отражать изменения по запросам INSERT - UPDATE - DELETE, выполняемые на мастере. 

В случае восстановления в базу данных на слэйве дампа базы, созданного pg_dump'ом, кроме дампа, созданного с параметрами "Использовать команды Insert", зеркало перестает синхронизироваться с мастером и работает только на чтение. 

В случае создания в кластере слэйва триггер-файла и перевода баз в режим чтение-запись, обратно в режим зеркала (доступ на чтение и синхронизация с мастером) уже нельзя.

После создания зеркала на слэйве нужно создать файл *recovery.conf* для запуска потоковой репликации и восстановления из "горячего" резерва (команда restore_command) одновременно.

    standby_mode='on'
    primary_conninfo='host=pc1 user=postgres password=postgres'
    trigger_file='/home/pg_repl/trigger_file'
    #restore_command='curl -v ftp://pc1/home/wal_arc/%f -o "%p"'
    restore_command='cp /mnt/disk/home/wal_arc/%f -o "%p"'