import subprocess,time,re
from playwright.sync_api import sync_playwright
srv=subprocess.Popen(["python3","-m","http.server","8123","-d","dist"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(executablePath="/opt/pw-browsers/chromium") if False else p.chromium.launch()
    pg=b.new_page(viewport={"width":390,"height":800});pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto("http://localhost:8123/quiz/what-kind-of-traveler-are-you/")
    for i in range(6): pg.click(".opt >> nth=0")
    print("personality:",pg.inner_text(".res h2"), pg.url)
    pg.goto("http://localhost:8123/quiz/general-knowledge-quiz/")
    for i in range(10):
        pg.click(".opt >> nth=1");pg.click("#nx")
    print("knowledge:",pg.inner_text(".res h2"))
    pg.goto("http://localhost:8123/daily/")
    print("daily:",pg.inner_text("#dl"),pg.inner_text("h2 >> nth=0")[:60])
    pg.screenshot(path="/tmp/home.png");pg.goto("http://localhost:8123/");pg.screenshot(path="/tmp/home.png",full_page=False)
    # links
    hrefs=set(pg.eval_on_selector_all('a',"els=>els.map(a=>a.getAttribute('href'))"))
    import os
    for h in hrefs:
        if h.startswith("/") and not h.startswith("/#"):
            f="dist"+h+("index.html" if h.endswith("/") else "")
            if not os.path.exists(f): print("BROKEN",h)
    b.close()
srv.kill();print("errors:",errs)
