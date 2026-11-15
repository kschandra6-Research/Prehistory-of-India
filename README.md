# Prehistoric Archaeological Sites of the Indian Subcontinent: GIS & Academic Database

> **Idea & Design by K.S.Chandra 2026** • [kavikondalaschandra@gmail.com](mailto:kavikondalaschandra@gmail.com)  
> Aligned with the University Curriculum Paper: **Prehistory of India – Origin and Evolution of Man in Indian Subcontinent**.

This database contains **104 georeferenced archaeological sites** spanning Lower, Middle, and Upper Paleolithic, Mesolithic, and Neolithic phases across the Indian Subcontinent (India, Pakistan).

---

## 📚 Direct Mapping to the "Prehistory of India" Syllabus

### **Unit-1: Geological Time Scale, Human Evolution, Palaeoenvironment (Flora & Fauna)**
* Column `palaeofauna_palaeoflora`: Details Pleistocene megafauna (*Bos namadicus*, *Elephas antiquus/namadicus*, *Equus namadicus*, *Hexaprotodon palaeindicus*) and Holocene wild/domesticated taxa (*Oryza sativa*, *Hordeum vulgare*, *Rucervus duvaucelii*).
* Human Evolutionary Evidence: Includes **Hathnora** (*Narmada Man* / archaic *Homo sapiens* calvarium).

### **Unit-2: Stone Age Technologies – Tool Types, Techniques of Manufacture & Probable Usages**
* Column `tool_typology`: Formal lithic & organic classifications (Handaxes, Cleavers, Levallois points, Prismatic blades, Geometric microliths, Ground stone celts, Bone harpoons).
* Column `manufacturing_technique`: Categorized into:
  1. *Block-on-block / anvil technique* & *stone hammer direct percussion* (Early Acheulian & Soanian).
  2. *Soft hammer / cylinder hammer billet technique* (Late Acheulian).
  3. *Levallois prepared-core technique* (Middle Paleolithic).
  4. *Punch blade / indirect percussion technique* (Upper Paleolithic).
  5. *Pressure flaking & micro-burin technique* (Mesolithic).
  6. *Pecking, grinding and hone-polishing* (Neolithic).
* Quantified metric dimensions (`length_min_mm`, `length_max_mm`, `width`, `thickness`).

### **Unit-3: Palaeolithic Cultures – Regional Distribution, Stratigraphy & Cultural Evidence**
Tracked via column `geographical_zone` and pre-built view `view_unit3_palaeolithic_cultures`:
1. **The Himalayan context**: **Soan Valley & Riwat** (Potwar Plateau), **Guler** (Beas Terraces T1–T5, Kangra), **Nalagarh** (Sirsa Valley).
2. **Western India**: 
   - *Rajasthan*: **Didwana (Singi Talav & 16R Dune)**, **Budha Pushkar**.
   - *Gujarat*: **Umrethi / Hiran Valley** (Miliolite stratigraphy), **Visadi**, **Dhaneti**.
3. **Central India**: 
   - *Madhya Pradesh*: **Bhimbetka (Auditorium & III F-23)**, **Hathnora**, **Samnapur**, **Sihawal**, **Baghor I & II**, **Mandasor**, **Chorhat**.
4. **The Peninsular India**:
   - *Maharashtra*: **Nevasa**, **Chirki-on-Nevasa**, **Bori**, **Morgaon**, **Patne**, **Inamgaon**, **Khandivli**, **Wadoli**.
   - *Andhra Pradesh*: **Jwalapuram (Loc. 22 & 9)**, **Muchchatla Chintamanu Gavi (Kurnool Caves)**, **Renigunta**, **Giddalur**, **Nagarjunakonda**, **Gunjana Valley**, **Nandipalle**, **Dornal**.
   - *Telangana*: **Jalampur**, **Gauri Gundam**, **Polakonda**, **Utnur**.
   - *Tamil Nadu*: **Attirampakkam**, **Pallavaram**, **Vadamadurai**, **Gudiyam Cave**, **Paiyampalli**, **Teri Sites**.
   - *Karnataka*: **Isampur**, **Hunsgi**, **Yediyapur**, **Anagawadi**, **Khyad**, **Kovalli**, **Taminhal**, **Sangankallu**, **Piklihal**, **Brahmagiri**, **Maski**, **Tekkalakota**, **Hallur**, **T. Narasipur**, **Hemmige**, **Kudatini**.
5. **Eastern India**:
   - *West Bengal*: **Birbhanpur**, **Pandu Rajar Dhibi**, **Bharatpur**.
   - *Odisha*: **Kuliana**, **Kuchai**, **Bonaigarh**, **Golbai Sasan**.

### **Unit-4: Mesolithic Culture – Adaptations, Typology & Prehistoric Rock Art**
Tracked via column `environmental_adaptation` and pre-built view `view_unit4_mesolithic_adaptations`:
1. **Alluvial plain adaptation**: **Chopani-Mando (Mesolithic Phase)**, **Birbhanpur**.
2. **Horse-shoe lake sites (Oxbow lakes of Ganga Plain)**: **Sarai-Nahar Rai**, **Mahadaha**, **Damdama**.
3. **Sand dune landscape**: **Langhnaj**, **Bagor (Phase I)**, **Tilwara**.
4. **Plateau occupation**: **Paisra (Mesolithic Phase)** (Kharagpur hill plateau basin).
5. **Prehistoric Rock Art in India**:
   - *Central India*: **Bhimbetka** (Cupules, petroglyphs & Mesolithic polychrome paintings), **Adamgarh** (hunting scenes), **Pachmarhi (Dorothy Deep)** (Mahadeo Hills white/red pictographs).
   - *Peninsular India*: **Kupgal / Sangankallu** (Dolerite rock bruisings of humped cattle & anthropomorphs), **Gauri Gundam** (Godavari basin petroglyphs).
   - *Vindhyan Range*: **Morhana Pahar & Lekhahia**, **Baghaikhor** (Carlleyle's pioneer rock art discoveries).

---

## 📁 Repository Contents

1. **`prehistoric_sites_subcontinent.csv`**:
   - 104 rows $\times$ 33 columns with exact WGS 84 coordinates (`latitude`, `longitude`), elevation, metric dimensions, environmental adaptations, manufacturing techniques, fauna/flora, and citations.
2. **`prehistoric_sites_subcontinent.db`**:
   - SQLite3 database equipped with spatial and topical indexes, plus dedicated syllabus views:
     - `view_unit3_palaeolithic_cultures`
     - `view_unit4_mesolithic_adaptations`
     - `view_unit4_prehistoric_rock_art`
     - `view_unit2_stone_age_technologies`
3. **Python Scripts**:
   - `build_database.py`, `add_comprehensive_records.py`, `patch_syllabus_exact.py`.

---

## 🗺️ How to Load into QGIS

1. Open **QGIS** > **Layer** > **Add Layer** > **Add Delimited Text Layer...**
2. Browse to `prehistoric_sites_subcontinent.csv`.
3. In **Geometry Definition**:
   - **X field**: `longitude`
   - **Y field**: `latitude`
   - **CRS**: `EPSG:4326 - WGS 84`
4. Style points by categorizing under `period`, `geographical_zone`, or `environmental_adaptation`.
