//
// load script
//
function loadScript(p, clfunc){
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.onload = function () {
    if (clfunc) clfunc(p);
  };
  script.src = p.url;
  document.head.appendChild(script);
}
//
// XmlHttpRequest updater
//
function upfunc(p, clfunc, id){
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() { 
    if (xhr.readyState == 4) {
      if (id) document.getElementById(id).innerHTML = xhr.responseText;
      if (clfunc) clfunc(xhr.responseText, p);
    }
  };
  xhr.open("GET", p.url, true);
  xhr.responseType = 'text';
  xhr.send();
}
//
// get URL GET params
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
  for (var p in par){ href.push( p + (par[p] ? '=' + par[p]: '') ); };
  return href.join('&');
}
//
//
// Check empty obj
//
function isEmpty(o){
  return JSON.stringify(o) === JSON.stringify({});
}