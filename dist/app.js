
(function(){
var $=function(s){return document.querySelector(s)};
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function share(box,title,url){
 var h='<button class="btn" id="sh1">Share</button><a class="btn g" target="_blank" rel="noopener" href="https://wa.me/?text='+encodeURIComponent(title+' '+url)+'">WhatsApp</a>'+
 '<a class="btn g" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text='+encodeURIComponent(title)+'&url='+encodeURIComponent(url)+'">X</a>'+
 '<a class="btn g" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(url)+'">Facebook</a>'+
 '<a class="btn g" target="_blank" rel="noopener" href="https://pinterest.com/pin/create/button/?url='+encodeURIComponent(url)+'&description='+encodeURIComponent(title)+'">Pinterest</a>';
 box.innerHTML=h;
 $('#sh1').onclick=function(){if(navigator.share){navigator.share({title:title,url:url}).catch(function(){})}else{navigator.clipboard&&navigator.clipboard.writeText(url);this.textContent='Link copied!'}};
}
var D=window.QUIZ;if(!D){return}
var root=$('#quiz');
if(D.type==='personality'){
 var qs=D.qs.map(function(q){return {q:q[0],o:shuffle(q[1].map(function(t,i){return {t:t,i:i}}))}});
 var n=0,tally=[0,0,0,0];
 function showRes(r){
  var x=D.results[r];var url=location.origin+location.pathname+'#r='+r;
  root.innerHTML='<div class="res card"><div class="big">'+D.emoji+'</div><p class="sub">Your result</p><h2>'+x[0]+'</h2><p>'+x[1]+'</p><div class="share" id="shb"></div><p style="margin-top:20px"><button class="btn g" id="again">Take it again</button></p></div>';
  share($('#shb'),'I got "'+x[0]+'" on '+D.title+' What do you get?',url);
  $('#again').onclick=function(){history.replaceState(null,'',location.pathname);n=0;tally=[0,0,0,0];draw()};
 }
 function draw(){
  if(n>=qs.length){var m=0;for(var i=1;i<4;i++){if(tally[i]>tally[m])m=i}history.replaceState(null,'','#r='+m);showRes(m);return}
  var q=qs[n];var h='<div class="card"><div class="bar"><i style="width:'+(n/qs.length*100)+'%"></i></div><p class="sub">Question '+(n+1)+' of '+qs.length+'</p><h2 style="margin-top:0">'+q.q+'</h2>';
  q.o.forEach(function(o,k){h+='<button class="opt" data-i="'+o.i+'">'+o.t+'</button>'});
  root.innerHTML=h+'</div>';
  [].forEach.call(root.querySelectorAll('.opt'),function(b){b.onclick=function(){tally[+b.dataset.i]++;n++;draw();window.scrollTo(0,0)}});
 }
 var m=location.hash.match(/r=(\d)/);
 if(m&&D.results[+m[1]]){showRes(+m[1])}else{draw()}
}else{ // knowledge + daily
 var qs=D.qs,n=0,score=0,locked=false;
 function end(){
  var pct=Math.round(score/qs.length*100);var msg=pct>=90?'Genius level!':pct>=70?'Great job!':pct>=40?'Not bad, keep going!':'Keep learning, you will get there!';
  root.innerHTML='<div class="res card"><div class="big">'+D.emoji+'</div><h2>'+score+' / '+qs.length+'</h2><p>'+msg+'</p><div class="share" id="shb"></div><p style="margin-top:20px"><button class="btn g" id="again">Try again</button></p></div>';
  share($('#shb'),'I scored '+score+'/'+qs.length+' on "'+D.title+'". Can you beat me?',location.origin+location.pathname);
  try{if(D.type==='daily'){localStorage.setItem('daily-'+D.key,score+'')}}catch(e){}
  $('#again').onclick=function(){n=0;score=0;draw()};
 }
 function draw(){
  if(n>=qs.length){end();return}
  var q=qs[n];locked=false;
  var h='<div class="card"><div class="bar"><i style="width:'+(n/qs.length*100)+'%"></i></div><p class="sub">Question '+(n+1)+' of '+qs.length+'</p><h2 style="margin-top:0">'+q[0]+'</h2>';
  q[1].forEach(function(t,i){h+='<button class="opt" data-i="'+i+'">'+t+'</button>'});
  root.innerHTML=h+'<div id="fb"></div></div>';
  [].forEach.call(root.querySelectorAll('.opt'),function(b){b.onclick=function(){
   if(locked)return;locked=true;var i=+b.dataset.i;
   if(i===q[2]){score++;b.classList.add('ok')}else{b.classList.add('no');root.querySelectorAll('.opt')[q[2]].classList.add('ok')}
   $('#fb').innerHTML='<div class="fact">'+q[3]+'</div><p><button class="btn" id="nx">'+(n+1>=qs.length?'See my score':'Next')+'</button></p>';
   $('#nx').onclick=function(){n++;draw()};
  }});
 }
 draw();
}
})();
(function(){
 var c=document.getElementById('cookie');if(!c)return;var ok=false;try{ok=localStorage.getItem('cc')}catch(e){}
 if(!ok){c.style.display='block'}
 document.getElementById('cc-ok').onclick=function(){try{localStorage.setItem('cc','1')}catch(e){}c.style.display='none'};
})();
