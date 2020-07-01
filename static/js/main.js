// 
//  Add body tags (header, ontent, footer)
//
function addBodyTags(sel){
  document.body.className = 'nomarg';
  var header = document.createElement('div');
  document.body.appendChild(header);
  header.id = 'header';
  header.className = 'main wrapbg';
  var ul = document.createElement('ul');
  header.appendChild(ul);
  ul.className = 'nomarg mtext';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'about';
  li.className = 'inl' + (sel == 'about' ? ' wrap3' : '');
  var li = document.createElement('li');
  ul.appendChild(li);
  li.className = 'inl hspace';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'news';
  li.className = 'inl hspace ' + (sel == 'news' ? ' wrap3' : '');
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'posts';
  li.className = 'inl hspace ' + (sel == 'posts' ? ' wrap3' : '');
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'fotos';
  li.className = 'inl hspace' + (sel == 'fotos' ? ' wrap3' : '');
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'chords';
  li.className = 'inl hspace' + (sel == 'chords' ? ' wrap3' : '');
  var li = document.createElement('li');
  ul.appendChild(li);
  li.className = 'inl';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'login';
  li.className = 'inl' + (sel == 'login' ? ' wrap3' : '');
  var content = document.createElement('div');
  document.body.appendChild(content);
  content.id = 'content';
  content.className = 'main';
  var contview = document.createElement('div');
  content.appendChild(contview);
  contview.className = 'view';
  var pageheader = document.createElement('div');
  contview.appendChild(pageheader);
  pageheader.id = 'page_header';
  var pagecontent = document.createElement('div');
  contview.appendChild(pagecontent);
  pagecontent.id = 'page_content';
  var footer = document.createElement('div');
  document.body.appendChild(footer);
  footer.id = 'footer';
  footer.className = 'main';
  var mtab = document.createElement('table');
  footer.appendChild(mtab);
  mtab.width = '100%';
  var tb = document.createElement('tbody');
  mtab.appendChild(tb);
  var row = document.createElement('tr');
  tb.appendChild(row);

  var col = document.createElement('td');
  col.align = 'right';
  col.width = '45%';
  col.style.fontSize = 'smaller';
  var el = document.createElement('a');
  el.href = '/about.html';
  el.appendChild(document.createTextNode('egaxegax'));
  col.appendChild(document.createTextNode(' © 2011-2020 '));
  col.appendChild(el);
  row.appendChild(col);

  var col = document.createElement('td');
  col.align = 'center';
  col.width = '10%';
  row.appendChild(col);

  var col = document.createElement('td');
  col.align = 'left';
  col.width = '45%';
  var el = document.createElement('div');
  el.className = 'share42init';
  col.appendChild(el);
  row.appendChild(col);
    //
  upfunc({url: '/static/img/about.svg'}, false, 'about');
  upfunc({url: '/static/img/news.svg'}, false, 'news');
  upfunc({url: '/static/img/posts.svg'}, false, 'posts');
  upfunc({url: '/static/img/fotos.svg'}, false, 'fotos');
  upfunc({url: '/static/img/songs.svg'}, false, 'chords');
  upfunc({url: '/static/img/login.svg'}, false, 'login');
}
//
// Add META tags (description, keywords, author) to page.
//
function addMetaTags(text){
  if (text) {
    var meta = document.createElement('meta');
    meta.name = 'description';
    meta.content = text
    document.head.appendChild(meta);
  }
  var meta = document.createElement('meta');
  meta.name = 'keywords';
  meta.content = 'записки, сообщения, комментарии, новости, тексты, заметки, фото';
  document.head.appendChild(meta);
  
  var meta = document.createElement('meta');
  meta.name = 'author';
  meta.content = 'Grigoriy Eremin, Григорий Еремин, egax@bk.ru';
  document.head.appendChild(meta);
  
  var meta = document.createElement('meta');
  meta.name = 'google-site-verification';
  meta.content = 'eWwGSnvveM7GniusD-nYN2KXBDPtXBHmhKRezn_TBg8';
  document.head.appendChild(meta);

  var meta = document.createElement('meta');
  meta.name = 'yandex-verification';
  meta.content = 'bf07f0af8e739c66';
  document.head.appendChild(meta);
  
};
