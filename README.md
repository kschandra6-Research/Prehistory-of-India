# Prehistoric Archaeological Sites of the Indian Subcontinent: GIS & Academic Database

> **Idea & Design by K.S.Chandra 2026** • [kavikondalaschandra@gmail.com](mailto:kavikondalaschandra@gmail.com)  
> Aligned with the University Curriculum Paper: **Prehistory of India – Origin and Evolution of Man in Indian Subcontinent**.

This database contains **1,588 georeferenced archaeological sites** spanning Lower Paleolithic, Middle Paleolithic, Upper Paleolithic, Mesolithic, and Neolithic phases across the Indian Subcontinent, combining:
1. **104 Curated Syllabus Landmark Sites**: In-depth benchmark sites with metric dimensions, radiocarbon/OSL/cosmogenic dates, lithic manufacturing techniques, palaeofauna/flora, and rock art.
2. **1,484 IAR Comprehensive National Survey Sites (1953–1976)**: Complete digitized survey records of Palaeolithic discoveries published across 22 annual volumes of *Indian Archaeology: A Review* (ASI), systematically compiled in Vidyarthi & Chauhan (2025).

---

## 📖 Peer-Reviewed Primary Reference

All IAR Palaeolithic survey records and mapping classifications in this compendium are cited and sourced from:

```bibtex
@article{vidyarthi2025mapping,
  title     = {Mapping the Indian Palaeolithic},
  author    = {Vidyarthi, Vibha and Chauhan, Parth},
  journal   = {Journal of Computer Applications in Archaeology},
  volume    = {8},
  number    = {1},
  pages     = {78--93},
  year      = {2025},
  doi       = {10.5334/jcaa.148},
  url       = {https://doi.org/10.5334/jcaa.148}
}
```

* **Full APA Citation**: Vidyarthi, V. and Chauhan, P. 2025. Mapping the Indian Palaeolithic. *Journal of Computer Applications in Archaeology*, 8(1): 78–93. DOI: [https://doi.org/10.5334/jcaa.148](https://doi.org/10.5334/jcaa.148).
* **Archival Survey Source**: Archaeological Survey of India (ASI), *Indian Archaeology: A Review* (IAR), Volumes 1953–54 to 1975–76.

---

## 📊 Summary of Database Coverage

| Metric | Count / Coverage | Notes |
| :--- | :--- | :--- |
| **Total Archaeological Sites** | **1,588** | 1,484 IAR Survey Sites + 104 Syllabus Landmark Sites |
| **Lower Paleolithic** | **985** | Acheulian bifaces, cleavers, and Soanian pebble-choppers |
| **Middle Paleolithic** | **426** | Levallois prepared-core, Nevasan, and flake-tool traditions |
| **Upper Paleolithic** | **38** | Blade-and-burin industries (Series III) |
| **Mesolithic** | **98** | Microlithic assemblages, rockshelters, and open camp sites |
| **Neolithic** | **41** | Polished celts, ground stone axes, and early agro-pastoral settlements |
| **Excavated Sites** | **45** | Includes Bhimbetka, Hunsgi, Nevasa, Attirampakkam, Adamgarh, Paisra |
| **Fossil / Megafauna Localities** | **80+** | *Bos namadicus*, *Elephas*, *Equus*, *Hexaprotodon*, Hathnora calvarium |
| **Geographical States / UTs** | **22** | Maharashtra (397), Madhya Pradesh (309), Andhra Pradesh (203), UP, GJ, RJ, etc. |
| **Spatial CRS** | **EPSG:4326** | WGS 84 Coordinates (Latitude / Longitude) |

---

## 📚 Direct Mapping to the "Prehistory of India" Syllabus

### **Unit-1: Geological Time Scale, Human Evolution, Palaeoenvironment (Flora & Fauna)**
* Column `palaeofauna_palaeoflora`: Details Pleistocene megafauna (*Bos namadicus*, *Elephas antiquus/namadicus*, *Equus namadicus*, *Hexaprotodon palaeindicus*) and Holocene wild/domesticated taxa (*Oryza sativa*, *Hordeum vulgare*, *Rucervus duvaucelii*).
* Human Evolutionary Evidence: Includes **Hathnora** (*Narmada Man* / archaic *Homo sapiens* calvarium discovered by Arun Sonakia 1982; clavicle discovered by A.A. Sankhyan 1997).

### **Unit-2: Stone Age Technologies – Tool Types, Techniques of Manufacture & Probable Usages**
* Column `tool_typology`: Formal lithic & organic classifications (Handaxes, Cleavers, Levallois points, Prismatic blades, Geometric microliths, Ground stone celts, Bone harpoons).
* Column `manufacturing_technique`: Categorized into:
  1. *Block-on-block / anvil technique* & *stone hammer direct percussion* (Early Acheulian & Soanian).
  2. *Soft hammer / cylinder hammer billet technique* (Late Acheulian).
  3. *Levallois prepared-core technique* (Middle Paleolithic).
  4. *Punch blade / indirect percussion technique* (Upper Paleolithic).
  5. *Pressure flaking & micro-burin technique* (Mesolithic).
  6. *Pecking, grinding and hone-polishing* (Neolithic).
* Metric dimensions: `length_min_mm`, `length_max_mm`, `width_min_mm`, `width_max_mm`, `thickness_min_mm`, `thickness_max_mm`.

### **Unit-3: Palaeolithic Cultures – Regional Distribution, Stratigraphy & Cultural Evidence**
Tracked via column `geographical_zone` and pre-built view `view_unit3_palaeolithic_cultures`:
1. **The Himalayan context**: **Soan Valley & Riwat** (Potwar Plateau), **Guler** (Beas Terraces T1–T5, Kangra), **Nalagarh** (Sirsa Valley).
2. **Western India**: 
   - *Rajasthan*: **Didwana (Singi Talav & 16R Dune)**, **Budha Pushkar**, **Sonita**, **Bichore**, **Chittorgarh**.
   - *Gujarat*: **Umrethi / Hiran Valley** (Miliolite stratigraphy), **Visadi**, **Dhaneti**, **Surat & Kutch complexes**.
3. **Central India**: 
   - *Madhya Pradesh*: **Bhimbetka (Auditorium & III F-23)**, **Hathnora**, **Samnapur**, **Sihawal**, **Baghor I & II**, **Mandasor**, **Adamgarh**, **Chorhat**.
4. **The Peninsular India**:
   - *Maharashtra*: **Nevasa**, **Chirki-on-Nevasa**, **Bori**, **Morgaon**, **Patne**, **Inamgaon**, **Khandivli**, **Dhulia & Chanda basins**.
   - *Andhra Pradesh & Telangana*: **Attirampakkam**, **Jwalapuram (Loc. 22 & 9)**, **Kurnool Caves**, **Renigunta**, **Giddalur**, **Nagarjunakonda**, **Nellore survey sites**.
   - *Tamil Nadu*: **Pallavaram**, **Vadamadurai**, **Gudiyam Cave**, **Paiyampalli**, **Teri Sites**.
   - *Karnataka*: **Isampur**, **Hunsgi**, **Yediyapur**, **Anagawadi**, **Khyad**, **Kovalli**, **Taminhal**, **Sangankallu**, **Piklihal**, **Brahmagiri**.
5. **Eastern India**:
   - *West Bengal*: **Birbhanpur**, **Susunia Hill**, **Pandu Rajar Dhibi**, **Bankura & Midnapore complexes**.
   - *Odisha*: **Kuliana**, **Kuchai**, **Mayurbhanj (Baripada)**, **Bonaigarh**, **Golbai Sasan**.
   - *Bihar & Jharkhand*: **Paisra**, **Bhimbandh**, **Ranchi & Singhbhum gravels**.

### **Unit-4: Mesolithic Culture – Adaptations, Typology & Prehistoric Rock Art**
Tracked via column `environmental_adaptation` and pre-built view `view_unit4_mesolithic_adaptations`:
1. **Alluvial plain adaptation**: **Chopani-Mando (Mesolithic Phase)**, **Birbhanpur**.
2. **Horse-shoe lake sites (Oxbow lakes of Ganga Plain)**: **Sarai-Nahar Rai**, **Mahadaha**, **Damdama**.
3. **Sand dune landscape**: **Langhnaj**, **Bagor (Phase I)**, **Tilwara**.
4. **Plateau occupation**: **Paisra (Mesolithic Phase)** (Kharagpur hill plateau basin).
5. **Prehistoric Rock Art in India**:
   - *Central India*: **Bhimbetka** (Cupules, petroglyphs & Mesolithic polychrome paintings), **Adamgarh** (hunting scenes), **Pachmarhi (Dorothy Deep)**.
   - *Peninsular India*: **Kupgal / Sangankallu** (Dolerite rock bruisings of humped cattle & anthropomorphs), **Gauri Gundam**.
   - *Vindhyan Range*: **Morhana Pahar & Lekhahia**, **Baghaikhor**.

---

## 📁 Repository Contents

1. **`index.html`**:
   - Interactive GIS & academic dashboard with responsive Leaflet map, Chart.js visualizer, dataset filters (All / IAR / Landmarks / Excavated), Site Dossier inspector, and toolplate Lightbox modal.
2. **`launch_dashboard.py`**:
   - Python HTTP launcher script. Automatically opens `index.html` on `http://localhost:8000/`.
3. **`Indian Palaeolithic Data.xlsx`**:
   - Complete original spreadsheet containing:
     - Sheet 1: `Data` (1,484 IAR survey entries, 1953–54 to 1975–76)
     - Sheet 2: `Reference` (Vidyarthi & Chauhan 2025 citation and DOI)
4. **`prehistoric_sites_subcontinent.csv`**:
   - Master CSV table containing all **1,588 georeferenced archaeological sites** with WGS 84 coordinates (`latitude`, `longitude`), period, district, state, artifacts, and academic citations.
5. **`iar_palaeolithic_survey_1484.csv`**:
   - Dedicated CSV extract of the 1,484 *Indian Archaeology: A Review* survey records with volume, page, context, and investigators.
6. **`prehistoric_sites_subcontinent.db`**:
   - SQLite3 database equipped with spatial and topical indexes:
     - `prehistoric_sites`: 1,588 unified master records
     - `iar_palaeolithic_sites`: 1,484 IAR survey entries
     - `landmark_syllabus_sites`: 104 curriculum benchmark sites
     - `project_metadata`: Citation, provenance, and metadata
     - Pre-built Analytical Views:
       - `view_iar_state_summary`
       - `view_iar_volume_summary`
       - `view_iar_excavations`
       - `view_academic_references`
       - `view_unit3_palaeolithic_cultures`
       - `view_unit4_mesolithic_adaptations`
       - `view_unit4_prehistoric_rock_art`
       - `view_unit2_stone_age_technologies`
7. **`sites_data.json` & `iar_sites_data.json`**:
   - Structured JSON records consumed by the web application.
8. **`build_updated_palaeolithic_database.py` & `generate_complete_interactive_app.py`**:
   - Reproducible Python pipeline scripts for database building and dashboard generation.

---

## 🗺️ How to Load into QGIS

1. Open **QGIS** > **Layer** > **Add Layer** > **Add Delimited Text Layer...**
2. Browse to `prehistoric_sites_subcontinent.csv` (or `iar_palaeolithic_survey_1484.csv`).
3. In **Geometry Definition**:
   * **X field**: `longitude`
   * **Y field**: `latitude`
   * **CRS**: `EPSG:4326 - WGS 84`
4. Style points by categorizing under `period`, `dataset_source`, `state_province`, or `location_integrity`.
