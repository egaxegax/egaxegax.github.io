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
'<p class="mtext cfloat">'+
(has_previous ? 
  '<a class="nodecor" href="?'+urlBuild({page: has_first ? 'null' : prev_page_num})+'"><span class="bigger2">&larr;&emsp;</span> </a>'
: 
(has_next ? 
  '<span class="gray"><span class="bigger2">&larr;&emsp;</span> </span>'
: 
  ''))+
(num_pages > 1 ?
  '<span> <b><i>'+String(page_num+1)+'</i></b> &nbsp; '+(page_btn||'из')+' &nbsp; <b><i>'+String(num_pages)+'</i></b> </span>'
:
  '')+
(has_next ? 
  '<a class="nodecor" href="?'+urlBuild({page: next_page_num})+'"> <span class="bigger2">&emsp;&rarr;</span></a>'
:
(has_previous ?
  '<span class="gray"> <span class="bigger2">&emsp;&rarr;</span></span>'
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
  return '<div><svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="240" height="240">'+
'<g stroke-linecap="round" stroke-width="4px" fill="none" stroke="#aaa">'+
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
// return loader image html
//
function addLoader(bl){
  return (bl ? '<span class="hspace"><img class="rounded loader" src="/static/img/loader.gif"></span>' : '');
}
//
// build path to title from TITLES from index.js
//
function buildSubPath(roots, subjects, subjkey){
  var root = roots[ subjects[subjkey][3] ][0],
      subj = subjects[subjkey][0];
  return root == '.' ? subj : root + ' / ' + subj;
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
  d = String(d);
  if(d.length>=12)
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
// translater from //gist.github.com/diolavr/d2d50686cb5a472f5696.js
//
function tr(s){
  var ru = {
    'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 
    'е':'e', 'ё':'e', 'ж':'j', 'з':'z', 'и':'i', 'й':'j', 
    'к':'k', 'л':'l', 'м':'m', 'н':'n', 'о':'o', 
    'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 
    'ф':'f', 'х':'h', 'ц':'c', 'ч':'ch', 'ш':'sh', 
    'щ':'shch', 'ы':'y', 'э':'e', 'ю':'ju', 'я':'ya'
  }, tr = [];

  s = s.replace(/[ъь'"«»`\(\)%]+/g, '').replace(/[\s\.,]+/g,'_');

  for(var i=0; i<s.length; ++i){
    tr.push( 
      ru[ s[i] ] || 
      ru[ s[i].toLowerCase() ] == undefined && s[i] ||
      ru[ s[i].toLowerCase() ].toUpperCase() );
  }

  return tr.join('').toLowerCase();
}
