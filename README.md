# Quizlark - Kurulum (Turkce, adim adim)

## 0) Once ismi ve domaini sec
1. `build.py` icinde SITE_NAME ve EMAIL'i degistir (Quizlark bos mu kontrol et: Google'da ara).
2. Bir domain al (~10$/yil, Cloudflare Registrar ya da Namecheap). AdSense icin kendi domain sart gibi dusun.
3. Mailin: domaininde bir e-posta ac (ya da gecici gmail yaz ama Contact sayfasinda gorunur).

## 1) Siteyi uret
Bilgisayarinda Python kuruluysa:
    pip install pillow
    set SITE_DOMAIN=https://seninalanadin.com   (Mac/Linux: export SITE_DOMAIN=...)
    python build.py
`dist` klasoru yayinlanacak sitedir.
Python istemiyorsan: bu zip'teki `dist` klasoru zaten hazir ama domain "quizlark.example" yazar; domain alinca bana yaz, yeniden uretelim.

## 2) Yayinla (ucretsiz)
GitHub'a yeni repo ac -> `dist` icindekileri yukle -> Cloudflare Pages -> Connect to Git -> build command bos, output dir `/`.
Sonra Custom domain ekle.

## 3) Google
- Search Console: domaini ekle, sitemap.xml gonder.
- AdSense: site hazir ve gercek ziyaretci gelmeye baslayinca basvur (18+ olmalisin, banka hesabi gerekir).
- Onaylaninca: `ADSENSE_PUB=pub-XXXXXXXX` ile tekrar build et (reklam kodu ve ads.txt otomatik eklenir).
- AB/UK ziyaretcisi icin AdSense'in ucretsiz consent (CMP) mesajini Privacy & messaging bolumunden ac.

## 4) Icerik ekleme
`content.py` dosyasina yeni test/soru ekle, `python build.py`, yeniden yukle. Haftada 2-3 yeni test hedefle.

## Dikkat
- Kendi reklamina ASLA tiklama, trafik satin alma.
- Vergi: gelir icin muhasebeciye danis.

# 14 gunluk tanitim plani (ziyaretci SENDEN gelir)
Gun 1-2: siteyi yayinla, Search Console, 3 sosyal hesap ac (Pinterest, TikTok, X/Reddit).
Gun 3-14, her gun: 
- Pinterest: `dist/pin` icindeki gorsellerden 3 pin (her pin test linkine).
- TikTok/Reels/Shorts: 1 video - ekranda soruyu goster, "sonucun ne cikti?" de, linki bio'ya koy.
- Reddit: sadece izin veren alt toplulukta (or. r/SampleSize degil; kurallari oku) 1 paylasim; spam yapma.
- Her gun yeni test cikmasa da gunluk trivia skorunu paylas.
Hedef: ilk ay 1-3 bin ziyaret gercekci; 10 bin sansa ve icerige bagli.
