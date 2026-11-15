import sqlite3
import csv
import os

db_path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\prehistoric_sites_subcontinent.db"
csv_path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\prehistoric_sites_subcontinent.csv"

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT * FROM prehistoric_sites")
rows = [dict(r) for r in cur.fetchall()]
conn.close()

# Check if Chopani Mando Mesolithic and Paisra Mesolithic exist
has_chopani_meso = any("Chopani" in r["site_name"] and r["period"] == "Mesolithic" for r in rows)
has_paisra_meso = any("Paisra" in r["site_name"] and r["period"] == "Mesolithic" for r in rows)

if not has_chopani_meso:
    chopani_meso = {
        "site_id": max(r["site_id"] for r in rows) + 1,
        "period": "Mesolithic",
        "cultural_tradition": "Belan Advanced Mesolithic",
        "site_name": "Chopani-Mando (Mesolithic Phase)",
        "alternative_names": "Chopani Mando Phases II & III, Belan Alluvial Plain",
        "country": "India",
        "state_province": "Uttar Pradesh",
        "district": "Prayagraj (Allahabad)",
        "river_basin": "Belan River / Ganga Basin",
        "latitude": 24.9167,
        "longitude": 82.0500,
        "elevation_approx_m": 95,
        "excavator_discoverer": "G.R. Sharma & V.D. Misra (University of Allahabad)",
        "year_of_discovery": "1967",
        "excavation_seasons": "1972-1977",
        "tool_typology": "Geometric microliths (lunates, triangles, trapezes), Querns, Mullers, Hand-made corded pottery, Ring stones",
        "length_min_mm": 10.0,
        "length_max_mm": 26.0,
        "width_min_mm": 3.0,
        "width_max_mm": 7.5,
        "thickness_min_mm": 1.2,
        "thickness_max_mm": 2.8,
        "primary_raw_materials": "Chert, Chalcedony, Agate, Vindhyan Sandstone",
        "typical_usage": "Harvesting wild rice (Oryza nivara), game hunting, grain storage, wattle-and-daub hut construction",
        "associated_features": "Syllabus Benchmark: Alluvial plain adaptation; 13 circular/oval hut floors, storage pits, wild rice impressions in clay",
        "visual_link_archive": "https://commons.wikimedia.org/wiki/File:Chopani_Mando_Huts.jpg",
        "key_references": "Sharma, G.R. et al. (1980). Beginnings of Agriculture; Sankalia, H.D. (1977); Misra, V.N. (2001).",
        "geographical_zone": "Ganga Valley & Vindhyan Tract",
        "environmental_adaptation": "Alluvial plain adaptation",
        "manufacturing_technique": "Pressure flaking, punch bladelet technique, micro-burin technique, and blunting for geometric microliths",
        "palaeofauna_palaeoflora": "Wild rice (Oryza nivara), cattle (Bos gaurus), swamp deer, wild pig, bird bones",
        "rock_art_details": "None recorded",
        "syllabus_unit_coverage": "Unit-2 (Technology), Unit-4 (Mesolithic Alluvial Plain Adaptation)"
    }
    rows.append(chopani_meso)

if not has_paisra_meso:
    paisra_meso = {
        "site_id": max(r["site_id"] for r in rows) + 1,
        "period": "Mesolithic",
        "cultural_tradition": "Kharagpur Plateau Microlithic",
        "site_name": "Paisra (Mesolithic Phase)",
        "alternative_names": "Paisra Plateau Habitation Floor",
        "country": "India",
        "state_province": "Bihar",
        "district": "Munger",
        "river_basin": "Kharagpur Hills Basin / Kiul Tributary",
        "latitude": 25.1500,
        "longitude": 86.4167,
        "elevation_approx_m": 88,
        "excavator_discoverer": "P.C. Pant & Vidula Jayaswal (Banaras Hindu University)",
        "year_of_discovery": "1984",
        "excavation_seasons": "1984-1990",
        "tool_typology": "Geometric microliths (lunates, triangles, trapezes), Micro-cores, Scrapers, Fireplaces",
        "length_min_mm": 11.0,
        "length_max_mm": 25.0,
        "width_min_mm": 3.2,
        "width_max_mm": 7.0,
        "thickness_min_mm": 1.2,
        "thickness_max_mm": 2.6,
        "primary_raw_materials": "Quartz, Chert, Chalcedony",
        "typical_usage": "Plateau hill-tract foraging, bow and arrow hunting, animal skinning",
        "associated_features": "Syllabus Benchmark: Plateau occupation; circular stone alignments of hut floors, hearths with charcoal and burnt clay",
        "visual_link_archive": "https://commons.wikimedia.org/wiki/File:Paisra_Mesolithic_Floor.jpg",
        "key_references": "Pant, P.C., & Jayaswal, V. (1991). Paisra: The Stone Age Settlement of a Bihar Village; Misra, V.N. (2001).",
        "geographical_zone": "Eastern India",
        "environmental_adaptation": "Plateau occupation",
        "manufacturing_technique": "Micro-blade core reduction, pressure retouch, and micro-burin technique",
        "palaeofauna_palaeoflora": "Mammalian bone fragments, charcoal nodules, forest edible plant residues",
        "rock_art_details": "None recorded",
        "syllabus_unit_coverage": "Unit-2 (Technology), Unit-4 (Mesolithic Plateau Occupation)"
    }
    rows.append(paisra_meso)

# Update exact wording for syllabus benchmark sites:
for r in rows:
    name = r["site_name"]
    # Unit-4 Adaptations
    if "Birbhanpur" in name:
        r["environmental_adaptation"] = "Alluvial plain adaptation"
        r["syllabus_unit_coverage"] = "Unit-2 (Technology), Unit-3 (Eastern India), Unit-4 (Mesolithic Alluvial Plain Adaptation)"
        r["associated_features"] += " [Syllabus Benchmark: Alluvial plain adaptation]"
    elif "Chopani" in name and r["period"] == "Mesolithic":
        r["environmental_adaptation"] = "Alluvial plain adaptation"
    elif "Sarai Nahar Rai" in name or "Mahadaha" in name or "Damdama" in name:
        r["environmental_adaptation"] = "Horse-shoe lake sites"
        r["syllabus_unit_coverage"] = "Unit-1 (Palaeoenvironment & Fauna), Unit-2 (Technology), Unit-4 (Mesolithic Horse-shoe Lake Sites)"
        r["associated_features"] += " [Syllabus Benchmark: Horse-shoe lake sites]"
    elif "Langhnaj" in name or "Bagor" in name or "Tilwara" in name:
        r["environmental_adaptation"] = "Sand dune landscape"
        r["syllabus_unit_coverage"] = "Unit-1 (Faunal Evidence), Unit-2 (Technology), Unit-3 (Western India), Unit-4 (Mesolithic Sand Dune Landscape)"
        r["associated_features"] += " [Syllabus Benchmark: Sand dune landscape]"
    elif "Paisra" in name and r["period"] == "Mesolithic":
        r["environmental_adaptation"] = "Plateau occupation"

    # Unit-3 Regional Distribution tags
    if "Soan" in name or "Riwat" in name or "Nalagarh" in name or "Guler" in name:
        r["geographical_zone"] = "The Himalayan context (Soan Valley & Himachal Siwaliks)"
        r["syllabus_unit_coverage"] += ", Unit-3 (Himalayan Context)"
    elif r["state_province"] in ["Rajasthan", "Gujarat"] and r["period"] in ["Lower Paleolithic", "Middle Paleolithic", "Upper Paleolithic"]:
        r["geographical_zone"] = "Western India (Rajasthan & Gujarat)"
        r["syllabus_unit_coverage"] += ", Unit-3 (Western India)"
    elif r["state_province"] in ["Madhya Pradesh"] and r["period"] in ["Lower Paleolithic", "Middle Paleolithic", "Upper Paleolithic"]:
        r["geographical_zone"] = "Central India (Madhya Pradesh)"
        r["syllabus_unit_coverage"] += ", Unit-3 (Central India)"
    elif r["state_province"] in ["Maharashtra", "Andhra Pradesh", "Telangana", "Tamil Nadu", "Karnataka"] and r["period"] in ["Lower Paleolithic", "Middle Paleolithic", "Upper Paleolithic"]:
        r["geographical_zone"] = f"Peninsular India ({r['state_province']})"
        r["syllabus_unit_coverage"] += ", Unit-3 (Peninsular India)"
    elif r["state_province"] in ["West Bengal", "Odisha"] and r["period"] in ["Lower Paleolithic", "Middle Paleolithic", "Upper Paleolithic"]:
        r["geographical_zone"] = f"Eastern India ({r['state_province']})"
        r["syllabus_unit_coverage"] += ", Unit-3 (Eastern India)"

# Re-write CSV
fieldnames = list(rows[0].keys())
with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

# Re-create SQLite DB
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cols_sql = []
for f in fieldnames:
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

cur.execute("CREATE INDEX idx_period ON prehistoric_sites(period);")
cur.execute("CREATE INDEX idx_geo_zone ON prehistoric_sites(geographical_zone);")
cur.execute("CREATE INDEX idx_env_adaptation ON prehistoric_sites(environmental_adaptation);")
cur.execute("CREATE INDEX idx_spatial_coords ON prehistoric_sites(latitude, longitude);")

insert_sql = f"""
INSERT INTO prehistoric_sites (
    {", ".join(fieldnames)}
) VALUES ({", ".join(["?" for _ in fieldnames])})
"""

for r in rows:
    cur.execute(insert_sql, [r[f] for f in fieldnames])

# Create dedicated Views matching the Prehistory of India syllabus:

# View 1: Unit-3 Palaeolithic Cultures - Regional Distribution
cur.execute("""
CREATE VIEW view_unit3_palaeolithic_cultures AS
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
ORDER BY geographical_zone, period, site_name;
""")

# View 2: Unit-4 Mesolithic Adaptations (Alluvial plain, Horse-shoe lake, Sand dune, Plateau)
cur.execute("""
CREATE VIEW view_unit4_mesolithic_adaptations AS
SELECT 
    site_id,
    site_name,
    environmental_adaptation,
    geographical_zone,
    state_province,
    river_basin,
    tool_typology,
    manufacturing_technique,
    palaeofauna_palaeoflora,
    rock_art_details,
    associated_features,
    key_references
FROM prehistoric_sites
WHERE period = 'Mesolithic'
ORDER BY environmental_adaptation, site_name;
""")

# View 3: Unit-4 Prehistoric Rock Art
cur.execute("""
CREATE VIEW view_unit4_prehistoric_rock_art AS
SELECT 
    site_id,
    site_name,
    period,
    geographical_zone,
    state_province,
    district,
    latitude,
    longitude,
    rock_art_details,
    key_references
FROM prehistoric_sites
WHERE rock_art_details != 'None recorded'
ORDER BY geographical_zone, site_name;
""")

# View 4: Unit-2 Stone Age Technologies & Manufacturing Techniques
cur.execute("""
CREATE VIEW view_unit2_stone_age_technologies AS
SELECT 
    period,
    manufacturing_technique,
    COUNT(*) AS site_count,
    ROUND(AVG(length_max_mm), 1) AS avg_max_length_mm,
    ROUND(AVG(width_max_mm), 1) AS avg_max_width_mm,
    ROUND(AVG(thickness_max_mm), 1) AS avg_max_thickness_mm,
    GROUP_CONCAT(site_name, ', ') AS representative_sites
FROM prehistoric_sites
GROUP BY period, manufacturing_technique
ORDER BY period;
""")

conn.commit()

# Print confirmation
cur.execute("SELECT COUNT(*) FROM prehistoric_sites")
total_count = cur.fetchone()[0]

cur.execute("SELECT environmental_adaptation, GROUP_CONCAT(site_name, '; ') FROM prehistoric_sites WHERE period='Mesolithic' GROUP BY environmental_adaptation")
meso_summary = cur.fetchall()

conn.close()

print(f"Updated successfully! Total sites: {total_count}")
print("Mesolithic Adaptations exact alignment:")
for row in meso_summary:
    print(f" - {row[0]}: {row[1]}")
