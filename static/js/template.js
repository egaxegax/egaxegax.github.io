//
// XmlHttpRequest updater
//
function xhr(p, clfunc, id){
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() { 
    if (xhr.readyState == 4) {
      if (id) document.getElementById(id).innerHTML = xhr.responseText;
      if (clfunc) clfunc(xhr.status == 404 ? 'Page Not Found' : xhr.responseText, p, xhr.status);
    }
  };
  xhr.open("GET", p.url, true);
  xhr.responseType = 'text';
  xhr.send();
}
//
// return key/value object of URL GET params
//
function urlParams(url) {
  var o = {}, qs = url ? url.split('?')[1] : window.location.search.slice(1);
  if (qs) {
    qs = qs.split('#')[0];
    var arr = qs.split('&');
    for (var i=0; i<arr.length; i++) {
      var a = arr[i].split('=');
      var pnum, pname = a[0].replace(/\[\d*\]/, function(v) {
        pnum = v.slice(1,-1);
        return '';
      });
      var pval = typeof(a[1])==='undefined' ? '' : a[1];
      pname = pname.toLowerCase();
      pval = pval.toLowerCase();
      if (o[pname]) {
        if (typeof o[pname] === 'string')
          o[pname] = [o[pname]];
        if (typeof pnum === 'undefined')
          o[pname].push(pval);
        else
          o[pname][pnum] = pval;
      } else {
        o[pname] = pval;
      }
    }
  }
  return o;
}
//
// return URL string from key/value object
//
function urlBuild(o){
  var href = [], par = urlParams();
  for (var k in o){ par[k] = o[k]; }
  for (var p in par){ 
    if(String(par[p]) != 'null')
      href.push( p + (String(par[p]) ? '=' + par[p]: '') ); 
  };
  return href.join('&');
}
//
// array sort function from https://www.zachleat.com/web/array-sort/
//
function arraySort(aa,bb,dorev,donum){
  if(Number(dorev)) return arraySort(bb,aa);
  if(!donum){ //text sort
    aa=( ''+aa ).toLowerCase(),
    bb=( ''+bb ).toLowerCase();
  }
  if(aa > bb) return 1;
  if(aa < bb) return -1;
  return 0;
}
//
// change action link href to light/dark css
//
function actionChStyle(p){
  document.querySelectorAll("link[href^='/static/css/"+p+"']").forEach(function(e){
    localStorage.setItem('THEME_URL_'+window.location.pathname, e.href='/static/css/'+p+(e.href.search(p+'.dark.css')>-1 ? '.css' : '.dark.css')+'?'+(+Date.now()));
  });
}
//
// do link action to light/dark css
//
(function actionSetStyle(t){
  if(t=localStorage.getItem('THEME_URL_'+window.location.pathname)){
    document.querySelectorAll("link[href^='"+t.slice(0,t.indexOf('.'))+"']").forEach(function(e){
      if(e.href.slice(e.href.lastIndexOf('/'),e.href.indexOf('?')) != t.slice(t.lastIndexOf('/'),t.indexOf('?'))) e.href = t;
    });
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
function addFinder(){ return '<div class="nowrap"><a class="nodecor gray" href="/research.html" title="Поиск Яндекс по сайту"><i> Я </i></a><input id="tfind" class="hmarg" maxlength="100" size="5" type="text" placeholder="&#128269;" onkeydown="if(event.keyCode==13) { event.preventDefault(); actionFind(); return false; }"></div>'; }
//
// return loader image html
//
function addLoader(bl){ return (bl ? '<div class="main">&emsp;<img class="rounded loader" alt="" src="/static/img/loader.gif"></div>' : ''); }
//
// return share button svg icon
//
function addIShare(){ return '<svg width="15" height="15" role="img" xmlns="http://www.w3.org/2000/svg"><g fill="transparent" stroke="currentColor"><circle cx="3" cy="7.5" r="1.5" /><circle cx="11" cy="3" r="1.5" /><circle cx="11" cy="12" r="1.5" /><path d="M4 8 L10 11.5 M4 7 L10 3.5"></g></svg>'; }
//
// return clock button svg icon
//
function addIClock(){ return '<svg width="15" height="15" role="img" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0 0)"><circle cx="7.5" cy="7.5" r="6" fill="transparent" stroke="currentColor" /><circle cx="7.5" cy="7.5" r="0.75" fill="currentColor" /><path d="M3.5 6.5 7.5 7.5 9 11.5" fill="transparent" stroke="currentColor" /></g></svg>'; }
//
// return refresh button svg icon
//
function addIRefresh(){ return '<svg width="16" height="16" role="img" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M5.56277 2.51577C3.46372 3.4501 2.00024 5.55414 2.00024 7.99999C2.00024 11.3137 4.68654 14 8.00024 14C11.314 14 14.0002 11.3137 14.0002 7.99999C14.0002 5.32519 12.25 3.05919 9.83224 2.28482L9.52992 3.23832C11.5431 3.88454 13.0002 5.7721 13.0002 7.99999C13.0002 10.7614 10.7617 13 8.00024 13C5.23882 13 3.00024 10.7614 3.00024 7.99999C3.00024 6.31104 3.83766 4.81767 5.11994 3.91245L5.56277 2.51577Z M5.00024 3H2.00024V2H5.50024L6.00024 2.5V6H5.00024V3Z" /></svg>'; }
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
'<div class="paginator tcenter">'+
(has_previous ? 
  '<a class="nodecor" href="?'+urlBuild({page: prev_page_num})+'"><span class="bigger2">&larr;&nbsp;</span> </a>'
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
'</div>';
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
// return TITLES filtered by subj/tit + rels links
//
function addTitlesRels(pp, subjects, titles, date_filter, tit_filter){
  var msgs = titles.filter(function(tit){ return (tr(subjects[tit[0]][0])==pp[0]); }); // filter by subj
  if(!msgs.length) return msgs;
  msgs = [[msgs[0][0],0,'README',0,msgs[0][4]]].concat(msgs); // +README page (all titles)
  msgs = msgs.filter(function(tit){ return (tr(tit[2])==pp[1]); }); // filter by titl
  if(!msgs.length) return msgs;
  var rels_subj = titles.filter(function(tit){ return (tit[0] == msgs[0][0] && tit[1]!=msgs[0][1]); }).sort(function(a,b){ return arraySort(a[3],b[3]); });
  var rels_root = titles.filter(function(tit){ return (tit[4] == msgs[0][4] && tit[0]!=msgs[0][0]); }).sort(function(a,b){ return arraySort(a[3],b[3]); });
  if(date_filter) rels_subj = rels_subj.filter(function(tit){ return (tit[3]<=msgs[0][3]); });
  if(date_filter) rels_root = rels_root.filter(function(tit){ return (tit[3]<=msgs[0][3]); });
  var more_titles = [];
  if(tit_filter){
    more_titles = rels_subj;
  } else {
    more_titles = [rels_subj[rels_subj.length-1], rels_subj[rels_subj.length-2], rels_subj[rels_subj.length-3], rels_root[rels_root.length-1], rels_root[rels_root.length-2]];
  }
  msgs = msgs.map(function(tit){ 
    return tit.concat([more_titles.map(function(r){ return r ? [ subjects[r[0]][0], r[2], r[1] ] : [] }).filter(function(r){ return r.length>0; }) ]);
  });
  // console.log(msgs);
  return msgs;
}
//
// return html for rels links
//
function addTitlesRelsHtml(p, page_html, hdr_text, pid){
  (p.title[5]||[]).map(function(tit,i){
    document.getElementById(pid).innerHTML += 
  (document.getElementById('rels_links') ? '' : ('<div id="rels_links" class="hspace inlbl">'+(hdr_text||'')+'</div><br>') )+
  '<div class="msgtext mw_f scroll inlbl small">'+
    '<em style="padding-left:12px">'+tit[0]+'</em> &nbsp; <a class="light" href="/'+page_html+'?'+tr(tit[0])+'/'+tr(tit[1])+'">'+tit[1]+'</a>'+
  '</div><br>';
  });
}
//
// get RSS text from rssUrl to contId 
//
function fetchRSSFromXML(rssUrl, contId) {
  var cont = '';
  fetch('https://egax.ru/posts/read.php?url='+encodeURIComponent(rssUrl)).then((response) => { return response.text(); }).then((data) => {
      [].slice.call((new DOMParser()).parseFromString(data, 'application/xml').getElementsByTagName('item')).slice(0,10).map((item,i,items) => {
        const titl = item.getElementsByTagName('title')[0].textContent;
        const link = item.getElementsByTagName('link')[0].textContent;
        const pdate = item.getElementsByTagName('pubDate')[0]?.textContent.split(/\s\+\d+/)[0];
        if(i==0) document.getElementById(contId).innerHTML = '<h2>Новое с '+rssUrl.split('/')[2]+' на '+(new Date(pdate)).toLocaleDateString()+'</h2>';
        cont += `
            <div class="rssn">
              <div><span class="smaller gray hspace">${('0'+(new Date(pdate)).getHours()).slice(-2)}:${('0'+(new Date(pdate)).getMinutes()).slice(-2)}</span>
                <a class="nodecor" href="${link}"> ${titl}</a>
              </div>
            </div>`;
        if(i==items.length-1) document.getElementById(contId).innerHTML += cont;
      });
  });
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
function trstr(t,e){
  var tr = [];
  for (var i=0; i<t.length; ++i){
    if (((e||'')+' -_абвгдеёжзийклмнопрстуфхцчшщыъьэюяabcdefghjijklmnopqrstuvwxyz0123456789').indexOf(t[i].toLowerCase()) > -1){
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
