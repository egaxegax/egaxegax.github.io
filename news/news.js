//
// /news/index.html to /index.html
//
function addMsg(r, p){
  var converter = new showdown.Converter(),
      text = r
        .replace(/\/photos\//g, '/fotos/')
        .replace(/\r\r\n/g, '\n')
        .replace(/\r*\n>\r*\n*/g, '\n<p></p>\n')
        .replace(/\{: class=rounded :\}/g, ''),
      html = converter.makeHtml(text);
  var meta = document.head.getElementsByTagName('meta');
  for(var j in meta){
    if(meta[j].name == 'description') meta[j].content = html.replace(/(<([^>]+)>)/gi, '').slice(0,255);
  }
  document.getElementById(p.id).innerHTML = 
'<div class="msgtext">'+html+'</div>'+
'<div class="msgfooter">'+
  '<div class="gray smaller">'+' '+buildDate(p.title[3])+'</div>'+
'</div>';
}
//
// Append news from .txt
//
function addNews(){
  var tmpl =
'<p class="mtext hspace">'+
  'Что нового? Новости, изменения, обновления на сайте и не только.'+
'</p>';
  loadScript({url: '/news/index.js'}, function(p){
    var subjects = SUBJ,
        titles = TITLES;
    var per_page = 7,
        page_num = urlParams().page||1,
        page_bottom = (page_num-1)*per_page,
        page_top = page_bottom+per_page;
    var page_titles = titles.slice(page_bottom, page_top);
    for(var i=0; i<page_titles.length; i++){
      var subj = subjects[ parseInt(page_titles[i][0]) ][0], // skip lead 0
          title = page_titles[i][2];
      document.getElementById('page_content').innerHTML += 
    '<div id="msg'+i+'">'+
      (i==0 ? '<img class="hspace1" src="/static/img/loader.gif">' : '')+
    '</div>';
      upfunc({id: 'msg'+ i, subj: subj, title: page_titles[i], url: '/news/' + subj + '/' + title + '.txt'}, function(r,p){
        var wrap = document.getElementById(p.id);
        wrap.className = 'wrap';
        addMsg(r,p);
      });
    }
    if (page_titles.length){
      document.getElementById('page_footer').innerHTML = addPaginator(titles, per_page, page_num);
    } else {
      document.getElementById('page_content').innerHTML += 
    '<p class="mtext hspace">'+
      'Нет данных.'+
    '</p>'+
    '<img src="/static/img/confuse.png" width="120px">';
    }
  });
  return tmpl;
}