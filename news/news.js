//
// /news/index.html to /index.html
//
function addMsg(r, p){
  var text, html;
  var root = document.createElement('div');
  var content = document.createElement('div');
  root.appendChild(content);
  content.className = 'msgtext';
    // to markdown
  text = r
    .replace(/\/photos\//g, '/fotos/')
    .replace(/\r\r\n/g, '\n')
    .replace(/\r*\n>\r*\n*/g, '\n<p></p>\n')
    .replace(/\{: class=rounded :\}/g, '');
  html = converter.makeHtml(text);
  content.innerHTML += html;
  var footer = document.createElement('div');
  root.appendChild(footer);
  footer.className = 'msgfooter';
  var ps = document.createElement('div');
  footer.appendChild(ps);
  ps.className = 'gray smaller';
  ps.appendChild(document.createTextNode(p.title[3]));
  return root.innerHTML;
}
//
// Append news from .txt
//
function addNews(){
  var p = document.createElement('p');
  document.getElementById('page_content').appendChild(p);
  p.className = 'mtext hspace';
  p.appendChild(document.createTextNode('Что нового? Новости, изменения, обновления на сайте и не только.'));

  loadScript({url: '/news/index.js'}, function(p){
    var subjects = SUBJ,
        titles = TITLES;
    var per_page = 5,
        page_num = urlParams().page||1,
        page_bottom = (page_num-1)*per_page,
        page_top = page_bottom+per_page;
    var page_titles = titles.slice(page_bottom, page_top);
    for(var i=0; i<page_titles.length; i++){
      var subj = subjects[ parseInt(page_titles[i][0]) ], // skip lead 0
          title = page_titles[i][2];
      var wrap = document.createElement('div');
      wrap.id = 'msg' + i;
      document.getElementById('page_content').appendChild(wrap);
      upfunc({id: wrap.id, subj: subj, title: page_titles[i], url: '/news/' + subj + '/' + title + '.txt'}, function(r, p){
        var el = document.getElementById(p.id);
        el.className = 'wrap';
        el.innerHTML = addMsg(r, p);
          // add description meta
        if(p.id == 'msg0'){
          var meta = document.head.getElementsByTagName('meta');
          for(var j in meta){
            if(meta[j].name == 'description') meta[j].content = el.innerHTML.replace(/(<([^>]+)>)/gi, "");
          }
        }
      });
    }
    if (!page_titles.length){
      var p = document.createElement('p');
      document.getElementById('page_content').appendChild(p);
      p.className = 'mtext hspace';
      p.appendChild(document.createTextNode('Нет данных.'));
    } else
      document.getElementById('page_footer').appendChild(addPaginator(titles, per_page, page_num));
  });
}