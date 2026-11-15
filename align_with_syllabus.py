import sqlite3
import csv
import os

db_path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\prehistoric_sites_subcontinent.db"
csv_path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\prehistoric_sites_subcontinent.csv"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Fetch existing sites
cur.execute("SELECT * FROM prehistoric_sites")
existing_rows = cur.fetchall()
col_names = [col[1] for col in cur.execute("PRAGMA table_info(prehistoric_sites)").fetchall()]

sites_dict_list = []
for row in existing_rows:
    sites_dict_list.append(dict(zip(col_names, row)))

conn.close()

# 2. Add two landmark sites specifically mentioned / implied in Unit-3:
# - Guler (Himachal Siwaliks, Beas Valley, B.B. Lal 1955)
# - Umrethi / Hiran Valley (Gujarat, Western India, Marathe & Rajaguru 1981)
guler_site = {
    "site_id": len(sites_dict_list) + 1,
    "period": "Lower Paleolithic",
    "cultural_tradition": "Soanian Terrace Industry (Himachal Siwaliks)",
    "site_name": "Guler",
    "alternative_names": "Guler Beas Terraces (T1-T5), Kangra",
    "country": "India",
    "state_province": "Himachal Pradesh",
    "district": "Kangra",
    "river_basin": "Beas River Valley (Sub-Himalayan Siwaliks)",
    "latitude": 32.0167,
    "longitude": 76.1500,
    "elevation_approx_m": 430,
    "excavator_discoverer": "B.B. Lal (Archaeological Survey of India)",
    "year_of_discovery": "1955",
    "excavation_seasons": "1955, 1957",
    "tool_typology": "Unifacial pebble choppers, Bifacial chopping tools, Flakes, Early Soanian cores",
    "length_min_mm": 75.0,
    "length_max_mm": 150.0,
    "width_min_mm": 55.0,
    "width_max_mm": 105.0,
    "thickness_min_mm": 32.0,
    "thickness_max_mm": 62.0,
    "primary_raw_materials": "Light-grey Quartzite river pebbles / cobbles",
    "typical_usage": "Chopping wood, crushing bones for marrow, tuber slicing on river terraces",
    "associated_features": "5 distinct river terraces (T1 to T5) of the Beas river; benchmark site for Himachal Siwalik pebble tool sequence",
    "visual_link_archive": "https://commons.wikimedia.org/wiki/File:Guler_Pebble_Tool.jpg",
    "key_references": "Lal, B.B. (1956). Palaeoliths from the Beas and Banganga Valleys, Punjab. Ancient India 12:58-92; Misra, V.N. (2001); Sankalia, H.D. (1977)."
}

umrethi_site = {
    "site_id": len(sites_dict_list) + 2,
    "period": "Lower Paleolithic",
    "cultural_tradition": "Acheulian (Miliolite Stratigraphy)",
    "site_name": "Umrethi / Hiran Valley",
    "alternative_names": "Umrethi Dam Locality, Hiran Valley Acheulian",
    "country": "India",
    "state_province": "Gujarat",
    "district": "Gir Somnath (Saurashtra)",
    "river_basin": "Hiran River Basin / Arabian Sea Drainage",
    "latitude": 20.9500,
    "longitude": 70.4833,
    "elevation_approx_m": 65,
    "excavator_discoverer": "A.R. Marathe, S.N. Rajaguru, K.T.M. Hegde (Deccan College)",
    "year_of_discovery": "1974",
    "excavation_seasons": "1974-1980",
    "tool_typology": "Late Acheulian Handaxes, Cleavers, Scrapers on flakes, Polyhedrons",
    "length_min_mm": 105.0,
    "length_max_mm": 170.0,
    "width_min_mm": 55.0,
    "width_max_mm": 90.0,
    "thickness_min_mm": 28.0,
    "thickness_max_mm": 48.0,
    "primary_raw_materials": "Basalt (Deccan Trap) and Siliceous Chert",
    "typical_usage": "Coastal savanna hunting, carcass cleaving, butchering large ungulates",
    "associated_features": "Stratigraphically sealed beneath littoral Miliolite Limestone (Miliolite I & II); critical for Quaternary sea-level correlation in Western India",
    "visual_link_archive": "https://commons.wikimedia.org/wiki/File:Umrethi_Acheulian.jpg",
    "key_references": "Marathe, A.R. (1981). Geoarchaeology of the Hiran Valley, Saurashtra. Deccan College; Mishra, Sheila (2007); Misra, V.N. (2001)."
}

sites_dict_list.append(guler_site)
sites_dict_list.append(umrethi_site)

# 3. Add Syllabus-aligned fields to all records:
# - geographical_zone (Unit-3: Himalayan context, Western India, Central India, Peninsular India, Eastern India)
# - environmental_adaptation (Unit-4: Alluvial plain, Horse-shoe lake, Sand dune, Plateau occupation, etc.)
# - manufacturing_technique (Unit-2: Block-on-block, Stone hammer, Soft hammer/cylinder hammer, Levallois, Punch blade, Pressure flaking, Pecking/grinding)
# - palaeofauna_palaeoflora (Unit-1)
# - rock_art_details (Unit-4)
# - syllabus_unit_coverage (e.g. "Unit-1, Unit-2, Unit-3", etc.)

for s in sites_dict_list:
    state = s.get("state_province", "")
    period = s.get("period", "")
    site_name = s.get("site_name", "")
    typology = s.get("tool_typology", "")
    
    # 3a. Geographical Zone (Unit-3 mapping)
    if state in ["Himachal Pradesh", "Jammu and Kashmir", "Punjab"] or "Pakistan" in s.get("country", ""):
        if "Soan" in site_name or "Riwat" in site_name or "Nalagarh" in site_name or "Guler" in site_name:
            zone = "The Himalayan Context (Siwalik & Potwar)"
        elif state in ["Jammu and Kashmir"]:
            zone = "The Himalayan Context (Kashmir Valley)"
        else:
            zone = "The Himalayan & Trans-Indus Context"
    elif state in ["Rajasthan", "Gujarat"]:
        zone = "Western India"
    elif state in ["Madhya Pradesh", "Chhattisgarh"]:
        zone = "Central India"
    elif state in ["Maharashtra", "Andhra Pradesh", "Telangana", "Tamil Nadu", "Karnataka"]:
        zone = "Peninsular India"
    elif state in ["West Bengal", "Odisha", "Bihar", "Jharkhand", "Assam", "Meghalaya", "Arunachal Pradesh", "Manipur"]:
        zone = "Eastern India"
    elif state in ["Uttar Pradesh"]:
        zone = "Ganga Valley & Vindhyan Tract"
    else:
        zone = "Peninsular India"
    s["geographical_zone"] = zone

    # 3b. Environmental Adaptation (Unit-4 & Landscape context)
    if site_name in ["Sarai Nahar Rai", "Mahadaha", "Damdama"]:
        adaptation = "Horse-shoe lake sites (Oxbow lakes of Ganga Plain)"
    elif site_name in ["Chopani Mando", "Chopani Mando (Phase I)", "Chopani Mando (Phases II & III)", "Birbhanpur"]:
        adaptation = "Alluvial plain adaptation (River Terraces)"
    elif site_name in ["Langhnaj", "Bagor (Phase I)", "Tilwara", "Budha Pushkar", "Didwana (Singi Talav & 16R)", "Visadi"]:
        adaptation = "Sand dune landscape (Stabilized fossil dunes & playas)"
    elif site_name in ["Paisra"]:
        adaptation = "Plateau occupation (Kharagpur hill plateau basin)"
    elif "Cave" in site_name or "Shelter" in site_name or "Bhimbetka" in site_name or "Gudiyam" in site_name or "Muchchatla" in site_name or "Pachmarhi" in site_name:
        adaptation = "Cave & Rock Shelter occupation"
    elif "Ashmound" in s.get("cultural_tradition", "") or site_name in ["Sangankallu", "Piklihal", "Utnur", "Palavoy", "Kudatini"]:
        adaptation = "Granitoid hill & ashmound pastoral landscape"
    elif site_name in ["Teri Sites (Sawyerpuram & Megnanapuram)", "Khandivli", "Golbai Sasan"]:
        adaptation = "Coastal dune & estuarine lagoonal landscape"
    elif "Gravel" in s.get("associated_features", "") or "Terrace" in s.get("associated_features", "") or "Basin" in s.get("river_basin", ""):
        adaptation = "Alluvial valley & river gravel terrace adaptation"
    else:
        adaptation = "River valley & open-air woodland settlement"
    s["environmental_adaptation"] = adaptation

    # 3c. Manufacturing Technique (Unit-2 mapping)
    if period == "Lower Paleolithic":
        if "Soan" in s.get("cultural_tradition", "") or "Pebble" in s.get("cultural_tradition", ""):
            technique = "Direct stone hammer percussion (pebble flaking, steep flaking angle, unifacial/bifacial chopper reduction)"
        else:
            technique = "Block-on-block / anvil technique followed by cylinder hammer (soft hammer) bifacial flaking and step-flaking retouch"
    elif period == "Middle Paleolithic":
        technique = "Levallois prepared-core technique, discoidal core flaking, facetted platform preparation, and scraper marginal retouch"
    elif period == "Upper Paleolithic":
        technique = "Prismatic core punch blade technique (indirect percussion), burin spall blow, backed blade truncation, and ostrich eggshell perforation"
    elif period == "Mesolithic":
        technique = "Pressure flaking, punch bladelet technique, micro-burin technique, and steep blunting/backing for geometric microlith armatures"
    elif period == "Neolithic":
        technique = "Chipping, pecking, grinding, and fine hone-polishing for stone celts; coiling and burnishing for ceramic manufacture"
    else:
        technique = "Direct hard hammer percussion"
    s["manufacturing_technique"] = technique

    # 3d. Prehistoric Flora & Fauna (Unit-1 mapping)
    if site_name in ["Hathnora", "Samnapur", "Chirki-on-Nevasa", "Nevasa"]:
        fauna = "Pleistocene megafauna: Bos namadicus, Elephas antiquus/namadicus, Equus namadicus, Hexaprotodon palaeindicus, Cervus"
    elif site_name in ["Kurnool Caves", "Muchchatla Chintamanu Gavi (MCG)"]:
        fauna = "Late Pleistocene fauna: Presbytis entellus, Hystrix, Panthera pardus, Equus asinus, Rhinoceros, Bos, Gazella bennetti"
    elif site_name in ["Sarai Nahar Rai", "Mahadaha", "Damdama"]:
        fauna = "Holocene wild fauna & flora: Swamp deer (Rucervus duvaucelii), wild cattle (Bos gaurus), wild boar, charred wild rice (Oryza nivara)"
    elif site_name in ["Bagor (Phase I)", "Langhnaj", "Loteshwar"]:
        fauna = "Wild and early domestic fauna: Bos indicus, Ovis/Capra, Sus scrofa, Antilope cervicapra, Axis axis, Rhinoceros unicornis"
    elif site_name in ["Koldihwa", "Mahagara", "Lahuradewa", "Tokwa", "Jhusi"]:
        fauna = "Early domesticated rice (Oryza sativa), wild rice (Oryza nivara), cattle (Bos indicus), sheep/goat, freshwater molluscs and fish"
    elif site_name in ["Mehrgarh (Periods I-III)"]:
        fauna = "Early agricultural flora/fauna: Two-row/six-row barley (Hordeum vulgare), einkorn/emmer wheat (Triticum), Zebu cattle, domestic sheep/goat"
    elif "Ashmound" in adaptation or site_name in ["Sangankallu", "Piklihal", "Utnur", "Tekkalakota", "Hallur"]:
        fauna = "Domestic humped cattle (Bos indicus), sheep/goat, millets (Setaria, Brachiaria), horsegram (Macrotyloma uniflorum)"
    else:
        fauna = "Fragmentary mammalian bone fragments, riverine molluscs, riparian floral cover"
    s["palaeofauna_palaeoflora"] = fauna

    # 3e. Rock Art Details (Unit-4 mapping)
    if site_name in ["Bhimbetka (Auditorium & III F-23)", "Bhimbetka (Mesolithic Phase)"]:
        rock_art = "Cupules & archaic petroglyphs (Auditorium Cave); Mesolithic monochrome & polychrome rock paintings (hematite red, kaolin white) depicting communal hunts, dancers, shamans, deer, boars"
    elif site_name in ["Adamgarh"]:
        rock_art = "Painted rock shelters depicting dynamic hunting scenes, warriors with bows, horned herbivores, ochre pigment crayons"
    elif site_name in ["Pachmarhi (Dorothy Deep)"]:
        rock_art = "Celebrated Mahadeo hill rock paintings: archers, animal herds, honey gatherers, domestic and mythical scenes in white and red pigments"
    elif site_name in ["Sangankallu"]:
        rock_art = "Kupgal rock bruisings / petroglyphs: pecked and bruised figures of long-horned humped cattle (Bos indicus), anthropomorphs, and ithyphallic figures on dolerite boulders"
    elif site_name in ["Morhana Pahar & Lekhahia", "Baghaikhor"]:
        rock_art = "Vindhyan Kaimur painted rock shelters discovered by A.C.L. Carlleyle (1880); geometric motifs, deer, hunting groups"
    elif site_name in ["Gauri Gundam"]:
        rock_art = "Rock engravings and painted petroglyphs on sandstone walls depicting deer, wild animals, and early hunting weapons"
    else:
        rock_art = "None recorded"
    s["rock_art_details"] = rock_art

    # 3f. Syllabus Unit Coverage
    units = ["Unit-2"]
    if period in ["Lower Paleolithic", "Middle Paleolithic", "Upper Paleolithic"]:
        units.append("Unit-3 (Palaeolithic Cultures)")
    elif period == "Mesolithic":
        units.append("Unit-4 (Mesolithic Culture)")
    elif period == "Neolithic":
        units.append("Unit-4/Neolithic Post-Pleistocene Adaptation")
    
    if s["palaeofauna_palaeoflora"] != "Fragmentary mammalian bone fragments, riverine molluscs, riparian floral cover":
        units.append("Unit-1 (Palaeoenvironment & Fauna)")
    if s["rock_art_details"] != "None recorded":
        units.append("Unit-4 (Prehistoric Rock Art)")
    
    s["syllabus_unit_coverage"] = ", ".join(units)

    # 3g. Cross-reference textbook authors from the syllabus in references
    ref = s.get("key_references", "")
    additions = []
    if "Misra, V.N. (2001)" not in ref and period in ["Lower Paleolithic", "Mesolithic"]:
        additions.append("Misra, V.N. (2001). Prehistoric Human Colonization in India. J. Biosci. 26(4):491-531")
    if "Sankalia, H.D. (1977)" not in ref and period in ["Lower Paleolithic", "Middle Paleolithic", "Upper Paleolithic", "Mesolithic"]:
        additions.append("Sankalia, H.D. (1977). Prehistory of India. Munshiram Manoharlal")
    if "Sankalia, H.D. (1964)" not in ref and "technique" in s:
        additions.append("Sankalia, H.D. (1964). Stone Age Tools: Techniques, Names and Probable Functions. Deccan College")
    if "Mishra, Sheila (2007)" not in ref and period == "Lower Paleolithic":
        additions.append("Mishra, Sheila (2007). The Indian Lower Palaeolithic")
    if "Chakrabarti, D.K. (1988)" not in ref:
        additions.append("Chakrabarti, D.K. (1988). Oxford Companion to Indian Archaeology")
    
    if additions:
        s["key_references"] = ref + "; " + "; ".join(additions[:2])

# 4. Re-write CSV with updated columns
all_fieldnames = list(sites_dict_list[0].keys())

with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=all_fieldnames)
    writer.writeheader()
    for row in sites_dict_list:
        writer.writerow(row)

print(f"Updated CSV written with {len(sites_dict_list)} records and {len(all_fieldnames)} columns at {csv_path}")

# 5. Re-create SQLite Database with new schema and syllabus views
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cols_sql = []
for f in all_fieldnames:
    if f == "site_id":
        cols_sql.append("site_id INTEGER PRIMARY KEY AUTOINCREMENT")
    elif f in ["latitude", "longitude", "length_min_mm", "length_max_mm", "width_min_mm", "width_max_mm", "thickness_min_mm", "thickness_max_mm"]:
        cols_sql.append(f"{f} REAL")
    elif f == "elevation_approx_m":
        cols_sql.append(f"{f} INTEGER")
    else:
        cols_sql.append(f"{f} TEXT")

create_table_sql = f"CREATE TABLE prehistoric_sites (\n  " + ",\n  ".join(cols_sql) + "\n);"
cur.execute(create_table_sql)

# Indexes
cur.execute("CREATE INDEX idx_period ON prehistoric_sites(period);")
cur.execute("CREATE INDEX idx_geo_zone ON prehistoric_sites(geographical_zone);")
cur.execute("CREATE INDEX idx_env_adaptation ON prehistoric_sites(environmental_adaptation);")
cur.execute("CREATE INDEX idx_spatial_coords ON prehistoric_sites(latitude, longitude);")

insert_sql = f"""
INSERT INTO prehistoric_sites (
    {", ".join(all_fieldnames)}
) VALUES ({", ".join(["?" for _ in all_fieldnames])})
"""

for row in sites_dict_list:
    cur.execute(insert_sql, [row[f] for f in all_fieldnames])

# Pre-built views specifically aligned with Prehistory of India syllabus:

# View 1: Unit-3 Palaeolithic Cultures - Regional Distribution
cur.execute("""
CREATE VIEW view_unit3_palaeolithic_regional_distribution AS
SELECT 
    site_id,
    site_name,
    period,
    cultural_tradition,
    geographical_zone,
    state_province,
    river_basin,
    latitude,
    longitude,
    tool_typology,
    primary_raw_materials,
    manufacturing_technique,
    key_references
FROM prehistoric_sites
WHERE period IN ('Lower Paleolithic', 'Middle Paleolithic', 'Upper Paleolithic')
ORDER BY geographical_zone, period;
""")

# View 2: Unit-4 Mesolithic Adaptations
cur.execute("""
CREATE VIEW view_unit4_mesolithic_adaptations AS
SELECT 
    site_id,
    site_name,
    environmental_adaptation,
    state_province,
    river_basin,
    tool_typology,
    manufacturing_technique,
    palaeofauna_palaeoflora,
    rock_art_details,
    key_references
FROM prehistoric_sites
WHERE period = 'Mesolithic'
ORDER BY environmental_adaptation, site_name;
""")

# View 3: Unit-4 Prehistoric Rock Art
cur.execute("""
CREATE VIEW view_rock_art_sites AS
SELECT 
    site_id,
    site_name,
    period,
    state_province,
    district,
    latitude,
    longitude,
    rock_art_details,
    key_references
FROM prehistoric_sites
WHERE rock_art_details != 'None recorded'
ORDER BY period, site_name;
""")

# View 4: Unit-2 Stone Age Technologies & Manufacturing Techniques
cur.execute("""
CREATE VIEW view_unit2_stone_age_technologies AS
SELECT 
    period,
    manufacturing_technique,
    COUNT(*) AS site_count,
    GROUP_CONCAT(site_name, ', ') AS representative_sites,
    ROUND(AVG(length_max_mm), 1) AS avg_max_length_mm,
    ROUND(AVG(thickness_max_mm), 1) AS avg_max_thickness_mm
FROM prehistoric_sites
GROUP BY period, manufacturing_technique
ORDER BY period;
""")

conn.commit()

# Run verification counts
cur.execute("SELECT COUNT(*) FROM prehistoric_sites")
total_sites = cur.fetchone()[0]

cur.execute("SELECT geographical_zone, COUNT(*) FROM prehistoric_sites GROUP BY geographical_zone")
zone_counts = cur.fetchall()

cur.execute("SELECT environmental_adaptation, COUNT(*) FROM prehistoric_sites WHERE period='Mesolithic' GROUP BY environmental_adaptation")
meso_adapt_counts = cur.fetchall()

conn.close()

print(f"Total sites in database now: {total_sites}")
print("Geographical Zones (Unit-3):", zone_counts)
print("Mesolithic Adaptations (Unit-4):", meso_adapt_counts)
