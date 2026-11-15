"""
Script to create the in-artifact dashboard prehistoric_dashboard.html
using allowlisted Tailwind CSS and native SVG / Canvas / Vanilla JS.
"""
import json
import os

data_path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\sites_data.json"
with open(data_path, "r", encoding="utf-8") as f:
    sites = json.load(f)

# Sort sites alphabetically by name
sites.sort(key=lambda s: s.get("site_name", ""))

artifact_path = r"C:\Users\DuDu-PC\.gemini\antigravity\brain\56c9ba5d-fc02-4acf-a11e-3bc90cf38fd5\prehistoric_dashboard.html"

# Pre-calculate stats
period_counts = {}
zone_counts = {}
adaptation_counts = {}
tech_counts = {
    "Block-on-Block / Anvil": 0,
    "Soft Hammer / Billet": 0,
    "Levallois Prepared Core": 0,
    "Punch Blade": 0,
    "Pressure Flaking": 0,
    "Pecking / Grinding / Polishing": 0
}

rock_art_count = 0
fauna_count = 0

for s in sites:
    p = s.get("period", "Other")
    period_counts[p] = period_counts.get(p, 0) + 1
    
    z = s.get("geographic_zone", "Other")
    zone_counts[z] = zone_counts.get(z, 0) + 1
    
    env = s.get("environmental_adaptation", "Other")
    adaptation_counts[env] = adaptation_counts.get(env, 0) + 1
    
    techs = s.get("manufacturing_techniques", "")
    if "block-on-block" in techs.lower() or "anvil" in techs.lower():
        tech_counts["Block-on-Block / Anvil"] += 1
    if "soft hammer" in techs.lower() or "cylinder" in techs.lower() or "billet" in techs.lower():
        tech_counts["Soft Hammer / Billet"] += 1
    if "levallois" in techs.lower():
        tech_counts["Levallois Prepared Core"] += 1
    if "punch blade" in techs.lower() or "punch" in techs.lower():
        tech_counts["Punch Blade"] += 1
    if "pressure" in techs.lower():
        tech_counts["Pressure Flaking"] += 1
    if "polish" in techs.lower() or "grind" in techs.lower() or "peck" in techs.lower():
        tech_counts["Pecking / Grinding / Polishing"] += 1
        
    if s.get("rock_art_present") == "Yes":
        rock_art_count += 1
    if s.get("fauna_flora_remains") and s.get("fauna_flora_remains") != "None reported" and s.get("fauna_flora_remains") != "Not preserved":
        fauna_count += 1

sites_json = json.dumps(sites, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prehistoric Archaeology Dashboard | Indian Subcontinent</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* Custom scrollbars */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #0f172a;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #475569;
    }}
    .site-dot {{
      transition: all 0.2s ease;
      cursor: pointer;
    }}
    .site-dot:hover {{
      r: 9;
      stroke-width: 2.5;
      filter: drop-shadow(0 0 6px rgba(255,255,255,0.8));
    }}
    .site-dot.selected {{
      r: 10;
      stroke: #ffffff;
      stroke-width: 3;
      filter: drop-shadow(0 0 8px #f59e0b);
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased selection:bg-amber-500 selection:text-slate-950">

  <!-- TOP HEADER -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-40 px-6 py-4">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-3">
          <span class="px-2.5 py-1 text-xs font-bold tracking-wider uppercase bg-amber-500/20 text-amber-400 border border-amber-500/30 rounded-full">
            Archaeological GIS Explorer
          </span>
          <span class="text-xs text-slate-400">Prehistory of India • Units 1–4</span>
        </div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-white mt-1 tracking-tight flex items-center gap-2">
          <span>Prehistoric Sites of the Indian Subcontinent</span>
          <span class="text-xs font-normal px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">104 Geo-Indexed Sites</span>
        </h1>
        <p class="text-xs md:text-sm text-slate-400 mt-0.5">
          Comprehensive spatial registry spanning Lower Palaeolithic Acheulian (1.5 Ma) to Neolithic Farming Cultures (1000 BCE).
        </p>
        <div class="mt-2 flex flex-wrap items-center gap-2 text-xs text-amber-400 font-medium">
          <span class="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-300">
            💡 Idea &amp; Design by <strong class="text-white">K.S.Chandra 2026</strong>
          </span>
          <span class="text-slate-600">•</span>
          <a href="mailto:kavikondalaschandra@gmail.com" class="text-sky-400 hover:text-sky-300 underline underline-offset-2">kavikondalaschandra@gmail.com</a>
        </div>
      </div>

      <!-- Quick Action / Leaflet GIS Launcher notice -->
      <div class="flex items-center gap-3 bg-slate-800/80 border border-slate-700 p-2.5 rounded-xl text-xs">
        <div class="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center font-bold text-sm">
          GIS
        </div>
        <div>
          <div class="font-semibold text-slate-200">Full Leaflet GIS Application Ready</div>
          <div class="text-slate-400">Run <code class="bg-slate-900 text-amber-300 px-1 py-0.5 rounded">python launch_dashboard.py</code> for Pan/Zoom Satellite Maps</div>
        </div>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">

    <!-- KPI STATS CARDS -->
    <section class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      <!-- Total Sites -->
      <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-3.5 hover:border-slate-700 transition">
        <div class="text-xs font-medium text-slate-400">Total Sites</div>
        <div class="text-2xl font-black text-white mt-1">104</div>
        <div class="text-[11px] text-slate-500 mt-0.5">1863 – 2026 Reports</div>
      </div>
      <!-- Lower Paleolithic -->
      <div class="bg-rose-950/20 border border-rose-900/40 rounded-xl p-3.5 hover:border-rose-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-rose-300">Lower Palaeolithic</span>
          <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
        </div>
        <div class="text-2xl font-black text-rose-400 mt-1">27</div>
        <div class="text-[11px] text-rose-300/60 mt-0.5">Acheulian & Soanian</div>
      </div>
      <!-- Middle Paleolithic -->
      <div class="bg-amber-950/20 border border-amber-900/40 rounded-xl p-3.5 hover:border-amber-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-amber-300">Middle Palaeolithic</span>
          <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
        </div>
        <div class="text-2xl font-black text-amber-400 mt-1">23</div>
        <div class="text-[11px] text-amber-300/60 mt-0.5">Nevasan & Flake-Core</div>
      </div>
      <!-- Upper Paleolithic -->
      <div class="bg-purple-950/20 border border-purple-900/40 rounded-xl p-3.5 hover:border-purple-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-purple-300">Upper Palaeolithic</span>
          <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
        </div>
        <div class="text-2xl font-black text-purple-400 mt-1">19</div>
        <div class="text-[11px] text-purple-300/60 mt-0.5">Blade-Burin & Ostrich Shell</div>
      </div>
      <!-- Mesolithic -->
      <div class="bg-emerald-950/20 border border-emerald-900/40 rounded-xl p-3.5 hover:border-emerald-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-emerald-300">Mesolithic</span>
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
        </div>
        <div class="text-2xl font-black text-emerald-400 mt-1">23</div>
        <div class="text-[11px] text-emerald-300/60 mt-0.5">Geometric Microliths</div>
      </div>
      <!-- Neolithic -->
      <div class="bg-cyan-950/20 border border-cyan-900/40 rounded-xl p-3.5 hover:border-cyan-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-cyan-300">Neolithic</span>
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-500"></span>
        </div>
        <div class="text-2xl font-black text-cyan-400 mt-1">12</div>
        <div class="text-[11px] text-cyan-300/60 mt-0.5">Polished Celts & Cereals</div>
      </div>
    </section>

    <!-- INTERACTIVE CONTROLS BAR -->
    <section class="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-xl space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
        <!-- Search -->
        <div class="md:col-span-5 relative">
          <input 
            type="text" 
            id="searchInput" 
            placeholder="Search site, river valley, state, tool typology, excavator..." 
            class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500 transition"
          >
        </div>

        <!-- Geo Zone Filter -->
        <div class="md:col-span-4">
          <select id="zoneSelect" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
            <option value="ALL">All Geographical Zones (Himalayan, Peninsular, etc.)</option>
            <option value="Himalayan / Sub-Himalayan Foothills">Himalayan / Sub-Himalayan (Soan, Beas, Sirsa)</option>
            <option value="Western India / Thar Desert Margin">Western India / Thar Margin (Didwana, Luni)</option>
            <option value="Central India / Narmada-Son Basin">Central India / Narmada-Son Basin</option>
            <option value="Peninsular India / Deccan Plateau">Peninsular India / Deccan Plateau</option>
            <option value="Eastern India / Chota Nagpur Plateau">Eastern India / Chota Nagpur Plateau</option>
            <option value="Southern Peninsular / Coromandel Coast">Southern Peninsular / Coromandel (Kortallayar)</option>
            <option value="Indo-Gangetic Alluvial Plain">Indo-Gangetic Alluvial Plain (Belan, Lakes)</option>
            <option value="Northern Highland / Kashmir Valley">Northern Highland / Kashmir Valley</option>
          </select>
        </div>

        <!-- Environmental Adaptation -->
        <div class="md:col-span-3">
          <select id="adaptationSelect" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
            <option value="ALL">All Environmental Adaptations</option>
            <option value="Alluvial Plain">Alluvial Plain (Unit 4)</option>
            <option value="Oxbow Lake / Horseshoe Lake Margin">Oxbow / Horseshoe Lake (Unit 4)</option>
            <option value="Sand Dune (Stabilized Longitudinal/Parabolic)">Sand Dune / Inter-dunal (Unit 4)</option>
            <option value="Plateau Floor / Open-air">Plateau Floor / Open-air (Unit 4)</option>
            <option value="Sandstone Rock Shelter / Escarpment">Sandstone Rock Shelter / Escarpment</option>
            <option value="Karstic Limestone Cave Complex">Karstic Cave Complex</option>
            <option value="Coastal Sand Dune / Teri Site">Coastal / Teri Red Dune</option>
          </select>
        </div>
      </div>

      <!-- PERIOD TOGGLE PILLS -->
      <div class="flex flex-wrap items-center gap-2 pt-1 border-t border-slate-800/80">
        <span class="text-xs font-semibold text-slate-400 mr-2">Filter Period:</span>
        <button onclick="setPeriodFilter('ALL')" id="pill-ALL" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-amber-500 text-slate-950 transition">All (104)</button>
        <button onclick="setPeriodFilter('Lower Paleolithic')" id="pill-LP" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-rose-300 hover:bg-slate-700 transition">Lower Palaeolithic (27)</button>
        <button onclick="setPeriodFilter('Middle Paleolithic')" id="pill-MP" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-amber-300 hover:bg-slate-700 transition">Middle Palaeolithic (23)</button>
        <button onclick="setPeriodFilter('Upper Paleolithic')" id="pill-UP" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-purple-300 hover:bg-slate-700 transition">Upper Palaeolithic (19)</button>
        <button onclick="setPeriodFilter('Mesolithic')" id="pill-MESO" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-emerald-300 hover:bg-slate-700 transition">Mesolithic (23)</button>
        <button onclick="setPeriodFilter('Neolithic')" id="pill-NEO" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-cyan-300 hover:bg-slate-700 transition">Neolithic (12)</button>

        <div class="ml-auto flex items-center gap-2">
          <label class="flex items-center gap-1.5 text-xs text-slate-300 cursor-pointer bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800">
            <input type="checkbox" id="rockArtOnly" class="rounded bg-slate-800 border-slate-700 text-amber-500 focus:ring-0">
            <span>Rock Art Only (12)</span>
          </label>
          <label class="flex items-center gap-1.5 text-xs text-slate-300 cursor-pointer bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800">
            <input type="checkbox" id="faunaOnly" class="rounded bg-slate-800 border-slate-700 text-emerald-500 focus:ring-0">
            <span>Fossil Fauna Preserved</span>
          </label>
        </div>
      </div>
    </section>

    <!-- WORKSPACE SPLIT VIEW: MAP & ARCHAEOLOGICAL DOSSIER -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      
      <!-- LEFT: INTERACTIVE SVG MAP PROJECTION -->
      <div class="lg:col-span-7 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative">
        <div class="flex items-center justify-between mb-3">
          <div>
            <h2 class="text-base font-bold text-white flex items-center gap-2">
              <span>Spatial Distribution Map</span>
              <span id="mapCounter" class="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-amber-400">104 / 104 Sites</span>
            </h2>
            <p class="text-xs text-slate-400">South Asia Projection (65°E–98°E, 7°N–36°N). Hover/click pin to inspect site details.</p>
          </div>
          <!-- Legend -->
          <div class="flex items-center gap-3 text-[11px]">
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span> Lower Pal</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span> Mid Pal</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-purple-500 inline-block"></span> Upper Pal</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Meso</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-cyan-500 inline-block"></span> Neo</span>
          </div>
        </div>

        <!-- SVG Map Container -->
        <div class="relative bg-slate-950 rounded-xl border border-slate-800/80 overflow-hidden flex items-center justify-center p-2">
          <svg id="subcontinentMap" viewBox="0 0 660 700" class="w-full h-auto max-h-[620px] select-none">
            <!-- Background Graticule Lines -->
            <defs>
              <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.7" stroke-dasharray="2,2"/>
              </pattern>
            </defs>
            <rect width="660" height="700" fill="#0b0f19" />
            <rect width="660" height="700" fill="url(#grid)" />

            <!-- Subcontinent Silhouette Approximate Boundary Polygon -->
            <path d="M 120,40 L 260,35 L 360,65 L 430,110 L 530,140 L 610,190 L 620,270 L 570,300 L 520,330 L 480,335 L 485,380 L 460,420 L 415,480 L 350,560 L 330,620 L 310,635 L 290,620 L 275,540 L 260,470 L 220,410 L 195,380 L 160,380 L 140,320 L 120,280 L 105,210 L 95,140 Z" 
                  fill="#111827" stroke="#1e293b" stroke-width="1.5" />
            
            <!-- Sri Lanka Outline -->
            <ellipse cx="360" cy="625" rx="16" ry="24" fill="#111827" stroke="#1e293b" stroke-width="1.5" />

            <!-- Major River Systems (Approximate Geographic Flowlines for Context) -->
            <!-- Indus -->
            <path d="M 280,60 Q 210,100 190,160 T 150,260 T 140,330" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.45" stroke-linecap="round"/>
            <text x="145" y="240" fill="#38bdf8" font-size="9" opacity="0.6">Indus</text>
            <!-- Ganga / Yamuna -->
            <path d="M 260,140 Q 320,170 380,210 T 500,270 T 560,310" fill="none" stroke="#0369a1" stroke-width="1.8" opacity="0.45" stroke-linecap="round"/>
            <text x="390" y="205" fill="#38bdf8" font-size="9" opacity="0.6">Ganga</text>
            <!-- Narmada / Tapti -->
            <path d="M 440,300 Q 340,310 240,315" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.45" stroke-linecap="round"/>
            <text x="320" y="305" fill="#38bdf8" font-size="9" opacity="0.6">Narmada</text>
            <!-- Godavari -->
            <path d="M 250,370 Q 340,385 435,405" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.45" stroke-linecap="round"/>
            <text x="320" y="375" fill="#38bdf8" font-size="9" opacity="0.6">Godavari</text>
            <!-- Krishna -->
            <path d="M 260,430 Q 330,445 420,460" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.45" stroke-linecap="round"/>
            <text x="330" y="435" fill="#38bdf8" font-size="9" opacity="0.6">Krishna</text>
            <!-- Kaveri -->
            <path d="M 285,520 Q 330,535 375,545" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.45" stroke-linecap="round"/>
            <text x="330" y="525" fill="#38bdf8" font-size="9" opacity="0.6">Kaveri</text>

            <!-- Geographic Zone Labels -->
            <text x="175" y="80" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">HIMALAYAN FOOTHILLS (SOAN)</text>
            <text x="140" y="200" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">THAR DESERT (DIDWANA)</text>
            <text x="310" y="270" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">VINDHYAN ESCARPMENT (BHIMBETKA)</text>
            <text x="260" y="480" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">DECCAN BASIN (HUNSGI-ISAMPUR)</text>
            <text x="310" y="585" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">KORTALLAYAR BASIN (ATTIRAMPAKKAM)</text>

            <!-- Dynamic Site Markers Container -->
            <g id="siteMarkersLayer"></g>
          </svg>

          <!-- Floating Tooltip -->
          <div id="mapTooltip" class="absolute pointer-events-none hidden bg-slate-900/95 border border-slate-700 text-xs rounded-lg px-3 py-2 shadow-2xl z-20 max-w-xs backdrop-blur"></div>
        </div>

        <!-- Quick Map Action Help -->
        <div class="mt-3 flex items-center justify-between text-xs text-slate-400">
          <span>Click any pin to inspect complete stratigraphy, tools & dates.</span>
          <button onclick="resetFilters()" class="text-amber-400 hover:text-amber-300 font-medium">Reset All Filters</button>
        </div>
      </div>

      <!-- RIGHT: ARCHAEOLOGICAL DOSSIER INSPECTOR -->
      <div class="lg:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col h-full min-h-[620px]">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-amber-500 animate-pulse"></span>
            <h2 class="text-base font-bold text-white uppercase tracking-wider text-xs">Archaeological Site Dossier</h2>
          </div>
          <span id="selectedPeriodBadge" class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">
            Select a Site
          </span>
        </div>

        <!-- Scrollable Dossier Card -->
        <div id="dossierContent" class="space-y-4 text-xs overflow-y-auto max-h-[580px] pr-2">
          <!-- Default Welcome State -->
          <div class="text-center py-16 space-y-3">
            <div class="w-16 h-16 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center mx-auto text-2xl text-amber-400">
              ⛏️
            </div>
            <h3 class="text-base font-bold text-slate-200">Select an Archaeological Site</h3>
            <p class="text-slate-400 max-w-xs mx-auto text-xs leading-relaxed">
              Click on any colored marker on the South Asian map or select a site from the data registry table below to inspect its stratigraphy, lithic assemblages, manufacturing techniques, fauna, and syllabus concordance.
            </p>
          </div>
        </div>
      </div>

    </div>

    <!-- STATISTICAL VISUALIZATIONS SECTION -->
    <section class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <h3 class="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
        <span>Prehistoric Technological & Environmental Breakdown</span>
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Chart 1: Cultural Chronology Distribution -->
        <div class="bg-slate-950 border border-slate-800 rounded-xl p-4">
          <div class="text-xs font-semibold text-slate-300 mb-3 flex items-center justify-between">
            <span>Period Chronology</span>
            <span class="text-slate-500">104 Sites</span>
          </div>
          <div class="space-y-2.5 text-xs">
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-rose-400">Lower Palaeolithic (Acheulian)</span>
                <span class="text-slate-300 font-bold">27 (26.0%)</span>
              </div>
              <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-rose-500 rounded-full" style="width: 26.0%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-amber-400">Middle Palaeolithic (Nevasan)</span>
                <span class="text-slate-300 font-bold">23 (22.1%)</span>
              </div>
              <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-amber-500 rounded-full" style="width: 22.1%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-purple-400">Upper Palaeolithic (Blade-Burin)</span>
                <span class="text-slate-300 font-bold">19 (18.3%)</span>
              </div>
              <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-purple-500 rounded-full" style="width: 18.3%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-emerald-400">Mesolithic (Microlithic)</span>
                <span class="text-slate-300 font-bold">23 (22.1%)</span>
              </div>
              <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full" style="width: 22.1%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-cyan-400">Neolithic (Polished Celts)</span>
                <span class="text-slate-300 font-bold">12 (11.5%)</span>
              </div>
              <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-cyan-500 rounded-full" style="width: 11.5%"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Chart 2: Manufacturing Techniques (Unit 2) -->
        <div class="bg-slate-950 border border-slate-800 rounded-xl p-4">
          <div class="text-xs font-semibold text-slate-300 mb-3 flex items-center justify-between">
            <span>Manufacturing Techniques (Unit 2)</span>
            <span class="text-slate-500">Indexed Assemblages</span>
          </div>
          <div class="space-y-2 text-xs">
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-slate-300">Block-on-Block / Anvil</span>
                <span class="text-amber-400 font-bold">{tech_counts['Block-on-Block / Anvil']}</span>
              </div>
              <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-amber-500 rounded-full" style="width: {min(100, int(tech_counts['Block-on-Block / Anvil']/104*100*2))}%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-slate-300">Soft Hammer / Billet</span>
                <span class="text-emerald-400 font-bold">{tech_counts['Soft Hammer / Billet']}</span>
              </div>
              <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full" style="width: {min(100, int(tech_counts['Soft Hammer / Billet']/104*100*2))}%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-slate-300">Levallois Prepared Core</span>
                <span class="text-blue-400 font-bold">{tech_counts['Levallois Prepared Core']}</span>
              </div>
              <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full" style="width: {min(100, int(tech_counts['Levallois Prepared Core']/104*100*2))}%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-slate-300">Punch Blade Flaking</span>
                <span class="text-purple-400 font-bold">{tech_counts['Punch Blade']}</span>
              </div>
              <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-purple-500 rounded-full" style="width: {min(100, int(tech_counts['Punch Blade']/104*100*2))}%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-slate-300">Pressure Flaking</span>
                <span class="text-pink-400 font-bold">{tech_counts['Pressure Flaking']}</span>
              </div>
              <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-pink-500 rounded-full" style="width: {min(100, int(tech_counts['Pressure Flaking']/104*100*2))}%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between mb-1">
                <span class="text-slate-300">Pecking / Polishing</span>
                <span class="text-cyan-400 font-bold">{tech_counts['Pecking / Grinding / Polishing']}</span>
              </div>
              <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-cyan-500 rounded-full" style="width: {min(100, int(tech_counts['Pecking / Grinding / Polishing']/104*100*2))}%"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Chart 3: Key Syllabus Highlights -->
        <div class="bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div class="text-xs font-semibold text-slate-300 mb-2 flex items-center justify-between">
              <span>Syllabus Highlights (Units 1–4)</span>
              <span class="text-amber-400 font-bold">100% Match</span>
            </div>
            <div class="space-y-2 text-xs text-slate-400">
              <div class="p-2 rounded bg-slate-900 border border-slate-800">
                <strong class="text-slate-200">Unit 1: Hominin Calvarium</strong>
                <div>Hathnora (Narmada Man, <em>Homo erectus/archaic sapiens</em>) with Pleistocene megafauna.</div>
              </div>
              <div class="p-2 rounded bg-slate-900 border border-slate-800">
                <strong class="text-slate-200">Unit 3: Regional Lithics</strong>
                <div>Himalayan Soan & Guler, Thar Didwana, Narmada-Son, Deccan Hunsgi-Isampur, Kortallayar Attirampakkam.</div>
              </div>
              <div class="p-2 rounded bg-slate-900 border border-slate-800">
                <strong class="text-slate-200">Unit 4: Mesolithic Adaptations</strong>
                <div>Sarai-Nahar Rai & Mahadaha (lakes), Bagor & Langhnaj (dunes), Chopani-Mando (alluvial), Paisra (plateau).</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- LIVE FILTERABLE DATA REGISTRY TABLE -->
    <section class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-4">
        <div>
          <h3 class="text-base font-bold text-white">Master Archaeological Registry</h3>
          <p class="text-xs text-slate-400">Searchable and sortable catalogue of all excavated, explored, and surveyed sites.</p>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="exportCSV()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1.5">
            <span>Download Filtered CSV</span>
          </button>
          <button onclick="exportGeoJSON()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1.5">
            <span>Export GeoJSON</span>
          </button>
        </div>
      </div>

      <!-- Table Container -->
      <div class="overflow-x-auto rounded-xl border border-slate-800 max-h-[500px] overflow-y-auto">
        <table class="w-full text-left text-xs text-slate-300">
          <thead class="bg-slate-950 text-slate-400 uppercase tracking-wider sticky top-0 z-10 border-b border-slate-800 text-[11px]">
            <tr>
              <th class="px-3 py-3 font-semibold">Site Name</th>
              <th class="px-3 py-3 font-semibold">Period</th>
              <th class="px-3 py-3 font-semibold">State / Region</th>
              <th class="px-3 py-3 font-semibold">River Valley</th>
              <th class="px-3 py-3 font-semibold">Excavator / Discoverer</th>
              <th class="px-3 py-3 font-semibold">Year</th>
              <th class="px-3 py-3 font-semibold">Coordinates</th>
              <th class="px-3 py-3 font-semibold text-center">Action</th>
            </tr>
          </thead>
          <tbody id="sitesTableBody" class="divide-y divide-slate-800/80 bg-slate-900/40">
            <!-- Dynamic Rows -->
          </tbody>
        </table>
      </div>
      <div class="mt-3 flex items-center justify-between text-xs text-slate-400">
        <span id="tableSummary">Showing 104 of 104 archaeological sites</span>
        <span>Click "Inspect" on any site to view complete dossier and focus map</span>
      </div>
    </section>

  </main>

  <!-- FOOTER ATTRIBUTION -->
  <footer class="border-t border-slate-800 bg-slate-900/90 py-6 px-6 mt-12 text-xs text-slate-400">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
      <div class="flex items-center justify-center sm:justify-start gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
        <span class="font-bold text-slate-200">Prehistoric Archaeological GIS Dashboard</span>
        <span>• Indian Subcontinent</span>
      </div>
      <div class="bg-slate-950 px-4 py-1.5 rounded-full border border-slate-800 text-slate-300 flex items-center justify-center gap-2 shadow-inner">
        <span class="font-semibold text-amber-400">Idea &amp; Design by K.S.Chandra 2026</span>
        <span class="text-slate-600">|</span>
        <a href="mailto:kavikondalaschandra@gmail.com" class="text-sky-400 hover:text-sky-300 underline underline-offset-2 flex items-center gap-1">
          kavikondalaschandra@gmail.com
        </a>
      </div>
      <div class="text-[11px] text-slate-500">
        Source Data: IAR, Ancient India, MASI &amp; University Excavation Reports
      </div>
    </div>
  </footer>

  <!-- JAVASCRIPT LOGIC & DATASET -->
  <script>
    const SITES_DATA = {sites_json};

    let activeFilter = {{
      period: 'ALL',
      zone: 'ALL',
      adaptation: 'ALL',
      search: '',
      rockArtOnly: false,
      faunaOnly: false
    }};

    let selectedSiteId = null;

    // Period colors
    const PERIOD_COLORS = {{
      'Lower Paleolithic': '#f43f5e',
      'Middle Paleolithic': '#f59e0b',
      'Upper Paleolithic': '#a855f7',
      'Mesolithic': '#10b981',
      'Neolithic': '#06b6d4',
      'Other': '#94a3b8'
    }};

    // Geographic bounds for SVG Projection
    // South Asia: Lon 66 to 96, Lat 8 to 35
    const LON_MIN = 66.0;
    const LON_MAX = 96.0;
    const LAT_MIN = 8.0;
    const LAT_MAX = 35.0;

    const SVG_WIDTH = 660;
    const SVG_HEIGHT = 700;

    function projectCoords(lat, lon) {{
      const x = ((lon - LON_MIN) / (LON_MAX - LON_MIN)) * 560 + 50;
      const y = ((LAT_MAX - lat) / (LAT_MAX - LAT_MIN)) * 600 + 50;
      return {{ x, y }};
    }}

    // Filter Logic
    function getFilteredSites() {{
      return SITES_DATA.filter(s => {{
        if (activeFilter.period !== 'ALL' && s.period !== activeFilter.period) return false;
        if (activeFilter.zone !== 'ALL' && s.geographic_zone !== activeFilter.zone) return false;
        if (activeFilter.adaptation !== 'ALL' && s.environmental_adaptation !== activeFilter.adaptation) return false;
        if (activeFilter.rockArtOnly && s.rock_art_present !== 'Yes') return false;
        if (activeFilter.faunaOnly && (!s.fauna_flora_remains || s.fauna_flora_remains === 'None reported' || s.fauna_flora_remains === 'Not preserved')) return false;
        
        if (activeFilter.search) {{
          const q = activeFilter.search.toLowerCase();
          const match = 
            (s.site_name && s.site_name.toLowerCase().includes(q)) ||
            (s.state_province && s.state_province.toLowerCase().includes(q)) ||
            (s.river_valley && s.river_valley.toLowerCase().includes(q)) ||
            (s.excavator_discoverer && s.excavator_discoverer.toLowerCase().includes(q)) ||
            (s.tool_typology && s.tool_typology.toLowerCase().includes(q)) ||
            (s.manufacturing_techniques && s.manufacturing_techniques.toLowerCase().includes(q));
          if (!match) return false;
        }}
        return true;
      }});
    }}

    // Render Map Markers
    function renderMapMarkers() {{
      const filtered = getFilteredSites();
      const container = document.getElementById('siteMarkersLayer');
      container.innerHTML = '';

      document.getElementById('mapCounter').innerText = `${{filtered.length}} / 104 Sites`;

      filtered.forEach(s => {{
        const lat = parseFloat(s.latitude_decimal);
        const lon = parseFloat(s.longitude_decimal);
        if (isNaN(lat) || isNaN(lon)) return;

        const pos = projectCoords(lat, lon);
        const color = PERIOD_COLORS[s.period] || '#94a3b8';
        const isSelected = selectedSiteId === s.site_id;

        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', pos.x);
        circle.setAttribute('cy', pos.y);
        circle.setAttribute('r', isSelected ? '9' : '5.5');
        circle.setAttribute('fill', color);
        circle.setAttribute('stroke', isSelected ? '#ffffff' : '#0f172a');
        circle.setAttribute('stroke-width', isSelected ? '2.5' : '1.2');
        circle.setAttribute('class', `site-dot ${{isSelected ? 'selected' : ''}}`);
        circle.setAttribute('id', `marker-${{s.site_id}}`);

        // Tooltip Events
        circle.addEventListener('mouseenter', (e) => showTooltip(e, s));
        circle.addEventListener('mousemove', (e) => moveTooltip(e));
        circle.addEventListener('mouseleave', hideTooltip);

        // Click Event -> Inspect Site
        circle.addEventListener('click', () => {{
          selectSite(s.site_id);
        }});

        container.appendChild(circle);
      }});
    }}

    // Tooltip Logic
    const tooltip = document.getElementById('mapTooltip');
    function showTooltip(e, site) {{
      tooltip.innerHTML = `
        <div class="font-bold text-white">${{site.site_name}}</div>
        <div class="text-[11px] text-amber-400 font-medium">${{site.period}}</div>
        <div class="text-slate-400 text-[10px] mt-0.5">${{site.district_locality || ''}}, ${{site.state_province}} (${{site.river_valley}})</div>
        <div class="text-slate-300 text-[10px] mt-1 italic">${{site.cultural_stage_lithic_industry || ''}}</div>
      `;
      tooltip.classList.remove('hidden');
      moveTooltip(e);
    }}

    function moveTooltip(e) {{
      const mapBox = document.getElementById('subcontinentMap').getBoundingClientRect();
      const x = e.clientX - mapBox.left + 15;
      const y = e.clientY - mapBox.top + 15;
      tooltip.style.left = `${{x}}px`;
      tooltip.style.top = `${{y}}px`;
    }}

    function hideTooltip() {{
      tooltip.classList.add('hidden');
    }}

    // Select and inspect site
    function selectSite(siteId) {{
      selectedSiteId = siteId;
      const site = SITES_DATA.find(s => s.site_id === siteId);
      if (!site) return;

      // Update map markers selection
      document.querySelectorAll('.site-dot').forEach(el => {{
        el.classList.remove('selected');
        el.setAttribute('r', '5.5');
        el.setAttribute('stroke-width', '1.2');
        el.setAttribute('stroke', '#0f172a');
      }});

      const marker = document.getElementById(`marker-${{siteId}}`);
      if (marker) {{
        marker.classList.add('selected');
        marker.setAttribute('r', '9');
        marker.setAttribute('stroke', '#ffffff');
        marker.setAttribute('stroke-width', '2.5');
      }}

      // Update Badge
      const badge = document.getElementById('selectedPeriodBadge');
      badge.innerText = site.period;
      badge.className = `text-xs font-semibold px-2.5 py-0.5 rounded-full border ${{
        site.period === 'Lower Paleolithic' ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' :
        site.period === 'Middle Paleolithic' ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' :
        site.period === 'Upper Paleolithic' ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' :
        site.period === 'Mesolithic' ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' :
        'bg-cyan-500/20 text-cyan-300 border-cyan-500/30'
      }}`;

      // Render Dossier Content
      const dossier = document.getElementById('dossierContent');
      dossier.innerHTML = `
        <div class="space-y-4 animate-fade-in">
          <!-- Site Header -->
          <div class="border-b border-slate-800 pb-3">
            <h3 class="text-xl font-black text-white">${{site.site_name}}</h3>
            <div class="text-xs text-slate-400 mt-0.5">
              ${{site.alternate_names ? `<em>Alt: ${{site.alternate_names}}</em> • ` : ''}}
              ${{site.district_locality || ''}}, <strong class="text-slate-200">${{site.state_province}}</strong>, ${{site.country}}
            </div>
            <div class="mt-2 flex flex-wrap items-center gap-1.5">
              <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono">${{site.latitude_decimal}}°N, ${{site.longitude_decimal}}°E</span>
              <span class="px-2 py-0.5 rounded bg-slate-800 text-amber-300 text-[10px]">${{site.river_valley}}</span>
              <span class="px-2 py-0.5 rounded bg-slate-800 text-indigo-300 text-[10px]">${{site.geographic_zone}}</span>
            </div>
          </div>

          <!-- Unit Concordance Pill -->
          <div class="p-2.5 rounded-xl bg-slate-950 border border-slate-800">
            <div class="text-[10px] uppercase font-bold text-amber-400 tracking-wider">Prehistory of India Syllabus Concordance</div>
            <div class="text-slate-200 font-semibold mt-0.5">${{site.syllabus_unit_concordance || 'Unit 3: Regional Palaeolithic / Unit 4: Mesolithic'}}</div>
            <div class="text-[11px] text-slate-400 mt-0.5">Adaptation: <span class="text-slate-300 font-medium">${{site.environmental_adaptation}}</span></div>
          </div>

          <!-- Discovery & Excavation -->
          <div class="grid grid-cols-2 gap-2 text-xs">
            <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <div class="text-[10px] text-slate-500 uppercase font-semibold">Excavator / Discoverer</div>
              <div class="text-slate-200 font-medium mt-0.5">${{site.excavator_discoverer || 'Surveyed / Explored'}}</div>
            </div>
            <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <div class="text-[10px] text-slate-500 uppercase font-semibold">Year of Discovery / Work</div>
              <div class="text-slate-200 font-medium mt-0.5">${{site.year_of_discovery || 'Multiple seasons'}}</div>
            </div>
          </div>

          <!-- Chronology & Stratigraphy -->
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-1.5">
            <div class="text-[10px] text-slate-500 uppercase font-semibold">Stratigraphy & Chronological Dating</div>
            <div class="text-slate-200"><strong class="text-slate-400">Context:</strong> ${{site.stratigraphic_context || 'Primary Acheulian/Mesolithic deposit'}}</div>
            <div class="text-slate-200"><strong class="text-slate-400">Absolute Chronology:</strong> ${{site.absolute_chronology_dates || 'Typologically / Relative dated'}}</div>
          </div>

          <!-- Lithic Typology & Manufacturing Techniques -->
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-2">
            <div class="text-[10px] text-amber-400 uppercase font-bold tracking-wider">Lithic Industry & Technology (Unit 2)</div>
            <div>
              <span class="text-slate-400 font-medium">Cultural Stage:</span> 
              <span class="text-slate-200 font-bold">${{site.cultural_stage_lithic_industry}}</span>
            </div>
            <div>
              <span class="text-slate-400 font-medium">Tool Typology:</span> 
              <span class="text-slate-200">${{site.tool_typology}}</span>
            </div>
            <div>
              <span class="text-slate-400 font-medium">Manufacturing Techniques:</span> 
              <span class="text-emerald-300 font-mono text-[11px]">${{site.manufacturing_techniques}}</span>
            </div>
            <div class="grid grid-cols-2 gap-2 pt-1 border-t border-slate-900">
              <div>
                <span class="text-slate-400">Raw Material:</span>
                <div class="text-slate-300 font-medium">${{site.raw_material}}</div>
              </div>
              <div>
                <span class="text-slate-400">Metric Ranges:</span>
                <div class="text-slate-300 font-mono text-[11px]">${{site.metric_dimensions_size_ranges}}</div>
              </div>
            </div>
          </div>

          <!-- Fauna, Flora & Rock Art -->
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-1.5">
            <div class="text-[10px] text-slate-500 uppercase font-semibold">Faunal, Floral & Rock Art Evidence</div>
            <div class="text-slate-200"><strong class="text-slate-400">Fauna / Flora:</strong> ${{site.fauna_flora_remains || 'None reported'}}</div>
            <div class="text-slate-200"><strong class="text-slate-400">Hominin / Skeletal:</strong> ${{site.hominin_human_skeletal_remains || 'None found'}}</div>
            <div class="text-slate-200"><strong class="text-slate-400">Rock Art:</strong> <span class="${{site.rock_art_present === 'Yes' ? 'text-amber-400 font-bold' : 'text-slate-500'}}">${{site.rock_art_present === 'Yes' ? `Present (${{site.rock_art_details || 'Petroglyphs / Ochre paintings'}})` : 'None recorded'}}</span></div>
          </div>

          <!-- Archaeological Significance -->
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
            <div class="text-[10px] text-slate-500 uppercase font-semibold">Archaeological Significance</div>
            <p class="text-slate-300 mt-1 leading-relaxed">${{site.typical_usage_significance || 'Regional benchmark locality.'}}</p>
          </div>

          <!-- Academic References & Citations -->
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-[11px]">
            <div class="text-[10px] text-slate-500 uppercase font-semibold">Publications & Citations (IAR / MASI / Ancient India)</div>
            <div class="text-slate-400 mt-1 italic">${{site.references_citations || 'Excavation Reports & Memoir'}}</div>
          </div>
        </div>
      `;

      // Highlight row in table if present
      document.querySelectorAll('#sitesTableBody tr').forEach(row => {{
        row.classList.remove('bg-amber-500/10', 'border-l-4', 'border-l-amber-500');
      }});
      const tableRow = document.getElementById(`row-${{siteId}}`);
      if (tableRow) {{
        tableRow.classList.add('bg-amber-500/10', 'border-l-4', 'border-l-amber-500');
        tableRow.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }}
    }}

    // Render Registry Table
    function renderTable() {{
      const filtered = getFilteredSites();
      const tbody = document.getElementById('sitesTableBody');
      tbody.innerHTML = '';

      document.getElementById('tableSummary').innerText = `Showing ${{filtered.length}} of 104 archaeological sites`;

      filtered.forEach(s => {{
        const tr = document.createElement('tr');
        tr.id = `row-${{s.site_id}}`;
        tr.className = 'hover:bg-slate-800/60 transition cursor-pointer';
        
        const periodColorClass = 
          s.period === 'Lower Paleolithic' ? 'text-rose-400 font-semibold' :
          s.period === 'Middle Paleolithic' ? 'text-amber-400 font-semibold' :
          s.period === 'Upper Paleolithic' ? 'text-purple-400 font-semibold' :
          s.period === 'Mesolithic' ? 'text-emerald-400 font-semibold' :
          'text-cyan-400 font-semibold';

        tr.innerHTML = `
          <td class="px-3 py-2.5 font-bold text-white whitespace-nowrap">${{s.site_name}}</td>
          <td class="px-3 py-2.5 ${{periodColorClass}} whitespace-nowrap">${{s.period}}</td>
          <td class="px-3 py-2.5 text-slate-300 whitespace-nowrap">${{s.state_province}}</td>
          <td class="px-3 py-2.5 text-slate-400 whitespace-nowrap">${{s.river_valley}}</td>
          <td class="px-3 py-2.5 text-slate-300 max-w-xs truncate" title="${{s.excavator_discoverer}}">${{s.excavator_discoverer}}</td>
          <td class="px-3 py-2.5 text-slate-400 whitespace-nowrap">${{s.year_of_discovery}}</td>
          <td class="px-3 py-2.5 font-mono text-[11px] text-slate-400 whitespace-nowrap">${{s.latitude_decimal}}°, ${{s.longitude_decimal}}°</td>
          <td class="px-3 py-2.5 text-center whitespace-nowrap">
            <button onclick="selectSite('${{s.site_id}}')" class="px-2.5 py-1 rounded-md bg-slate-800 hover:bg-amber-500 hover:text-slate-950 text-slate-200 font-medium transition text-[11px]">
              Inspect
            </button>
          </td>
        `;

        tr.addEventListener('click', (e) => {{
          if (e.target.tagName !== 'BUTTON') {{
            selectSite(s.site_id);
          }}
        }});

        tbody.appendChild(tr);
      }});
    }}

    // Filter Handlers
    function setPeriodFilter(period) {{
      activeFilter.period = period;
      document.querySelectorAll('.period-pill').forEach(btn => {{
        btn.className = 'period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition';
      }});
      const activeBtn = document.getElementById(
        period === 'ALL' ? 'pill-ALL' :
        period === 'Lower Paleolithic' ? 'pill-LP' :
        period === 'Middle Paleolithic' ? 'pill-MP' :
        period === 'Upper Paleolithic' ? 'pill-UP' :
        period === 'Mesolithic' ? 'pill-MESO' : 'pill-NEO'
      );
      if (activeBtn) {{
        activeBtn.className = 'period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-amber-500 text-slate-950 transition';
      }}
      updateView();
    }}

    function resetFilters() {{
      activeFilter = {{
        period: 'ALL',
        zone: 'ALL',
        adaptation: 'ALL',
        search: '',
        rockArtOnly: false,
        faunaOnly: false
      }};
      document.getElementById('searchInput').value = '';
      document.getElementById('zoneSelect').value = 'ALL';
      document.getElementById('adaptationSelect').value = 'ALL';
      document.getElementById('rockArtOnly').checked = false;
      document.getElementById('faunaOnly').checked = false;
      setPeriodFilter('ALL');
    }}

    function updateView() {{
      renderMapMarkers();
      renderTable();
    }}

    // Event Listeners for Filters
    document.getElementById('searchInput').addEventListener('input', (e) => {{
      activeFilter.search = e.target.value.trim();
      updateView();
    }});

    document.getElementById('zoneSelect').addEventListener('change', (e) => {{
      activeFilter.zone = e.target.value;
      updateView();
    }});

    document.getElementById('adaptationSelect').addEventListener('change', (e) => {{
      activeFilter.adaptation = e.target.value;
      updateView();
    }});

    document.getElementById('rockArtOnly').addEventListener('change', (e) => {{
      activeFilter.rockArtOnly = e.target.checked;
      updateView();
    }});

    document.getElementById('faunaOnly').addEventListener('change', (e) => {{
      activeFilter.faunaOnly = e.target.checked;
      updateView();
    }});

    // Export CSV
    function exportCSV() {{
      const filtered = getFilteredSites();
      if (filtered.length === 0) return alert('No sites to export with current filters.');

      const headers = Object.keys(filtered[0]);
      let csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\\n";

      filtered.forEach(row => {{
        const rowVals = headers.map(h => {{
          let val = row[h] ? String(row[h]).replace(/"/g, '""') : '';
          return `"${{val}}"`;
        }});
        csvContent += rowVals.join(",") + "\\n";
      }});

      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "prehistoric_filtered_sites.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    // Export GeoJSON
    function exportGeoJSON() {{
      const filtered = getFilteredSites();
      const geojson = {{
        type: "FeatureCollection",
        features: filtered.map(s => ({{
          type: "Feature",
          geometry: {{
            type: "Point",
            coordinates: [parseFloat(s.longitude_decimal), parseFloat(s.latitude_decimal)]
          }},
          properties: {{ ...s }}
        }}))
      }};

      const blob = new Blob([JSON.stringify(geojson, null, 2)], {{ type: "application/geo+json" }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.setAttribute("href", url);
      link.setAttribute("download", "prehistoric_sites_gis.geojson");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    // Initialize on Load
    window.addEventListener('DOMContentLoaded', () => {{
      updateView();
      // Select first site (e.g. Attirampakkam or Hathnora or Bhimbetka)
      const featured = SITES_DATA.find(s => s.site_name === 'Bhimbetka') || SITES_DATA[0];
      if (featured) {{
        selectSite(featured.site_id);
      }}
    }});
  </script>
</body>
</html>
"""

with open(artifact_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated in-artifact dashboard at {artifact_path} (Size: {os.path.getsize(artifact_path)} bytes)")
