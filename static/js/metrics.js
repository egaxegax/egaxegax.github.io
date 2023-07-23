//
// Add metrics, counters
//
if(!String(window.location).match(/file:|localhost|127.0.1.1/)){
{ // liveinternet metrics
  (function(d,s){if(d.getElementById("licntADF8"))d.getElementById("licntADF8").src="//counter.yadro.ru/hit?t45.12;r"+escape(d.referrer)+
  ((typeof(s)=="undefined")?"":";s"+s.width+"*"+s.height+"*"+(s.colorDepth?s.colorDepth:s.pixelDepth))+";u"+escape(d.URL)+
  ";h"+escape(d.title.substring(0,150))+";"+Math.random();})(document,screen);
}
{ // yandex metrics
  (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments);};
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, "script", "//mc.yandex.ru/metrika/tag.js", "ym");
   ym(65044687, "init", {
     clickmap:true,
     trackLinks:true,
     accurateTrackBounce:true
   });
}
{ // google analytics
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments);},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m);
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-25857345-4', 'egaxegax.github.io');
  ga('send', 'pageview');
}
{ // rambler top 100 counter
  (function (w, d, c) {
  (w[c] = w[c] || []).push(function() {
      var options = {project: 7715588};
      try{w.top100Counter = new top100(options);} catch(e){}
    });
    var n = d.getElementsByTagName("script")[0],
    s = d.createElement("script"),
    f = function () { n.parentNode.insertBefore(s, n); };
    s.type = "text/javascript";
    s.async = true;
    s.src = 
    (d.location.protocol == "https:" ? "https:" : "http:") +
    "//st.top100.ru/top100/top100.js";
    if (w.opera == "[object Opera]") {
      d.addEventListener("DOMContentLoaded", f, false);
    } else { f(); }
  })(window, document, "_top100q");
}
{ // google adsense
  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
   m[i].l=1*new Date();k=e.createElement(t),a=document.head;k.async=1;k.crossorigin='anonymous';k.src=r;a.appendChild(k);})
   (window, document, 'script', '//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2243951601941043', 'googleContextCb');
}
{ // reklama Yandex.RTB
  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, "script", "//yandex.ru/ads/system/context.js", "yaContextCb");
}
}