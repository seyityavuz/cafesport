import requests
import re
import sys

# Terminal renkleri
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Kanallar listesi
KANALLAR = [
    {"dosya": "yayinzirve.m3u8", "tvgid": "BeinSports1.tr", "kanaladi": "Bein Sports 1 HD (VIP)"},
    {"dosya": "yayin1.m3u8", "tvgid": "BeinSports1.tr", "kanaladi": "Bein Sports 1 HD"},
    {"dosya": "yayinb2.m3u8", "tvgid": "BeinSports2.tr", "kanaladi": "Bein Sports 2 HD"},
    {"dosya": "yayinb3.m3u8", "tvgid": "BeinSports3.tr", "kanaladi": "Bein Sports 3 HD"},
    {"dosya": "yayinb4.m3u8", "tvgid": "BeinSports4.tr", "kanaladi": "Bein Sports 4 HD"},
    {"dosya": "yayinb5.m3u8", "tvgid": "BeinSports5.tr", "kanaladi": "Bein Sports 5 HD"},
    {"dosya": "yayinbm1.m3u8", "tvgid": "BeinMax1.tr", "kanaladi": "Bein Max 1 HD"},
    {"dosya": "yayinbm2.m3u8", "tvgid": "BeinMax2.tr", "kanaladi": "Bein Max 2 HD"},
    {"dosya": "yayinss.m3u8", "tvgid": "SSport1.tr", "kanaladi": "S Sport 1 HD"},
    {"dosya": "yayinss2.m3u8", "tvgid": "SSport2.tr", "kanaladi": "S Sport 2 HD"},
    {"dosya": "yayinssp2.m3u8", "tvgid": "SSportPlus.tr", "kanaladi": "S Sport Plus HD"},
    {"dosya": "yayint1.m3u8", "tvgid": "TivibuSpor1.tr", "kanaladi": "Tivibu Spor 1 HD"},
    {"dosya": "yayint2.m3u8", "tvgid": "TivibuSpor2.tr", "kanaladi": "Tivibu Spor 2 HD"},
    {"dosya": "yayint3.m3u8", "tvgid": "TivibuSpor3.tr", "kanaladi": "Tivibu Spor 3 HD"},
    {"dosya": "yayinsmarts.m3u8", "tvgid": "SmartSpor1.tr", "kanaladi": "Smart Spor 1 HD"},
    {"dosya": "yayinsms2.m3u8", "tvgid": "SmartSpor2.tr", "kanaladi": "Smart Spor 2 HD"},
    {"dosya": "yayintrtspor.m3u8", "tvgid": "TRTSpor.tr", "kanaladi": "TRT Spor HD"},
    {"dosya": "yayintrtspor2.m3u8", "tvgid": "TRTSporYildiz.tr", "kanaladi": "TRT Spor Yıldız HD"},
    {"dosya": "yayinas.m3u8", "tvgid": "ASpor.tr", "kanaladi": "A Spor HD"},
    {"dosya": "yayinatv.m3u8", "tvgid": "ATV.tr", "kanaladi": "ATV HD"},
    {"dosya": "yayintv8.m3u8", "tvgid": "TV8.tr", "kanaladi": "TV8 HD"},
    {"dosya": "yayintv85.m3u8", "tvgid": "TV85.tr", "kanaladi": "TV8.5 HD"},
    {"dosya": "yayinnbatv.m3u8", "tvgid": "NBATV.tr", "kanaladi": "NBA TV HD"},
    {"dosya": "yayinex1.m3u8", "tvgid": "ExxenSpor1.tr", "kanaladi": "Exxen Spor 1 HD"},
    {"dosya": "yayinex2.m3u8", "tvgid": "ExxenSpor2.tr", "kanaladi": "Exxen Spor 2 HD"},
    {"dosya": "yayinex3.m3u8", "tvgid": "ExxenSpor3.tr", "kanaladi": "Exxen Spor 3 HD"},
    {"dosya": "yayinex4.m3u8", "tvgid": "ExxenSpor4.tr", "kanaladi": "Exxen Spor 4 HD"},
    {"dosya": "yayinex5.m3u8", "tvgid": "ExxenSpor5.tr", "kanaladi": "Exxen Spor 5 HD"},
    {"dosya": "yayinex6.m3u8", "tvgid": "ExxenSpor6.tr", "kanaladi": "Exxen Spor 6 HD"},
    {"dosya": "yayinex7.m3u8", "tvgid": "ExxenSpor7.tr", "kanaladi": "Exxen Spor 7 HD"},
    {"dosya": "yayinex8.m3u8", "tvgid": "ExxenSpor8.tr", "kanaladi": "Exxen Spor 8 HD"},
]

def siteyi_bul():
    print(f"\n{GREEN}[*] Site aranıyor...{RESET}")
    for i in range(1450, 1458):
        url = f"https://trgoals{i}.xyz/"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                if "channel.html?id=" in r.text:
                    print(f"{GREEN}[OK] Yayın bulundu: {url}{RESET}")
                    return url
                else:
                    print(f"{YELLOW}[-] {url} yayında ama yayın linki yok.{RESET}")
        except requests.RequestException:
            print(f"{RED}[-] {url} erişilemedi.{RESET}")
    return None

def find_baseurl(url):
    try:
        r = requests.get(url, timeout=10)
        r.raiseforstatus()
    except requests.RequestException:
        return None
    match = re.search(r'baseurl\s:=]\s["\'["\']', r.text)
    if match:
        return match.group(1)
    return None

def generatem3u(baseurl, referer, user_agent):
    lines = ["#EXTM3U"]
    for idx, k in enumerate(KANALLAR, start=1):
        name = f"{k['kanal_adi']}"
        lines.append(f'#EXTINF:-1 tvg-id="{k["tvg_id"]}" tvg-name="{name}",{name}')
        lines.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
        lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        lines.append(base_url + k["dosya"])
        print(f"  ✔ {idx:02d}. {name}")
    return "\n".join(lines)

if name == "main":
    site = siteyi_bul()
    if not site:
        print(f"{RED}[HATA] Yayın yapan site bulunamadı.{RESET}")
        sys.exit(1)

    channel_url = site.rstrip("/") + "/channel.html?id=yayinzirve"
    baseurl = findbaseurl(channel_url)
    if not base_url:
        print(f"{RED}[HATA] Base URL bulunamadı.{RESET}")
        sys.exit(1)

    playlist = generatem3u(baseurl, site, "Mozilla/5.0")
    with open("trgoalas.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"{GREEN}[OK] Playlist oluşturuldu: trgoalas.m3u{RESET}")
