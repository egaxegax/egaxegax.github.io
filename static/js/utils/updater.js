//
// XmlHttpRequest updater
//
function upfunc(p, clfunc, id){
  fetch(p.url).then(r => r.text()).then(function(r){
    if (clfunc) clfunc(r, p);
    if (id) document.getElementById(id).innerHTML = r;
  });
}
// get URL GET params
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

      var pval = typeof(a[1])==='undefined' ? true : a[1];

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
