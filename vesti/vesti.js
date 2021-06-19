//
// /vesti/index.html to /index.html
//
function addMsg(r, p){
  var converter = new showdown.Converter(),
      text = r
        .replace(/\/photos\//g, '/fotki/')
        .replace(/\r\r\n/g, '\n')
        .replace(/\r*\n>\r*\n*/g, '\n<p></p>\n')
        .replace(/\{: class=rounded :\}/g, ''),
      html = converter.makeHtml(text);
  var meta = document.head.getElementsByTagName('meta');
  for(var j in meta){
    if(meta[j].name == 'description' && p.if) meta[j].content = html.replace(/(<([^>]+)>)/gi, '').slice(0,255);
  }
  document.getElementById(p.id).innerHTML = 
'<div class="msgtext">'+html+'</div>'+
'<div class="msgfooter">'+
  '<div class="gray">'+' '+buildDate(p.title[3])+'</div>'+
'</div>';
}
//
// Append vesti from .txt
//
function addNews(){
  loadScript({url: '/vesti/index.js'}, function(p){
    var roots = ROOTS,
        subjects = SUBJ,
        msgs = TITLES;
    for(var p in urlParams()){
      var pp = p.split('/');
      console.log(pp);
      if(p == 'page' && urlParams().page){ // ?page
        // paginate
      }else if(pp.length>1){ // ?subj/msg
        msgs = msgs.filter(function(tit){ return (tr(subjects[tit[0]][0])==pp[0] && tr(tit[2])==pp[1]); });
      }else if(pp.length>0){ // ?subj
        msgs = msgs.filter(function(tit){ return (tr(subjects[tit[0]][0]) == pp[0]); });
      }
    }
    var per_page = 7,
        page_num = urlParams().page||1,
        page_bottom = (page_num-1)*per_page,
        page_top = page_bottom+per_page;
    var page_titles = msgs.slice(page_bottom, page_top);
    document.getElementById('page_content').innerHTML = '';
    for(var i=0; i<page_titles.length; i++){
      var subj = subjects[ parseInt(page_titles[i][0]) ][0], // skip lead 0
          root = roots[page_titles[i][4]][0],
          title = page_titles[i][2];
      document.getElementById('page_content').innerHTML += 
    '<div id="msg'+i+'">'+
      (i==0 ? '<img class="hspace1" src="/static/img/loader.gif">' : '')+
    '</div>';
      upfunc({id: 'msg'+ i, if: i==0, subj: subj, title: page_titles[i], url: '/vesti/'+root+'/'+subj+'/'+title+'.txt'}, function(r,p){
        var wrap = document.getElementById(p.id);
        wrap.className = 'wrap';
        addMsg(r,p);
      });
    }
    if (page_titles.length){
      document.getElementById('page_footer').innerHTML = addPaginator(msgs, per_page, page_num);
    } else {
      document.getElementById('page_content').innerHTML += 
    '<div class="mtext hspace">Нет данных </div>'+addImgConfuse();
    }
  });
}