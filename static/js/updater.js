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
      if (clfunc) clfunc(xhr.status == 404 ? '' : xhr.responseText, p, xhr.status);
    }
  };
  xhr.open("GET", p.url, true);
  xhr.responseType = 'text';
  xhr.send();
}
//
// Add image to element during ajax loading
//
function addAjaxLoader(el){
  if (el) el.innerHTML = '<img class="hspace1" src="/static/img/loader.gif">';
}
//
// URL GET params
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
// url build
//
function urlBuild(o){
  var href = [], par = urlParams();
  for (var k in o){ par[k] = o[k]; }
  for (var p in par){ href.push( (par[p] ? p+ '=' + par[p]: '') ); };
  return href.join('&');
}
//
// Check empty obj
//
function isEmpty(o){
  return JSON.stringify(o) === JSON.stringify({});
}