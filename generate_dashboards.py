import json
import os

data_path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\sites_data.json"
with open(data_path, "r", encoding="utf-8") as f:
    sites = json.load(f)

print(f"Loaded {len(sites)} sites for dashboard generation.")

# 1. Build standalone full-featured web dashboard (index.html) with Leaflet, Chart.js, Tailwind CSS
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prehistoric Archaeology of Indian Subcontinent | Interactive GIS Dashboard</title>
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
    
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #0b0f19;
      color: #e2e8f0;
    }
    
    .font-display {
      font-family: 'Space Grotesk', sans-serif;
    }
    
    #map {
      height: 600px;
      border-radius: 1rem;
      z-index: 10;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #111827;
    }
    ::-webkit-scrollbar-thumb {
      background: #374151;
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #4b5563;
    }

    /* Leaflet Dark Theme Overrides */
    .leaflet-popup-content-wrapper {
      background: #111827;
      color: #f3f4f6;
      border: 1px solid #374151;
      border-radius: 0.75rem;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    .leaflet-popup-tip {
      background: #111827;
    }
    .leaflet-container {
      background: #0b0f19;
    }
    
    .pulse-dot {
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0% { transform: scale(0.95); opacity: 0.8; }
      50% { transform: scale(1.3); opacity: 1; }
      100% { transform: scale(0.95); opacity: 0.8; }
    }
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- TOP NAVIGATION HEADER -->
  <header class="border-b border-gray-800 bg-gray-900/80 backdrop-blur sticky top-0 z-50 px-6 py-4">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-amber-500 to-rose-600 flex items-center justify-center text-white shadow-lg shadow-amber-500/20">
          <i data-lucide="compass" class="w-6 h-6"></i>
        </div>
        <div>
          <h1 class="text-xl font-bold font-display tracking-tight text-white flex items-center gap-2">
            Prehistory of India <span class="text-xs px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 font-sans border border-amber-500/30">104 Excavated Sites</span>
          </h1>
          <p class="text-xs text-gray-400">Palaeolithic, Mesolithic & Neolithic Archaeological GIS Compendium (1863–Present)</p>
          <div class="mt-1 flex items-center gap-2 text-xs text-amber-400 font-medium">
            <span class="flex items-center gap-1"><i data-lucide="sparkles" class="w-3.5 h-3.5"></i> Idea & Design by <strong>K.S.Chandra 2026</strong></span>
            <span class="text-gray-600">•</span>
            <a href="mailto:kavikondalaschandra@gmail.com" class="text-sky-400 hover:text-sky-300 underline underline-offset-2">kavikondalaschandra@gmail.com</a>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2 flex-wrap">
        <button onclick="exportFilteredCSV()" class="px-3 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-xs font-medium text-gray-200 border border-gray-700 flex items-center gap-1.5 transition">
          <i data-lucide="download" class="w-3.5 h-3.5 text-amber-400"></i> Export CSV
        </button>
        <button onclick="exportGeoJSON()" class="px-3 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-xs font-medium text-gray-200 border border-gray-700 flex items-center gap-1.5 transition">
          <i data-lucide="map" class="w-3.5 h-3.5 text-cyan-400"></i> Export GeoJSON
        </button>
        <button onclick="resetFilters()" class="px-3 py-1.5 rounded-lg bg-rose-950/40 hover:bg-rose-900/60 text-xs font-medium text-rose-300 border border-rose-800/40 flex items-center gap-1.5 transition">
          <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i> Reset
        </button>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-7xl w-full mx-auto p-4 md:p-6 flex-1 space-y-6">

    <!-- KPI STATS CARDS -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      <div class="bg-gray-900/90 border border-gray-800 p-3.5 rounded-xl flex flex-col justify-between hover:border-gray-700 transition">
        <div class="flex items-center justify-between text-gray-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Total Sites</span>
          <i data-lucide="landmark" class="w-4 h-4 text-amber-400"></i>
        </div>
        <div class="text-2xl font-bold font-display text-white" id="stat-total-sites">104</div>
        <span class="text-[10px] text-gray-400 mt-1">Across 18 States & Prov.</span>
      </div>

      <div class="bg-gray-900/90 border border-amber-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-amber-800/50 transition">
        <div class="flex items-center justify-between text-amber-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Lower Paleo</span>
          <span class="pulse-dot bg-amber-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-amber-300" id="stat-lp-sites">25</div>
        <span class="text-[10px] text-gray-400 mt-1">Acheulian & Soanian</span>
      </div>

      <div class="bg-gray-900/90 border border-cyan-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-cyan-800/50 transition">
        <div class="flex items-center justify-between text-cyan-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Middle Paleo</span>
          <span class="pulse-dot bg-cyan-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-cyan-300" id="stat-mp-sites">12</div>
        <span class="text-[10px] text-gray-400 mt-1">Levallois & Nevasian</span>
      </div>

      <div class="bg-gray-900/90 border border-purple-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-purple-800/50 transition">
        <div class="flex items-center justify-between text-purple-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Upper Paleo</span>
          <span class="pulse-dot bg-purple-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-purple-300" id="stat-up-sites">12</div>
        <span class="text-[10px] text-gray-400 mt-1">Blade, Burin & Eggshell</span>
      </div>

      <div class="bg-gray-900/90 border border-emerald-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-emerald-800/50 transition">
        <div class="flex items-center justify-between text-emerald-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Mesolithic</span>
          <span class="pulse-dot bg-emerald-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-emerald-300" id="stat-meso-sites">18</div>
        <span class="text-[10px] text-gray-400 mt-1">Microlithic & Lakes</span>
      </div>

      <div class="bg-gray-900/90 border border-rose-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-rose-800/50 transition">
        <div class="flex items-center justify-between text-rose-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Neolithic</span>
          <span class="pulse-dot bg-rose-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-rose-300" id="stat-neo-sites">37</div>
        <span class="text-[10px] text-gray-400 mt-1">Celts, Ashmounds, Rice</span>
      </div>
    </div>

    <!-- FILTER CONTROL BAR -->
    <div class="bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
        
        <!-- Search Input -->
        <div class="relative">
          <i data-lucide="search" class="w-4 h-4 text-gray-400 absolute left-3 top-3"></i>
          <input type="text" id="search-input" oninput="handleSearch()" placeholder="Search site, river, material, excavator..." 
            class="w-full bg-gray-800 border border-gray-700 text-xs rounded-xl pl-9 pr-3 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition" />
        </div>

        <!-- Period Select -->
        <div>
          <select id="period-filter" onchange="applyFilters()" 
            class="w-full bg-gray-800 border border-gray-700 text-xs rounded-xl px-3 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition">
            <option value="ALL">All Archaeological Periods</option>
            <option value="Lower Paleolithic">Lower Paleolithic (Acheulian & Soanian)</option>
            <option value="Middle Paleolithic">Middle Paleolithic (Nevasian/Levallois)</option>
            <option value="Upper Paleolithic">Upper Paleolithic (Blade & Burin)</option>
            <option value="Mesolithic">Mesolithic (Microlithic & Lakes)</option>
            <option value="Neolithic">Neolithic (Polished Celts & Farming)</option>
          </select>
        </div>

        <!-- Geographical Zone (Unit-3) -->
        <div>
          <select id="zone-filter" onchange="applyFilters()" 
            class="w-full bg-gray-800 border border-gray-700 text-xs rounded-xl px-3 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition">
            <option value="ALL">All Geographical Zones (Unit-3)</option>
            <option value="The Himalayan">The Himalayan Context (Siwalik & Potwar)</option>
            <option value="Western India">Western India (Rajasthan & Gujarat)</option>
            <option value="Central India">Central India (Madhya Pradesh)</option>
            <option value="Peninsular India">Peninsular India (MH, KA, AP, TG, TN)</option>
            <option value="Eastern India">Eastern India (WB, Odisha, Bihar, NE)</option>
            <option value="Ganga Valley">Ganga Valley & Vindhyan Tract</option>
          </select>
        </div>

        <!-- Environmental Adaptation (Unit-4) -->
        <div>
          <select id="adapt-filter" onchange="applyFilters()" 
            class="w-full bg-gray-800 border border-gray-700 text-xs rounded-xl px-3 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition">
            <option value="ALL">All Landscapes (Unit-4)</option>
            <option value="Alluvial plain adaptation">Alluvial Plain Adaptation</option>
            <option value="Horse-shoe lake sites">Horse-shoe Lake (Oxbow) Sites</option>
            <option value="Sand dune landscape">Sand Dune Landscape</option>
            <option value="Plateau occupation">Plateau Occupation</option>
            <option value="Cave & Rock Shelter">Cave & Rock Shelter Occupation</option>
            <option value="Ashmound">Ashmound Pastoral Settlement</option>
          </select>
        </div>
      </div>

      <!-- Quick Toggles -->
      <div class="mt-3 pt-3 border-t border-gray-800 flex items-center justify-between flex-wrap gap-2 text-xs">
        <div class="flex items-center gap-3">
          <label class="flex items-center gap-2 cursor-pointer text-gray-300 hover:text-white">
            <input type="checkbox" id="rock-art-only" onchange="applyFilters()" class="rounded bg-gray-800 border-gray-700 text-amber-500 focus:ring-0">
            <span class="flex items-center gap-1.5"><i data-lucide="image" class="w-3.5 h-3.5 text-amber-400"></i> Prehistoric Rock Art Only (Unit-4)</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer text-gray-300 hover:text-white">
            <input type="checkbox" id="fauna-only" onchange="applyFilters()" class="rounded bg-gray-800 border-gray-700 text-emerald-500 focus:ring-0">
            <span class="flex items-center gap-1.5"><i data-lucide="bone" class="w-3.5 h-3.5 text-emerald-400"></i> With Megafauna / Floral Remains (Unit-1)</span>
          </label>
        </div>
        <div class="text-xs text-gray-400">
          Showing <span id="filtered-count" class="font-bold text-white font-display">104</span> of <span id="total-count" class="font-bold text-gray-400">104</span> sites
        </div>
      </div>
    </div>

    <!-- MAP & STATS SECTION -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Interactive GIS Leaflet Map (2 Cols) -->
      <div class="lg:col-span-2 bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl flex flex-col">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <i data-lucide="map-pin" class="w-4 h-4 text-rose-500"></i>
            <h2 class="font-bold font-display text-white text-sm">Spatial GIS Map (EPSG:4326 WGS84)</h2>
          </div>
          <!-- Legend Pill -->
          <div class="flex items-center gap-2 text-[10px] text-gray-400 flex-wrap">
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Lower P.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-cyan-500"></span> Middle P.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span> Upper P.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Meso.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Neo.</span>
          </div>
        </div>

        <div id="map" class="w-full flex-1"></div>
        <p class="text-[11px] text-gray-400 mt-2 flex items-center justify-between">
          <span>Click any marker to inspect site data or fly to locality.</span>
          <span>Basemap: CartoDB Dark Matter / Positron</span>
        </p>
      </div>

      <!-- Charts & Analytical Insights (1 Col) -->
      <div class="space-y-6 flex flex-col">
        <!-- Period Breakdown Chart -->
        <div class="bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl flex-1 flex flex-col">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-xs font-bold uppercase tracking-wider text-gray-300 flex items-center gap-1.5">
              <i data-lucide="pie-chart" class="w-3.5 h-3.5 text-amber-400"></i> Period Distribution
            </h3>
          </div>
          <div class="relative flex-1 min-h-[180px] flex items-center justify-center">
            <canvas id="periodChart"></canvas>
          </div>
        </div>

        <!-- Geographical Zone Breakdown Chart -->
        <div class="bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl flex-1 flex flex-col">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-xs font-bold uppercase tracking-wider text-gray-300 flex items-center gap-1.5">
              <i data-lucide="bar-chart-2" class="w-3.5 h-3.5 text-cyan-400"></i> Regional Distribution (Unit-3)
            </h3>
          </div>
          <div class="relative flex-1 min-h-[180px]">
            <canvas id="zoneChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- DATA TABLE SECTION -->
    <div class="bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl space-y-4">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center gap-2">
          <i data-lucide="database" class="w-4 h-4 text-emerald-400"></i>
          <h2 class="font-bold font-display text-white text-sm">Archaeological Sites Registry & Metrics</h2>
        </div>
        <div class="text-xs text-gray-400">
          Click any row to open the complete site dossier.
        </div>
      </div>

      <div class="overflow-x-auto rounded-xl border border-gray-800">
        <table class="w-full text-left text-xs text-gray-300">
          <thead class="bg-gray-800/80 text-gray-400 uppercase font-semibold text-[10px] tracking-wider border-b border-gray-700">
            <tr>
              <th class="p-3">Site Name</th>
              <th class="p-3">Period</th>
              <th class="p-3">State / Province</th>
              <th class="p-3">River Basin / Setting</th>
              <th class="p-3">Key Tool Typology</th>
              <th class="p-3">Max Dimensions</th>
              <th class="p-3">Primary Material</th>
              <th class="p-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody id="sites-table-body" class="divide-y divide-gray-800/60 font-normal">
            <!-- Populated via JavaScript -->
          </tbody>
        </table>
      </div>

      <!-- Pagination / Count Footer -->
      <div class="flex items-center justify-between text-xs text-gray-400 pt-2">
        <div id="table-info">Showing page 1 of 1</div>
        <div class="flex items-center gap-2">
          <button id="prev-page" onclick="changePage(-1)" class="px-2.5 py-1 bg-gray-800 hover:bg-gray-700 rounded text-gray-300 disabled:opacity-30 disabled:cursor-not-allowed">Previous</button>
          <span id="page-num" class="font-bold text-white">1</span>
          <button id="next-page" onclick="changePage(1)" class="px-2.5 py-1 bg-gray-800 hover:bg-gray-700 rounded text-gray-300 disabled:opacity-30 disabled:cursor-not-allowed">Next</button>
        </div>
      </div>
    </div>

  </main>

  <!-- FOOTER ATTRIBUTION -->
  <footer class="border-t border-gray-800 bg-gray-900/90 py-6 px-6 text-xs text-gray-400">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
      <div class="flex items-center justify-center sm:justify-start gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
        <span class="font-bold text-gray-200">Prehistoric Archaeological GIS Dashboard</span>
        <span>• Indian Subcontinent</span>
      </div>
      <div class="bg-gray-800/80 px-4 py-1.5 rounded-full border border-gray-700/80 text-gray-300 flex items-center justify-center gap-2 shadow-sm">
        <span class="font-semibold text-amber-400">Idea &amp; Design by K.S.Chandra 2026</span>
        <span class="text-gray-500">|</span>
        <a href="mailto:kavikondalaschandra@gmail.com" class="text-sky-400 hover:text-sky-300 underline underline-offset-2 flex items-center gap-1">
          kavikondalaschandra@gmail.com
        </a>
      </div>
      <div class="text-[11px] text-gray-500">
        Data based on IAR, Ancient India, MASI &amp; University Excavations
      </div>
    </div>
  </footer>

  <!-- SITE DOSSIER MODAL DIALOG -->
  <div id="site-modal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-gray-900 border border-gray-800 w-full max-w-3xl max-h-[90vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
      
      <!-- Modal Header -->
      <div class="p-5 border-b border-gray-800 flex items-start justify-between bg-gray-800/40">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span id="modal-period-badge" class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold"></span>
            <span id="modal-geo-zone" class="text-xs text-gray-400"></span>
          </div>
          <h2 id="modal-site-name" class="text-2xl font-bold font-display text-white"></h2>
          <p id="modal-alt-names" class="text-xs text-gray-400 mt-0.5"></p>
        </div>
        <button onclick="closeModal()" class="p-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Modal Body Content -->
      <div class="p-6 overflow-y-auto space-y-5 text-xs text-gray-300">
        
        <!-- Key Metadata Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-950/60 p-4 rounded-xl border border-gray-800/60">
          <div>
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">Coordinates</span>
            <span id="modal-coords" class="font-mono text-white text-xs font-semibold"></span>
          </div>
          <div>
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">Elevation</span>
            <span id="modal-elevation" class="text-white text-xs font-semibold"></span>
          </div>
          <div>
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">Discovery Year</span>
            <span id="modal-year" class="text-white text-xs font-semibold"></span>
          </div>
          <div>
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">Excavator(s)</span>
            <span id="modal-excavator" class="text-white text-xs font-semibold truncate block"></span>
          </div>
        </div>

        <!-- Typology & Metrics -->
        <div class="space-y-2">
          <h4 class="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
            <i data-lucide="hammer" class="w-3.5 h-3.5"></i> Lithic Typology & Manufacturing Technique (Unit-2)
          </h4>
          <div class="bg-gray-800/40 p-3.5 rounded-xl border border-gray-800 space-y-2">
            <p><strong class="text-gray-200">Tools:</strong> <span id="modal-typology"></span></p>
            <p><strong class="text-gray-200">Technique:</strong> <span id="modal-technique" class="text-gray-300"></span></p>
            <p><strong class="text-gray-200">Raw Material:</strong> <span id="modal-material" class="text-amber-200"></span></p>
            <p><strong class="text-gray-200">Metric Bounds:</strong> <span id="modal-metrics" class="font-mono text-cyan-300"></span></p>
            <p><strong class="text-gray-200">Inferred Usage:</strong> <span id="modal-usage"></span></p>
          </div>
        </div>

        <!-- Landscape & Environmental Adaptations -->
        <div class="space-y-2">
          <h4 class="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
            <i data-lucide="trees" class="w-3.5 h-3.5"></i> Landscape & Ecological Adaptation (Unit-4)
          </h4>
          <div class="bg-gray-800/40 p-3.5 rounded-xl border border-gray-800 space-y-2">
            <p><strong class="text-gray-200">Environmental Adaptation:</strong> <span id="modal-adaptation" class="text-emerald-300 font-semibold"></span></p>
            <p><strong class="text-gray-200">Associated Features:</strong> <span id="modal-features"></span></p>
            <p><strong class="text-gray-200">Palaeofauna / Palaeoflora (Unit-1):</strong> <span id="modal-fauna" class="text-gray-300"></span></p>
            <p><strong class="text-gray-200">Prehistoric Rock Art Details:</strong> <span id="modal-rock-art" class="text-amber-300"></span></p>
          </div>
        </div>

        <!-- References & Archive -->
        <div class="space-y-2">
          <h4 class="text-xs font-bold uppercase tracking-wider text-purple-400 flex items-center gap-1.5">
            <i data-lucide="book-open" class="w-3.5 h-3.5"></i> Archival References & Citations
          </h4>
          <div class="bg-gray-800/40 p-3.5 rounded-xl border border-gray-800 text-[11px] leading-relaxed text-gray-300 space-y-2">
            <p id="modal-references"></p>
            <div id="modal-link-wrap" class="pt-2">
              <a id="modal-link" href="#" target="_blank" class="inline-flex items-center gap-1.5 text-amber-400 hover:text-amber-300 underline font-medium">
                <i data-lucide="external-link" class="w-3.5 h-3.5"></i> Open Archival Digital Image Reference
              </a>
            </div>
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-4 border-t border-gray-800 bg-gray-950/80 flex items-center justify-between">
        <button id="modal-fly-btn" class="px-3.5 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-600 text-black font-semibold text-xs flex items-center gap-1.5 transition">
          <i data-lucide="navigation" class="w-3.5 h-3.5"></i> Center on Map
        </button>
        <button onclick="closeModal()" class="px-4 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 font-medium text-xs transition">
          Close Dossier
        </button>
      </div>

    </div>
  </div>

  <!-- SITES DATASET EMBED -->
  <script>
    const SITES_DATA = """ + json.dumps(sites) + """;
  </script>

  <!-- APPLICATION LOGIC -->
  <script>
    let map, markersLayer;
    let filteredSites = [...SITES_DATA];
    let currentPage = 1;
    const pageSize = 12;
    let periodChart, zoneChart;

    // Period Color Mapping
    const PERIOD_COLORS = {
      "Lower Paleolithic": "#f59e0b", // Amber
      "Middle Paleolithic": "#06b6d4", // Cyan
      "Upper Paleolithic": "#a855f7", // Purple
      "Mesolithic": "#10b981",        // Emerald
      "Neolithic": "#f43f5e"          // Rose
    };

    function initMap() {
      // Centered on the Indian Subcontinent
      map = L.map('map', {
        zoomControl: true,
        scrollWheelZoom: true
      }).setView([22.5, 78.5], 5);

      // CartoDB Dark Matter Basemap
      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
      }).addTo(map);

      markersLayer = L.layerGroup().addTo(map);
      renderMarkers();
    }

    function renderMarkers() {
      markersLayer.clearLayers();

      filteredSites.forEach(site => {
        const color = PERIOD_COLORS[site.period] || "#94a3b8";
        
        const customMarker = L.circleMarker([site.latitude, site.longitude], {
          radius: 6.5,
          fillColor: color,
          color: '#ffffff',
          weight: 1.5,
          opacity: 0.9,
          fillOpacity: 0.85
        });

        // Popup Content
        const popupContent = `
          <div class="text-xs p-1 space-y-1.5 max-w-[240px]">
            <div class="flex items-center justify-between gap-2">
              <span class="px-1.5 py-0.5 rounded text-[10px] font-bold" style="background:${color}22; color:${color};">${site.period}</span>
              <span class="text-gray-400 text-[10px]">${site.state_province}</span>
            </div>
            <h4 class="font-bold text-white text-sm leading-tight">${site.site_name}</h4>
            <p class="text-gray-300 text-[11px]">${site.cultural_tradition}</p>
            <p class="text-gray-400 text-[10px] line-clamp-2">${site.tool_typology}</p>
            <div class="pt-1 border-t border-gray-700 flex justify-between items-center text-[10px]">
              <span class="text-gray-400 font-mono">${site.latitude.toFixed(2)}°N, ${site.longitude.toFixed(2)}°E</span>
              <button onclick="openSiteModal(${site.site_id})" class="text-amber-400 hover:underline font-semibold">View Details &rarr;</button>
            </div>
          </div>
        `;

        customMarker.bindPopup(popupContent);
        customMarker.on('click', () => {
          // Highlight
        });

        markersLayer.addLayer(customMarker);
      });
    }

    function initCharts() {
      // 1. Period Distribution Chart
      const periodCounts = {};
      SITES_DATA.forEach(s => periodCounts[s.period] = (periodCounts[s.period] || 0) + 1);

      const ctxPeriod = document.getElementById('periodChart').getContext('2d');
      periodChart = new Chart(ctxPeriod, {
        type: 'doughnut',
        data: {
          labels: Object.keys(periodCounts),
          datasets: [{
            data: Object.values(periodCounts),
            backgroundColor: Object.keys(periodCounts).map(k => PERIOD_COLORS[k] || '#888'),
            borderWidth: 2,
            borderColor: '#111827'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: { color: '#9ca3af', font: { size: 10 } }
            }
          },
          cutout: '65%'
        }
      });

      // 2. Zone Distribution Chart (Unit-3)
      const zoneCounts = {};
      SITES_DATA.forEach(s => {
        let z = s.geographical_zone.split('(')[0].trim();
        zoneCounts[z] = (zoneCounts[z] || 0) + 1;
      });

      const ctxZone = document.getElementById('zoneChart').getContext('2d');
      zoneChart = new Chart(ctxZone, {
        type: 'bar',
        data: {
          labels: Object.keys(zoneCounts),
          datasets: [{
            data: Object.values(zoneCounts),
            backgroundColor: '#06b6d4',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: { ticks: { color: '#9ca3af', font: { size: 9 } }, grid: { display: false } },
            y: { ticks: { color: '#9ca3af', font: { size: 9 } }, grid: { color: '#1f2937' } }
          }
        }
      });
    }

    function renderTable() {
      const tbody = document.getElementById('sites-table-body');
      tbody.innerHTML = '';

      const startIndex = (currentPage - 1) * pageSize;
      const paginatedSites = filteredSites.slice(startIndex, startIndex + pageSize);

      paginatedSites.forEach(site => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-gray-800/40 transition cursor-pointer";
        tr.onclick = (e) => {
          if (!e.target.closest('button')) openSiteModal(site.site_id);
        };

        const color = PERIOD_COLORS[site.period] || "#94a3b8";

        tr.innerHTML = `
          <td class="p-3 font-semibold text-white flex items-center gap-2">
            <span class="w-2 h-2 rounded-full" style="background:${color};"></span>
            ${site.site_name}
          </td>
          <td class="p-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold" style="background:${color}22; color:${color};">${site.period}</span>
          </td>
          <td class="p-3 text-gray-300">${site.state_province}</td>
          <td class="p-3 text-gray-400 text-[11px] truncate max-w-[140px]">${site.river_basin}</td>
          <td class="p-3 text-gray-300 text-[11px] truncate max-w-[160px]">${site.tool_typology}</td>
          <td class="p-3 font-mono text-[11px] text-cyan-300">${site.length_max_mm} × ${site.width_max_mm} mm</td>
          <td class="p-3 text-gray-400 text-[11px] truncate max-w-[120px]">${site.primary_raw_materials}</td>
          <td class="p-3 text-right">
            <button onclick="flyToSite(${site.latitude}, ${site.longitude}, ${site.site_id})" class="px-2 py-1 bg-gray-800 hover:bg-gray-700 text-amber-400 hover:text-amber-300 rounded text-[10px] font-medium border border-gray-700 transition">
              Map &rarr;
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      const totalPages = Math.ceil(filteredSites.length / pageSize) || 1;
      document.getElementById('table-info').innerText = `Showing ${filteredSites.length === 0 ? 0 : startIndex + 1} - ${Math.min(startIndex + pageSize, filteredSites.length)} of ${filteredSites.length} sites`;
      document.getElementById('page-num').innerText = `${currentPage} / ${totalPages}`;
      document.getElementById('prev-page').disabled = currentPage === 1;
      document.getElementById('next-page').disabled = currentPage >= totalPages;
    }

    function changePage(delta) {
      const totalPages = Math.ceil(filteredSites.length / pageSize) || 1;
      currentPage = Math.max(1, Math.min(currentPage + delta, totalPages));
      renderTable();
    }

    function handleSearch() {
      applyFilters();
    }

    function applyFilters() {
      const searchTerm = document.getElementById('search-input').value.toLowerCase().trim();
      const periodVal = document.getElementById('period-filter').value;
      const zoneVal = document.getElementById('zone-filter').value;
      const adaptVal = document.getElementById('adapt-filter').value;
      const rockArtOnly = document.getElementById('rock-art-only').checked;
      const faunaOnly = document.getElementById('fauna-only').checked;

      filteredSites = SITES_DATA.filter(site => {
        // Search
        const matchesSearch = !searchTerm || 
          site.site_name.toLowerCase().includes(searchTerm) ||
          site.state_province.toLowerCase().includes(searchTerm) ||
          site.river_basin.toLowerCase().includes(searchTerm) ||
          site.tool_typology.toLowerCase().includes(searchTerm) ||
          site.primary_raw_materials.toLowerCase().includes(searchTerm) ||
          site.excavator_discoverer.toLowerCase().includes(searchTerm);

        // Period
        const matchesPeriod = periodVal === 'ALL' || site.period === periodVal;

        // Zone
        const matchesZone = zoneVal === 'ALL' || site.geographical_zone.includes(zoneVal);

        // Adaptation
        const matchesAdapt = adaptVal === 'ALL' || site.environmental_adaptation.includes(adaptVal);

        // Rock Art
        const matchesRockArt = !rockArtOnly || site.rock_art_details !== 'None recorded';

        // Fauna/Flora
        const matchesFauna = !faunaOnly || !site.palaeofauna_palaeoflora.includes('Fragmentary');

        return matchesSearch && matchesPeriod && matchesZone && matchesAdapt && matchesRockArt && matchesFauna;
      });

      currentPage = 1;
      renderMarkers();
      renderTable();
      updateKPICards();

      document.getElementById('filtered-count').innerText = filteredSites.length;
    }

    function updateKPICards() {
      let lp = 0, mp = 0, up = 0, meso = 0, neo = 0;
      filteredSites.forEach(s => {
        if (s.period === 'Lower Paleolithic') lp++;
        else if (s.period === 'Middle Paleolithic') mp++;
        else if (s.period === 'Upper Paleolithic') up++;
        else if (s.period === 'Mesolithic') meso++;
        else if (s.period === 'Neolithic') neo++;
      });

      document.getElementById('stat-total-sites').innerText = filteredSites.length;
      document.getElementById('stat-lp-sites').innerText = lp;
      document.getElementById('stat-mp-sites').innerText = mp;
      document.getElementById('stat-up-sites').innerText = up;
      document.getElementById('stat-meso-sites').innerText = meso;
      document.getElementById('stat-neo-sites').innerText = neo;
    }

    function resetFilters() {
      document.getElementById('search-input').value = '';
      document.getElementById('period-filter').value = 'ALL';
      document.getElementById('zone-filter').value = 'ALL';
      document.getElementById('adapt-filter').value = 'ALL';
      document.getElementById('rock-art-only').checked = false;
      document.getElementById('fauna-only').checked = false;
      applyFilters();
      map.setView([22.5, 78.5], 5);
    }

    function flyToSite(lat, lon, siteId) {
      map.flyTo([lat, lon], 10, { duration: 1.5 });
      openSiteModal(siteId);
    }

    function openSiteModal(siteId) {
      const site = SITES_DATA.find(s => s.site_id === siteId);
      if (!site) return;

      const color = PERIOD_COLORS[site.period] || "#94a3b8";

      const badge = document.getElementById('modal-period-badge');
      badge.innerText = site.period;
      badge.style.backgroundColor = `${color}22`;
      badge.style.color = color;
      badge.style.border = `1px solid ${color}44`;

      document.getElementById('modal-geo-zone').innerText = site.geographical_zone;
      document.getElementById('modal-site-name').innerText = site.site_name;
      document.getElementById('modal-alt-names').innerText = site.alternative_names ? `Alt: ${site.alternative_names} | District: ${site.district}, ${site.state_province} (${site.country})` : `District: ${site.district}, ${site.state_province}`;

      document.getElementById('modal-coords').innerText = `${site.latitude.toFixed(4)}°N, ${site.longitude.toFixed(4)}°E`;
      document.getElementById('modal-elevation').innerText = site.elevation_approx_m ? `${site.elevation_approx_m} m ASL` : 'Unspecified';
      document.getElementById('modal-year').innerText = site.year_of_discovery || 'Unknown';
      document.getElementById('modal-excavator').innerText = site.excavator_discoverer || 'N/A';
      document.getElementById('modal-excavator').title = site.excavator_discoverer || '';

      document.getElementById('modal-typology').innerText = site.tool_typology;
      document.getElementById('modal-technique').innerText = site.manufacturing_technique;
      document.getElementById('modal-material').innerText = site.primary_raw_materials;
      document.getElementById('modal-metrics').innerText = `L: ${site.length_min_mm}–${site.length_max_mm} mm | W: ${site.width_min_mm}–${site.width_max_mm} mm | T: ${site.thickness_min_mm}–${site.thickness_max_mm} mm`;
      document.getElementById('modal-usage').innerText = site.typical_usage;

      document.getElementById('modal-adaptation').innerText = site.environmental_adaptation;
      document.getElementById('modal-features').innerText = site.associated_features;
      document.getElementById('modal-fauna').innerText = site.palaeofauna_palaeoflora;
      document.getElementById('modal-rock-art').innerText = site.rock_art_details;

      document.getElementById('modal-references').innerText = site.key_references;

      const linkEl = document.getElementById('modal-link');
      if (site.visual_link_archive && site.visual_link_archive.startsWith('http')) {
        linkEl.href = site.visual_link_archive;
        document.getElementById('modal-link-wrap').classList.remove('hidden');
      } else {
        document.getElementById('modal-link-wrap').classList.add('hidden');
      }

      document.getElementById('modal-fly-btn').onclick = () => {
        closeModal();
        map.flyTo([site.latitude, site.longitude], 10, { duration: 1.5 });
      };

      document.getElementById('site-modal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('site-modal').classList.add('hidden');
    }

    function exportFilteredCSV() {
      if (!filteredSites.length) return alert('No sites to export!');
      const headers = Object.keys(filteredSites[0]);
      const csvRows = [headers.join(',')];

      filteredSites.forEach(s => {
        const values = headers.map(h => {
          const val = s[h] === null || s[h] === undefined ? '' : String(s[h]);
          return `"${val.replace(/"/g, '""')}"`;
        });
        csvRows.push(values.join(','));
      });

      const blob = new Blob([csvRows.join('\\n')], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `prehistoric_sites_export_${Date.now()}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    }

    function exportGeoJSON() {
      if (!filteredSites.length) return alert('No sites to export!');
      const features = filteredSites.map(s => ({
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [s.longitude, s.latitude]
        },
        properties: s
      }));

      const geojson = {
        type: "FeatureCollection",
        features: features
      };

      const blob = new Blob([JSON.stringify(geojson, null, 2)], { type: 'application/geo+json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `prehistoric_sites_${Date.now()}.geojson`;
      a.click();
      URL.revokeObjectURL(url);
    }

    // Initialize application on DOM ready
    window.addEventListener('DOMContentLoaded', () => {
      lucide.createIcons();
      initMap();
      initCharts();
      renderTable();
      updateKPICards();

      // Close modal on Escape
      window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
      });
    });
  </script>
</body>
</html>
"""

out_html_path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\index.html"
with open(out_html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Generated standalone GIS web dashboard at {out_html_path}")
