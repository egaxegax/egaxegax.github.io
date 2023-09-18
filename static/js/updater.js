//
// fix Yandex.RTB block height
//
function adjustRtbHeight(){
  var elem, hsum = 0;
  if(!(String(window.location).match(/file:|localhost|127.0.0.1/))){
    [1,2,3].map(function(i){
      if(elem = document.getElementById('yandex_rtb_R-A-2277013-'+i)){
        elem.style.height = elem.style.maxHeight;
        hsum += elem.style.height;
      }
    });
  }
  return hsum;
}
//
// load script
//
function loadScript(p, clfunc){
  var script = document.createElement('script');
  script.setAttribute( 'src', p.url );
//  script.setAttribute( 'charset', 'windows-1251' );
  script.onload = function () { if (clfunc) clfunc(p); };
  document.body.appendChild(script);
}
//
// XmlHttpRequest updater
//
function upfunc(p, clfunc, id){
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
      var pval = typeof(a[1])==='undefined' ? "" : a[1];
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
