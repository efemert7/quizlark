# -*- coding: utf-8 -*-
import json, os, shutil, sys, html, datetime
from content import PERSONALITY, KNOWLEDGE, TRIVIA

# ======= EDIT THESE =======
SITE_NAME = "Quizlark"
DOMAIN = os.environ.get("SITE_DOMAIN", "https://quizlark.example")   # no trailing slash
EMAIL = "hello@quizlark.example"
ADSENSE_PUB = os.environ.get("ADSENSE_PUB", "")   # e.g. pub-1234567890123456 (after approval)
# ==========================
OUT = "dist"
today = datetime.date.today().isoformat()
e = html.escape

CSS = """
:root{--bg:#f8fafc;--card:#fff;--ink:#0f172a;--mut:#64748b;--line:#e2e8f0;--pri:#4f46e5}
*{box-sizing:border-box}body{margin:0;font:17px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--ink)}
a{color:var(--pri)}header{background:#fff;border-bottom:1px solid var(--line)}
.wrap{max-width:960px;margin:0 auto;padding:0 16px}.nav{display:flex;align-items:center;justify-content:space-between;height:60px}
.logo{font-weight:800;font-size:22px;text-decoration:none;color:var(--ink)}.nav a.l{margin-left:16px;text-decoration:none;color:var(--mut);font-size:15px}
h1{font-size:32px;line-height:1.2;margin:28px 0 8px}h2{margin:32px 0 12px}.sub{color:var(--mut);margin:0 0 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.tile{display:block;text-decoration:none;color:#fff;border-radius:16px;padding:22px;min-height:150px;transition:transform .15s}
.tile:hover{transform:translateY(-3px)}.tile b{display:block;font-size:19px;line-height:1.3;margin-top:8px}.tile small{opacity:.9}.tile .em{font-size:36px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;margin:16px 0}
.hero{background:linear-gradient(135deg,#4f46e5,#ec4899);color:#fff;border-radius:20px;padding:30px;margin:24px 0}
.hero h1{margin:0 0 8px}.hero p{margin:0 0 16px;opacity:.95}
.btn{display:inline-block;background:var(--pri);color:#fff;border:0;border-radius:12px;padding:13px 22px;font-size:17px;font-weight:700;cursor:pointer;text-decoration:none}
.btn.w{background:#fff;color:var(--pri)}.btn.g{background:#e2e8f0;color:var(--ink)}
.opt{display:block;width:100%;text-align:left;background:#fff;border:2px solid var(--line);border-radius:12px;padding:14px 16px;margin:10px 0;font-size:17px;cursor:pointer;color:var(--ink)}
.opt:hover{border-color:var(--pri)}.opt.ok{border-color:#16a34a;background:#dcfce7}.opt.no{border-color:#dc2626;background:#fee2e2}
.bar{height:8px;background:var(--line);border-radius:8px;overflow:hidden;margin-bottom:14px}.bar i{display:block;height:100%;background:var(--pri);width:0;transition:width .3s}
.res{text-align:center}.res .big{font-size:60px}.res h2{margin:4px 0}.share{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:16px}
.fact{background:#eef2ff;border-radius:10px;padding:10px 14px;margin-top:10px;font-size:15px}
.ad{min-height:100px;margin:20px 0;text-align:center}footer{margin-top:50px;padding:24px 0;border-top:1px solid var(--line);color:var(--mut);font-size:14px;text-align:center}
footer a{color:var(--mut);margin:0 8px}#cookie{position:fixed;left:12px;right:12px;bottom:12px;background:#0f172a;color:#fff;padding:14px 16px;border-radius:12px;font-size:14px;display:none;z-index:9;max-width:620px;margin:auto}
#cookie button{margin-left:8px;border:0;border-radius:8px;padding:6px 14px;font-weight:700;cursor:pointer}
.prose p,.prose li{max-width:700px}@media(max-width:600px){h1{font-size:26px}}
"""

JS = r"""
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
"""

def adslot():
    if not ADSENSE_PUB: return ""
    return '<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-%s" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>' % ADSENSE_PUB

def page(path, title, desc, body, extra_head="", script="", og=None, ld=""):
    url = DOMAIN + path
    og = og or "/og/default.png"
    ads = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-%s" crossorigin="anonymous"></script>' % ADSENSE_PUB) if ADSENSE_PUB else ""
    h = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{DOMAIN}{og}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css">{ads}{extra_head}{ld}</head><body>
<header><div class="wrap nav"><a class="logo" href="/">🎯 {SITE_NAME}</a><nav><a class="l" href="/daily/">Daily Trivia</a><a class="l" href="/#quizzes">All Quizzes</a></nav></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy Policy</a><a href="/terms/">Terms</a><p>&copy; {datetime.date.today().year} {SITE_NAME}. Quizzes are for entertainment.</p></div></footer>
<div id="cookie">We use cookies to run the site and show ads. See our <a style="color:#a5b4fc" href="/privacy/">Privacy Policy</a>. <button id="cc-ok">OK</button></div>
{script}<script src="/app.js" defer></script></body></html>"""
    d = os.path.join(OUT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(h)

def tile(q, href, label):
    return f'<a class="tile" href="{href}" style="background:{q["color"]}"><span class="em">{q["emoji"]}</span><b>{e(q["title"])}</b><small>{label}</small></a>'

shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
open(f"{OUT}/style.css", "w").write(CSS); open(f"{OUT}/app.js", "w").write(JS)
open(f"{OUT}/favicon.svg", "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#4f46e5"/><text x="32" y="45" font-size="36" text-anchor="middle">🎯</text></svg>')

urls = ["/", "/daily/", "/about/", "/contact/", "/privacy/", "/terms/"]
allq = PERSONALITY + KNOWLEDGE

tiles = "".join(tile(q, f"/quiz/{q['slug']}/", "Personality quiz · 1 min") for q in PERSONALITY) + \
        "".join(tile(q, f"/quiz/{q['slug']}/", "Knowledge quiz · 10 questions") for q in KNOWLEDGE)
home = f"""<div class="hero"><h1>Fun quizzes. Fresh trivia every day.</h1><p>Find out who you really are, test your knowledge and share your results with friends.</p><a class="btn w" href="/daily/">Play today's trivia</a></div>
{adslot()}<h2 id="quizzes">Popular quizzes</h2><div class="grid">{tiles}</div>{adslot()}
<div class="card prose"><h2 style="margin-top:0">Why people love {SITE_NAME}</h2><p>Every quiz takes about a minute, works on any phone and gives you a result worth sharing. New personality quizzes and a brand-new daily trivia challenge are added regularly.</p></div>"""
page("/", f"{SITE_NAME} - Fun Personality Quizzes & Daily Trivia", "Take fun personality quizzes, test your knowledge and play a new daily trivia challenge. Free, fast and made to share.", home)

for q in PERSONALITY:
    p = f"/quiz/{q['slug']}/"; urls.append(p)
    data = {"type": "personality", "title": q["title"], "emoji": q["emoji"], "results": q["results"], "qs": q["qs"]}
    names = ", ".join(r[0] for r in q["results"])
    body = f"""<h1>{e(q['title'])}</h1><p class="sub">{e(q['desc'])}</p>{adslot()}<div id="quiz"></div>{adslot()}
<div class="card prose"><h2 style="margin-top:0">About this quiz</h2><p>This quiz has {len(q['qs'])} questions and {len(q['results'])} possible results: {e(names)}. Answer honestly and quickly for the best match. Results are for fun and self-reflection, not professional advice.</p></div>
<h2>More quizzes</h2><div class="grid">{"".join(tile(o, f"/quiz/{o['slug']}/", "Take quiz") for o in allq if o['slug'] != q['slug'])}</div>"""
    page(p, q["title"] + f" | {SITE_NAME}", q["desc"], body, script=f"<script>window.QUIZ={json.dumps(data)}</script>", og=f"/og/{q['slug']}.png")

for q in KNOWLEDGE:
    p = f"/quiz/{q['slug']}/"; urls.append(p)
    data = {"type": "knowledge", "title": q["title"], "emoji": q["emoji"], "qs": q["qs"]}
    body = f"""<h1>{e(q['title'])}</h1><p class="sub">{e(q['desc'])}</p>{adslot()}<div id="quiz"></div>{adslot()}
<h2>More quizzes</h2><div class="grid">{"".join(tile(o, f"/quiz/{o['slug']}/", "Take quiz") for o in allq if o['slug'] != q['slug'])}</div>"""
    page(p, q["title"] + f" | {SITE_NAME}", q["desc"], body, script=f"<script>window.QUIZ={json.dumps(data)}</script>", og=f"/og/{q['slug']}.png")

# Daily trivia: JS picks 5 questions by date from the full pool (rotates automatically)
daily_js = """<script>
(function(){var P=%s;var d=new Date();var key=d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
var day=Math.floor(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())/86400000);
var qs=[];for(var i=0;i<5;i++){qs.push(P[(day*5+i)%%P.length])}
document.getElementById('dl').textContent=d.toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'});
window.QUIZ={type:'daily',key:key,title:'Daily Trivia',emoji:'🗓️',qs:qs};})();</script>""" % json.dumps(TRIVIA)
body = f"""<h1>Daily Trivia Challenge</h1><p class="sub" id="dl"></p>{adslot()}<div id="quiz"></div>{adslot()}
<div class="card prose"><h2 style="margin-top:0">How it works</h2><p>Five new questions every day. Come back tomorrow for a fresh set and challenge your friends to beat your score.</p></div>
<h2>Try a quiz</h2><div class="grid">{"".join(tile(o, f"/quiz/{o['slug']}/", "Take quiz") for o in allq[:6])}</div>"""
page("/daily/", f"Daily Trivia Challenge - 5 New Questions Every Day | {SITE_NAME}", "Play today's free trivia challenge: five new questions every day. Share your score and challenge friends.", body, script=daily_js)

about = f"""<h1>About {SITE_NAME}</h1><div class="prose"><p>{SITE_NAME} is a free website with personality quizzes and daily trivia, made to be quick, fun and easy to share. We write our quizzes ourselves and check trivia facts before publishing.</p><p>Our goal is simple: give you a smile and something to talk about with friends. Results are for entertainment only.</p><p>Questions or ideas? <a href="/contact/">Contact us</a>.</p></div>"""
page("/about/", f"About | {SITE_NAME}", f"About {SITE_NAME}", about)
contact = f"""<h1>Contact</h1><div class="prose"><p>We read every message. Email us at <a href="mailto:{EMAIL}">{EMAIL}</a> for feedback, corrections, quiz ideas or business inquiries.</p></div>"""
page("/contact/", f"Contact | {SITE_NAME}", f"Contact {SITE_NAME}", contact)
privacy = f"""<h1>Privacy Policy</h1><div class="prose"><p>Last updated: {today}</p>
<p>{SITE_NAME} ("we", "us") respects your privacy. This policy explains what information is collected when you use {DOMAIN}.</p>
<h2>Information we collect</h2><p>We do not ask you to create an account and we do not collect your name or email through the quizzes. Your quiz answers are processed in your browser and are not sent to our servers. We may store small preferences (for example, that you dismissed the cookie notice or finished the daily trivia) in your browser's local storage.</p>
<h2>Cookies and advertising</h2><p>We use cookies and similar technologies. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to our site and/or other sites on the Internet. You may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info" rel="noopener">aboutads.info</a>.</p>
<h2>Analytics</h2><p>We may use privacy-friendly analytics to understand which pages are popular. These tools may collect your IP address, browser type and pages visited.</p>
<h2>Your choices</h2><p>You can delete cookies in your browser settings. If you are in the EEA, UK or Switzerland, you can manage consent for personalized ads through the consent message shown on the site.</p>
<h2>Children</h2><p>Our site is not directed to children under 13 and we do not knowingly collect their personal information.</p>
<h2>Contact</h2><p>Questions about this policy: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>"""
page("/privacy/", f"Privacy Policy | {SITE_NAME}", f"Privacy Policy for {SITE_NAME}", privacy)
terms = f"""<h1>Terms of Use</h1><div class="prose"><p>Last updated: {today}</p><p>By using {SITE_NAME} you agree to these terms. Quizzes and trivia are provided for entertainment and education only; results are not professional, medical, financial or career advice. Content is provided "as is" without warranties. We may change or remove content at any time. Do not copy or republish our content without permission. You may link to and share our pages freely.</p><p>Contact: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>"""
page("/terms/", f"Terms of Use | {SITE_NAME}", f"Terms of Use for {SITE_NAME}", terms)

open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{DOMAIN}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + "</urlset>")
open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
open(f"{OUT}/ads.txt", "w").write(f"google.com, {ADSENSE_PUB}, DIRECT, f08c47fec0942fa0\n" if ADSENSE_PUB else "# After AdSense approval set ADSENSE_PUB and rebuild.\n")
open(f"{OUT}/404.html", "w").write(f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><link rel=stylesheet href=/style.css><div class=wrap><h1>Page not found</h1><p><a href=/>Back to {SITE_NAME}</a></p></div>")
print("built", len(urls), "pages")

# share images
try:
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(f"{OUT}/og", exist_ok=True); os.makedirs(f"{OUT}/pin", exist_ok=True)
    F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    def wrap(d, t, f, w):
        ws, ln, out = t.split(), "", []
        for x in ws:
            if d.textlength((ln + " " + x).strip(), font=f) <= w: ln = (ln + " " + x).strip()
            else: out.append(ln); ln = x
        return out + [ln]
    def mk(size, title, color, name, small):
        W, H = size
        im = Image.new("RGB", size, color); d = ImageDraw.Draw(im)
        d.rectangle([0, H - 110, W, H], fill=(0, 0, 0))
        ft = ImageFont.truetype(F, int(W * 0.07)); fs = ImageFont.truetype(F, 34)
        lines = wrap(d, title, ft, W - 120); y = int(H * 0.28)
        for l in lines:
            d.text((60, y), l, font=ft, fill="white"); y += int(W * 0.09)
        d.text((60, y + 20), small, font=fs, fill=(255, 255, 255))
        d.text((60, H - 75), name, font=ImageFont.truetype(F, 44), fill="white")
        return im
    for q in allq:
        c = q["color"]; col = tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
        mk((1200, 630), q["title"], col, SITE_NAME, "Take the quiz - free, 1 minute").save(f"{OUT}/og/{q['slug']}.png")
        mk((1000, 1500), q["title"], col, SITE_NAME, "Take the quiz - free, 1 minute").save(f"{OUT}/pin/{q['slug']}.png")
    mk((1200, 630), "Fun Quizzes & Daily Trivia", (79, 70, 229), SITE_NAME, "Free - fast - share with friends").save(f"{OUT}/og/default.png")
except Exception as ex:
    print("image skip", ex)
