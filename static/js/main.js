﻿// 
//  Add body tags (header, ontent, footer)
//
function addBodyTags(sel){
  document.body.className = 'nomarg';
  var header = document.createElement('div');
  document.body.appendChild(header);
  header.id = 'header';
  header.className = 'main wrapbg';
  var ul = document.createElement('ul');
  header.appendChild(ul);
  ul.className = 'nomarg mtext';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'about';
  li.className = 'inl' + (sel == 'about' ? ' wrap3' : '');
  li.innerHTML =
'<svg width="120" height="80" xmlns="http://www.w3.org/2000/svg">'+
'<style>.a{fill:rgb(221,107,107);stroke:rgb(221,107,107)} .b{fill:rgb(149,124,143);stroke:rgb(149,124,143)}</style>'+
'<a class="nodecor" xlink:href="/about.html">'+
'<g style="stroke-miterlimit:10;stroke-width:5px" transform="scale(0.4 0.4) translate(24 -80)"><path d="M51,163c6-4,12-10,20-12,1-1,1-3,2-5a41.67,41.67,0,0,0-18,8c2-6-1-12,3-17s12-6,19-8c1-1,1-3,1-4-7,1-13,5-20,7-1-4,2-8,1-12,8-3,15-6,24-7a10.07,10.07,0,0,0,1-3c-11-1-21,5-31,10,0,14-3,29-2,43Z" class="a"/><path d="M106,134a21.77,21.77,0,0,0,8,5c-3,4-7,7-9,12-7-3-16-6-16-14,1-11,9-21,21-21a24.67,24.67,0,0,1,18,12c1-1,3-2,3-3-4-7-12-11-20-12s-15,1-20,7c-6,8-11,19-4,28,5,5,13,6,20,8,3-7,9-12,14-17-4-3-7-7-12-8-1,0-2,2-3,3Z" class="a"/><path d="M149,136c-5,7-12,11-20,13-7,3-13,7-19,11,5,9,9-3,15-4,4,5,10,8,16,10,0,4-1,9,1,12,1,1,4,1,6,1-4-14,2-27,4-41,0-1-2-1-3-2Zm-20,18c7-3,14-6,19-12-4,6-4,13-6,20-5-1-9-5-13-8Z" class="a"/><path d="M179,159a110.88,110.88,0,0,0,17-30,21.86,21.86,0,0,0-5,3c-4,9-8,17-14,24-4-5-3-11-5-16-1,0-3,1-5,1,2,6,2,13,6,19-7,8-16,13-24,19,2,0,4,1,6,1a82,82,0,0,0,20-17c2,5,7,9,11,10,2,1,5-1,8-2-6-3-11-6-15-12Z" class="a"/><path d="M68,183c-6,1-9,5-13,9,0-1-1-2-1-3-1,1-3,1-4,2-3,17-3,33-3,50,8-6,1-18,5-26,11,4,19-7,25-14,3-4,4-9,5-13,0-7-9-7-14-5Zm1,22c-4,2-8,9-13,6-6-3-2-11,0-16,3-7,12-11,19-8,2,7-3,12-6,18Z" class="b"/><path d="M112,184c-11-5-23,3-26,14-1,6,1,12,8,14,11,2,22-4,27-14a10.91,10.91,0,0,0-9-14Zm-8,23c-5,2-12,2-13-4-1-8,4-15,12-17,4,0,9,0,12,4,4,8-4,14-11,17Z" class="b"/><path d="M140,205a12.68,12.68,0,0,0-6,1c1-2,8-1,0-8-6,9-16,14-22,23,0,1,2,3,3,4,6-9,19-23,29-12,1-1,3-3,3-4-1-2-3-4-7-4Z" class="b"/><path d="M144,240c-1-1-4-2-3-5,4-6,8-12,13-16,2-1,5,1,8,1,1-1,1-3,2-4-3-1-5-1-8-2,1-3,3-5,4-8l-2-1c-2,2-3,6-6,7-2,0-4-1-6,2,1,1,3,1,4,2-5,7-14,13-15,22,4,3,8,7,13,6,1,0,1-2,1-3a9,9,0,0,1-5-1Z" class="b"/><path d="M182,215a56.38,56.38,0,0,0-12,4v4a15.92,15.92,0,0,1,13-3c3,0,1,4,1,7-10,5-28,1-29,15,0,4,6,5,10,5,5-1,11-2,15-6v4c2-1,4-1,5-2,2-9,9-19,3-28,0-1-4,0-6,0Zm0,19c-4,7-14,13-21,7,3-8,14-8,22-10,0,1-1,2-1,3Z" class="b"/><path d="M202,190c1,8-1,16-1,24-1,8-3,16-3,24,2-1,5-2,6-3,1-3,0-6,0-9,2-14,2-27,2-40l-4,4Z" class="b"/></g>'+
'</a></svg>';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.className = 'inl hspace';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'news';
  li.className = 'inl hspace ' + (sel == 'news' ? ' wrap3' : '');
  li.innerHTML = 
'<svg width="120" height="80" xmlns="http://www.w3.org/2000/svg">'+
'<a class="nodecor" title="Записки" xlink:href="/index.html">'+
'<g transform="translate(44 10) scale(0.06 0.06)"><path style="fill:#99AAB5;" d="M512,369.777c0,78.55-114.616,142.222-256,142.222S0,448.327,0,369.777s114.616-142.222,256-142.222 S512,291.228,512,369.777"/><path style="fill:#CCD6DD;" d="M512,341.333c0,78.55-114.616,142.222-256,142.222S0,419.882,0,341.333s114.616-142.222,256-142.222 S512,262.783,512,341.333"/><path style="fill:#F5F8FA;" d="M256,440.888c-212.736,0-241.778-213.333-241.778-270.222h483.556 C497.778,199.111,469.93,440.888,256,440.888"/><path style="fill:#CCD6DD;" d="M453.43,98.868c-19.299-13.341-44.132-24.092-72.832-32C407.264,58.677,445.324,62.474,453.43,98.868 M489.028,137.155C523.759-6.803,349.921,27.558,315.46,54.694c-19.058-2.119-38.912-3.328-59.464-3.328 c-133.532,0-241.778,45.91-241.778,120.092s108.246,134.314,241.778,134.314s241.778-60.132,241.778-134.314 C497.774,159.199,494.574,147.792,489.028,137.155"/><path style="fill:#8A4B38;" d="M469.333,184.888c0,54.984-95.517,99.556-213.333,99.556S42.667,239.872,42.667,184.888 S138.184,85.333,256,85.333S469.333,129.905,469.333,184.888"/><path style="fill:#D99E82;" d="M284.444,241.777c-3.641,0-7.282-1.394-10.055-4.167c-33.237-33.237-33.792-69.476-1.778-117.504 c10.51-15.772,12.8-31.929,6.798-48.028c-6.557-17.564-20.452-28.388-24.619-29.526c-7.865,0-13.625-6.314-13.625-14.166 c0-7.865,6.984-14.166,14.834-14.166c14.179,0,34.062,16.398,45.27,37.333c14.705,27.492,12.942,57.443-4.992,84.338 c-27.89,41.842-21.775,61.61-1.778,81.607c5.561,5.561,5.561,14.55,0,20.11C291.726,240.383,288.086,241.777,284.444,241.777"/><path style="fill:#D99E82;" d="M199.111,213.333c-3.641,0-7.282-1.394-10.055-4.167c-33.237-33.237-33.792-69.476-1.778-117.504 c10.339-15.517,12.701-29.61,7.025-41.913c-6.314-13.668-20.352-20.892-23.95-21.319c-7.85,0-14.065-6.357-14.065-14.208 c0-7.865,6.528-14.222,14.379-14.222c14.179,0,36.764,13.852,47.787,34.461c6.841,12.785,14.976,39.268-7.51,72.988 c-27.89,41.842-21.775,61.61-1.778,81.607c5.561,5.561,5.561,14.55,0,20.11C206.393,211.939,202.752,213.333,199.111,213.333"/></g>'+
'<g transform="scale(0.35 0.35) translate(34 70)" fill="#4d3ca0" stroke="#4d3ca0" stroke-width="2"><path d="M38,88.2c5-2,15-3.1,14-11.2c0-0.9-1-2.7-3-3c-12-1.8-22,0.5-30,0.9c1,0.8,2,2.3,3,3c4,0.3,6-1.9,10-2.5c3-1,8,0.8,12,1.8c1,0.3,3,0.7,2,3.1c-5,6.8-15,6.5-23,5.7c0,0.8,0,2.5,0,3.3c6,1.7,12-2.8,19,4.5c1,1.2,0,3.4-1,4.8c-6,5.7-15,5.4-24,0.8c0,0.8,0,2.4,0,4.1c12,6.4,23,3,30-4.9c1-1.5,1-4.1,1-6.7C47,87.5,41,89.4,38,88.2L38,88.2z"/><path d="M78,73.3c-2,0.5-5,1.1-7,2.3c-2,1.2-4,3.2-7,3.4c0,0.9,1,1.7,1,2.6c5-2.9,12-6.1,17-4.7c1,1.6-1,5.8-2,6c-9,4-18,4.6-24,10.2c-2,3.4-6,6.2-2,9.4c7,6.2,14-0.2,20-4.8c-1,2-1,2.9-2,4.8c1-0.1,3-0.4,4-0.6c4-5.3,5-11.9,9-17.6c2-3.3,5-9,2-10.8C85,72.4,81,73.6,78,73.3L78,73.3z M77,90c-3,7-11,11.7-18,10.4c-1-9.5,12-10.4,20-13.5C78,87.9,78,88.9,77,90L77,90z"/><path d="M85,101c1-0.3,3,0.1,4-0.2c7-9.6,10-19.2,17-29c5,0.6,11-0.3,16,0.1c-7,10.3-13,20.8-19,29.7c1,0.6,3,0.7,4,1.3c6-11,15-23,22-34.5c-8-1.9-17-1.2-26-0.1c-5,7.9-9,15-13,22.8C89,94.3,87,97.7,85,101L85,101z"/><path d="M120,102.3c6-9.5,14-19.3,21-28.8c-1-0.5-3-1.6-4-2.1c-7,12.5-17,23.2-23,34.5c2,0.1,4,2.2,5,0.8c10-7.3,21-12.6,31-20c-7,8.2-12,17.6-18,27.2c1,0.6,3,0.7,4,1.3c5-11.2,14-22.3,21-33.5c-2,0.8-4-0.4-5,0.1C141,87.5,130,94,120,102.3L120,102.3z"/><path d="M174,89.1c4-3.2,2,7.9,10-3.6c-6-0.9-11-2.6-17,0.6c-9,5.3-17,15-18,24.6c0,4.1,3,7,7,7.6c4,0.6,9,0,13-2.2c1-0.3,1-2.4,2-3.7c-6,1.6-17,4.6-16-4c1-4.5,4-8.8,7-13C166,91.7,169,87.4,174,89.1L174,89.1z"/><path d="M217,80.6c-2,0.7-4,0.4-6,1.3c-8,4.8-13,12.6-21,17.9c3-5.8,4-11.4,7-16c-2,0.1-4-0.7-5,0.5c-7,10.7-10,21.2-14,32.7c9,1.4,8-11.1,12-17.2c1,2.1,2,4.1,4,6.2c2,0.9,4,3.1,5,5.3c2,3.3,6,2.3,10,1.8c-5-5.1-9-8.5-13-13.8C203,92.1,211,87.2,217,80.6L217,80.6z"/><path d="M246,76.5c-1,1.6-1,4-2,5.6c-1,1.6-3,1.5-4,3.2c-5,7.4-11,14.8-17,21.8c3-9.2,4-19.1,6-28.7c-2,0.3-4,0.8-5,1.6c-3,10.5-4,21.5-7,32.1c3,0.8,6,0.6,8-0.9c10-8.7,17-19.1,23-29.8c-1,9.8-2,18.5-2,29.1c2,0.4,4,0.9,4-0.3c2-10.1,3-22.2,2-35C250,74.9,248,75.6,246,76.5C246,76.5,246,76.5,246,76.5z"/></g>'+
'</a></svg>';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'posts';
  li.className = 'inl hspace ' + (sel == 'posts' ? ' wrap3' : '');
  li.innerHTML = 
'<svg width="120" height="80" xmlns="http://www.w3.org/2000/svg">'+
'<a class="nodecor" title="Заметки" xlink:href="/posts.html">'+
'<g transform="translate(45 10) scale(0.25 0.25)"><path d="M110.16,96.56h-0.02V64.25V18.1c0-7.64-6.2-13.85-13.85-13.85H17.84 c-7.64,0-13.85,6.2-13.85,13.85s6.2,13.85,13.85,13.85l0,0c0.01,0,0.01,0,0.02,0h4.62h4.6v32.31v46.15 c0,7.64,6.2,13.85,13.85,13.85c0.1,0,0.18-0.03,0.27-0.03h68.98v0.03c7.65,0,13.85-6.2,13.85-13.85 C124.01,102.76,117.81,96.56,110.16,96.56z" style="fill:#A1887F;"/><path d="M17.84,8.87c5.1,0,9.23,4.14,9.23,9.23v4.44c-0.1-5-4.18-9.05-9.21-9.05 c-4.3,0-7.89,2.97-8.91,6.95c-0.2-0.75-0.34-1.52-0.34-2.34C8.61,13.01,12.75,8.87,17.84,8.87z" style="fill:#5D4037;"/><circle cx="17.86" cy="21.2" r="4.62" style="fill:#6D4C41;"/><path d="M31.68,110.4V64.25V31.94h0.02v-9.23h-0.02V18.1c0-3.56-1.38-6.78-3.59-9.23H96.3 c5.09,0,9.23,4.14,9.23,9.23v46.15v32.31h-64.6c0,0,0,0-0.01,0c0,0,0,0-0.01,0l0,0c-5.08,0.01-9.21,4.14-9.21,9.23 c0,5.09,4.14,9.23,9.23,9.23c4.28,0,7.85-2.94,8.9-6.9c0.18,0.73,0.31,1.49,0.31,2.28c0,5-3.99,9.06-8.96,9.2H40.9v0.03 C35.82,119.62,31.68,115.49,31.68,110.4z" style="fill:#D7C1AE;"/><path d="M45.55,105.79c0,2.54-2.07,4.62-4.62,4.62c-2.54,0-4.62-2.07-4.62-4.62c0-2.54,2.07-4.61,4.61-4.62 c0.01,0,0.01,0,0.02,0C43.49,101.19,45.55,103.25,45.55,105.79z" style="fill:#5D4037;"/><path d="M110.16,119.63v-0.03H51.19c2.19-2.45,3.57-5.65,3.57-9.2c0-3.56-1.38-6.78-3.59-9.23h58.99c5.09,0,9.23,4.14,9.23,9.23 C119.39,115.49,115.25,119.63,110.16,119.63z"/><path d="M110.14,119.63v-0.03H51.17c2.2-2.45,3.57-5.65,3.57-9.2c0-3.56-1.38-6.78-3.59-9.23h58.99 c5.09,0,9.23,4.14,9.23,9.23C119.38,115.49,115.24,119.63,110.14,119.63z" style="fill:#D7C1AE;"/><path d="M94.5,30.43H45.93c-1.11,0-2.01-1.03-2.01-2.3s0.9-2.3,2.01-2.3H94.5c1.11,0,2.01,1.03,2.01,2.3 S95.61,30.43,94.5,30.43z" style="fill:#8D6E63;"/><path d="M94.5,44.49H45.93c-1.11,0-2.01-1.03-2.01-2.3c0-1.27,0.9-2.3,2.01-2.3H94.5 c1.11,0,2.01,1.03,2.01,2.3C96.51,43.45,95.61,44.49,94.5,44.49z" style="fill:#8D6E63;"/><path d="M94.5,58.55H45.93c-1.11,0-2.01-1.03-2.01-2.3c0-1.27,0.9-2.3,2.01-2.3H94.5 c1.11,0,2.01,1.03,2.01,2.3C96.51,57.52,95.61,58.55,94.5,58.55z" style="fill:#8D6E63;"/><path d="M94.5,72.61H45.93c-1.11,0-2.01-1.03-2.01-2.3s0.9-2.3,2.01-2.3H94.5c1.11,0,2.01,1.03,2.01,2.3 S95.61,72.61,94.5,72.61z" style="fill:#8D6E63;"/><path d="M66.71,86.67H45.93c-1.11,0-2.01-1.03-2.01-2.3c0-1.27,0.9-2.3,2.01-2.3h20.77 c1.11,0,2.01,1.03,2.01,2.3C68.71,85.64,67.81,86.67,66.71,86.67z" style="fill:#8D6E63;"/><path d="M96.3,7.25c5.98,0,10.85,4.87,10.85,10.85v46.15v32.31c0,1.66,1.36,3,3.02,3 c5.98,0,10.85,4.87,10.85,10.85c0,5.86-4.67,10.65-10.48,10.84c-0.12-0.01-0.24-0.02-0.36-0.02H41.19 c-0.17,0-0.32,0.01-0.43,0.03c-5.91-0.09-10.68-4.92-10.68-10.84V64.25V31.94c0-1.66-1.34-3-3-3h-4.6h-4.63 c-5.98,0-10.85-4.87-10.85-10.85S11.86,7.25,17.84,7.25H96.3 M96.3,4.25H17.84c-7.64,0-13.85,6.2-13.85,13.85 c0,7.64,6.2,13.85,13.85,13.85c0.01,0,0.01,0,0.02,0h4.62h4.6v32.31v46.15c0,7.64,6.2,13.85,13.85,13.85 c0.1,0,0.18-0.03,0.27-0.03h68.98v0.03c7.65,0,13.85-6.2,13.85-13.85c0-7.65-6.2-13.85-13.85-13.85h-0.02V64.25V18.1 C110.14,10.45,103.95,4.25,96.3,4.25L96.3,4.25z" style="opacity:0.2;fill:#424242;"/></g>'+
'<g transform="scale(0.35 0.35) translate(34 70)" fill="#4d3ca0" stroke="#4d3ca0" stroke-width="2"><path d="M38,89.2c5-2,15-2.3,14-11.7c0-1-1-3.2-3-3.8c-12-3.5-22-1.9-30-2.1c1,1,2,3,3,3.9c6-0.4,13-3.2,22,0.4c1,0.4,3,3.1,2,4.7c-5,7.5-15,6.3-23,4.8c0,1,0,3,0,4c6,2.4,12-2.5,19,6.7c1,1.4,0,4-1,5.5c-6,6.3-15,5.6-24-0.1c0,1,0,3,0,5c12,7.9,23,4.2,30-4.5c1-2.7,3-6.1,0-10C45,89.5,41,88.9,38,89.2L38,89.2z"/><path d="M78,75.4c-5,1-10,2.5-14,5.4c0,1,1,2,1,3c5-3,12-6,17-4.4c1,1.7-1,6.3-2,6.5c-7,3.7-14,4.2-20,6.7c-5,2.6-8,7.7-6,15.2c7,4.4,14-0.8,20-5.7c0,2-1,3.1-1,5.1c1-0.1,3-0.5,3-0.5c3-9.3,12-19,12-29.1C88,73.8,82,73.7,78,75.4L78,75.4z M77,93.6c-1,5.2-6,8.1-10,10.2c-3,1.1-6,3-7-0.1c-3-10,11-12.1,19-13.5C78,91.4,78,92.4,77,93.6L77,93.6z"/><path d="M108,92.2c-2,2-4,5-6,6.9c4-9.9,7-20.4,6-28.9c0-1-4,0-5,0.4c-8,11.7-12,24.2-18,35c1-0.3,3,0.1,4-0.3c5-10.7,11-20.3,15-30.2c-1,9.5-5,20.3-6,29.7c0,0,2,0.1,3-0.3c9-10.1,18-20.2,27-29.5c-7,10.1-14,20.1-19,30.6c0,1,2,1,3,1.4c6-12.1,15-24.4,23-37.2c-2,0.2-4-1.6-5,0C122,75.7,115,83.7,108,92.2L108,92.2z"/><path d="M151,76.6c-5-1.2-11,1.4-16,6.3c-7,7.2-11,15.5-12,23.1c0,4,3,7.3,6,8.5c2-0.2,3,0.2,5,0c2-0.2,3,5.2,8-5.7c-6,1.5-11,1.5-14-2.7c-1-3.4,1-8.6,4-13.4c4,4.6,11,4.4,17,6C156,89.8,157,79.3,151,76.6C151,76.6,151,76.6,151,76.6z M135,89c3-4.8,7-6.2,10-7.9c6-1.5,6,6.6,2,12.8C143,92.2,139,90.6,135,89L135,89z"/><path d="M161,85.2c3-0.5,6-1,9-0.3c-5,9.2-11,19.3-15,29.5c2-0.1,4-0.1,5-0.7c5-10.5,8-21.1,16-29.4c2-2.8,7,3.4,11-5.7c-8,1.2-15,0.1-23,2C163,80.2,162,83.7,161,85.2L161,85.2z"/><path d="M219,73.8c-2,0.5-4,0.1-6,0.8c-6,5.2-13,11.3-21,16.9c3-5.6,4-10.7,7-15.1c-2,0.2-4-0.5-5,0.7c-6,10.1-11,20.7-14,31.7c9,0.1,8-10.4,12-16.4c6,3.2,6,12.2,19,9.9c-2-1.2-4-2.3-6-4.3c-1-2-3-3.9-5-4.8c-1-0.9-2-2.8-2-2.8C205,83.6,213,79.2,219,73.8L219,73.8z"/><path d="M248,75.6c-7,6.5-14,14.6-23,22.1c4-6.4,4-15.3,6-23.3c-2,0-4-0.9-5-0.3c-3,8.8-4,18.5-7,27.7c3,0.7,6,0.8,8-0.3c10-6.7,17-13.8,23-21c-1,8-2,15.1-2,24.1c2,0.9,4,2,4,1c2-7.9,3-17.7,2-28.8C252,75.5,250,75.4,248,75.6C248,75.6,248,75.6,248,75.6z"/></g>'+
'</a></svg>';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'fotos';
  li.className = 'inl hspace' + (sel == 'fotos' ? ' wrap3' : '');
  li.innerHTML =
'<svg width="120" height="80" xmlns="http://www.w3.org/2000/svg">'+
'<a class="nodecor" title="Фотки" xlink:href="/fotos.html">'+
'<g transform="translate(27 -4) scale(0.25 0.25)"><circle fill="#d5e2eb" cx="128" cy="137" r="29"/><path fill="#3e5063" d="M186.9,70.7h-23.8c-2.3,0-4.2,1.9-4.2,4.2v4.8c0,2.3,1.9,4.2,4.2,4.2h23.8c2.3,0,4.2-1.9,4.2-4.2v-4.8 C191.1,72.6,189.2,70.7,186.9,70.7z"/><path fill="#4b687f" d="M205.5,83.6v71.9h-30c2.3-5.8,3.5-12.1,3.5-18.7c0-28.1-22.9-51-51-51s-51,22.9-51,51c0,6.6,1.3,12.9,3.5,18.7 h-30V83.6c0-3.3,2.7-6,6-6h143C202.8,77.5,205.5,80.2,205.5,83.6z"/><path fill="#3e5063" d="M95.1,175.7H56.5c-3.3,0-6-2.7-6-6v-14.2h30C83.7,163.4,88.7,170.3,95.1,175.7z"/><path fill="#3e5063" d="M205.5,155.5v14.2c0,3.3-2.7,6-6,6h-38.6c6.4-5.4,11.4-12.3,14.6-20.2H205.5z"/><path fill="#3e5063" d="M81.9,77.6c0,0.2,0,0.3,0,0.5H68.2c0-0.2,0-0.3,0-0.5c0-3.8,3.1-6.9,6.9-6.9S81.9,73.8,81.9,77.6z"/><path fill="#4b687f" d="M128,90.8c-25.4,0-46,20.6-46,46c0,25.4,20.6,46,46,46s46-20.6,46-46C174,111.4,153.4,90.8,128,90.8z M128,176.7c-22,0-39.9-17.8-39.9-39.9c0-22,17.8-39.9,39.9-39.9s39.9,17.9,39.9,39.9C167.9,158.8,150,176.7,128,176.7z"/><path fill="#3e5063" d="M128,96.9c-22,0-39.9,17.9-39.9,39.9c0,22,17.8,39.9,39.9,39.9s39.9-17.8,39.9-39.9 C167.9,114.8,150,96.9,128,96.9z M128,165.2c-15.7,0-28.4-12.7-28.4-28.4c0-15.7,12.7-28.4,28.4-28.4s28.4,12.7,28.4,28.4 C156.4,152.5,143.7,165.2,128,165.2z"/><path fill="#d5e2eb" d="M85.4,96H64.7c-1.5,0-2.8-1.2-2.8-2.8v-5.3c0-1.5,1.2-2.8,2.8-2.8h20.8c1.5,0,2.8,1.2,2.8,2.8v5.3 C88.2,94.8,87,96,85.4,96z"/><circle fill="#ea685e" cx="189.4" cy="92.7" r="6.1"/><circle fill="#fff" cx="136" cy="127.8" r="9"/></g>'+
'<g transform="scale(0.35 0.35) translate(55 70)" fill="#4d3ca0" stroke="#4d3ca0" stroke-width="2"><path d="M62,73.1c-4,0.9-9,1.4-13,1.3c0-0.9,1-2.6,1-3.5c-2,1.8-7-4.8-7,4.6c-9,1.2-17,0.3-21,3.6c-2,2.5-6,3.7-1,13.1c5,7.7,10,7.5,15,7.9c-1,2.1-1,3.8-2,5.9c6,2.7,5-4,7-5.8c1-0.5,4,0.2,6-0.5c3-1.3,6-2.1,9-4.1c6-3.9,11-10,11-16.4C68,76,68,72.6,62,73.1C62,73.1,62,73.1,62,73.1z M37,96.2c-4,0.4-11-1.5-12-7.4c-2-9.7,7-10,17-10C40,84.4,39,91,37,96.2L37,96.2z M53,93c-3,1.8-7,4.1-11,3.1c2-5.6,4-12.2,6-18.2c4,0.4,11-3.1,13,1.8C62,84.9,57,89.5,53,93L53,93z"/><path d="M94,69.4c-8-0.5-16,7.2-22,14.7c-4,5-6,10.9-5,16.2c3,5.8,11,6.4,18,1.4c1-1.4,3-3.2,5-5.1c3-4.3,7-7.3,9-12.2C103,75.4,102,67.9,94,69.4L94,69.4z M84,97.4c-3,3.2-7,3.7-10,2.8c-1-1.5-3-2.8-2-5.9c2-7.1,7-14.5,14-18.9c5-3.4,11-2.8,10,2.7C96,84,90,92,84,97.4L84,97.4z"/><path d="M108,77.7c2,2,4,4,7,4.5c-8,10.1-16,19.1-18,28.8c-1,1.4,2,1.1,4,1.1c4-9.7,11-19.3,17-28.3c2,1.1,5,1.8,8,1.6c1-0.4,2-2.9,3-4.4c-2-1.3-5-1.1-8-1.8c-2-1.1-4-3.2-7-3.7c-1-0.5-2-2-3-2.5C110,74.6,109,76.1,108,77.7L108,77.7z"/><path d="M158,80.6c-2-0.1-4-1.2-6,0.1c-7,6-14,11.9-22,17.9c4-5.6,6-11.5,9-17.7c-2,0.5-4,0.1-5,0.5c-6,11.6-13,21.8-17,33.7c2,0.2,4-0.6,6-0.3c1-5.6,4-10.9,7-16.1c1,7,6,9.6,10,14.2c2,0.7,5-0.9,8-1.1c-4-5.3-11-6.8-12-13.9C144,92.3,151,84.8,158,80.6L158,80.6z"/><path d="M187,77.8c-2,3.2-4,5.2-7,8.1c-1,1.7-2,3.5-3,5.3c-5,4.4-9,11-15,15.4c2-9.7,5-18.1,7-27.7c-1-0.3-3-0.8-4,0.2c-4,9.4-7,20.3-10,31.2c3,0.1,6,0.6,8-0.2c11-7.8,19-16.4,25-26.9c-2,7.8-1,19.1-3,26.9c2,0.3,5,1.8,5,0.7c2-9.9,3-22,2-34.8C191,77.6,189,78.2,187,77.8L187,77.8z"/></g>'+
'</a></svg>';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'chords';
  li.className = 'inl hspace' + (sel == 'chords' ? ' wrap3' : '');
  li.innerHTML = 
'<svg width="120" height="80" xmlns="http://www.w3.org/2000/svg">'+
'<a class="nodecor" title="Аккорды" xlink:href="/songs.html">'+
'<g transform="translate(52 4) scale(0.575 0.575)"><path style="fill-rule:evenodd;clip-rule:evenodd;fill:#ED7161;" d="M34.399,40c-1.569-0.516-0.846-2.848-0.524-3.692c0.077-0.17,0.125-0.29,0.125-0.307C34,31.582,30.418,28,26,28c-3.376,0-6.258,2.094-7.432,5.053C16.803,36.164,14,36.001,14,36.001C6.268,36.001,0,42.269,0,50c0,5.982,8.018,14.001,14,14.001c7.731,0,14-6.269,14-14.001c0-0.068-0.009-0.134-0.01-0.202L28,49.801c0-6.571,5.463-5.719,6.399-5.801c1.105,0,2-0.895,2-1.999C36.399,40.896,35.505,40,34.399,40z"/><path style="fill-rule:evenodd;clip-rule:evenodd;fill:#9D5F57;" d="M27.988,49.797L28,49.801c0-6.571,5.463-5.719,6.399-5.801c1.105,0,2-0.895,2-1.999c0-1.105-0.895-2.001-2-2.001c-1.569-0.516-0.846-2.846-0.525-3.691C33.953,36.135,34,36.019,34,36.001c0-1.193-0.269-2.321-0.736-3.338C29.667,35.9,14,50,14,50s7.375,7.85,12.121,6.986C27.309,54.928,28,52.547,28,50C28,49.932,27.989,49.866,27.988,49.797z"/><path style="fill:#fff;" d="M25.463,40.972l-2.491-2.492c-0.688-0.688-1.803-0.688-2.491,0c-0.688,0.688-0.688,1.804,0,2.492l2.491,2.49c0.688,0.688,1.804,0.688,2.491,0C26.151,42.774,26.151,41.659,25.463,40.972z"/><path style="fill:#fff;" d="M17.463,48.972l-2.491-2.491c-0.688-0.688-1.803-0.688-2.49,0c-0.688,0.688-0.688,1.803,0,2.491l2.49,2.49c0.688,0.688,1.804,0.688,2.491,0C18.151,50.774,18.151,49.659,17.463,48.972z"/><path style="fill-rule:evenodd;clip-rule:evenodd;fill:#fff;" d="M15,55.998c-0.553,0-1,0.448-1,1.001c0,0.552,0.447,0.999,1,0.999c0.552,0,1-0.447,1-0.999C16,56.446,15.552,55.998,15,55.998z M19,55.998c-0.553,0-1,0.448-1,1.001c0,0.552,0.447,0.999,1,0.999c0.552,0,1-0.447,1-0.999C20,56.446,19.552,55.998,19,55.998z"/><polygon style="fill-rule:evenodd;clip-rule:evenodd;fill:#E8AD72;" points="43,17 24,36 28,40 47,21"/><polygon style="fill-rule:evenodd;clip-rule:evenodd;fill:#666;" transform="translate(-10 10)" points="62,2.001 60,0 58,0 52,6 52,8 54,10 56,12.001 58,12.001 64,6 64,4"/></g>'+
'<g transform="scale(0.35 0.35) translate(30 70)" fill="#4d3ca0" stroke="#4d3ca0" stroke-width="2"><path d="M38,73C28,85,21,96.2,15,107.4c8,5.4,6-8.5,12-10c5-0.6,13,3.4,19,2.2c2,3.8,0,8.3,2,12.1c1,0.3,4,0.1,4,0c2-12.2-1-25.6-9-38.2C42,73,40,73.1,38,73L38,73z M29,92.8c4-4,8-8.8,11-14.6c2,5.2,4,11.2,5,16.8C39,94.7,35,95.5,29,92.8L29,92.8z"/><path d="M98,72c-2,0.9-4,0.7-6,1.5c-8,6.2-15,13.3-22,20.3c2-5.4,4-9.9,5-15.2c-2,0.4-5,0.8-5,0.8c-5,10.9-8,21.2-12,31.2c9,2.6,8-11.3,12-16.7c4,3.6,5,9.6,8,14.1c1,0.8,4-1,6-1.7c-2-5.6-4-10.1-8-14.4C83,86.3,91,79.3,98,72L98,72z"/><path d="M131,67.6c-8-1.5-18,11.4-27,17.9c2-6.1,5-10.7,8-16.4c-2,0.1-5,0.6-5,0.6c-7,12.7-11,24.8-18,35.7c8,0,10-12.5,14-19.4c2,5.1,2,12.3,4,17.4c1,0.5,3,0.4,4,0.9c0-7.1-1-12.7-2-19.3C116,78.3,124,73.7,131,67.6L131,67.6z"/><path d="M148,72c-4-4.8-14,1.9-20,9.5c-5,8-10,15.9-8,22.9c2,6,9,7.8,17,1c8-6.8,15-16.7,16-25.1C154,75.7,151,73.3,148,72L148,72z M134,103.1c-7,3.2-11-0.5-9-7.7c2-6.2,7-14.2,13-17.7c5-3.9,11-2.2,10,4.3C147,89.4,141,96.8,134,103.1C134,103.1,134,103.1,134,103.1z"/><path d="M176,80.1c-4-0.4-8,2.3-12,5.3c1-1.5,2-3.9,3-5.3c-1-0.5-3-0.6-3-0.6c-11,16-24,33-28,49.5c-1,1.6,2,0.8,3,1.2c3-6.8,5-14,9-18.4c3-3.7,1,0.4,1,1.4c1,1.4,2,2.8,4,2.7c5,0.1,10-1.6,15-5c7-6.3,12-14.9,14-23.3C183,82.4,180,80.5,176,80.1L176,80.1z M165,108.4c-6,3.9-14,5.6-13-1.9c1-4.5,4-10.2,8-14.2c2-2,3-3.5,5-5.4c5-4.4,12-4.2,11,2C176,94.7,171,102.5,165,108.4L165,108.4z"/><path d="M218,79c-5-0.6-11,1.4-16,1c-5,10-13,20.1-23,28.9c-1,0.4-2-0.2-2-0.2c-4,4.6-5,9.9-7,14.8c8,1.2,6-6.6,10-12.1c9-0.6,18-3.9,27-4.6c-1,2.9-2,5.8-3,8.8c9,1,6-8.9,10-13.7c-2,0-4,0.9-6,1.1C211,94.3,216,87.1,218,79L218,79z M203,104.4c-6,1.7-12,0.3-18,3.3c8-8.4,13-17,20-24.2c2-1.1,5-0.3,7-1.2C210,89.7,204,96.7,203,104.4L203,104.4z"/><path d="M260,79.5c0,9.5-2,17.5-2,27.1c2,0.6,5,1.4,5,0.5c2-7.8,2-16.3,2-25.8C263,80.3,262,80.3,260,79.5C260,79.5,260,79.5,260,79.5z"/><path d="M250,92.3c-7-4.3-12-2.1-19-2.4c1-4.2,2-8.5,4-11.3c-2,0.1-4-0.5-5,0.1c-5,7.7-6,17.7-10,26.4c9-1.8,17-0.2,25-1.5c4-0.6,7-2.1,8-5.9C253,96,253,95.1,250,92.3C250,92.3,250,92.3,250,92.3z M237,100.9c-3,0.7-6,0.6-10-0.2c2-2.3,2-5,3-7.5c4-2.6,11,0.1,16,1.2C249,101.3,241,100.4,237,100.9L237,100.9z"/></g>'+
'</a></svg>';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.className = 'inl hspace';
  var li = document.createElement('li');
  ul.appendChild(li);
  li.id = 'login';
  li.className = 'inl' + (sel == 'login' ? ' wrap3' : '');
  li.innerHTML =
'<svg width="120" height="80" xmlns="http://www.w3.org/2000/svg">'+
'<a class="nodecor" xlink:href="/">'+
'<g transform="translate(40 18) scale(0.7 0.7)" stroke="rgb(149,124,143)" fill="transparent"><ellipse stroke="rgb(221,107,107)" stroke-width="6" cx="24" cy="33" rx="39" ry="45" /><path stroke-width="6" d="M22,58 12,58 18,31 a13.1,13.1 20 1 1 11,0 L36,58z" /></g>'+
'</a></svg>';
  var content = document.createElement('div');
  document.body.appendChild(content);
  content.id = 'content';
  content.className = 'main';
  var contview = document.createElement('div');
  content.appendChild(contview);
  contview.className = 'view';
  var pageheader = document.createElement('div');
  contview.appendChild(pageheader);
  pageheader.id = 'page_header';
  var pagecontent = document.createElement('div');
  contview.appendChild(pagecontent);
  pagecontent.id = 'page_content';
  var pagefooter = document.createElement('div');
  contview.appendChild(pagefooter);
  pagefooter.id = 'page_footer';
  var footer = document.createElement('div');
  document.body.appendChild(footer);
  footer.id = 'footer';
  footer.className = 'main';
  var mtab = document.createElement('table');
  footer.appendChild(mtab);
  mtab.width = '100%';
  var tb = document.createElement('tbody');
  mtab.appendChild(tb);
  var row = document.createElement('tr');
  tb.appendChild(row);

  var col = document.createElement('td');
  col.align = 'right';
  col.width = '45%';
  col.style.fontSize = 'smaller';
  var el = document.createElement('a');
  el.href = '/about.html';
  el.appendChild(document.createTextNode('egaxegax'));
  col.appendChild(document.createTextNode(' © 2011-2020 '));
  col.appendChild(el);
  row.appendChild(col);

  var col = document.createElement('td');
  col.align = 'center';
  col.width = '10%';
  row.appendChild(col);

  var col = document.createElement('td');
  col.align = 'left';
  col.width = '45%';
  var el = document.createElement('div');
  el.className = 'share42init';
  col.appendChild(el);
  row.appendChild(col);
}
//
// Add META tags (description, keywords, author) to page.
//
function addMetaTags(text){
  if (text) {
    var meta = document.createElement('meta');
    meta.name = 'description';
    meta.content = text
    document.head.appendChild(meta);
  }
  var meta = document.createElement('meta');
  meta.name = 'keywords';
  meta.content = 'записки, сообщения, комментарии, новости, тексты, заметки, фото';
  document.head.appendChild(meta);
  
  var meta = document.createElement('meta');
  meta.name = 'author';
  meta.content = 'Grigoriy Eremin, Григорий Еремин, egax@bk.ru';
  document.head.appendChild(meta);
  
  var meta = document.createElement('meta');
  meta.name = 'google-site-verification';
  meta.content = 'eWwGSnvveM7GniusD-nYN2KXBDPtXBHmhKRezn_TBg8';
  document.head.appendChild(meta);

  var meta = document.createElement('meta');
  meta.name = 'yandex-verification';
  meta.content = 'bf07f0af8e739c66';
  document.head.appendChild(meta);
  
};
//
// Paginator
// 
function addPaginator(list, per_page, page_num){
  per_page = parseInt(per_page);
  page_num = parseInt(page_num);
  var num_pages = Math.ceil(list.length / per_page ),
      has_previous = page_num > 1,
      has_next = page_num < num_pages,
      previous_page_number = page_num - 1,
      next_page_number = page_num + 1;
  var p = document.createElement('p');
  p.className = 'mtext cfloat';

  var sp = document.createElement('span');
  p.appendChild(sp);
  sp.className = 'hspace2';
  if (has_previous){
    var a = document.createElement('a');
    sp.appendChild(a);
    a.href = '?' + urlBuild({page: previous_page_number});
    a.appendChild(document.createTextNode( 'Назад' ));
  } else if (has_next) {
    sp.className += ' lightgray';
    sp.appendChild(document.createTextNode( 'Назад' ));
  }
  if (num_pages > 1){
    var sp = document.createElement('span');
    p.appendChild(sp);
    sp.className = 'hspace2';
    var b = document.createElement('b');
    sp.appendChild(b);
    b.appendChild(document.createTextNode( String(page_num) ));
    sp.appendChild(document.createTextNode( ' из ' ));
    var b = document.createElement('b');
    sp.appendChild(b);
    b.appendChild(document.createTextNode( String(num_pages) ));
  }
  var sp = document.createElement('span');
  p.appendChild(sp);
  sp.className = 'hspace2';
  if (has_next){
    var a = document.createElement('a');
    sp.appendChild(a);
    a.href = '?' + urlBuild({page: next_page_number});
    a.appendChild(document.createTextNode( 'Вперед' ));
  } else if (has_previous) {
    sp.className += ' lightgray';
    sp.appendChild(document.createTextNode( 'Вперед' ));
  }
  if (has_previous || has_next) return p;
  else return document.createTextNode('');
}