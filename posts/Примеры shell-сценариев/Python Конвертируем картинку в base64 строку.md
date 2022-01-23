<!--2016-07-23 11:15:01-->
Скрипт для конвертирования изображений в base64-строку для использования в теге img. 
Тип в data берем из расширения файла.

    #!python
    # base64 encode image

    import sys, os.path
    import base64

    img = file(sys.argv[1], "rb")
    ext = os.path.splitext(sys.argv[1])[1][1:]
    print ( "data:image/" + ext + ";base64," + base64.b64encode(img.read()) )