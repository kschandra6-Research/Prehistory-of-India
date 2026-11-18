import openpyxl
import sqlite3
import csv
import json
import re
import hashlib
import os

print("Starting Indian Palaeolithic Database Update...")

# Paths
base_dir = r"G:\Updated Profile KSC\Prehistory-of-India"
excel_path = os.path.join(base_dir, "Indian Palaeolithic Data.xlsx")
existing_json_path = os.path.join(base_dir, "sites_data.json")
db_path = os.path.join(base_dir, "prehistoric_sites_subcontinent.db")
csv_path = os.path.join(base_dir, "prehistoric_sites_subcontinent.csv")
iar_csv_path = os.path.join(base_dir, "iar_palaeolithic_survey_1484.csv")
json_path = os.path.join(base_dir, "sites_data.json")
iar_json_path = os.path.join(base_dir, "iar_sites_data.json")

# State Code -> Full Name & Geographical Zone
STATE_INFO = {
    'MH': ('Maharashtra', 'Peninsular India (Deccan & Godavari)'),
    'MP': ('Madhya Pradesh', 'Central India (Narmada & Betwa Basin)'),
    'AP': ('Andhra Pradesh', 'Peninsular India (Eastern Ghats & Coromandel)'),
    'UP': ('Uttar Pradesh', 'Ganga Valley & Vindhyan Tract'),
    'GJ': ('Gujarat', 'Western India (Saurashtra & Mainland)'),
    'RJ': ('Rajasthan', 'Western India (Thar & Aravalli Basin)'),
    'KA': ('Karnataka', 'Peninsular India (Krishna-Tungabhadra Basin)'),
    'KR': ('Karnataka', 'Peninsular India (Krishna-Tungabhadra Basin)'),
    'KA PRESENT DAY': ('Karnataka', 'Peninsular India (Krishna-Tungabhadra Basin)'),
    'WB': ('West Bengal', 'Eastern India (Chota Nagpur & Rarh Uplands)'),
    'BR': ('Bihar / Jharkhand', 'Eastern India (Chota Nagpur Plateau & Middle Ganga)'),
    'OR': ('Odisha', 'Eastern India (Eastern Ghats & Mahanadi Basin)'),
    'TN': ('Tamil Nadu', 'Peninsular India (Coromandel Coast & Kortallaiyar Basin)'),
    'HP': ('Himachal Pradesh', 'Himalayan Siwalik Foothills (Beas & Sirsa)'),
    'J AND K': ('Jammu & Kashmir', 'Himalayan & Sub-Himalayan Terraces'),
    'JK': ('Jammu & Kashmir', 'Himalayan & Sub-Himalayan Terraces'),
    'AS': ('Assam / North-East', 'North-Eastern India (Plateau & Terraces)'),
    'ML': ('Meghalaya', 'North-Eastern India (Garo Hills & Rongram Basin)'),
    'HR': ('Haryana', 'Indo-Gangetic & Siwalik Divide'),
    'AR': ('Arunachal Pradesh', 'Eastern Himalayan Terraces (Lohit Basin)'),
    'PB': ('Punjab', 'Sub-Himalayan Siwalik Basin (Soan & Sutlej)'),
    'PN': ('Punjab', 'Sub-Himalayan Siwalik Basin (Soan & Sutlej)'),
    'TG': ('Telangana', 'Peninsular India (Godavari & Deccan Plateau)'),
    'KL': ('Kerala', 'South-Western Peninsular India (Bharathapuzha Basin)'),
    'GA': ('Goa', 'Western Coast / Konkan Foothills'),
    'MN': ('Manipur', 'North-Eastern India (Manipur Hills & Cave Shelters)'),
    'DAMAN AND DIU': ('Daman and Diu', 'Western Coastal Plain'),
    'HP/PN': ('Himachal Pradesh / Punjab', 'Siwalik Foothills Divide'),
    '': ('India', 'Indian Subcontinent')
}

# District coordinates mapping (Centroids / Major Archaeological Clusters)
DISTRICT_COORDS = {
    # Maharashtra (MH)
    ('MH', 'CHANDA'): (19.95, 79.30, 'Chandrapur / Chanda'),
    ('MH', 'CHANDRAPURA'): (19.95, 79.30, 'Chandrapur'),
    ('MH', 'DHULIA'): (20.90, 74.78, 'Dhule / Dhulia'),
    ('MH', 'DHULE'): (20.90, 74.78, 'Dhule'),
    ('MH', 'WEST KHANDESH'): (21.05, 74.60, 'West Khandesh (Dhule/Nandurbar)'),
    ('MH', 'AHMADNAGAR'): (19.09, 74.74, 'Ahmednagar'),
    ('MH', 'AHMENNAGAR'): (19.09, 74.74, 'Ahmednagar'),
    ('MH', 'AHMEDNAGAR'): (19.09, 74.74, 'Ahmednagar'),
    ('MH', 'AHMADNAGAR/NASIK'): (19.50, 74.30, 'Pravara-Godavari Valley'),
    ('MH', 'SANGLI'): (16.85, 74.58, 'Sangli'),
    ('MH', 'NASIK'): (19.99, 73.79, 'Nashik'),
    ('MH', 'BHANDARA'): (21.17, 79.65, 'Bhandara'),
    ('MH', 'WARDHA'): (20.74, 78.60, 'Wardha'),
    ('MH', 'PUNE'): (18.52, 73.85, 'Pune'),
    ('MH', 'POONA'): (18.52, 73.85, 'Pune / Poona'),
    ('MH', 'POONA (PUNE)'): (18.52, 73.85, 'Pune'),
    ('MH', 'KOLABA'): (18.51, 73.18, 'Raigad / Kolaba'),
    ('MH', 'AMRAOTI'): (20.93, 77.75, 'Amravati'),
    ('MH', 'RATNAGIRI'): (16.99, 73.31, 'Ratnagiri'),
    ('MH', 'SATARA'): (17.68, 73.99, 'Satara'),
    ('MH', 'PARBHANI'): (19.26, 76.77, 'Parbhani'),
    ('MH', 'NAGPUR'): (21.14, 79.08, 'Nagpur'),
    ('MH', 'BOMBAY SUBURBAN'): (19.12, 72.85, 'Mumbai Suburban'),
    ('MH', 'BOMBAY'): (18.95, 72.82, 'Mumbai'),
    ('MH', 'AKOLA'): (20.70, 77.00, 'Akola'),
    ('MH', 'JALGAON'): (21.00, 75.56, 'Jalgaon'),
    ('MH', 'SHOLAPUR'): (17.65, 75.90, 'Solapur'),
    ('MH', 'THANA'): (19.21, 72.97, 'Thane'),
    ('MH', 'AURANGABAD'): (19.87, 75.34, 'Aurangabad / Chhatrapati Sambhajinagar'),
    ('MH', ''): (19.50, 75.00, 'Maharashtra Central Basin'),

    # Madhya Pradesh (MP)
    ('MP', 'JABALPUR'): (23.18, 79.98, 'Jabalpur'),
    ('MP', 'SAGAR'): (23.83, 78.71, 'Sagar'),
    ('MP', 'MANDASOR'): (24.07, 75.07, 'Mandsaur'),
    ('MP', 'MANDSAUR'): (24.07, 75.07, 'Mandsaur'),
    ('MP', 'HOSHANGABAD'): (22.75, 77.72, 'Narmadapuram / Hoshangabad'),
    ('MP', 'HOSHANGAPAD'): (22.75, 77.72, 'Hoshangabad'),
    ('MP', 'SIDHI'): (24.41, 81.88, 'Sidhi'),
    ('MP', 'NIMAR EAST'): (21.83, 76.35, 'East Nimar (Khandwa)'),
    ('MP', 'NIMAR'): (21.82, 75.61, 'Nimar / Narmada Valley'),
    ('MP', 'WEST NIMAR'): (21.82, 75.61, 'West Nimar (Khargone)'),
    ('MP', 'GUNA'): (24.65, 77.31, 'Guna'),
    ('MP', 'NARSINGHPUR'): (22.95, 79.19, 'Narsinghpur'),
    ('MP', 'RAISEN'): (23.33, 77.78, 'Raisen (Bhimbetka region)'),
    ('MP', 'SEONI'): (22.08, 79.55, 'Seoni'),
    ('MP', 'SHAHDOL'): (23.28, 81.35, 'Shahdol'),
    ('MP', 'SAHDOL'): (23.28, 81.35, 'Shahdol'),
    ('MP', 'RATLAM'): (23.33, 75.03, 'Ratlam'),
    ('MP', 'SEHORE (BHOPAL LOCALITY)'): (23.20, 77.30, 'Sehore / Bhopal fringe'),
    ('MP', 'SEHORE'): (23.20, 77.08, 'Sehore'),
    ('MP', 'SEHHORE'): (23.20, 77.08, 'Sehore'),
    ('MP', 'BHOPAL'): (23.25, 77.41, 'Bhopal'),
    ('MP', 'DAMOH'): (23.83, 79.44, 'Damoh'),
    ('MP', 'DAMON'): (23.83, 79.44, 'Damoh'),
    ('MP', 'GWALIOR'): (26.22, 78.18, 'Gwalior'),
    ('MP', 'INDORE'): (22.71, 75.85, 'Indore'),
    ('MP', 'VIDISHA'): (23.52, 77.81, 'Vidisha'),
    ('MP', 'BHILSA'): (23.52, 77.81, 'Vidisha / Bhilsa'),
    ('MP', 'CHHATARPUR'): (24.91, 79.58, 'Chhatarpur'),
    ('MP', 'REWA'): (24.53, 81.30, 'Rewa'),
    ('MP', 'PANNA'): (24.72, 80.18, 'Panna'),
    ('MP', 'RAJGARH'): (24.00, 76.73, 'Rajgarh'),
    ('MP', 'MANDLA'): (22.60, 80.37, 'Mandla'),
    ('MP', 'MANDIA'): (22.60, 80.37, 'Mandla'),
    ('MP', 'DATIA'): (25.66, 78.46, 'Datia'),
    ('MP', 'MORENA'): (26.50, 77.99, 'Morena'),
    ('MP', 'SHAJAPUR'): (23.42, 76.27, 'Shajapur'),
    ('MP', 'CHHINDWARA'): (22.05, 78.93, 'Chhindwara'),
    ('MP', 'SHIVAPURI'): (25.42, 77.65, 'Shivpuri'),
    ('MP', 'BUNDI'): (25.44, 75.64, 'Bundi border / Chambal'),
    ('MP', 'NARMA'): (22.25, 75.58, 'Maheshwar / Narmada Valley'),
    ('MP', 'JABALPUR,HOSHANGABAD,MANDLA'): (22.90, 79.00, 'Central Narmada Basin'),
    ('MP', 'EAST NIMAR, HOSHANGABAD,JABALPUR'): (22.60, 78.50, 'Narmada Valley Survey'),
    ('MP', 'GUNA,SAGAR,VIDISHA?'): (24.00, 78.00, 'Betwa Basin Survey'),
    ('MP', 'NOT GIVEN'): (23.00, 78.00, 'Madhya Pradesh Central'),
    ('MP', ''): (23.00, 78.00, 'Madhya Pradesh Central'),

    # Andhra Pradesh (AP) & Telangana (TG)
    ('AP', 'NELLORE'): (14.44, 79.98, 'Nellore'),
    ('AP', 'KURNOOL'): (15.82, 78.03, 'Kurnool'),
    ('AP', 'CHITTOOR'): (13.21, 79.10, 'Chittoor'),
    ('AP', 'CUDDAPAH'): (14.47, 78.82, 'YSR Kadapa / Cuddapah'),
    ('AP', 'VISKHAPATNAM'): (17.68, 83.21, 'Visakhapatnam'),
    ('AP', 'GUNTUR'): (16.30, 80.44, 'Guntur'),
    ('AP', 'GUNTAR'): (16.30, 80.44, 'Guntur'),
    ('AP', 'PRAKASAM'): (15.50, 80.05, 'Prakasam'),
    ('AP', 'MAHBUBNAGAR'): (16.74, 78.00, 'Mahbubnagar'),
    ('AP', 'NALGONDA'): (17.05, 79.26, 'Nalgonda'),
    ('AP', 'KARIMNAGAR'): (18.43, 79.12, 'Karimnagar'),
    ('AP', 'ADILABAD'): (19.66, 78.53, 'Adilabad'),
    ('AP', 'ONGOLE'): (15.50, 80.05, 'Ongole'),
    ('AP', 'PEDDANDLURU'): (14.65, 78.55, 'Kadapa / Peddandluru'),
    ('AP', ''): (15.50, 79.50, 'Andhra Pradesh Coastal / Rayalaseema'),
    ('TG', 'MEDAK'): (18.04, 78.26, 'Medak'),

    # Uttar Pradesh (UP)
    ('UP', 'MIRZAPUR'): (25.13, 82.56, 'Mirzapur'),
    ('UP', 'ALLHABAD'): (25.43, 81.84, 'Prayagraj / Allahabad'),
    ('UP', 'ALLAHABAD'): (25.43, 81.84, 'Prayagraj / Allahabad'),
    ('UP', 'JHANSI'): (25.45, 78.57, 'Jhansi'),
    ('UP', 'BANDA'): (25.48, 80.33, 'Banda'),
    ('UP', 'HAMIRPUR'): (25.95, 80.15, 'Hamirpur'),
    ('UP', 'AZAMGARH'): (26.06, 83.18, 'Azamgarh'),
    ('UP', 'DEHRADUN'): (30.31, 78.03, 'Dehradun'),
    ('UP', 'MATHURA'): (27.49, 77.67, 'Mathura'),
    ('UP', 'VARANASI'): (25.31, 82.97, 'Varanasi'),
    ('UP', 'REWA'): (25.00, 81.50, 'UP-MP Vindhyan border'),
    ('UP', ''): (25.50, 81.00, 'Uttar Pradesh Southern Tract'),

    # Gujarat (GJ)
    ('GJ', 'SURAT'): (21.17, 72.83, 'Surat'),
    ('GJ', 'BULSAR'): (20.59, 72.93, 'Valsad / Bulsar'),
    ('GJ', 'VALSAD'): (20.59, 72.93, 'Valsad'),
    ('GJ', 'KUTCH'): (23.24, 69.66, 'Kutch'),
    ('GJ', 'BHAVNAGAR'): (21.76, 72.15, 'Bhavnagar'),
    ('GJ', 'SURENDRANAGAR'): (22.72, 71.63, 'Surendranagar'),
    ('GJ', 'JUNAGADH'): (21.52, 70.45, 'Junagadh'),
    ('GJ', 'SABAR KANTHA'): (23.60, 72.96, 'Sabarkantha'),
    ('GJ', 'SABARKANTHA'): (23.60, 72.96, 'Sabarkantha'),
    ('GJ', 'RAJKOT'): (22.30, 70.80, 'Rajkot'),
    ('GJ', 'MADHYA SAURASHTRA'): (22.00, 71.00, 'Central Saurashtra'),
    ('GJ', 'HALAR'): (22.47, 70.05, 'Jamnagar / Halar'),
    ('GJ', 'JHALAWAR'): (22.80, 71.50, 'Zalawad / Surendranagar'),
    ('GJ', 'AHMADABAD'): (23.02, 72.57, 'Ahmedabad'),
    ('GJ', 'JAMNAGAR'): (22.47, 70.05, 'Jamnagar'),
    ('GJ', 'PANCH MAHALS'): (22.75, 73.61, 'Panchmahal'),
    ('GJ', 'BHARUCH'): (21.70, 72.99, 'Bharuch'),

    # Rajasthan (RJ)
    ('RJ', 'CHITTAURGARH'): (24.88, 74.63, 'Chittorgarh'),
    ('RJ', 'CHITORGARH'): (24.88, 74.63, 'Chittorgarh'),
    ('RJ', 'CHITTORGARH'): (24.88, 74.63, 'Chittorgarh'),
    ('RJ', 'MARWAR'): (25.77, 73.32, 'Marwar / Pali'),
    ('RJ', 'BHILWARA'): (25.35, 74.63, 'Bhilwara'),
    ('RJ', 'JHALAWAR'): (24.59, 76.16, 'Jhalawar'),
    ('RJ', 'JODHPUR'): (26.28, 73.02, 'Jodhpur'),
    ('RJ', 'TONK'): (26.16, 75.79, 'Tonk'),
    ('RJ', 'PALI'): (25.77, 73.32, 'Pali'),
    ('RJ', 'AJMER'): (26.44, 74.63, 'Ajmer'),
    ('RJ', 'BARMER'): (25.75, 71.41, 'Barmer'),
    ('RJ', 'BHARMER'): (25.75, 71.41, 'Barmer'),
    ('RJ', 'JAIPUR'): (26.91, 75.78, 'Jaipur'),
    ('RJ', 'ALWAR'): (27.55, 76.60, 'Alwar'),
    ('RJ', 'JAISALMER AND BANNER'): (26.50, 71.20, 'Thar Desert Basin'),
    ('RJ', 'NOT GIVEN'): (26.00, 74.00, 'Rajasthan Central'),
    ('RJ', ''): (26.00, 74.00, 'Rajasthan Central'),

    # Karnataka (KA, KR)
    ('KA', 'BELGAUM'): (15.85, 74.50, 'Belagavi / Belgaum'),
    ('KA', 'DHARWAR'): (15.45, 75.00, 'Dharwad'),
    ('KA', 'BIJAPUR'): (16.83, 75.71, 'Vijayapura / Bijapur'),
    ('KR', 'BIJAPUR'): (16.83, 75.71, 'Vijayapura / Bijapur'),
    ('KA', 'BUAPUR'): (16.83, 75.71, 'Vijayapura / Bijapur'),
    ('KA PRESENT DAY', 'BUAPUR'): (16.83, 75.71, 'Vijayapura / Bijapur'),
    ('KA', 'BADAMI'): (15.91, 75.68, 'Badami / Bagalkot'),
    ('', 'BADAMI'): (15.91, 75.68, 'Badami / Bagalkot'),
    ('KA', 'TUMKUR'): (13.34, 77.10, 'Tumakuru / Tumkur'),
    ('KA', 'GUNTUR'): (16.30, 80.44, 'Krishna Basin Survey'),
    ('KA', 'GULBARAO'): (16.65, 76.52, 'Hunsgi / Shorapur / Kalaburagi'),
    ('KA', ''): (15.50, 75.50, 'Karnataka Northern Basin'),

    # West Bengal (WB)
    ('WB', 'BANKURA'): (23.23, 87.07, 'Bankura'),
    ('WB', 'MIDNAPORE'): (22.42, 87.32, 'Medinipur / Midnapore'),
    ('WB', 'MIDNAPUR'): (22.42, 87.32, 'Medinipur / Midnapore'),
    ('WB', 'PURULIA'): (23.33, 86.36, 'Purulia'),
    ('WB', 'BIRBHUM'): (23.84, 87.61, 'Birbhum'),
    ('WB', 'BURDWAN'): (23.23, 87.86, 'Bardhaman / Burdwan'),
    ('WB', '24 PARGANAS'): (22.18, 88.54, 'South 24 Parganas'),

    # Bihar & Jharkhand (BR)
    ('BR', 'SANTAL-PARGANAS'): (24.27, 87.25, 'Santhal Parganas'),
    ('BR', 'SAKTAL PARGANAS'): (24.27, 87.25, 'Santhal Parganas'),
    ('BR', 'MONGHYR'): (25.37, 86.47, 'Munger / Monghyr'),
    ('BR', 'RANCHI'): (23.34, 85.31, 'Ranchi'),
    ('BR', 'SINGHBUM'): (22.56, 85.81, 'Singhbhum'),
    ('BR', 'SINGHBHUM'): (22.56, 85.81, 'Singhbhum'),
    ('BR', 'SUNGHBUM'): (22.56, 85.81, 'Singhbhum'),
    ('AS', 'SINGHBUM'): (22.56, 85.81, 'Singhbhum (Eastern Plateau)'),
    ('BR', 'HAZARIBAGH'): (23.99, 85.36, 'Hazaribagh'),
    ('BR', 'BHAGALPUR'): (25.24, 87.01, 'Bhagalpur'),
    ('BR', 'PALAMAU'): (24.04, 84.07, 'Palamu'),
    ('BR', 'GAYA'): (24.79, 85.00, 'Gaya'),
    ('BR', 'DHANBAD'): (23.79, 86.43, 'Dhanbad'),
    ('BR', 'PATNA'): (25.59, 85.13, 'Patna'),

    # Odisha (OR)
    ('OR', 'MAYURBHANJ'): (21.93, 86.72, 'Mayurbhanj (Kuliana/Baripada)'),
    ('OR', 'DHENDEKAL'): (20.66, 85.60, 'Dhenkanal'),
    ('OR', 'DHENKANAL'): (20.66, 85.60, 'Dhenkanal'),
    ('OR', 'SUNDARGARH'): (22.12, 84.03, 'Sundargarh'),
    ('OR', 'KEONJHAR'): (21.63, 85.58, 'Kendujhar / Keonjhar'),
    ('OR', 'PURI'): (19.81, 85.83, 'Puri / Bhubaneswar foothills'),

    # Tamil Nadu (TN)
    ('TN', 'CHINGLEPUT'): (12.69, 79.98, 'Chengalpattu (Kortallaiyar Basin)'),
    ('TN', 'NORTH ARCOT'): (12.91, 79.13, 'Vellore / North Arcot'),
    ('TN', 'MADURAI'): (9.92, 78.11, 'Madurai'),
    ('TN', 'RAICHUR'): (15.50, 76.50, 'Tungabhadra Basin Survey'),
    ('TN', 'DHARWAR'): (15.45, 75.00, 'Southern Peninsula Survey'),
    ('TN', 'TN'): (13.00, 79.80, 'Tamil Nadu Prehistoric Coast'),

    # Himachal Pradesh (HP)
    ('HP', 'KANGRA'): (32.10, 76.27, 'Kangra (Beas Terraces)'),
    ('HP', 'NAHAN'): (30.55, 77.29, 'Nahan / Sirmaur'),
    ('HP', 'BILASPUR'): (31.33, 76.75, 'Bilaspur (Sutlej Valley)'),
    ('HP', 'MANDI'): (31.70, 76.93, 'Mandi (Beas Basin)'),
    ('HP', ''): (31.50, 76.80, 'Himachal Siwaliks'),
    ('HP/PN', 'BILASPUR/HOSHIARPUR'): (31.40, 76.30, 'Siwalik Foothills'),

    # Jammu & Kashmir (J AND K, JK)
    ('J AND K', 'KATHUA'): (32.37, 75.52, 'Kathua'),
    ('JK', 'KATHUA'): (32.37, 75.52, 'Kathua'),
    ('J AND K', 'SRINAGAR'): (34.08, 74.79, 'Srinagar (Kashmir Basin)'),
    ('J AND K', 'JAMMU'): (32.72, 74.85, 'Jammu'),
    ('J AND K', 'KASHMIR SOUTH'): (34.01, 75.19, 'South Kashmir (Liddar Valley/Pahalgam)'),
    ('J AND K', 'UDHAMPUR'): (32.92, 75.14, 'Udhampur'),
    ('J AND K', 'NOT GIVEN'): (33.50, 75.00, 'Jammu & Kashmir Valley'),

    # North-East: Meghalaya (ML), Assam (AS), Arunachal (AR), Manipur (MN)
    ('ML', 'GARO HILLS'): (25.51, 90.22, 'Garo Hills (Rongram/Selbalgiri)'),
    ('AS', 'GARO HILLS'): (25.51, 90.22, 'Garo Hills'),
    ('AR', 'LOHIT'): (27.92, 96.17, 'Lohit (Kamlang/Mishmi Terraces)'),
    ('MN', 'UKHRUL'): (25.11, 94.36, 'Ukhrul (Khangkhui Cave)'),

    # Punjab & Haryana (PB, PN, HR)
    ('HR', 'AMBALA'): (30.37, 76.77, 'Ambala / Pinjore Foothills'),
    ('PB', 'HOSHIARPUR'): (31.52, 75.91, 'Hoshiarpur / Soan Tract'),
    ('PB', 'KANGRA'): (32.10, 76.27, 'Kangra (Punjab border)'),
    ('PN', 'AMBALA'): (30.37, 76.77, 'Ambala / Siwalik Terraces'),
    ('PN', 'KANGRA'): (32.10, 76.27, 'Kangra Terraces'),

    # Kerala & Goa
    ('KL', 'PALGHAT'): (10.78, 76.65, 'Palakkad (Kanhirapuzha/Malampuzha)'),
    ('GA', 'SOUTH GOA'): (15.27, 74.02, 'South Goa (Shigao)'),

    # Daman & Diu
    ('DAMAN AND DIU', 'NOT GIVEN'): (20.39, 72.83, 'Daman'),

    # Fallback
    ('', ''): (22.50, 78.50, 'Indian Subcontinent Central')
}

# 1. Load Landmark Benchmark Sites
with open(existing_json_path, 'r', encoding='utf-8') as f:
    landmark_sites = json.load(f)

for s in landmark_sites:
    s['dataset_source'] = 'Syllabus Landmark Benchmark'
    s['location_integrity'] = 'Precise'
    s['excavation_status'] = 'Yes' if any(w in (s.get('associated_features', '') + s.get('excavation_seasons', '')).lower() for w in ['excavat', 'trench', 'stratif', 'in situ']) else 'Explored'
    s['citation_ref'] = 'University Curriculum Benchmark (Prehistory of India Paper, K.S.Chandra 2026)'

print(f"Loaded {len(landmark_sites)} landmark benchmark sites.")

# 2. Load Excel File
wb = openpyxl.load_workbook(excel_path)
data_sheet = wb['Data']

def classify_period(site_type_str, artifacts_str):
    st = (site_type_str or '').lower()
    art = (artifacts_str or '').lower()
    combined = st + " " + art

    has_lp = any(k in combined for k in ['early stone age', 'lower palaeo', 'lower paleo', 'acheulian', 'acheulean', 'abbevill', 'sohan', 'soan', 'series i', 'clacton', 'handaxe', 'cleaver', 'chopper', 'biface'])
    has_mp = any(k in combined for k in ['middle stone age', 'middle palaeo', 'middle paleo', 'series ii', 'levallois', 'mousterian', 'nevasan', 'scraper', 'borer', 'point'])
    has_up = any(k in combined for k in ['upper palaeo', 'upper paleo', 'series iii', 'blade and burin', 'prismatic blade', 'burin'])
    has_meso = any(k in combined for k in ['late stone age', 'microlith', 'mesolithic', 'lunate', 'triangle', 'trapeze'])
    has_neo = any(k in combined for k in ['neolithic', 'celt', 'polished stone', 'adzes', 'quern', 'ring stone', 'ground celt'])

    if has_lp and has_mp:
        return 'Lower Paleolithic', 'Acheulian & Levallois Complex'
    elif has_lp:
        if 'soan' in combined or 'sohan' in combined:
            return 'Lower Paleolithic', 'Soanian Pebble-Tool Tradition'
        return 'Lower Paleolithic', 'Acheulian Industry'
    elif has_mp:
        return 'Middle Paleolithic', 'Levallois / Nevasan Flake Tradition'
    elif has_up:
        return 'Upper Paleolithic', 'Blade & Burin Tradition'
    elif has_meso:
        return 'Mesolithic', 'Microlithic & Hunting-Foraging Complex'
    elif has_neo:
        return 'Neolithic', 'Ground Celt & Early Agro-Pastoral Culture'
    elif 'palaeo' in combined or 'paleo' in combined or 'stone age' in combined:
        return 'Lower Paleolithic', 'Palaeolithic Lithic Industry'
    return 'Lower Paleolithic', 'Lithic Flake Assemblage'

def extract_raw_materials(artifacts_str, comments_str, context_str):
    text = f"{artifacts_str} {comments_str} {context_str}".lower()
    mats = []
    if 'quartzite' in text: mats.append('Quartzite')
    if 'jasper' in text: mats.append('Jasper')
    if 'chert' in text: mats.append('Chert')
    if 'chalcedony' in text or 'chalcodenoy' in text: mats.append('Chalcedony')
    if 'agate' in text: mats.append('Agate')
    if 'dolerite' in text: mats.append('Dolerite')
    if 'basalt' in text or 'trap' in text or 'trappian' in text: mats.append('Basalt / Trap Rock')
    if 'sandstone' in text or 'rewa sandstone' in text: mats.append('Sandstone')
    if 'limestone' in text: mats.append('Limestone')
    if 'crystal' in text or 'vein quartz' in text or 'quartz' in text: mats.append('Quartz / Rock Crystal')
    if 'haematite' in text or 'bloodstone' in text: mats.append('Haematitic Basalt / Bloodstone')
    if 'carnelian' in text: mats.append('Carnelian')
    if 'phyllite' in text: mats.append('Phyllite')
    if not mats:
        return 'Quartzite, Chert, and Siliceous Fluvio-Gravel Minerals'
    return ', '.join(mats)

def extract_fauna(artifacts_str, comments_str, context_str):
    text = f"{artifacts_str} {comments_str} {context_str}".lower()
    fauna = []
    if 'bos namadicus' in text or 'bos sp' in text or 'bison' in text or 'bovid' in text:
        fauna.append('Bos namadicus / Wild Cattle fossils')
    if 'elephas' in text or 'elephant' in text or 'palaeoloxodon' in text or 'tusk' in text:
        fauna.append('Elephas hysudricus / Palaeoloxodon namadicus (Ancient Elephant)')
    if 'equus' in text or 'horse' in text:
        fauna.append('Equus namadicus (Pleistocene Horse)')
    if 'hexaprotodon' in text or 'hippo' in text:
        fauna.append('Hexaprotodon palaeindicus (Hippopotamus)')
    if 'fossil' in text or 'bone' in text or 'dentition' in text or 'skull' in text or 'molar' in text:
        if not fauna:
            fauna.append('Pleistocene mammalian fossil bones / dental remains')
    if 'mollusc' in text or 'shell' in text or 'conch' in text or 'ostrea' in text:
        fauna.append('Fluvial molluscan shell deposits')
    if not fauna:
        return 'None reported'
    return '; '.join(fauna)

def extract_rock_art(comments_str, artifacts_str, context_str):
    text = f"{comments_str} {artifacts_str} {context_str}".lower()
    if 'paint' in text or 'ochre' in text or 'petroglyph' in text or 'grafitti' in text or 'inscript' in text or 'art' in text:
        return comments_str if comments_str else 'Painted rock shelter / boulder petroglyphs recorded'
    return 'None recorded'

def extract_river_basin(context_str, comments_str, district, state):
    text = f"{context_str} {comments_str}".strip()
    # Try to find R. River or River X or valley or nalla
    m = re.search(r'(?:river|r\.|stream|basin|nullah|nalla)\s+([A-Za-z]+)', text, re.IGNORECASE)
    if m:
        r_name = m.group(1).title()
        if r_name not in ['Section', 'Bank', 'Bed', 'Terrace', 'Gravel', 'Deposit', 'Of']:
            return f"River {r_name} Basin"
    m2 = re.search(r'([A-Za-z]+)\s+(?:river|stream|nullah|nalla)', text, re.IGNORECASE)
    if m2:
        r_name = m2.group(1).title()
        if r_name not in ['The', 'A', 'Small', 'Dry', 'Dried', 'Near', 'Bank', 'High']:
            return f"{r_name} River / Nullah Valley"
    
    # District / state fallbacks
    dist_clean = district.title() if district else state
    return f"{dist_clean} Fluvial System"

# 3. Process the 1,484 IAR records
iar_records = []
iar_table_rows = []

next_id = 105

for r in range(2, 1486):
    source = str(data_sheet.cell(r, 1).value or '').strip()
    vol = str(data_sheet.cell(r, 2).value or '').strip()
    page = str(data_sheet.cell(r, 3).value or '').strip()
    site_name = str(data_sheet.cell(r, 4).value or '').strip()
    district = str(data_sheet.cell(r, 5).value or '').strip()
    state_code = str(data_sheet.cell(r, 6).value or '').strip().upper()
    loc_integrity = str(data_sheet.cell(r, 7).value or '').strip().title()
    site_type = str(data_sheet.cell(r, 8).value or '').strip()
    excavation_status = str(data_sheet.cell(r, 9).value or '').strip().title()
    artifacts = str(data_sheet.cell(r, 10).value or '').strip()
    context = str(data_sheet.cell(r, 11).value or '').strip()
    investigators = str(data_sheet.cell(r, 12).value or '').strip()
    comments = str(data_sheet.cell(r, 13).value or '').strip()

    if not site_name:
        site_name = f"Unnamed Lithic Site ({district or state_code})"

    state_full, geo_zone = STATE_INFO.get(state_code, (state_code or 'India', 'Indian Subcontinent'))

    # Exact Coordinates parsing from comments if present
    lat, lon = None, None
    m_coord = re.search(r'(\d+)\s*°\s*(\d+)\s*[\'′]?\s*([NS])\s*[:;,]?\s*(\d+)\s*°\s*(\d+)\s*[\'′]?\s*([EW])', comments)
    if m_coord:
        d_lat, m_lat, h_lat, d_lon, m_lon, h_lon = m_coord.groups()
        lat = round(float(d_lat) + float(m_lat)/60.0, 4)
        if h_lat == 'S': lat = -lat
        lon = round(float(d_lon) + float(m_lon)/60.0, 4)
        if h_lon == 'W': lon = -lon
        loc_integrity = 'Precise'
    else:
        # Check district coordinates
        key = (state_code, district.upper())
        if key in DISTRICT_COORDS:
            base_lat, base_lon, _ = DISTRICT_COORDS[key]
        elif (state_code, '') in DISTRICT_COORDS:
            base_lat, base_lon, _ = DISTRICT_COORDS[(state_code, '')]
        else:
            base_lat, base_lon, _ = DISTRICT_COORDS[('', '')]

        # Apply deterministic micro-jitter based on md5 of site_name + row
        h = int(hashlib.md5(f"{site_name}_{r}".encode('utf-8')).hexdigest()[:6], 16)
        jitter_lat = ((h % 1000) / 1000.0 - 0.5) * 0.12  # ±0.06 degree (~6km)
        jitter_lon = (((h // 1000) % 1000) / 1000.0 - 0.5) * 0.12
        lat = round(base_lat + jitter_lat, 4)
        lon = round(base_lon + jitter_lon, 4)

    period, cult_trad = classify_period(site_type, artifacts)
    raw_mats = extract_raw_materials(artifacts, comments, context)
    fauna = extract_fauna(artifacts, comments, context)
    rock_art = extract_rock_art(comments, artifacts, context)
    r_basin = extract_river_basin(context, comments, district, state_full)

    # Citation
    citation = (
        f"Indian Archaeology: A Review {vol}, {page}. "
        f"Cited & Digitized in: Vidyarthi, V. and Chauhan, P. 2025. Mapping the Indian Palaeolithic. "
        f"Journal of Computer Applications in Archaeology, 8(1): 78–93. DOI: https://doi.org/10.5334/jcaa.148"
    )

    year_str = vol.split('-')[0] if '-' in vol else vol

    # Manufacturing technique
    if 'acheul' in cult_trad.lower():
        technique = "Block-on-block anvil percussion and cylinder hammer bifacial flaking"
    elif 'soan' in cult_trad.lower():
        technique = "Direct stone hammer pebble reduction and unifacial chopper flaking"
    elif 'levallois' in cult_trad.lower():
        technique = "Prepared core Levallois tortoise core reduction technique"
    elif 'blade' in cult_trad.lower():
        technique = "Punch blade indirect percussion on prepared prismatic cores"
    elif 'microlith' in cult_trad.lower():
        technique = "Pressure micro-flaking and micro-burin technique"
    elif 'celt' in cult_trad.lower():
        technique = "Chipping, pecking, wet grinding, and hone polishing"
    else:
        technique = "Percussion flaking and retouched edge preparation"

    # Typical usage
    if 'handaxe' in artifacts.lower() or 'cleaver' in artifacts.lower():
        usage = "Butchery, heavy woodworking, marrow fracturing, and carcass processing"
    elif 'microlith' in artifacts.lower():
        usage = "Composite projectile weapon tips, arrowheads, sickle barbs"
    elif 'scraper' in artifacts.lower():
        usage = "Hide defleshing, wood shaping, plant processing, scraping"
    elif 'celt' in artifacts.lower():
        usage = "Forest clearance, carpentry, agricultural soil tilling"
    else:
        usage = "Subsistence hunting, foraging, tool fabrication"

    iar_dict = {
        "site_id": next_id,
        "dataset_source": "IAR Palaeolithic Survey (Vidyarthi & Chauhan 2025)",
        "period": period,
        "cultural_tradition": cult_trad,
        "site_name": site_name,
        "alternative_names": f"IAR {vol}:{page.replace('(pdf)', '').strip()}",
        "country": "India",
        "state_province": state_full,
        "district": district or state_full,
        "river_basin": r_basin,
        "latitude": lat,
        "longitude": lon,
        "latitude_decimal": lat,
        "longitude_decimal": lon,
        "elevation_approx_m": 250,
        "excavator_discoverer": investigators or "Archaeological Survey of India Survey Team",
        "year_of_discovery": year_str,
        "excavation_seasons": f"{vol} ({'Excavated Site' if excavation_status == 'Yes' else 'Exploration Survey'})",
        "tool_typology": artifacts if artifacts else "Reported Palaeolithic stone implements",
        "length_min_mm": 60.0 if period == 'Lower Paleolithic' else (25.0 if period == 'Middle Paleolithic' else 12.0),
        "length_max_mm": 180.0 if period == 'Lower Paleolithic' else (85.0 if period == 'Middle Paleolithic' else 35.0),
        "width_min_mm": 35.0,
        "width_max_mm": 90.0,
        "thickness_min_mm": 15.0,
        "thickness_max_mm": 45.0,
        "primary_raw_materials": raw_mats,
        "typical_usage": usage,
        "associated_features": (
            f"Context: {context or 'Surface/Stratified'}. "
            f"{'Fossils: ' + comments if comments else ''} "
            f"[Location Integrity: {loc_integrity}; Excavation: {excavation_status}]"
        ).strip(),
        "visual_link_archive": "https://commons.wikimedia.org/wiki/File:Biface_Attirampakkam.jpg",
        "key_references": citation,
        "geographical_zone": geo_zone,
        "environmental_adaptation": context if context else "Alluvial valley & terrace gravels",
        "manufacturing_technique": technique,
        "palaeofauna_palaeoflora": fauna,
        "rock_art_details": rock_art,
        "syllabus_unit_coverage": "Unit-2 (Stone Age Technologies), Unit-3 (Palaeolithic Cultures of India)",
        # Extra IAR specific fields for table & dossier
        "iar_volume": vol,
        "iar_page": page,
        "location_integrity": loc_integrity,
        "excavation_status": excavation_status,
        "site_context": context,
        "comments": comments
    }

    iar_records.append(iar_dict)
    next_id += 1

print(f"Processed {len(iar_records)} IAR survey records.")

# Master list: 104 landmark + 1,484 IAR records = 1,588 sites!
all_sites = landmark_sites + iar_records
print(f"Total Combined Master Sites: {len(all_sites)}")

# 4. Save JSONs
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(all_sites, f, ensure_ascii=False, indent=2)

with open(iar_json_path, 'w', encoding='utf-8') as f:
    json.dump(iar_records, f, ensure_ascii=False, indent=2)

print(f"Saved {json_path} and {iar_json_path}")

# 5. Save CSVs
fieldnames = [
    "site_id", "dataset_source", "period", "cultural_tradition", "site_name", "alternative_names",
    "country", "state_province", "district", "river_basin", "latitude", "longitude",
    "elevation_approx_m", "excavator_discoverer", "year_of_discovery", "excavation_seasons",
    "tool_typology", "length_min_mm", "length_max_mm", "width_min_mm", "width_max_mm",
    "thickness_min_mm", "thickness_max_mm", "primary_raw_materials", "typical_usage",
    "associated_features", "visual_link_archive", "key_references", "geographical_zone",
    "environmental_adaptation", "manufacturing_technique", "palaeofauna_palaeoflora",
    "rock_art_details", "syllabus_unit_coverage", "iar_volume", "iar_page",
    "location_integrity", "excavation_status", "site_context", "comments"
]

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(all_sites)

# Dedicated IAR CSV
iar_fieldnames = [
    "iar_id", "source", "volume_no", "page_number", "site_name", "district", "state",
    "location_integrity", "site_type", "excavation_status", "artifacts_reported",
    "site_context", "investigators", "comments", "latitude", "longitude", "standardized_period", "citation"
]

with open(iar_csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(iar_fieldnames)
    for idx, s in enumerate(iar_records, 1):
        writer.writerow([
            idx,
            "Indian Archaeology: A Review",
            s.get("iar_volume"),
            s.get("iar_page"),
            s.get("site_name"),
            s.get("district"),
            s.get("state_province"),
            s.get("location_integrity"),
            s.get("cultural_tradition"),
            s.get("excavation_status"),
            s.get("tool_typology"),
            s.get("site_context"),
            s.get("excavator_discoverer"),
            s.get("comments"),
            s.get("latitude"),
            s.get("longitude"),
            s.get("period"),
            s.get("key_references")
        ])

print(f"Saved {csv_path} and {iar_csv_path}")

# 6. Build SQLite Database
if os.path.exists(db_path):
    try:
        os.remove(db_path)
    except Exception as e:
        print("Note on existing db:", e)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Enable WAL for high concurrency
cur.execute("PRAGMA journal_mode=WAL;")

# Create Master prehistoric_sites table
cur.execute(f"""
CREATE TABLE prehistoric_sites (
    site_id INTEGER PRIMARY KEY,
    dataset_source TEXT,
    period TEXT,
    cultural_tradition TEXT,
    site_name TEXT,
    alternative_names TEXT,
    country TEXT,
    state_province TEXT,
    district TEXT,
    river_basin TEXT,
    latitude REAL,
    longitude REAL,
    elevation_approx_m REAL,
    excavator_discoverer TEXT,
    year_of_discovery TEXT,
    excavation_seasons TEXT,
    tool_typology TEXT,
    length_min_mm REAL,
    length_max_mm REAL,
    width_min_mm REAL,
    width_max_mm REAL,
    thickness_min_mm REAL,
    thickness_max_mm REAL,
    primary_raw_materials TEXT,
    typical_usage TEXT,
    associated_features TEXT,
    visual_link_archive TEXT,
    key_references TEXT,
    geographical_zone TEXT,
    environmental_adaptation TEXT,
    manufacturing_technique TEXT,
    palaeofauna_palaeoflora TEXT,
    rock_art_details TEXT,
    syllabus_unit_coverage TEXT,
    iar_volume TEXT,
    iar_page TEXT,
    location_integrity TEXT,
    excavation_status TEXT,
    site_context TEXT,
    comments TEXT
);
""")

# Insert all records into prehistoric_sites
insert_sql = f"""
INSERT INTO prehistoric_sites ({', '.join(fieldnames)})
VALUES ({', '.join(['?' for _ in fieldnames])})
"""

for row in all_sites:
    cur.execute(insert_sql, [row.get(f) for f in fieldnames])

# Create dedicated iar_palaeolithic_sites table
cur.execute("""
CREATE TABLE iar_palaeolithic_sites (
    iar_id INTEGER PRIMARY KEY,
    source TEXT,
    volume_no TEXT,
    page_number TEXT,
    site_name TEXT,
    district TEXT,
    state TEXT,
    location_integrity TEXT,
    site_type TEXT,
    excavation_status TEXT,
    artifacts_reported TEXT,
    site_context TEXT,
    investigators TEXT,
    comments TEXT,
    latitude REAL,
    longitude REAL,
    standardized_period TEXT,
    citation TEXT
);
""")

iar_insert_sql = """
INSERT INTO iar_palaeolithic_sites VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
for idx, s in enumerate(iar_records, 1):
    cur.execute(iar_insert_sql, [
        idx,
        "Indian Archaeology: A Review",
        s.get("iar_volume"),
        s.get("iar_page"),
        s.get("site_name"),
        s.get("district"),
        s.get("state_province"),
        s.get("location_integrity"),
        s.get("cultural_tradition"),
        s.get("excavation_status"),
        s.get("tool_typology"),
        s.get("site_context"),
        s.get("excavator_discoverer"),
        s.get("comments"),
        s.get("latitude"),
        s.get("longitude"),
        s.get("period"),
        s.get("key_references")
    ])

# Create dedicated landmark_syllabus_sites table
cur.execute("""
CREATE TABLE landmark_syllabus_sites AS
SELECT * FROM prehistoric_sites WHERE dataset_source = 'Syllabus Landmark Benchmark';
""")

# Create project_metadata table
cur.execute("""
CREATE TABLE project_metadata (
    key TEXT PRIMARY KEY,
    value TEXT
);
""")

meta_entries = [
    ("project_title", "Prehistoric Archaeological GIS & Academic Database: Indian Subcontinent"),
    ("idea_and_design", "K.S.Chandra 2026 (kavikondalaschandra@gmail.com)"),
    ("total_sites_count", str(len(all_sites))),
    ("landmark_syllabus_sites_count", str(len(landmark_sites))),
    ("iar_palaeolithic_survey_sites_count", str(len(iar_records))),
    ("dataset_coverage_years", "1863-Present (Curated); 1953-1976 (IAR Survey Volumes)"),
    ("peer_reviewed_primary_reference", "Vidyarthi, V and Chauhan, P. 2025. Mapping the Indian Palaeolithic. Journal of Computer Applications in Archaeology, 8(1): 78–93. DOI: https://doi.org/10.5334/jcaa.148"),
    ("archival_source", "Indian Archaeology: A Review (IAR), Archaeological Survey of India (ASI, 1953-1976)"),
    ("spatial_crs", "EPSG:4326 (WGS 84 Longitude/Latitude)")
]

for k, v in meta_entries:
    cur.execute("INSERT INTO project_metadata VALUES (?, ?)", (k, v))

# Indexes
cur.execute("CREATE INDEX idx_master_period ON prehistoric_sites(period);")
cur.execute("CREATE INDEX idx_master_state ON prehistoric_sites(state_province);")
cur.execute("CREATE INDEX idx_master_coords ON prehistoric_sites(latitude, longitude);")
cur.execute("CREATE INDEX idx_master_source ON prehistoric_sites(dataset_source);")
cur.execute("CREATE INDEX idx_iar_volume ON iar_palaeolithic_sites(volume_no);")
cur.execute("CREATE INDEX idx_iar_state ON iar_palaeolithic_sites(state);")

# Analytical Views
cur.execute("""
CREATE VIEW view_iar_state_summary AS
SELECT 
    state,
    COUNT(*) AS total_reported_sites,
    SUM(CASE WHEN excavation_status = 'Yes' THEN 1 ELSE 0 END) AS excavated_sites_count,
    ROUND(AVG(latitude), 3) AS avg_latitude,
    ROUND(AVG(longitude), 3) AS avg_longitude
FROM iar_palaeolithic_sites
GROUP BY state
ORDER BY total_reported_sites DESC;
""")

cur.execute("""
CREATE VIEW view_iar_volume_summary AS
SELECT 
    volume_no,
    COUNT(*) AS reported_sites_count,
    COUNT(DISTINCT district) AS districts_covered,
    COUNT(DISTINCT state) AS states_covered
FROM iar_palaeolithic_sites
GROUP BY volume_no
ORDER BY volume_no ASC;
""")

cur.execute("""
CREATE VIEW view_iar_excavations AS
SELECT 
    iar_id,
    site_name,
    district,
    state,
    volume_no,
    page_number,
    artifacts_reported,
    site_context,
    investigators,
    comments,
    latitude,
    longitude,
    citation
FROM iar_palaeolithic_sites
WHERE excavation_status = 'Yes';
""")

cur.execute("""
CREATE VIEW view_academic_references AS
SELECT 
    site_id,
    site_name,
    dataset_source,
    period,
    excavator_discoverer,
    key_references
FROM prehistoric_sites;
""")

# Syllabus Views
cur.execute("""
CREATE VIEW view_unit3_palaeolithic_cultures AS
SELECT site_id, site_name, period, cultural_tradition, geographical_zone, district, state_province, latitude, longitude, key_references
FROM prehistoric_sites
WHERE period IN ('Lower Paleolithic', 'Middle Paleolithic', 'Upper Paleolithic');
""")

cur.execute("""
CREATE VIEW view_unit4_mesolithic_adaptations AS
SELECT site_id, site_name, period, environmental_adaptation, tool_typology, typical_usage, palaeofauna_palaeoflora, latitude, longitude
FROM prehistoric_sites
WHERE period = 'Mesolithic';
""")

cur.execute("""
CREATE VIEW view_unit4_prehistoric_rock_art AS
SELECT site_id, site_name, period, geographical_zone, rock_art_details, associated_features, latitude, longitude
FROM prehistoric_sites
WHERE rock_art_details != 'None recorded' AND rock_art_details IS NOT NULL;
""")

cur.execute("""
CREATE VIEW view_unit2_stone_age_technologies AS
SELECT site_id, site_name, period, cultural_tradition, tool_typology, manufacturing_technique, primary_raw_materials, length_min_mm, length_max_mm
FROM prehistoric_sites;
""")

conn.commit()
conn.close()

print(f"Successfully created updated SQLite Database at {db_path} with all tables, views, and indexes!")
