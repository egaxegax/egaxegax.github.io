<!--2023-12-16 11:43:22-->
## Запись ISO-образа на флэшку

    dd if="./filename.iso" of="/dev/sdb" status="progress" conv="fsync"
