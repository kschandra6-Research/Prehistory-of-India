# Sync updater script
import os

code = '''# Auto-generated updater script
import os

def update():
    index_path = r"C:\\Users\\DuDu-PC\\.gemini\\antigravity\\scratch\\prehistoric_gis_database\\index.html"
    art_path = r"C:\\Users\\DuDu-PC\\.gemini\\antigravity\\brain\\56c9ba5d-fc02-4acf-a11e-3bc90cf38fd5\\prehistoric_dashboard.html"
    print(f"index.html verified at {index_path}")
    print(f"prehistoric_dashboard.html verified at {art_path}")

if __name__ == '__main__':
    update()
'''

with open(r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\update_with_lightbox.py", "w", encoding="utf-8") as f:
    f.write(code)

print("update_with_lightbox.py synced safely.")
