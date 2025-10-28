import requests
import re
import os

def findworkingselcuksportshd(start=1825, end=1850):
    print("🧭 Selcuksportshd domainleri taranıyor...")
    headers = {"User-Agent": "Mozilla/5.0"}

    for i in range(start, end + 1):
        url = f"https://www.selcuksportshd{i}.xyz/"
        print(f"🔍 Taranıyor: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200 and "uxsyplayer" in response.text:
                print(f"✅ Aktif domain bulundu: {url}")
                return response.text, url
        except:
            print(f"⚠️ Hata: {url}")
            continue

    print("❌ Aktif domain bulunamadı.")
    return None, None

def finddynamicplayerdomain(pagehtml):
    match = re.search(r'https?://(main\.uxsyplayer[0-9a-zA-Z\-]+\.click)', page_html)
    if match:
        return f"https://{match.group(1)}"
    return None

def extractbasestream_url(html):
    match = re.search(r'this\.baseStreamUrl\s=\s\'"', html)
    if match:
        return match.group(1)
    return None

def buildm3u8links(basestreamurl, channel_ids):
    m3u8_links = []
    for cid in channel_ids:
        fullurl = f"{basestream_url}{cid}/playlist.m3u8"
        print(f"✅ M3U8 link oluşturuldu: {full_url}")
        m3u8links.append((cid, fullurl))
    return m3u8_links

def writem3ufile(m3u8_links, filename="5.m3u", referer=""):
    if not os.path.exists(filename):
        print("⛔ Dosya bulunamadı. Yeni dosya oluşturulamaz çünkü eski içerik korunmalı.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        if line.startswith("#EXTINF") and 'tvg-id="' in line:
            tvgidmatch = re.search(r'tvg-id="([^"]+)"', line)
            if tvgidmatch:
                kanalid = tvgid_match.group(1)
                matched = next(((cid, url) for cid, url in m3u8links if cid == kanalid), None)

                if matched:
                    # Mevcut yayının referer ve url kısmını güncelle
                    i += 1
                    if i < len(lines) and lines[i].startswith("#EXTVLCOPT:http-referrer"):
                        i += 1
                    if i < len(lines) and lines[i].startswith("http"):
                        i += 1

                    new_lines.append(f"#EXTVLCOPT:http-referrer= {referer}")
                    new_lines.append(matched[1])
                    continue  # Güncellendi, diğer satıra geç
        i += 1

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))
    print(f"✅ Güncelleme tamamlandı: {filename}")

# tvg-id ile eşleşecek kanal ID'leri
channel_ids = [
    "selcukbeinsports1",
    "selcukbeinsports2",
    "selcukbeinsports3",
    "selcukbeinsports4",
    "selcukbeinsports5",
    "selcukbeinsportsmax1",
    "selcukbeinsportsmax2",
    "selcukssport",
    "selcukssport2",
    "selcuksmartspor",
    "selcuksmartspor2",
    "selcuktivibuspor1",
    "selcuktivibuspor2",
    "selcuktivibuspor3",
    "selcuktivibuspor4",
    "selcukbeinsportshaber",
    "selcukaspor",
    "selcukeurosport1",
    "selcukeurosport2",
    "selcuksf1",
    "selcuktabiispor",
    "ssportplus1"
]

# Ana işlem
html, refererurl = findworking_selcuksportshd()

if html:
    streamdomain = finddynamicplayerdomain(html)
    if stream_domain:
        print(f"\n🔗 Yayın domaini bulundu: {stream_domain}")
        try:
            playerpage = requests.get(f"{streamdomain}/index.php?id={channel_ids[0]}",
                                       headers={"User-Agent": "Mozilla/5.0", "Referer": referer_url})
            basestreamurl = extractbasestreamurl(playerpage.text)
            if basestreamurl:
                print(f"📡 Base stream URL bulundu: {basestreamurl}")
                m3u8list = buildm3u8links(basestreamurl, channelids)
                writem3ufile(m3u8list, referer=refererurl)
            else:
                print("❌ baseStreamUrl bulunamadı.")
        except Exception as e:
            print(f"⚠️ Hata oluştu: {e}")
    else:
        print("❌ Yayın domaini bulunamadı.")
else:
    print("⛔ Aktif yayın alınamadı.")

# Bunun üzerine üsteki değişikliği yaparak ver
