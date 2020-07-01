//
// XmlHttpRequest updater
//
function upfunc(p, clfunc, id){
  fetch(p.url).then(r => r.text()).then(function(r){
    if (clfunc) clfunc(r, p);
    if (id) document.getElementById(id).innerHTML = r;
  });
}