//
// array sort function from https://www.zachleat.com/web/array-sort/
//
function arraySort(aa,bb){
  var a=( ''+aa ).toLowerCase(),
      b=( ''+bb ).toLowerCase();
  if(a > b) return 1;
  if(a < b) return -1;
  return 0;
}
//
// change action link href to light/dark css
//
function actionChStyle(p){
  document.querySelectorAll("link[href^='/static/css/"+p+"']").forEach(function(e){
    localStorage.setItem('THEME_URL_'+window.location.pathname, e.href='/static/css/'+p+(e.href.search(p+'.dark.css')>-1 ? '.css' : '.dark.css'));
  });
}
//
// set link action to light/dark css
//
(function actionSetStyle(t){
  if(t=localStorage.getItem('THEME_URL_'+window.location.pathname)){
    document.querySelectorAll("link[href^='"+t.slice(0,t.indexOf('.'))+"']").forEach(function(e){ e.href = t; });
  }
})()
//
// find action
//
function actionFind(){
  if(!document.getElementById('tfind').value){
    document.getElementById('tfind').setCustomValidity("Заполните пустое поле");
  }else{
    window.location = window.location.pathname + '?find='+ document.getElementById('tfind').value;
  }
}
//
// return html for find input
//
function addFinder(p){ return ''+
  '<input id="tfind" maxlength="100" size="5" type="text" placeholder="&#128269;" onkeydown="if(event.keyCode==13) { event.preventDefault(); actionFind(); return false; }">'+
  '<button class="rounded chstyle dark" onclick="actionChStyle(\''+p+'\')" title="">&#9680;</button>'; 
}
//
// return loader image html
//
function addLoader(bl){ return (bl ? '<div class="main">&emsp;<img class="rounded loader" src="/static/img/loader.gif"></div>' : ''); }
//
// return html for paginator
//
function addPaginator(list, page, page_btn){
  var page_num = parseInt(page.num);
  var num_pages = Math.ceil(list.length / page.per),
      has_previous = page_num > 0,
      has_first = (page_num == 1),
      has_next = page_num < (num_pages-1),
      prev_page_num = page_num - 1,
      next_page_num = page_num + 1;
  var root = 
'<p class="paginator tcenter">'+
(has_previous ? 
  '<a class="nodecor" href="?'+urlBuild({page: has_first ? 'null' : prev_page_num})+'"><span class="bigger2">&larr;&nbsp;</span> </a>'
: 
(has_next ? 
  '<span class="gray"><span class="bigger2">&larr;&nbsp;</span></span>'
: 
  ''))+
(num_pages > 1 ?
  '<span> <b><i>'+String(page_num+1)+'</i></b> &nbsp; '+(page_btn||'из')+' &nbsp; <b><i>'+String(num_pages)+'</i></b> </span>'
:
  '')+
(has_next ? 
  '<a class="nodecor" href="?'+urlBuild({page: next_page_num})+'"> <span class="bigger2">&nbsp;&rarr;</span></a>'
:
(has_previous ?
  '<span class="gray"><span class="bigger2">&nbsp;&rarr;</span></span>'
:
  ''))+
'</p>';
  return (has_previous || has_next) ? root : '';
}
//
// return SVG image for '404 Not Found' page
//
function addNotFound(){
  updateMetaTag('robots', 'noindex'); // 404
  return '<div class="main"><svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="240" height="240">'+
'<g stroke-linecap="round" stroke-width="4px" fill="none" stroke="#777">'+
'<path d="M110 58 Q134 48 144 56" />'+
'<path d="M36 56 Q40 44 69 53" />'+
'<circle cx="56" cy="76" r="3" />'+
'<circle cx="127" cy="76" r="3" />'+
'<path d="M89 84 Q89 104 104 128 Q112 144 88 136" />'+
'<path d="M53 173 Q86 154 144 178" />'+
'</g>'+
'</svg></div>';
}
//
// fix header to non-scroll
//
function fixHeader(rtb_offset, offsTop){
  document.getElementById('header').style.position = 'fixed';
  offsTop = document.getElementById('header').offsetHeight;
  if(window.addYaRTB_Block && document.getElementById('ya_rtb_hd')){
    document.getElementById('ya_rtb_hd').style.position = 'fixed';
    document.getElementById('ya_rtb_hd').style.top = offsTop+'px';
    document.getElementById('ya_rtb_hd').style.width = '100%';
    rtb_offset = rtb_offset||160;
  }
  document.getElementById('page_header').style.paddingTop = String(
    offsTop+ (rtb_offset||0)) + 'px';
}
//
// build path to title from TITLES from index.js
//
function buildSubPath(roots, subjects, subjkey){
  var root = roots[ subjects[subjkey][3]][0],
      subj = subjects[subjkey][0];
  return (root == '.') ? subj : root + ' / ' + subj;
}
//
// remote/local path to sites files
//
function buildURL(path){
//  if(!String(window.location).match(/file:|localhost|127.0.1.1/)){
//    return 'https://raw.githubusercontent.com/egaxegax/egaxegax.github.io/master/'+path+'/';
//  }
  return '/'+path;
}
//
// build date from 'ymdhms' to 'd.m.y h:m'
//
function buildDate(d){
  if((d = String(d)).length>=12)
    return d[4]+d[5]+'.'+d[2]+d[3]+'.'+d[0]+d[1]+'&nbsp;'+d[6]+d[7]+':'+d[8]+d[9];
  return d;
}
//
// update meta tags
//
function updateMetaTag(name, content){
  var meta = document.head.getElementsByTagName('meta');
  for(var j in meta){
    if(meta[j].name == name) meta[j].content = content;
  }
}
//
// add link rel=canonical
//
(function addRelCanonical(){
  var link = !!document.querySelector("link[rel='canonical']") ? document.querySelector("link[rel='canonical']") : document.createElement('link');
  link.setAttribute('rel', 'canonical');
  link.setAttribute('href', location.protocol + '//' + location.host + location.pathname + location.search);
  console.log(link.outerHTML);
  document.head.appendChild(link);  
})();
//
// translater from //gist.github.com/diolavr/d2d50686cb5a472f5696.js
//
function tr(s){
  var ru = {
    'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'e', 
    'ж':'j', 'з':'z', 'и':'i', 'й':'j', 'к':'k', 'л':'l', 'м':'m', 
    'н':'n', 'о':'o', 'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 
    'ф':'f', 'х':'h', 'ц':'c', 'ч':'ch', 'ш':'sh', 'щ':'shch', 
    'ы':'y', 'ь':'', 'ъ':'', 'э':'e', 'ю':'ju', 'я':'ya'
  }, tr = [];

  s = s.toLowerCase();
  s = trstr(s);
  s = s.replace(/\s+/g,'_');

  for(var i=0; i<s.length; ++i){
    tr.push( 
      ru[ s[i] ] || 
      ru[ s[i] ] == undefined && s[i] || 
      ru[ s[i] ] == '' && ru[ s[i] ] );
  }

  return tr.join('').toLowerCase();
}
//
// remove special chars
//
function trstr(t){
  var tr = [];
  for (var i=0; i<t.length; ++i){
    if (' -_абвгдеёжзийклмнопрстуфхцчшщыъьэюяabcdefghjijklmnopqrstuvwxyz0123456789'.indexOf(t[i].toLowerCase()) > -1){
      tr.push( t[i] );
    } else {
      tr.push(' ');
    }
  }
  t = tr.join('').replace(/\s+/g,' ').trim();
  return t
}
//
// hash code for string
//
function hashstr(str){ return str.split('').reduce(function(a,b){ return (((a << 5 >>> 0) - a) + b.charCodeAt(0))|0; }, 0); }
//
// convert X,Y,Z openlayer tile coords to N..N sct code
//
function xyz2sct(X,Y,Z){
  var m=1, lx=0, ly=0, sct='';
  while(m<=Z){
    var d=Math.pow(2,Z)/Math.pow(2,m);
    if(lx   <= X && X < lx+d   && ly   <= Y && Y < ly+d)  { sct+='0'; }
    if(lx+d <= X && X < lx+d*2 && ly   <= Y && Y < ly+d)  { sct+='2'; lx += d; }
    if(lx   <= X && X < lx+d   && ly+d <= Y && Y < ly+d*2){ sct+='1'; ly += d; }
    if(lx+d <= X && X < lx+d*2 && ly+d <= Y && Y < ly+d*2){ sct+='3'; lx += d; ly += d; }
    m++;
  }
  return sct;
}