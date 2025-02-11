<!--2018-10-29 21:23:47-->
### iframe с autoheight по содержимому
Тэг *iframe* с автовыравниванием по содержимому

    <iframe frameborder=0 width="100%" height="this.height=this.contentWindow.document.body.scrollHeight" src="/">
    </iframe>

Пример

    <iframe frameborder=0 scrolling=no width="100%" height="this.height=this.contentWindow.document.body.scrollHeight" src="/"></iframe>