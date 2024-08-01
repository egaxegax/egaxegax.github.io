//
// make metrics, counters, ads
//
if(!String(window.location).match(/file:|localhost|127.0.0.1/)){
{ // Mail.ru metrica
  (function (d,w,id) {
    (w._tmr = w._tmr || []).push({id:'3210527',type:'pageView',start:(new Date()).getTime()});
    if (d.getElementById(id)) return;
    var ts = d.createElement('script'); ts.type = 'text/javascript'; ts.async = true; ts.id = id;
    ts.src = '//top-fwz1.mail.ru/js/code.js';
    var f = function(){var s = d.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ts, s);};
    if (w.opera == '[object Opera]') { d.addEventListener('DOMContentLoaded', f, false); } else { f(); }
  })(document, window, 'tmr-code');
}
{ // Yandex metrica
  (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments);};
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//mc.yandex.ru/metrika/tag.js', 'ym');
   ym(65044687, 'init', {
     clickmap:true,
     trackLinks:true,
     accurateTrackBounce:true,
     webvisor:true
   });
   window.YandexRotorSettings={ WaiterEnabled:true, IsLoaded:function(){ return document.getElementById('page_content').innerHTML.length>100; }};
}
//{ // Rambler top 100 counter
//  (function (w,d,c) {
//  (w[c] = w[c] || []).push(function() {
//      var options = {project:7715588};
//      try{w.top100Counter = new top100(options);} catch(e){}
//    });
//    var n = d.getElementsByTagName('script')[0],
//    s = d.createElement('script'),
//    f = function () { n.parentNode.insertBefore(s, n); };
//    s.type = 'text/javascript';
//    s.async = true;
//    s.src = 
//    (d.location.protocol == 'https:' ? 'https:' : 'http:') +
//    '//st.top100.ru/top100/top100.js';
//    if (w.opera == '[object Opera]') {
//      d.addEventListener('DOMContentLoaded', f, false);
//    } else { f(); }
//  })(window, document, '_top100q');
//}
{ // Google Analytics 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
   (i[r].q=i[r].q||[]).push(arguments);},i[r].l=1*new Date();a=s.createElement(o),
   m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m);
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-25857345-4', 'egaxegax.github.io');
  ga('send', 'pageview');
}
//{ // Google Adsense
//  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
//   m[i].l=1*new Date();k=e.createElement(t),a=document.head;k.async=1;k.crossorigin='anonymous';k.src=r;a.appendChild(k);})
//  (window, document, 'script', '//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2243951601941043', 'googleContextCb');
//}
{ // Yandex reklama
  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//yandex.ru/ads/system/context.js', 'yaContextCb');
  window.YA_RTB = {1:3, 2:4, 3:5, 4:6, 5:7, 6:8, 7:9, feed:10, widget:11, inimage:12};
  window.YA_TMR = [];
  window.addYaRTB_Block = function(blid,p_dark,rtbid,typ){
    function ads(){ if(document.getElementById(blid)){ 
      (new IntersectionObserver((es)=>{ es.forEach((e)=>{ if(e.isIntersecting){ switch(typ){
          case 'widget': window.yaContextCb.push(()=>{Ya.Context.AdvManager.renderWidget({darkTheme:p_dark, blockId:'C-A-7295044-'+rtbid, renderTo:blid});}); break;
          case 'flMob':  window.yaContextCb.push(()=>{Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-7295044-'+rtbid, type:'floorAd'});}); break;
          case 'flDesk': window.yaContextCb.push(()=>{Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-7295044-'+rtbid, type:'floorAd', platform:'desktop'});}); break;
          case 'inImg':  (function addInImage(blid,p_dark,rtbid,images) {
                            if(!images.length) return;
                            const image = images.shift();
                            console.log(image);
                            image.id = `ya_rtb_${blid}-${Math.random().toString(16).slice(2)}`;
                            window.yaContextCb.push(()=>{Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-7295044-'+rtbid, renderTo:image.id, type:'inImage'});});
                            addInImage(images);
                          })(Array.from(document.querySelectorAll('img'))); break;
          default:       window.yaContextCb.push(()=>{Ya.Context.AdvManager.render({darkTheme:p_dark, blockId:'R-A-7295044-'+rtbid, renderTo:blid, type:typ});}); break;
        }}});
      }, {threshold:0.9}).observe(document.getElementById(blid)));
    }};
    while(YA_TMR.length) clearInterval(YA_TMR.pop());
    YA_TMR.push( setInterval(ads, (Math.random()*20+9)*1000) );
    setTimeout(ads);
  };
  [].slice.call(document.getElementsByTagName('script')).filter((s)=>{return s.src.indexOf('metrics.js')>-1;}).map((sp)=>{
    if(sp.getAttribute('data-floor')) addYaRTB_Block('root', sp.getAttribute('data-dark')!=null, 1, 'flMob');
    if(sp.getAttribute('data-floor')) addYaRTB_Block('root', sp.getAttribute('data-dark')!=null, 2, 'flDesk');  
  });
}
{ // VK reklama
  (function(m,e,t,r,i,k,a){m[i]=m[i]||[];
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];k.async=1;k.src=r;a.parentNode.insertBefore(k,a);})
   (window, document, 'script', '//ad.mail.ru/static/ads-async.js', 'MRGtag');
  window.VK_RTB = {1:1542915, 2:1542917, 3:1542919};
  window.VK_TMR = [];
  window.addVkRTB_Block = function(){ 
    function ads(){ 
      (MRGtag = window.MRGtag || []).push({});
    };
    while(VK_TMR.length) clearInterval(VK_TMR.pop());
    VK_TMR.push( setInterval(ads, (Math.random()*20+9)*1000));
    ads();
  };
}
{ // add rel canonical
  var link = !!document.querySelector("link[rel='canonical']") ? document.querySelector("link[rel='canonical']") : document.createElement('link');
  link.setAttribute('rel', 'canonical');
  link.setAttribute('href', location.protocol + '//' + location.host + location.pathname + location.search);
  document.head.appendChild(link);  
}
}
