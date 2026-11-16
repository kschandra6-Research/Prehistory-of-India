import os

path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\update_with_lightbox.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('id="art-tab-palaeoenv"')
print(text[idx+1000:idx+2500])
