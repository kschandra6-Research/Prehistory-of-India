"""
Download original authentic archaeological tool photos & plates from Wikimedia Commons
"""
import urllib.request
import urllib.parse
import json
import os

headers = {'User-Agent': 'PrehistoryDashboardBot/1.0 (kavikondalaschandra@gmail.com)'}

images_dir = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\images"
os.makedirs(images_dir, exist_ok=True)

target_files = [
    ('handaxe.jpg', 'File:Biface de St Acheul MHNT.jpg'),
    ('cleaver.png', 'File:Hendidor.png'),
    ('chopper.jpg', 'File:Oldowan Chopper Stone Tool Sketch.jpeg'),
    ('levallois.jpg', 'File:Lithic core Levalois MHNT PRE 2004.0.86.fond.jpg'),
    ('blade.png', 'File:Lithic blade and core.png'),
    ('microlith.jpg', 'File:Microlith in hand.jpg'),
    ('celt.jpg', 'File:773 Neolithic polished stone axe fragment (FindID 114972).jpg'),
    ('bhimbetka.jpg', 'File:Rock painting, Bhimbetka, Raisen district, MP.jpg'),
    ('hathnora.jpg', 'File:Homo erectus new.JPG')
]

for filename, title in target_files:
    out_path = os.path.join(images_dir, filename)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
            pages = data.get('query', {}).get('pages', {})
            for p in pages.values():
                info = p.get('imageinfo', [{}])[0]
                img_url = info.get('url')
                if img_url:
                    print(f"Downloading {filename} from {img_url} ...")
                    img_req = urllib.request.Request(img_url, headers=headers)
                    with urllib.request.urlopen(img_req, timeout=20) as img_resp, open(out_path, "wb") as f_out:
                        f_out.write(img_resp.read())
                    print(f"  -> Saved {filename} ({os.path.getsize(out_path)} bytes)")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

print("All downloads complete. Directory contents:")
for f in os.listdir(images_dir):
    print(" ", f, os.path.getsize(os.path.join(images_dir, f)), "bytes")
