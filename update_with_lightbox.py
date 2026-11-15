"""
Update both index.html and prehistoric_dashboard.html with:
- "Click to Enlarge" image functionality in Prehistoric Foundations & Palaeoenvironmental Archive
- High-resolution Lightbox Modal with zoom, full captions, Prev/Next navigation, and Escape key
- Click to enlarge also available from the site dossier modal
"""

import json
import os

def update():
    json_path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\sites_data.json"
    with open(json_path, "r", encoding="utf-8") as f:
        sites = json.load(f)

    sites_json_str = json.dumps(sites, ensure_ascii=False)

    # -------------------------------------------------------------
    # 1. GENERATE index.html
    # -------------------------------------------------------------
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prehistoric Archaeology of Indian Subcontinent | Interactive GIS Dashboard</title>
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Leaflet CSS & JS (100% Free, NO API KEY REQUIRED, NO 403 ERROR) -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
    
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #0b0f19;
      color: #e2e8f0;
    }}
    
    .font-display {{
      font-family: 'Space Grotesk', sans-serif;
    }}
    
    #map {{
      height: 560px;
      border-radius: 1rem;
      z-index: 10;
    }}
    
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #111827;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #374151;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #4b5563;
    }}

    .leaflet-popup-content-wrapper {{
      background: #111827;
      color: #f3f4f6;
      border: 1px solid #374151;
      border-radius: 0.75rem;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }}
    .leaflet-popup-tip {{
      background: #111827;
    }}
    .leaflet-container {{
      background: #0b0f19;
    }}
    
    .pulse-dot {{
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
      0% {{ transform: scale(0.95); opacity: 0.8; }}
      50% {{ transform: scale(1.3); opacity: 1; }}
      100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}

    .tab-btn.active {{
      border-color: #f59e0b;
      color: #f59e0b;
      background-color: rgba(245, 158, 11, 0.1);
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- TOP NAVIGATION HEADER -->
  <header class="border-b border-gray-800 bg-gray-900/90 backdrop-blur sticky top-0 z-50 px-6 py-4">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="h-11 w-11 rounded-xl bg-gradient-to-tr from-amber-500 to-rose-600 flex items-center justify-center text-white shadow-lg shadow-amber-500/20">
          <i data-lucide="compass" class="w-6 h-6"></i>
        </div>
        <div>
          <h1 class="text-xl md:text-2xl font-bold font-display tracking-tight text-white flex items-center gap-2">
            <span>Prehistory of India</span>
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-400 font-sans border border-amber-500/30">104 Geo-Indexed Sites</span>
          </h1>
          <p class="text-xs text-gray-400 mt-0.5">Palaeolithic, Mesolithic & Neolithic Archaeological GIS Compendium (1863–Present)</p>
          <div class="mt-1 flex items-center gap-2 text-xs text-amber-400 font-medium">
            <span class="flex items-center gap-1"><i data-lucide="sparkles" class="w-3.5 h-3.5"></i> Idea & Design by <strong>K.S.Chandra 2026</strong></span>
            <span class="text-gray-600">•</span>
            <a href="mailto:kavikondalaschandra@gmail.com" class="text-sky-400 hover:text-sky-300 underline underline-offset-2">kavikondalaschandra@gmail.com</a>
          </div>
        </div>
      </div>

      <!-- Header Right: Reset & Quick Help -->
      <div class="flex items-center gap-3">
        <button onclick="resetFilters()" class="px-3.5 py-2 rounded-xl bg-rose-950/40 hover:bg-rose-900/60 text-xs font-semibold text-rose-300 border border-rose-800/40 flex items-center gap-1.5 transition">
          <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i> Reset All Filters
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
        <span class="text-[10px] text-gray-400 mt-1">Across Subcontinent</span>
      </div>

      <div class="bg-gray-900/90 border border-rose-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-rose-800/50 transition">
        <div class="flex items-center justify-between text-rose-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Lower Palaeo</span>
          <span class="pulse-dot bg-rose-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-rose-300" id="stat-lp-sites">27</div>
        <span class="text-[10px] text-gray-400 mt-1">Acheulian & Soanian</span>
      </div>

      <div class="bg-gray-900/90 border border-amber-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-amber-800/50 transition">
        <div class="flex items-center justify-between text-amber-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Middle Palaeo</span>
          <span class="pulse-dot bg-amber-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-amber-300" id="stat-mp-sites">12</div>
        <span class="text-[10px] text-gray-400 mt-1">Levallois & Nevasan</span>
      </div>

      <div class="bg-gray-900/90 border border-purple-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-purple-800/50 transition">
        <div class="flex items-center justify-between text-purple-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Upper Palaeo</span>
          <span class="pulse-dot bg-purple-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-purple-300" id="stat-up-sites">12</div>
        <span class="text-[10px] text-gray-400 mt-1">Blade & Burin</span>
      </div>

      <div class="bg-gray-900/90 border border-emerald-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-emerald-800/50 transition">
        <div class="flex items-center justify-between text-emerald-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Mesolithic</span>
          <span class="pulse-dot bg-emerald-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-emerald-300" id="stat-meso-sites">18</div>
        <span class="text-[10px] text-gray-400 mt-1">Microliths & Rock Art</span>
      </div>

      <div class="bg-gray-900/90 border border-cyan-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-cyan-800/50 transition">
        <div class="flex items-center justify-between text-cyan-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Neolithic</span>
          <span class="pulse-dot bg-cyan-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-cyan-300" id="stat-neo-sites">35</div>
        <span class="text-[10px] text-gray-400 mt-1">Polished Celts & Farming</span>
      </div>
    </div>

    <!-- CORE FOUNDATIONS, HUMAN EVOLUTION & LITHIC TOOL GALLERY TABS -->
    <div class="bg-gray-900/90 border border-gray-800 rounded-2xl p-5 shadow-2xl space-y-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-gray-800 pb-3">
        <div>
          <h2 class="text-base font-bold font-display text-white flex items-center gap-2">
            <i data-lucide="book-open" class="w-4 h-4 text-amber-400"></i>
            <span>Prehistoric Foundations & Palaeoenvironmental Archive</span>
          </h2>
          <p class="text-xs text-gray-400">Essential chronological, environmental, and technological archive of the Indian Subcontinent.</p>
        </div>
        
        <!-- Tab Navigation Buttons -->
        <div class="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
          <button onclick="switchTab('tab-typology')" id="btn-tab-typology" class="tab-btn active px-3 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition flex items-center gap-1.5 whitespace-nowrap">
            <i data-lucide="image" class="w-3.5 h-3.5"></i> Lithic Tool Gallery
          </button>
          <button onclick="switchTab('tab-geology')" id="btn-tab-geology" class="tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition flex items-center gap-1.5 whitespace-nowrap text-gray-400 hover:text-gray-200">
            <i data-lucide="layers" class="w-3.5 h-3.5"></i> Geological Time Scale
          </button>
          <button onclick="switchTab('tab-evolution')" id="btn-tab-evolution" class="tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition flex items-center gap-1.5 whitespace-nowrap text-gray-400 hover:text-gray-200">
            <i data-lucide="user-check" class="w-3.5 h-3.5"></i> Human Evolution (Hathnora)
          </button>
          <button onclick="switchTab('tab-palaeoenv')" id="btn-tab-palaeoenv" class="tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition flex items-center gap-1.5 whitespace-nowrap text-gray-400 hover:text-gray-200">
            <i data-lucide="trees" class="w-3.5 h-3.5"></i> Prehistoric Flora & Fauna
          </button>
        </div>
      </div>

      <!-- TAB 1: LITHIC TOOL TYPOLOGY GALLERY WITH ENLARGE OPTION -->
      <div id="tab-typology" class="tab-content space-y-4">
        <div class="flex items-center justify-between">
          <p class="text-xs text-gray-400">Photographic gallery of diagnostic lithic tool industries, fossil hominins, and rock art from the Indian Subcontinent. Click any card or the enlarge button to view high-resolution specimen plates.</p>
          <span class="text-[11px] text-amber-400 font-medium flex items-center gap-1">
            <i data-lucide="zoom-in" class="w-3.5 h-3.5"></i> Click any image to enlarge
          </span>
        </div>
        
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-9 gap-3">
          
          <!-- 1. Handaxe -->
          <div onclick="selectAndEnlargeTool('handaxe')" class="bg-gray-950 border border-gray-800 hover:border-amber-500 p-2.5 rounded-xl cursor-pointer transition text-center group">
            <div class="h-28 rounded-lg overflow-hidden bg-gray-900 border border-gray-800 mb-2 relative flex items-center justify-center">
              <img src="images/handaxe.jpg" alt="Acheulian Handaxe" class="h-full w-full object-cover group-hover:scale-105 transition duration-300">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white bg-gradient-to-t from-black/80 via-transparent to-transparent">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Enlarge
              </div>
            </div>
            <div class="text-xs font-bold text-white truncate">Acheulian Handaxe</div>
            <div class="text-[10px] text-rose-400">Lower Palaeo</div>
          </div>

          <!-- 2. Cleaver -->
          <div onclick="selectAndEnlargeTool('cleaver')" class="bg-gray-950 border border-gray-800 hover:border-amber-500 p-2.5 rounded-xl cursor-pointer transition text-center group">
            <div class="h-28 rounded-lg overflow-hidden bg-gray-900 border border-gray-800 mb-2 relative flex items-center justify-center p-1">
              <img src="images/cleaver.png" alt="Acheulian Cleaver" class="h-full w-auto object-contain group-hover:scale-105 transition duration-300">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white bg-gradient-to-t from-black/80 via-transparent to-transparent">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Enlarge
              </div>
            </div>
            <div class="text-xs font-bold text-white truncate">Acheulian Cleaver</div>
            <div class="text-[10px] text-rose-400">Lower Palaeo</div>
          </div>

          <!-- 3. Chopper -->
          <div onclick="selectAndEnlargeTool('chopper')" class="bg-gray-950 border border-gray-800 hover:border-amber-500 p-2.5 rounded-xl cursor-pointer transition text-center group">
            <div class="h-28 rounded-lg overflow-hidden bg-gray-900 border border-gray-800 mb-2 relative flex items-center justify-center">
              <img src="images/chopper.jpg" alt="Pebble Chopper" class="h-full w-full object-cover group-hover:scale-105 transition duration-300">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white bg-gradient-to-t from-black/80 via-transparent to-transparent">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Enlarge
              </div>
            </div>
            <div class="text-xs font-bold text-white truncate">Pebble Chopper</div>
            <div class="text-[10px] text-rose-400">Soanian Core</div>
          </div>

          <!-- 4. Levallois -->
          <div onclick="selectAndEnlargeTool('levallois')" class="bg-gray-950 border border-gray-800 hover:border-amber-500 p-2.5 rounded-xl cursor-pointer transition text-center group">
            <div class="h-28 rounded-lg overflow-hidden bg-gray-900 border border-gray-800 mb-2 relative flex items-center justify-center">
              <img src="images/levallois.jpg" alt="Levallois Core" class="h-full w-full object-cover group-hover:scale-105 transition duration-300">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white bg-gradient-to-t from-black/80 via-transparent to-transparent">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Enlarge
              </div>
            </div>
            <div class="text-xs font-bold text-white truncate">Levallois Core</div>
            <div class="text-[10px] text-amber-400">Middle Palaeo</div>
          </div>

          <!-- 5. Blade & Burin -->
          <div onclick="selectAndEnlargeTool('blade')" class="bg-gray-950 border border-gray-800 hover:border-amber-500 p-2.5 rounded-xl cursor-pointer transition text-center group">
            <div class="h-28 rounded-lg overflow-hidden bg-gray-900 border border-gray-800 mb-2 relative flex items-center justify-center p-1">
              <img src="images/blade.png" alt="Prismatic Blade & Core" class="h-full w-auto object-contain group-hover:scale-105 transition duration-300">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white bg-gradient-to-t from-black/80 via-transparent to-transparent">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Enlarge
              </div>
            </div>
            <div class="text-xs font-bold text-white truncate">Blade & Burin</div>
            <div class="text-[10px] text-purple-400">Upper Palaeo</div>
          </div>

          <!-- 6. Microliths -->
          <div onclick="selectAndEnlargeTool('microlith')" class="bg-gray-950 border border-gray-800 hover:border-amber-500 p-2.5 rounded-xl cursor-pointer transition text-center group">
            <div class="h-28 rounded-lg overflow-hidden bg-gray-900 border border-gray-800 mb-2 relative flex items-center justify-center">
              <img src="images/microlith.jpg" alt="Geometric Microliths" class="h-full w-full object-cover group-hover:scale-105 transition duration-300">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white bg-gradient-to-t from-black/80 via-transparent to-transparent">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Enlarge
              </div>
            </div>
            <div class="text-xs font-bold text-white truncate">Microliths</div>
            <div class="text-[10px] text-emerald-400">Mesolithic</div>
          </div>

          <!-- 7. Polished Celt -->
          <div onclick="selectAndEnlargeTool('celt')" class="bg-gray-950 border border-gray-800 hover:border-amber-500 p-2.5 rounded-xl cursor-pointer transition text-center group">
            <div class="h-28 rounded-lg overflow-hidden bg-gray-900 border border-gray-800 mb-2 relative flex items-center justify-center">
              <img src="images/celt.jpg" alt="Polished Stone Celt" class="h-full w-full object-cover group-hover:scale-105 transition duration-300">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white bg-gradient-to-t from-black/80 via-transparent to-transparent">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Enlarge
              </div>
            </div>
            <div class="text-xs font-bold text-white truncate">Polished Celt</div>
            <div class="text-[10px] text-cyan-400">Neolithic</div>
          </div>

          <!-- 8. Hathnora Calvarium -->
          <div onclick="selectAndEnlargeTool('hathnora')" class="bg-gray-950 border border-gray-800 hover:border-amber-500 p-2.5 rounded-xl cursor-pointer transition text-center group">
            <div class="h-28 rounded-lg overflow-hidden bg-gray-900 border border-gray-800 mb-2 relative flex items-center justify-center">
              <img src="images/hathnora.jpg" alt="Narmada Man Skull" class="h-full w-full object-cover group-hover:scale-105 transition duration-300">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white bg-gradient-to-t from-black/80 via-transparent to-transparent">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Enlarge
              </div>
            </div>
            <div class="text-xs font-bold text-white truncate">Narmada Skull</div>
            <div class="text-[10px] text-rose-400">Hathnora Fossil</div>
          </div>

          <!-- 9. Rock Art -->
          <div onclick="selectAndEnlargeTool('bhimbetka')" class="bg-gray-950 border border-gray-800 hover:border-amber-500 p-2.5 rounded-xl cursor-pointer transition text-center group">
            <div class="h-28 rounded-lg overflow-hidden bg-gray-900 border border-gray-800 mb-2 relative flex items-center justify-center">
              <img src="images/bhimbetka.jpg" alt="Bhimbetka Rock Art" class="h-full w-full object-cover group-hover:scale-105 transition duration-300">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white bg-gradient-to-t from-black/80 via-transparent to-transparent">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Enlarge
              </div>
            </div>
            <div class="text-xs font-bold text-white truncate">Rock Art Panel</div>
            <div class="text-[10px] text-amber-400">Bhimbetka Cave</div>
          </div>

        </div>

        <!-- Tool Detail Display Card with Enlarge Button -->
        <div id="toolDetailCard" class="bg-gray-950 p-4 rounded-xl border border-gray-800 text-xs">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-gray-800 pb-2 mb-3 gap-2">
            <div>
              <h4 id="toolDetailTitle" class="font-bold text-sm text-amber-400">Acheulian Bifacial Handaxe (Biface)</h4>
              <span id="toolDetailPeriod" class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-mono text-[10px]">Lower Palaeolithic (1.5 Ma – 120 ka)</span>
            </div>
            <button onclick="openImageLightbox(currentToolKey)" class="px-3.5 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-600 text-black font-semibold text-xs flex items-center gap-1.5 transition shadow">
              <i data-lucide="zoom-in" class="w-3.5 h-3.5"></i> Click to Enlarge Image
            </button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-gray-300">
            <div>
              <strong class="text-gray-200 block mb-1">Morphological Definition:</strong>
              <p id="toolDetailDesc" class="text-gray-400 leading-relaxed">
                Bifacially flaked core/large-flake implement with pointed or amygdaloid apex, sharp bilateral cutting edges, and rounded butt. Manufactured initially by block-on-block/hard hammer followed by soft hammer (billet) step retouch.
              </p>
            </div>
            <div>
              <strong class="text-gray-200 block mb-1">Manufacturing Technology:</strong>
              <p id="toolDetailTech" class="text-gray-400 leading-relaxed">
                Direct stone hammer percussion, soft antler/wood cylinder hammer thinning, invasive flaking creating lenticular cross-section.
              </p>
            </div>
            <div>
              <strong class="text-gray-200 block mb-1">Key Indian Subcontinent Localities:</strong>
              <p id="toolDetailSites" class="text-amber-300 font-medium leading-relaxed">
                Attirampakkam (TN), Isampur (KA), Bhimbetka (MP), Didwana (RJ), Hunsgi (KA), Chirki-Nevasa (MH), Kuliana (OD).
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: GEOLOGICAL TIME SCALE -->
      <div id="tab-geology" class="tab-content hidden grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-rose-400 font-bold uppercase tracking-wider text-[11px]">Lower / Early Pleistocene</span>
            <span class="text-gray-500 font-mono text-[10px]">2.58 – 0.78 Ma</span>
          </div>
          <h3 class="text-white font-bold text-sm">Matuyama Reversed Chron</h3>
          <p class="text-gray-400 leading-relaxed">
            Onset of Northern Hemisphere glaciation; Indian Siwalik Pinjor formation faunal turnover. Early Acheulian stone tools emerge in peninsular India (Attirampakkam dated by cosmogenic nuclides to 1.5 Ma; Isampur quarry 1.2 Ma).
          </p>
          <div class="pt-2 text-[11px] text-amber-300 font-medium">MIS Stages 63 to 19 • Glacio-eustatic fluctuations</div>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-amber-400 font-bold uppercase tracking-wider text-[11px]">Middle Pleistocene</span>
            <span class="text-gray-500 font-mono text-[10px]">780 – 126 ka</span>
          </div>
          <h3 class="text-white font-bold text-sm">Brunhes Normal Chron</h3>
          <p class="text-gray-400 leading-relaxed">
            Climax of the Acheulian tradition (handaxes & cleavers); hominin occupation in the Narmada, Hunsgi, and Kortallayar basins. Hathnora cranial calvarium (*Narmada Man*) positioned in the basal gravels of the Surajkund Formation (~250–300 ka).
          </p>
          <div class="pt-2 text-[11px] text-amber-300 font-medium">MIS Stages 19 to 6 • Acheulian & Archaic Hominins</div>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-purple-400 font-bold uppercase tracking-wider text-[11px]">Late / Upper Pleistocene</span>
            <span class="text-gray-500 font-mono text-[10px]">126 – 11.7 ka</span>
          </div>
          <h3 class="text-white font-bold text-sm">Last Glacial Cycle & Toba Tephra</h3>
          <p class="text-gray-400 leading-relaxed">
            Transition from Middle Palaeolithic (Levallois, scrapers) to Upper Palaeolithic blade-burin industries. Catastrophic Youngest Toba Tuff volcanic eruption (74 ka) documented with human occupation beneath and above ash at Jwalapuram.
          </p>
          <div class="pt-2 text-[11px] text-amber-300 font-medium">MIS Stages 5 to 2 • Toba Tephra (74 ka) • LGM (21 ka)</div>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-emerald-400 font-bold uppercase tracking-wider text-[11px]">Holocene Epoch</span>
            <span class="text-gray-500 font-mono text-[10px]">11.7 ka – Present</span>
          </div>
          <h3 class="text-white font-bold text-sm">Post-Glacial Warm Optimum</h3>
          <p class="text-gray-400 leading-relaxed">
            Intensification of southwest monsoon; emergence of intensive Mesolithic foraging, geometric microlithic hunting weaponry, rock shelter paintings, followed by early Neolithic agriculture (Mehrgarh, Belan Valley, Kashmir, Southern Ashmounds).
          </p>
          <div class="pt-2 text-[11px] text-amber-300 font-medium">MIS Stage 1 • Holocene Climatic Optimum • Farming</div>
        </div>
      </div>

      <!-- TAB 3: HUMAN EVOLUTION -->
      <div id="tab-evolution" class="tab-content hidden grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center gap-2 text-rose-400 font-bold uppercase text-[11px]">
            <i data-lucide="skull" class="w-4 h-4"></i> The Hathnora Hominin Calvarium
          </div>
          <h3 class="text-white font-bold text-sm">Arun Sonakia Discovery (Dec 5, 1982)</h3>
          <p class="text-gray-400 leading-relaxed">
            Discovered at Hathnora on the northern bank of the Narmada River (Sehore district, MP). Stratigraphically embedded in a cemented boulder conglomerate (Surajkund Formation). Classified as an archaic *Homo sapiens* or advanced *Homo erectus* female.
          </p>
          <div class="bg-gray-900 p-2.5 rounded-lg border border-gray-800 text-[11px] space-y-1 text-gray-300">
            <div><strong>Cranial Capacity:</strong> 1,155 – 1,421 cc (robust encephalization)</div>
            <div><strong>Morphology:</strong> Continuous prominent supraorbital torus, thick cranial vault</div>
            <div><strong>Associated Finds:</strong> Acheulian bifaces, fossil *Bos namadicus*, *Equus*</div>
          </div>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center gap-2 text-amber-400 font-bold uppercase text-[11px]">
            <i data-lucide="bone" class="w-4 h-4"></i> Post-Cranial Clavicle & Anatomy
          </div>
          <h3 class="text-white font-bold text-sm">A.A. Sankhyan Discovery (1997)</h3>
          <p class="text-gray-400 leading-relaxed">
            Discovery of a complete right human clavicle at Hathnora. Morphometric analysis suggests a diminutive female individual (~130–140 cm in stature), indicating anatomical polymorphism in Middle Pleistocene Indian hominins.
          </p>
          <div class="bg-gray-900 p-2.5 rounded-lg border border-gray-800 text-[11px] space-y-1 text-gray-300">
            <div><strong>Skeletal Evidence:</strong> Human clavicle and second rib fragment</div>
            <div><strong>Chronology:</strong> Middle to early Late Pleistocene (~250–150 ka)</div>
            <div><strong>Palaeopathology:</strong> No severe nutritional trauma recorded</div>
          </div>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center gap-2 text-emerald-400 font-bold uppercase text-[11px]">
            <i data-lucide="activity" class="w-4 h-4"></i> Modern Human Dispersal & Burials
          </div>
          <h3 class="text-white font-bold text-sm">Homo sapiens sapiens Dispersal</h3>
          <p class="text-gray-400 leading-relaxed">
            Behavioral and physical evidence of anatomically modern humans:
          </p>
          <ul class="space-y-1.5 text-gray-300 text-[11px]">
            <li>• <strong>Jwalapuram (AP):</strong> Lithic tool continuity across the 74 ka Toba ash event.</li>
            <li>• <strong>Kurnool Caves (AP):</strong> Upper Palaeolithic bone implements and awls.</li>
            <li>• <strong>Ganga Valley Burials:</strong> Sarai-Nahar Rai, Mahadaha, Damdama: complete Mesolithic skeletons, extended burials, bone ornaments, tall stature (~180 cm).</li>
            <li>• <strong>Symbolic Expression:</strong> Engraved ostrich eggshells at Patne & Mehtakheri (25–40 ka).</li>
          </ul>
        </div>
      </div>

      <!-- TAB 4: PALAEOENVIRONMENT (FLORA & FAUNA) -->
      <div id="tab-palaeoenv" class="tab-content hidden grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center gap-2 text-amber-400 font-bold uppercase text-[11px]">
            <i data-lucide="binary" class="w-4 h-4"></i> Pleistocene Mammalian Megafauna
          </div>
          <h3 class="text-white font-bold text-sm">Extinct Archaic Fauna of Central & Peninsular India</h3>
          <p class="text-gray-400 leading-relaxed">
            Rich mammalian fossil beds in the Godavari, Narmada, Krishna, and Manjra alluvial valleys reveal heavy savannah and perennial riparian ecosystems:
          </p>
          <div class="space-y-1 text-gray-300 text-[11px]">
            <div>• <strong>Bos namadicus:</strong> Extinct giant wild ox with 1.5 m horn cores.</div>
            <div>• <strong>Elephas namadicus & E. hysudricus:</strong> Straight-tusked archaic elephants.</div>
            <div>• <strong>Hexaprotodon palaeindicus:</strong> Six-incisor river hippopotamus.</div>
            <div>• <strong>Stegodon namadicus:</strong> Archaic proboscidean with ridge-crested molars.</div>
            <div>• <strong>Equus namadicus:</strong> Large Pleistocene wild horse.</div>
          </div>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center gap-2 text-emerald-400 font-bold uppercase text-[11px]">
            <i data-lucide="paw-print" class="w-4 h-4"></i> Holocene Ecological Shift
          </div>
          <h3 class="text-white font-bold text-sm">Post-Glacial Faunal Turnover</h3>
          <p class="text-gray-400 leading-relaxed">
            Extinction of swamp-loving *Hexaprotodon* and *Stegodon* at the Pleistocene-Holocene boundary, replaced by agile open-woodland and grassland species:
          </p>
          <div class="space-y-1 text-gray-300 text-[11px]">
            <div>• <strong>Bos gaurus (Indian Gaur):</strong> Maintained in central highlands.</div>
            <div>• <strong>Antilope cervicapra (Blackbuck) & Gazella bennettii:</strong> Thar & Deccan.</div>
            <div>• <strong>Axis axis (Chital) & Rucervus duvaucelii:</strong> Ganga lake margins.</div>
            <div>• <strong>Sus scrofa (Wild Boar):</strong> Universal prey species in Mesolithic middens.</div>
            <div>• <strong>Domesticates:</strong> Cattle, sheep, goat emerging in Neolithic (Mehrgarh).</div>
          </div>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-2">
          <div class="flex items-center gap-2 text-cyan-400 font-bold uppercase text-[11px]">
            <i data-lucide="sprout" class="w-4 h-4"></i> Prehistoric Flora & Plant Domestication
          </div>
          <h3 class="text-white font-bold text-sm">Pollen Profiles & Early Cultivation</h3>
          <p class="text-gray-400 leading-relaxed">
            Macrobotanical, phytolith, and palynological studies reveal ancient vegetation and transitions to farming:
          </p>
          <div class="space-y-1.5 text-gray-300 text-[11px]">
            <div>• <strong>Rice (Oryza sativa & O. nivara):</strong> Belan Valley (Chopani-Mando, Koldihwa, Lahuradewa) reveals early exploitation and 7th–6th millennium BCE cultivated grains.</div>
            <div>• <strong>Barley (Hordeum vulgare) & Wheat:</strong> Mehrgarh (Baluchistan) and Burzahom (Kashmir) show early winter-crop agricultural packages.</div>
            <div>• <strong>Palynology:</strong> Didwana and Sambhar lake cores document heightened monsoon rainfall and freshwater vegetation 9000–5000 BP.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- FILTER CONTROL BAR -->
    <div class="bg-gray-900/90 border border-gray-800 p-4 rounded-2xl shadow-xl space-y-3">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-3 items-center">
        <div class="lg:col-span-5 relative">
          <i data-lucide="search" class="w-4 h-4 text-gray-500 absolute left-3.5 top-3"></i>
          <input type="text" id="search-input" placeholder="Search site, river valley, state, tool type, excavator..." 
            class="w-full bg-gray-800 border border-gray-700 text-xs rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition">
        </div>

        <div class="lg:col-span-3">
          <select id="period-filter" onchange="applyFilters()" 
            class="w-full bg-gray-800 border border-gray-700 text-xs rounded-xl px-3 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition">
            <option value="ALL">All Archaeological Periods (104 Sites)</option>
            <option value="Lower Paleolithic">Lower Palaeolithic (27 Sites)</option>
            <option value="Middle Paleolithic">Middle Palaeolithic (12 Sites)</option>
            <option value="Upper Paleolithic">Upper Palaeolithic (12 Sites)</option>
            <option value="Mesolithic">Mesolithic (18 Sites)</option>
            <option value="Neolithic">Neolithic (35 Sites)</option>
          </select>
        </div>

        <div class="lg:col-span-2">
          <select id="zone-filter" onchange="applyFilters()" 
            class="w-full bg-gray-800 border border-gray-700 text-xs rounded-xl px-3 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition">
            <option value="ALL">All Geographical Zones</option>
            <option value="The Himalayan">The Himalayan Context</option>
            <option value="Western India">Western India (Rajasthan / Gujarat)</option>
            <option value="Central India">Central India (Narmada-Son)</option>
            <option value="Peninsular India">Peninsular India (Deccan)</option>
            <option value="Eastern India">Eastern India (Plateau)</option>
            <option value="Ganga Valley">Ganga Valley & Vindhyas</option>
          </select>
        </div>

        <div class="lg:col-span-2">
          <select id="adapt-filter" onchange="applyFilters()" 
            class="w-full bg-gray-800 border border-gray-700 text-xs rounded-xl px-3 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition">
            <option value="ALL">All Landscape Adaptations</option>
            <option value="Alluvial plain adaptation">Alluvial Plain Adaptation</option>
            <option value="Horse-shoe lake sites">Horse-shoe Lake (Oxbow) Sites</option>
            <option value="Sand dune landscape">Sand Dune Landscape</option>
            <option value="Plateau occupation">Plateau Occupation</option>
            <option value="Cave & Rock Shelter">Cave & Rock Shelter Occupation</option>
            <option value="Ashmound">Ashmound Settlement</option>
          </select>
        </div>
      </div>

      <div class="pt-2 border-t border-gray-800 flex items-center justify-between flex-wrap gap-3 text-xs">
        <div class="flex items-center gap-4">
          <label class="flex items-center gap-2 cursor-pointer text-gray-300 hover:text-white">
            <input type="checkbox" id="rock-art-only" onchange="applyFilters()" class="rounded bg-gray-800 border-gray-700 text-amber-500 focus:ring-0">
            <span class="flex items-center gap-1.5"><i data-lucide="image" class="w-3.5 h-3.5 text-amber-400"></i> Prehistoric Rock Art Localities (12 Sites)</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer text-gray-300 hover:text-white">
            <input type="checkbox" id="fauna-only" onchange="applyFilters()" class="rounded bg-gray-800 border-gray-700 text-emerald-500 focus:ring-0">
            <span class="flex items-center gap-1.5"><i data-lucide="bone" class="w-3.5 h-3.5 text-emerald-400"></i> Fossil Megafauna & Flora Preserved</span>
          </label>
        </div>
        <div class="text-xs text-gray-400">
          Showing <span id="filtered-count" class="font-bold text-white font-display">104</span> of <span id="total-count" class="font-bold text-gray-400">104</span> sites
        </div>
      </div>
    </div>

    <!-- MAP & REGIONAL DISTRIBUTION SECTION -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
      
      <!-- Interactive GIS Leaflet Map (8 Cols) - ESRI DEFAULT -->
      <div class="lg:col-span-7 xl:col-span-8 bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl flex flex-col justify-between">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <i data-lucide="map-pin" class="w-4 h-4 text-rose-500"></i>
            <h2 class="font-bold font-display text-white text-sm">Spatial GIS Map (EPSG:4326 WGS84)</h2>
          </div>
          <div class="flex items-center gap-2 text-[10px] text-gray-400 flex-wrap">
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Lower P.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Middle P.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span> Upper P.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Meso.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-cyan-500"></span> Neo.</span>
          </div>
        </div>

        <div id="map" class="w-full flex-1"></div>
        <div class="text-[11px] text-gray-400 mt-2 flex items-center justify-between">
          <span>Click any marker to inspect site data & original tool plate. Switch layers using the top-right control.</span>
          <span class="text-amber-400 font-medium">Esri Topographic &amp; Satellite Basemap Layers</span>
        </div>
      </div>

      <!-- Regional Distribution Breakdown Chart (4 Cols) - FULL HEIGHT -->
      <div class="lg:col-span-5 xl:col-span-4 bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl flex flex-col">
        <div class="flex items-center justify-between mb-3 border-b border-gray-800 pb-2">
          <h3 class="text-xs font-bold uppercase tracking-wider text-gray-300 flex items-center gap-1.5">
            <i data-lucide="bar-chart-2" class="w-3.5 h-3.5 text-cyan-400"></i> Regional Geographical Distribution
          </h3>
          <span class="text-xs text-gray-500">104 Sites</span>
        </div>
        <p class="text-xs text-gray-400 mb-2">Prehistoric site concentration across major physiographic zones of the Subcontinent.</p>
        <div class="relative flex-1 min-h-[460px]">
          <canvas id="zoneChart"></canvas>
        </div>
      </div>

    </div>

    <!-- MASTER SITES TABLE -->
    <div class="bg-gray-900/90 border border-gray-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <h2 class="font-bold font-display text-white text-base">Master Prehistoric Site Registry</h2>
          <p class="text-xs text-gray-400">All 104 surveyed, explored, and excavated prehistoric sites across the Indian Subcontinent.</p>
        </div>
        
        <div class="flex items-center gap-2 text-xs">
          <span class="text-gray-400">Rows per page:</span>
          <select id="pageSizeSelect" onchange="changePageSize(this.value)" class="bg-gray-800 border border-gray-700 text-xs rounded-lg px-2.5 py-1 text-white focus:outline-none">
            <option value="15">15</option>
            <option value="30">30</option>
            <option value="50">50</option>
            <option value="104" selected>All 104 Sites</option>
          </select>
        </div>
      </div>

      <div class="overflow-x-auto rounded-xl border border-gray-800 max-h-[550px] overflow-y-auto">
        <table class="w-full text-left text-xs text-gray-300">
          <thead class="bg-gray-950 text-gray-400 uppercase tracking-wider sticky top-0 z-10 border-b border-gray-800 text-[10px]">
            <tr>
              <th class="px-3 py-3 font-semibold">Site Name</th>
              <th class="px-3 py-3 font-semibold">Period</th>
              <th class="px-3 py-3 font-semibold">State / Region</th>
              <th class="px-3 py-3 font-semibold">River Valley</th>
              <th class="px-3 py-3 font-semibold">Excavator(s)</th>
              <th class="px-3 py-3 font-semibold">Year</th>
              <th class="px-3 py-3 font-semibold">Diagnostic Typology</th>
              <th class="px-3 py-3 font-semibold">Coordinates</th>
              <th class="px-3 py-3 font-semibold text-center">Action</th>
            </tr>
          </thead>
          <tbody id="sites-table-body" class="divide-y divide-gray-800/80 bg-gray-900/40">
          </tbody>
        </table>
      </div>

      <div class="flex items-center justify-between text-xs text-gray-400 pt-2">
        <div id="table-info">Showing all 104 sites</div>
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
        Source Data: IAR, Ancient India, MASI &amp; University Excavations
      </div>
    </div>
  </footer>

  <!-- HIGH-RESOLUTION LIGHTBOX MODAL (FOR ENLARGING IMAGES) -->
  <div id="image-lightbox-modal" class="fixed inset-0 bg-black/90 backdrop-blur-md z-[100] hidden flex items-center justify-center p-4">
    <div class="relative max-w-4xl w-full bg-gray-950 border border-gray-800 rounded-2xl shadow-2xl flex flex-col max-h-[92vh] overflow-hidden animate-in fade-in zoom-in-95 duration-200">
      <!-- Header -->
      <div class="p-4 border-b border-gray-800 flex items-center justify-between bg-gray-900/70">
        <div class="flex items-center gap-2.5">
          <span id="lightbox-period-badge" class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30"></span>
          <h3 id="lightbox-title" class="text-base font-bold font-display text-white"></h3>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="prevLightboxImage()" class="px-2.5 py-1 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white transition text-xs flex items-center gap-1">
            <i data-lucide="chevron-left" class="w-4 h-4"></i> Prev
          </button>
          <button onclick="nextLightboxImage()" class="px-2.5 py-1 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white transition text-xs flex items-center gap-1">
            Next <i data-lucide="chevron-right" class="w-4 h-4"></i>
          </button>
          <button onclick="closeImageLightbox()" class="p-1.5 rounded-lg bg-gray-800 hover:bg-rose-900/60 text-gray-400 hover:text-rose-300 transition ml-2">
            <i data-lucide="x" class="w-5 h-5"></i>
          </button>
        </div>
      </div>

      <!-- Main Image View -->
      <div class="flex-1 bg-black/80 flex items-center justify-center p-4 min-h-[300px] max-h-[60vh] overflow-hidden relative">
        <img id="lightbox-img" src="" alt="Enlarged archaeological specimen" class="max-h-[56vh] max-w-full w-auto object-contain rounded-lg shadow-2xl border border-gray-800">
        <div class="absolute bottom-2 right-4 bg-black/70 px-2 py-0.5 rounded text-[10px] text-gray-400 font-mono">
          Press Esc to close • Left/Right arrows to browse
        </div>
      </div>

      <!-- Caption / Archaeological Details -->
      <div class="p-4 border-t border-gray-800 bg-gray-900/90 text-xs space-y-2">
        <p id="lightbox-caption" class="text-gray-300 leading-relaxed text-[11px]"></p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] pt-1.5 border-t border-gray-800/80">
          <div><strong class="text-gray-400">Manufacturing Technology:</strong> <span id="lightbox-tech" class="text-gray-200"></span></div>
          <div><strong class="text-gray-400">Key Subcontinent Localities:</strong> <span id="lightbox-sites" class="text-amber-300"></span></div>
        </div>
      </div>
    </div>
  </div>

  <!-- SITE DOSSIER MODAL DIALOG (WITH ORIGINAL TOOL PHOTOGRAPH) -->
  <div id="site-modal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-gray-900 border border-gray-800 w-full max-w-3xl max-h-[92vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
      
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

      <!-- Modal Body (Scrollable) -->
      <div class="p-6 overflow-y-auto space-y-5 text-xs">
        
        <!-- EMBEDDED ORIGINAL TOOL IMAGE & VISUAL FINDS (WITH ENLARGE OPTION) -->
        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 flex flex-col md:flex-row items-center gap-4">
          <div id="modal-tool-plate-wrap" onclick="enlargeModalImage()" class="w-36 h-36 flex-shrink-0 bg-gray-900 rounded-lg border border-gray-800 overflow-hidden flex items-center justify-center p-1 shadow-inner relative group cursor-pointer" title="Click to enlarge image">
            <img id="modal-tool-img" src="images/handaxe.jpg" alt="Archaeological specimen" class="w-full h-full object-cover rounded group-hover:scale-105 transition duration-300">
            <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1 text-[10px] font-semibold text-white">
              <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-amber-400"></i> Click to Enlarge
            </div>
          </div>
          <div class="space-y-1.5 flex-1">
            <div class="flex items-center justify-between">
              <div class="text-[10px] uppercase font-bold text-amber-400 tracking-wider flex items-center gap-1.5">
                <i data-lucide="image" class="w-3.5 h-3.5"></i> Diagnostic Archaeological Visual Plate
              </div>
              <button onclick="enlargeModalImage()" class="text-[11px] text-amber-400 hover:text-amber-300 underline font-medium flex items-center gap-1">
                <i data-lucide="zoom-in" class="w-3 h-3"></i> Enlarge Photo
              </button>
            </div>
            <h4 id="modal-tool-plate-title" class="text-sm font-bold text-white">Acheulian Bifacial Lithic Assemblage</h4>
            <p id="modal-tool-plate-caption" class="text-gray-400 text-[11px] leading-relaxed">
              Diagnostic biface specimen demonstrating primary flaking scars, longitudinal profile, and working margins typical of this locality.
            </p>
            <div class="pt-1 flex items-center gap-3 text-[11px]">
              <span class="text-cyan-400 font-mono" id="modal-plate-metrics">Size Bounds: L: 140-185mm | W: 85-110mm</span>
            </div>
          </div>
        </div>

        <!-- Locality & Administration -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="bg-gray-800/40 p-2.5 rounded-xl border border-gray-800">
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">State / Region</span>
            <span id="modal-state" class="text-white text-xs font-semibold truncate block"></span>
          </div>
          <div class="bg-gray-800/40 p-2.5 rounded-xl border border-gray-800">
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">District</span>
            <span id="modal-district" class="text-white text-xs font-semibold truncate block"></span>
          </div>
          <div class="bg-gray-800/40 p-2.5 rounded-xl border border-gray-800">
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">River Basin</span>
            <span id="modal-river" class="text-white text-xs font-semibold truncate block"></span>
          </div>
          <div class="bg-gray-800/40 p-2.5 rounded-xl border border-gray-800">
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">Coordinates</span>
            <span id="modal-coords" class="text-amber-400 text-xs font-mono font-semibold truncate block"></span>
          </div>
        </div>

        <!-- Excavators & Year -->
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-gray-800/40 p-2.5 rounded-xl border border-gray-800">
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">Discovery Year / Work</span>
            <span id="modal-year" class="text-white text-xs font-semibold truncate block"></span>
          </div>
          <div class="bg-gray-800/40 p-2.5 rounded-xl border border-gray-800">
            <span class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold block">Excavator(s) / Investigators</span>
            <span id="modal-excavator" class="text-white text-xs font-semibold truncate block"></span>
          </div>
        </div>

        <!-- Typology & Metrics -->
        <div class="space-y-2">
          <h4 class="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
            <i data-lucide="hammer" class="w-3.5 h-3.5"></i> Lithic Typology & Manufacturing Technique
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
            <i data-lucide="trees" class="w-3.5 h-3.5"></i> Landscape & Ecological Adaptation
          </h4>
          <div class="bg-gray-800/40 p-3.5 rounded-xl border border-gray-800 space-y-2">
            <p><strong class="text-gray-200">Environmental Adaptation:</strong> <span id="modal-adaptation" class="text-emerald-300 font-semibold"></span></p>
            <p><strong class="text-gray-200">Associated Features:</strong> <span id="modal-features"></span></p>
            <p><strong class="text-gray-200">Palaeofauna / Palaeoflora:</strong> <span id="modal-fauna" class="text-gray-300"></span></p>
            <p><strong class="text-gray-200">Prehistoric Rock Art Details:</strong> <span id="modal-rock-art" class="text-amber-300"></span></p>
          </div>
        </div>

        <!-- References & Archive -->
        <div class="space-y-2">
          <h4 class="text-xs font-bold uppercase tracking-wider text-purple-400 flex items-center gap-1.5">
            <i data-lucide="book-open" class="w-3.5 h-3.5"></i> Archival References & Publications
          </h4>
          <div class="bg-gray-800/40 p-3.5 rounded-xl border border-gray-800 text-[11px] leading-relaxed text-gray-300 space-y-2">
            <p id="modal-references"></p>
            <div id="modal-link-wrap" class="pt-2 flex flex-wrap items-center gap-3">
              <a href="https://archive.org/search?query=%22Indian+Archaeology%22+%22A+Review%22" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 text-amber-400 hover:text-amber-300 underline font-medium">
                <i data-lucide="library" class="w-3.5 h-3.5"></i> Search IAR Volumes on Internet Archive (200 OK)
              </a>
              <span class="text-gray-600">•</span>
              <a href="https://archive.org/search?query=%22Ancient+India%22+bulletin+archaeological+survey" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 text-sky-400 hover:text-sky-300 underline font-medium">
                <i data-lucide="book" class="w-3.5 h-3.5"></i> Ancient India Bulletin Archive
              </a>
              <span class="text-gray-600">•</span>
              <a href="https://asi.nic.in/" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 text-emerald-400 hover:text-emerald-300 underline font-medium">
                <i data-lucide="external-link" class="w-3.5 h-3.5"></i> Archaeological Survey of India (ASI) Portal
              </a>
            </div>
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-4 border-t border-gray-800 bg-gray-950/80 flex items-center justify-between">
        <button id="modal-fly-btn" class="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-600 text-black font-semibold text-xs flex items-center gap-1.5 transition">
          <i data-lucide="navigation" class="w-3.5 h-3.5"></i> Center on Map
        </button>
        <button onclick="closeModal()" class="px-4 py-2 rounded-xl bg-gray-800 hover:bg-gray-700 text-gray-300 font-medium text-xs transition">
          Close Dossier
        </button>
      </div>

    </div>
  </div>

  <!-- SITES DATASET EMBED -->
  <script>
    const SITES_DATA = {sites_json_str};
  </script>

  <!-- APPLICATION LOGIC -->
  <script>
    let map, markersLayer;
    let filteredSites = [...SITES_DATA];
    let currentPage = 1;
    let pageSize = 104;

    const PERIOD_CONFIG = {{
      'Lower Paleolithic': {{ color: '#f43f5e', badge: 'bg-rose-500/20 text-rose-300 border-rose-500/30' }},
      'Middle Paleolithic': {{ color: '#f59e0b', badge: 'bg-amber-500/20 text-amber-300 border-amber-500/30' }},
      'Upper Paleolithic': {{ color: '#a855f7', badge: 'bg-purple-500/20 text-purple-300 border-purple-500/30' }},
      'Mesolithic': {{ color: '#10b981', badge: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' }},
      'Neolithic': {{ color: '#06b6d4', badge: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30' }}
    }};

    const TOOL_CATALOG = {{
      handaxe: {{
        title: "Acheulian Bifacial Handaxe (Biface)",
        period: "Lower Palaeolithic (1.5 Ma – 120 ka)",
        desc: "Bifacially flaked core/large-flake implement with pointed or amygdaloid apex, sharp bilateral cutting edges, and rounded butt. Manufactured initially by block-on-block/hard hammer followed by soft hammer (billet) step retouch.",
        tech: "Direct stone hammer percussion, soft antler/wood cylinder hammer thinning, invasive flaking creating lenticular cross-section.",
        sites: "Attirampakkam (TN), Isampur (KA), Bhimbetka (MP), Didwana (RJ), Hunsgi (KA), Chirki-Nevasa (MH), Kuliana (OD)."
      }},
      cleaver: {{
        title: "Acheulian Cleaver (Transverse Bit)",
        period: "Lower Palaeolithic (1.2 Ma – 120 ka)",
        desc: "Heavy-duty bifacial tool characterized by a broad, razor-sharp transverse cutting bit formed by the intersection of two large flake scars or tranchet blow. Parallelogram or trapezoidal cross-section.",
        tech: "Prepared block-on-block quarrying, Kombewa/side-struck large flake blank extraction, followed by controlled bilateral shaping.",
        sites: "Isampur (KA), Chirki-Nevasa (MH), Bhimbetka (MP), Attirampakkam (TN), Hunsgi (KA), Morgaon (MH)."
      }},
      chopper: {{
        title: "Soanian / Early Pebble Chopper",
        period: "Lower Palaeolithic (Pebble-Core Tradition)",
        desc: "Massive unifacially flaked river cobble tool with natural smooth pebble cortex preserved over the butt to provide a comfortable grip, and a jagged, undulating cutting edge.",
        tech: "Direct block-on-block or heavy stone hammer percussion removing 3-6 large flakes along one margin.",
        sites: "Soan Valley (Potwar), Guler (Beas Terraces T1-T5), Nalagarh (Sirsa Valley), Riwat."
      }},
      levallois: {{
        title: "Levallois Prepared Core & Points",
        period: "Middle Palaeolithic (385 ka – 40 ka)",
        desc: "Standardized flake, point, or blade tool detached from a deliberately pre-shaped 'tortoise' core. Radial centripetal flake removals establish precise surface convexities and a faceted striking platform.",
        tech: "Careful volumetric core shaping (Levallois technique), followed by a single decisive strike detaching a predetermined flake/point.",
        sites: "Nevasa (MH), Samnapur (MP), Attirampakkam MP phase (TN), Didwana 16R (RJ), Kalpi (UP), Jetpur (GJ)."
      }},
      blade: {{
        title: "Prismatic Blades & Angle Burins",
        period: "Upper Palaeolithic (45 ka – 10 ka)",
        desc: "Elongated, parallel-sided blades with length at least twice the width and parallel dorsal ridges. Includes specialized burins with chisel-like working edges for working bone, antler, and shell.",
        tech: "Punch-blade indirect percussion on prepared cylindrical or conical cores, soft organic punch, and pressure backing.",
        sites: "Renigunta (AP), Baghor I (MP), Jwalapuram (AP), Patne (MH), Mehtakheri (MP), Kurnool Caves (AP)."
      }},
      microlith: {{
        title: "Geometric Microliths & Composite Sickles",
        period: "Mesolithic (12 ka – 2500 BCE)",
        desc: "Minute, standardized geometric tools (lunates, trapezes, triangles) with steep blunting retouch along one or more margins. Hafted in grooved bone, antler, or wood handles with resin/mastic to form composite harpoons, sickles, and arrowheads.",
        tech: "Micro-burin technique, pressure flaking on micro-blade cores using chalcedony, chert, and agate.",
        sites: "Bagor (RJ), Sarai-Nahar Rai (UP), Mahadaha (UP), Damdama (UP), Langhnaj (GJ), Birbhanpur (WB), Chopani-Mando (UP)."
      }},
      celt: {{
        title: "Ground & Polished Stone Celts",
        period: "Neolithic (7000 BCE – 1000 BCE)",
        desc: "Heavy-duty celts, axes, and adzes ground and hone-polished over fine-grained igneous basalt or dolerite. Feature sharp symmetrical or asymmetrical convex bits used for forest clearance, carpentry, and cultivation.",
        tech: "Rough flaking, extensive battering/pecking to shape, followed by intensive wet grinding and hone polishing on bedrock grooving boulders.",
        sites: "Burzahom (JK), Gufkral (JK), Sangankallu (KA), Brahmagiri (KA), Paiyampalli (TN), Kuchai (OD), Daojali Hading (AS)."
      }},
      hathnora: {{
        title: "Hathnora Archaic Hominin Cranial Calvarium (Narmada Man)",
        period: "Middle Pleistocene (~250–300 ka)",
        desc: "Fossil skullcap of an archaic hominin (Homo erectus / archaic Homo sapiens) discovered by Arun Sonakia (1982) in the Surajkund boulder conglomerate of Narmada. Cranial capacity 1155–1421 cc with massive supraorbital torus.",
        tech: "Associated in situ with Late Acheulian handaxes, cleavers, and Pleistocene megafauna (Bos namadicus, Equus).",
        sites: "Hathnora (Narmada Valley, Sehore District, Madhya Pradesh)."
      }},
      bhimbetka: {{
        title: "Prehistoric Rock Art Panel (Bhimbetka)",
        period: "Mesolithic & Upper Palaeolithic",
        desc: "Dynamic red ochre and white mineral wall paintings inside sandstone rockshelters depicting communal hunts, wild animal herds (gaur, boars, deer), stick-figure archers, and ritual dances.",
        tech: "Natural mineral pigments (hematite, manganese oxide) mixed with animal fat/water, applied with bird feather or animal hair brushes.",
        sites: "Bhimbetka (MP), Adamgarh (MP), Pachmarhi (MP), Kupgal (KA), Morhana Pahar (UP)."
      }}
    }};

    const LIGHTBOX_KEYS = ['handaxe', 'cleaver', 'chopper', 'levallois', 'blade', 'microlith', 'celt', 'hathnora', 'bhimbetka'];
    const IMAGE_PATHS = {{
      handaxe: 'images/handaxe.jpg',
      cleaver: 'images/cleaver.png',
      chopper: 'images/chopper.jpg',
      levallois: 'images/levallois.jpg',
      blade: 'images/blade.png',
      microlith: 'images/microlith.jpg',
      celt: 'images/celt.jpg',
      hathnora: 'images/hathnora.jpg',
      bhimbetka: 'images/bhimbetka.jpg'
    }};

    let currentToolKey = 'handaxe';
    let currentLightboxIndex = 0;

    function showToolDetail(key) {{
      currentToolKey = key;
      const d = TOOL_CATALOG[key];
      if (!d) return;
      document.getElementById('toolDetailTitle').innerText = d.title;
      document.getElementById('toolDetailPeriod').innerText = d.period;
      document.getElementById('toolDetailDesc').innerText = d.desc;
      document.getElementById('toolDetailTech').innerText = d.tech;
      document.getElementById('toolDetailSites').innerText = d.sites;
    }}

    function selectAndEnlargeTool(key) {{
      showToolDetail(key);
      openImageLightbox(key);
    }}

    function openImageLightbox(key) {{
      currentToolKey = key || 'handaxe';
      const idx = LIGHTBOX_KEYS.indexOf(currentToolKey);
      if (idx !== -1) currentLightboxIndex = idx;
      updateLightboxContent();
      document.getElementById('image-lightbox-modal').classList.remove('hidden');
    }}

    function closeImageLightbox() {{
      document.getElementById('image-lightbox-modal').classList.add('hidden');
    }}

    function nextLightboxImage() {{
      currentLightboxIndex = (currentLightboxIndex + 1) % LIGHTBOX_KEYS.length;
      currentToolKey = LIGHTBOX_KEYS[currentLightboxIndex];
      updateLightboxContent();
    }}

    function prevLightboxImage() {{
      currentLightboxIndex = (currentLightboxIndex - 1 + LIGHTBOX_KEYS.length) % LIGHTBOX_KEYS.length;
      currentToolKey = LIGHTBOX_KEYS[currentLightboxIndex];
      updateLightboxContent();
    }}

    function updateLightboxContent() {{
      const d = TOOL_CATALOG[currentToolKey];
      if (!d) return;

      document.getElementById('lightbox-img').src = IMAGE_PATHS[currentToolKey] || 'images/handaxe.jpg';
      document.getElementById('lightbox-title').innerText = d.title;
      document.getElementById('lightbox-period-badge').innerText = d.period;
      document.getElementById('lightbox-caption').innerText = d.desc;
      document.getElementById('lightbox-tech').innerText = d.tech;
      document.getElementById('lightbox-sites').innerText = d.sites;

      if (window.lucide) lucide.createIcons();
    }}

    function enlargeModalImage() {{
      const imgSrc = document.getElementById('modal-tool-img').getAttribute('src');
      for (const k of LIGHTBOX_KEYS) {{
        if (imgSrc.includes(k)) {{
          openImageLightbox(k);
          return;
        }}
      }}
      openImageLightbox('handaxe');
    }}

    // Tab Switcher
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active', 'border-amber-500', 'text-amber-400', 'bg-amber-500/10'));
      
      const target = document.getElementById(tabId);
      if (target) target.classList.remove('hidden');

      const btn = document.getElementById(`btn-${{tabId}}`);
      if (btn) btn.classList.add('active', 'border-amber-500', 'text-amber-400', 'bg-amber-500/10');
    }}

    function getToolImagePathForSite(site) {{
      const period = site.period;
      const name = (site.site_name || '').toLowerCase();
      const tools = (site.tool_typology || '').toLowerCase();

      if (name.includes('hathnora')) return 'images/hathnora.jpg';
      if (site.rock_art_details && site.rock_art_details !== 'None recorded' && (name.includes('bhimbetka') || name.includes('adamgarh') || name.includes('pachmarhi'))) {{
        return 'images/bhimbetka.jpg';
      }}

      if (period === 'Lower Paleolithic') {{
        if (tools.includes('cleaver') || name.includes('isampur')) return 'images/cleaver.png';
        if (tools.includes('chopper') || tools.includes('pebble') || name.includes('soan') || name.includes('guler')) return 'images/chopper.jpg';
        return 'images/handaxe.jpg';
      }}
      if (period === 'Middle Paleolithic') return 'images/levallois.jpg';
      if (period === 'Upper Paleolithic') return 'images/blade.png';
      if (period === 'Mesolithic') return 'images/microlith.jpg';
      return 'images/celt.jpg';
    }}

    // Leaflet Map Initialization - ESRI AS DEFAULT (NO 403 ERROR, NO API KEY)
    function initMap() {{
      map = L.map('map', {{
        center: [22.5, 78.5],
        zoom: 5,
        minZoom: 4,
        maxZoom: 18
      }});

      const esriTopoLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
        maxZoom: 18,
        attribution: 'Tiles &copy; Esri &mdash; Topographic Basemap'
      }}).addTo(map);

      const esriStreetLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
        maxZoom: 18,
        attribution: 'Tiles &copy; Esri &mdash; Street Basemap'
      }});

      const esriSatLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
        maxZoom: 18,
        attribution: 'Tiles &copy; Esri &mdash; National Geographic, Esri'
      }});

      const baseMaps = {{
        "Esri Topographic Terrain (Default)": esriTopoLayer,
        "Esri Street Basemap": esriStreetLayer,
        "Esri Satellite Imagery": esriSatLayer
      }};
      L.control.layers(baseMaps, null, {{ position: 'topright' }}).addTo(map);

      markersLayer = L.layerGroup().addTo(map);
      plotMarkers();
    }}

    function plotMarkers() {{
      markersLayer.clearLayers();

      filteredSites.forEach(site => {{
        if (!site.latitude || !site.longitude) return;

        const config = PERIOD_CONFIG[site.period] || {{ color: '#94a3b8' }};
        
        const marker = L.circleMarker([site.latitude, site.longitude], {{
          radius: 6,
          fillColor: config.color,
          color: '#ffffff',
          weight: 1.5,
          opacity: 1,
          fillOpacity: 0.9
        }});

        marker.bindTooltip(`
          <div class="text-xs p-1">
            <div class="font-bold text-white">${{site.site_name}}</div>
            <div class="text-amber-400 font-medium">${{site.period}}</div>
            <div class="text-gray-400 text-[10px]">${{site.district || ''}}, ${{site.state_province}} (${{site.river_basin || ''}})</div>
            <div class="text-gray-300 text-[10px] mt-0.5">${{site.tool_typology || ''}}</div>
          </div>
        `, {{ direction: 'top', offset: [0, -6], className: 'custom-tooltip' }});

        marker.on('click', () => {{
          openSiteModal(site);
        }});

        markersLayer.addLayer(marker);
      }});
    }}

    let zoneChart;

    function initCharts() {{
      const zCtx = document.getElementById('zoneChart').getContext('2d');
      const zCounts = {{}};
      SITES_DATA.forEach(s => {{
        const z = s.geographical_zone || 'Other';
        zCounts[z] = (zCounts[z] || 0) + 1;
      }});

      zoneChart = new Chart(zCtx, {{
        type: 'bar',
        data: {{
          labels: Object.keys(zCounts),
          datasets: [{{
            label: 'Sites Count',
            data: Object.values(zCounts),
            backgroundColor: [
              '#38bdf8', '#818cf8', '#f59e0b', '#10b981', '#f43f5e', '#a855f7', '#06b6d4'
            ],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: function(context) {{
                  return ` ${{context.raw}} Excavated/Surveyed Sites`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#9ca3af', font: {{ size: 10 }} }}, grid: {{ color: '#1f2937' }} }},
            y: {{ ticks: {{ color: '#e5e7eb', font: {{ size: 11, weight: 'bold' }} }}, grid: {{ display: false }} }}
          }}
        }}
      }});
    }}

    function renderTable() {{
      const tbody = document.getElementById('sites-table-body');
      tbody.innerHTML = '';

      const total = filteredSites.length;
      document.getElementById('filtered-count').innerText = total;
      document.getElementById('total-count').innerText = SITES_DATA.length;

      let start = (currentPage - 1) * pageSize;
      let end = start + pageSize;
      if (pageSize >= total) {{
        start = 0;
        end = total;
      }}
      const pageSites = filteredSites.slice(start, end);

      pageSites.forEach(s => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-gray-800/60 transition cursor-pointer';

        const config = PERIOD_CONFIG[s.period] || {{ color: '#9ca3af' }};

        tr.innerHTML = `
          <td class="px-3 py-2.5 font-bold text-white whitespace-nowrap">${{s.site_name}}</td>
          <td class="px-3 py-2.5 whitespace-nowrap">
            <span class="inline-flex items-center gap-1.5 font-semibold" style="color: ${{config.color}}">
              <span class="w-2 h-2 rounded-full" style="background-color: ${{config.color}}"></span>
              ${{s.period}}
            </span>
          </td>
          <td class="px-3 py-2.5 text-gray-300 whitespace-nowrap">${{s.state_province}}</td>
          <td class="px-3 py-2.5 text-gray-400 whitespace-nowrap">${{s.river_basin || '-'}}</td>
          <td class="px-3 py-2.5 text-gray-300 max-w-xs truncate" title="${{s.excavator_discoverer}}">${{s.excavator_discoverer}}</td>
          <td class="px-3 py-2.5 text-gray-400 whitespace-nowrap">${{s.year_of_discovery}}</td>
          <td class="px-3 py-2.5 text-gray-300 max-w-xs truncate" title="${{s.tool_typology}}">${{s.tool_typology || '-'}}</td>
          <td class="px-3 py-2.5 font-mono text-[11px] text-gray-400 whitespace-nowrap">${{s.latitude}}°, ${{s.longitude}}°</td>
          <td class="px-3 py-2.5 text-center whitespace-nowrap">
            <button onclick="openSiteModalById('${{s.site_id}}')" class="px-2.5 py-1 rounded-md bg-gray-800 hover:bg-amber-500 hover:text-black text-gray-200 font-semibold transition text-[11px]">
              Inspect
            </button>
          </td>
        `;

        tr.addEventListener('click', (e) => {{
          if (e.target.tagName !== 'BUTTON') openSiteModal(s);
        }});

        tbody.appendChild(tr);
      }});

      const maxPages = Math.ceil(total / pageSize) || 1;
      document.getElementById('page-num').innerText = currentPage;
      document.getElementById('table-info').innerText = pageSize >= total ? 
        `Showing all ${{total}} archaeological sites` : 
        `Showing ${{start + 1}} to ${{Math.min(end, total)}} of ${{total}} sites (Page ${{currentPage}} of ${{maxPages}})`;
      
      document.getElementById('prev-page').disabled = (currentPage <= 1);
      document.getElementById('next-page').disabled = (currentPage >= maxPages);
    }}

    function changePage(direction) {{
      const maxPages = Math.ceil(filteredSites.length / pageSize) || 1;
      currentPage = Math.min(Math.max(1, currentPage + direction), maxPages);
      renderTable();
    }}

    function changePageSize(val) {{
      pageSize = parseInt(val, 10);
      currentPage = 1;
      renderTable();
    }}

    function updateKPICards() {{
      const counts = {{
        'Total': filteredSites.length,
        'Lower Paleolithic': 0,
        'Middle Paleolithic': 0,
        'Upper Paleolithic': 0,
        'Mesolithic': 0,
        'Neolithic': 0
      }};

      filteredSites.forEach(s => {{
        if (counts[s.period] !== undefined) counts[s.period]++;
      }});

      document.getElementById('stat-total-sites').innerText = counts['Total'];
      document.getElementById('stat-lp-sites').innerText = counts['Lower Paleolithic'];
      document.getElementById('stat-mp-sites').innerText = counts['Middle Paleolithic'];
      document.getElementById('stat-up-sites').innerText = counts['Upper Paleolithic'];
      document.getElementById('stat-meso-sites').innerText = counts['Mesolithic'];
      document.getElementById('stat-neo-sites').innerText = counts['Neolithic'];
    }}

    function applyFilters() {{
      const query = document.getElementById('search-input').value.toLowerCase().trim();
      const period = document.getElementById('period-filter').value;
      const zone = document.getElementById('zone-filter').value;
      const adapt = document.getElementById('adapt-filter').value;
      const rockArtOnly = document.getElementById('rock-art-only').checked;
      const faunaOnly = document.getElementById('fauna-only').checked;

      filteredSites = SITES_DATA.filter(s => {{
        if (period !== 'ALL' && s.period !== period) return false;
        if (zone !== 'ALL' && s.geographical_zone !== zone) return false;
        if (adapt !== 'ALL' && s.environmental_adaptation !== adapt) return false;
        if (rockArtOnly && (!s.rock_art_details || s.rock_art_details === 'None recorded')) return false;
        if (faunaOnly && (!s.palaeofauna_palaeoflora || s.palaeofauna_palaeoflora === 'None reported' || s.palaeofauna_palaeoflora === 'Not preserved')) return false;

        if (query) {{
          const target = [
            s.site_name, s.alternative_names, s.state_province, s.district, s.river_basin,
            s.excavator_discoverer, s.tool_typology, s.primary_raw_materials, s.manufacturing_technique
          ].filter(Boolean).join(' ').toLowerCase();
          if (!target.includes(query)) return false;
        }}
        return true;
      }});

      currentPage = 1;
      plotMarkers();
      renderTable();
      updateKPICards();
    }}

    function resetFilters() {{
      document.getElementById('search-input').value = '';
      document.getElementById('period-filter').value = 'ALL';
      document.getElementById('zone-filter').value = 'ALL';
      document.getElementById('adapt-filter').value = 'ALL';
      document.getElementById('rock-art-only').checked = false;
      document.getElementById('fauna-only').checked = false;
      applyFilters();
    }}

    document.getElementById('search-input').addEventListener('input', applyFilters);

    function openSiteModalById(siteId) {{
      const site = SITES_DATA.find(s => s.site_id === siteId);
      if (site) openSiteModal(site);
    }}

    function openSiteModal(site) {{
      const config = PERIOD_CONFIG[site.period] || {{ color: '#94a3b8', badge: 'bg-gray-800 text-gray-300' }};

      document.getElementById('modal-site-name').innerText = site.site_name;
      document.getElementById('modal-alt-names').innerText = site.alternative_names ? `Alternate Names: ${{site.alternative_names}}` : '';
      
      const badge = document.getElementById('modal-period-badge');
      badge.innerText = site.period;
      badge.className = `px-2.5 py-0.5 rounded-full text-[11px] font-semibold border ${{config.badge}}`;

      document.getElementById('modal-geo-zone').innerText = `${{site.geographical_zone || ''}} • ${{site.country}}`;
      document.getElementById('modal-state').innerText = site.state_province || '-';
      document.getElementById('modal-district').innerText = site.district || '-';
      document.getElementById('modal-river').innerText = site.river_basin || '-';
      document.getElementById('modal-coords').innerText = `${{site.latitude}}°N, ${{site.longitude}}°E`;

      document.getElementById('modal-year').innerText = `${{site.year_of_discovery || 'Various'}} (${{site.excavation_seasons || 'Explored'}})` ;
      document.getElementById('modal-excavator').innerText = site.excavator_discoverer || '-';

      document.getElementById('modal-typology').innerText = site.tool_typology || 'Assemblage documented';
      document.getElementById('modal-technique').innerText = site.manufacturing_technique || 'Lithic flaking technique';
      document.getElementById('modal-material').innerText = site.primary_raw_materials || 'Quartzite / Siliceous minerals';
      document.getElementById('modal-metrics').innerText = `L: ${{site.length_min_mm}}-${{site.length_max_mm}} mm | W: ${{site.width_min_mm}}-${{site.width_max_mm}} mm | T: ${{site.thickness_min_mm}}-${{site.thickness_max_mm}} mm`;
      document.getElementById('modal-usage').innerText = site.typical_usage || 'Primary subsistence, butchery, woodcraft';

      document.getElementById('modal-adaptation').innerText = site.environmental_adaptation || 'Alluvial floodplain';
      document.getElementById('modal-features').innerText = site.associated_features || 'Primary stratigraphic deposit';
      document.getElementById('modal-fauna').innerText = site.palaeofauna_palaeoflora || 'None reported';
      document.getElementById('modal-rock-art').innerText = site.rock_art_details || 'None recorded';
      document.getElementById('modal-references').innerText = site.key_references || 'Archival report documented in Indian Archaeology - A Review.';

      const imgPath = getToolImagePathForSite(site);
      document.getElementById('modal-tool-img').src = imgPath;
      document.getElementById('modal-tool-plate-title').innerText = `${{site.period}} Diagnostic Industry (${{site.site_name}})`;
      document.getElementById('modal-tool-plate-caption').innerText = `${{site.tool_typology}} — Manufactured via ${{site.manufacturing_technique}}. Raw material: ${{site.primary_raw_materials}}.`;
      document.getElementById('modal-plate-metrics').innerText = `Size Bounds: Length ${{site.length_min_mm}}–${{site.length_max_mm}}mm | Width ${{site.width_min_mm}}–${{site.width_max_mm}}mm`;

      document.getElementById('modal-fly-btn').onclick = () => {{
        closeModal();
        map.flyTo([site.latitude, site.longitude], 10, {{ duration: 1.5 }});
      }};

      document.getElementById('site-modal').classList.remove('hidden');
    }}

    function closeModal() {{
      document.getElementById('site-modal').classList.add('hidden');
    }}

    document.getElementById('site-modal').addEventListener('click', (e) => {{
      if (e.target.id === 'site-modal') closeModal();
    }});

    document.getElementById('image-lightbox-modal').addEventListener('click', (e) => {{
      if (e.target.id === 'image-lightbox-modal') closeImageLightbox();
    }});

    window.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();
      initMap();
      initCharts();
      renderTable();
      updateKPICards();

      window.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape') {{
          closeModal();
          closeImageLightbox();
        }}
        if (!document.getElementById('image-lightbox-modal').classList.contains('hidden')) {{
          if (e.key === 'ArrowRight') nextLightboxImage();
          if (e.key === 'ArrowLeft') prevLightboxImage();
        }}
      }});
    }});
  </script>
</body>
</html>
"""

    out_index = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\index.html"
    with open(out_index, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"Updated index.html at {out_index}")

    # -------------------------------------------------------------
    # 2. GENERATE prehistoric_dashboard.html (In-Artifact)
    # -------------------------------------------------------------
    artifact_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prehistoric Archaeology Dashboard | Indian Subcontinent</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
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
      r: 8.5;
      stroke-width: 2.5;
      filter: drop-shadow(0 0 6px rgba(255,255,255,0.8));
    }}
    .site-dot.selected {{
      r: 10;
      stroke: #ffffff;
      stroke-width: 3;
      filter: drop-shadow(0 0 8px #f59e0b);
    }}
    .tab-btn.active {{
      border-color: #f59e0b;
      color: #f59e0b;
      background-color: rgba(245, 158, 11, 0.1);
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
          <span class="text-xs text-slate-400">Prehistory of the Indian Subcontinent</span>
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

      <div class="flex items-center gap-3 bg-slate-800/80 border border-slate-700 p-2.5 rounded-xl text-xs">
        <div class="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center font-bold text-sm">
          GIS
        </div>
        <div>
          <div class="font-semibold text-slate-200">Full Leaflet GIS Application Ready</div>
          <div class="text-slate-400">Run <code class="bg-slate-900 text-amber-300 px-1 py-0.5 rounded">python launch_dashboard.py</code> for Satellite Maps</div>
        </div>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">

    <!-- KPI STATS CARDS -->
    <section class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-3.5 hover:border-slate-700 transition">
        <div class="text-xs font-medium text-slate-400">Total Sites</div>
        <div class="text-2xl font-black text-white mt-1" id="kpiTotal">104</div>
        <div class="text-[11px] text-slate-500 mt-0.5">Subcontinent Wide</div>
      </div>
      <div class="bg-rose-950/20 border border-rose-900/40 rounded-xl p-3.5 hover:border-rose-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-rose-300">Lower Palaeo</span>
          <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
        </div>
        <div class="text-2xl font-black text-rose-400 mt-1" id="kpiLP">27</div>
        <div class="text-[11px] text-rose-300/60 mt-0.5">Acheulian & Soanian</div>
      </div>
      <div class="bg-amber-950/20 border border-amber-900/40 rounded-xl p-3.5 hover:border-amber-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-amber-300">Middle Palaeo</span>
          <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
        </div>
        <div class="text-2xl font-black text-amber-400 mt-1" id="kpiMP">12</div>
        <div class="text-[11px] text-amber-300/60 mt-0.5">Nevasan & Flake-Core</div>
      </div>
      <div class="bg-purple-950/20 border border-purple-900/40 rounded-xl p-3.5 hover:border-purple-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-purple-300">Upper Palaeo</span>
          <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
        </div>
        <div class="text-2xl font-black text-purple-400 mt-1" id="kpiUP">12</div>
        <div class="text-[11px] text-purple-300/60 mt-0.5">Blade & Burin</div>
      </div>
      <div class="bg-emerald-950/20 border border-emerald-900/40 rounded-xl p-3.5 hover:border-emerald-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-emerald-300">Mesolithic</span>
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
        </div>
        <div class="text-2xl font-black text-emerald-400 mt-1" id="kpiMeso">18</div>
        <div class="text-[11px] text-emerald-300/60 mt-0.5">Microliths & Rock Art</div>
      </div>
      <div class="bg-cyan-950/20 border border-cyan-900/40 rounded-xl p-3.5 hover:border-cyan-700/60 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-cyan-300">Neolithic</span>
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-500"></span>
        </div>
        <div class="text-2xl font-black text-cyan-400 mt-1" id="kpiNeo">35</div>
        <div class="text-[11px] text-cyan-300/60 mt-0.5">Polished Celts & Farming</div>
      </div>
    </section>

    <!-- CORE FOUNDATIONS & LITHIC TOOL GALLERY TABS -->
    <section class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
        <div>
          <h2 class="text-base font-bold text-white flex items-center gap-2">
            <span>Prehistoric Foundations & Palaeoenvironmental Archive</span>
          </h2>
          <p class="text-xs text-slate-400">Essential chronological, environmental, and technological archive.</p>
        </div>
        <div class="flex items-center gap-2 overflow-x-auto w-full sm:w-auto">
          <button onclick="switchTabArtifact('art-tab-typology')" id="btn-art-typology" class="tab-btn active px-3 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition whitespace-nowrap">
            Lithic Tool Gallery
          </button>
          <button onclick="switchTabArtifact('art-tab-geology')" id="btn-art-geology" class="tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition whitespace-nowrap text-slate-400 hover:text-slate-200">
            Geological Time Scale
          </button>
          <button onclick="switchTabArtifact('art-tab-evolution')" id="btn-art-evolution" class="tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition whitespace-nowrap text-slate-400 hover:text-slate-200">
            Human Evolution (Hathnora)
          </button>
          <button onclick="switchTabArtifact('art-tab-palaeoenv')" id="btn-art-palaeoenv" class="tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition whitespace-nowrap text-slate-400 hover:text-slate-200">
            Prehistoric Flora & Fauna
          </button>
        </div>
      </div>

      <!-- Tab 1: Original Tool Images (With Enlarge Option) -->
      <div id="art-tab-typology" class="art-tab-content space-y-3">
        <div class="flex items-center justify-between">
          <p class="text-xs text-slate-400">Click any archaeological specimen to enlarge with high-resolution details and morphometric notes.</p>
          <span class="text-[11px] text-amber-400 font-medium">🔍 Click any specimen to enlarge</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-9 gap-3 text-xs">
          
          <div onclick="openLightboxArtifact('handaxe')" class="bg-slate-950 border border-slate-800 hover:border-amber-500 p-2 rounded-xl text-center cursor-pointer transition group">
            <div class="h-20 rounded bg-slate-900 overflow-hidden mb-1.5 relative flex items-center justify-center">
              <img src="images/handaxe.jpg" alt="Handaxe" class="h-full w-full object-cover group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">Enlarge</div>
            </div>
            <div class="font-bold text-white truncate">Handaxe</div>
            <div class="text-[10px] text-rose-400">Lower Palaeo</div>
          </div>

          <div onclick="openLightboxArtifact('cleaver')" class="bg-slate-950 border border-slate-800 hover:border-amber-500 p-2 rounded-xl text-center cursor-pointer transition group">
            <div class="h-20 rounded bg-slate-900 overflow-hidden mb-1.5 relative flex items-center justify-center p-1">
              <img src="images/cleaver.png" alt="Cleaver" class="h-full w-auto object-contain group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">Enlarge</div>
            </div>
            <div class="font-bold text-white truncate">Cleaver</div>
            <div class="text-[10px] text-rose-400">Lower Palaeo</div>
          </div>

          <div onclick="openLightboxArtifact('chopper')" class="bg-slate-950 border border-slate-800 hover:border-amber-500 p-2 rounded-xl text-center cursor-pointer transition group">
            <div class="h-20 rounded bg-slate-900 overflow-hidden mb-1.5 relative flex items-center justify-center">
              <img src="images/chopper.jpg" alt="Chopper" class="h-full w-full object-cover group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">Enlarge</div>
            </div>
            <div class="font-bold text-white truncate">Chopper</div>
            <div class="text-[10px] text-rose-400">Soanian Core</div>
          </div>

          <div onclick="openLightboxArtifact('levallois')" class="bg-slate-950 border border-slate-800 hover:border-amber-500 p-2 rounded-xl text-center cursor-pointer transition group">
            <div class="h-20 rounded bg-slate-900 overflow-hidden mb-1.5 relative flex items-center justify-center">
              <img src="images/levallois.jpg" alt="Levallois" class="h-full w-full object-cover group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">Enlarge</div>
            </div>
            <div class="font-bold text-white truncate">Levallois</div>
            <div class="text-[10px] text-amber-400">Middle Palaeo</div>
          </div>

          <div onclick="openLightboxArtifact('blade')" class="bg-slate-950 border border-slate-800 hover:border-amber-500 p-2 rounded-xl text-center cursor-pointer transition group">
            <div class="h-20 rounded bg-slate-900 overflow-hidden mb-1.5 relative flex items-center justify-center p-1">
              <img src="images/blade.png" alt="Blade" class="h-full w-auto object-contain group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">Enlarge</div>
            </div>
            <div class="font-bold text-white truncate">Blade & Burin</div>
            <div class="text-[10px] text-purple-400">Upper Palaeo</div>
          </div>

          <div onclick="openLightboxArtifact('microlith')" class="bg-slate-950 border border-slate-800 hover:border-amber-500 p-2 rounded-xl text-center cursor-pointer transition group">
            <div class="h-20 rounded bg-slate-900 overflow-hidden mb-1.5 relative flex items-center justify-center">
              <img src="images/microlith.jpg" alt="Microlith" class="h-full w-full object-cover group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">Enlarge</div>
            </div>
            <div class="font-bold text-white truncate">Microlith</div>
            <div class="text-[10px] text-emerald-400">Mesolithic</div>
          </div>

          <div onclick="openLightboxArtifact('celt')" class="bg-slate-950 border border-slate-800 hover:border-amber-500 p-2 rounded-xl text-center cursor-pointer transition group">
            <div class="h-20 rounded bg-slate-900 overflow-hidden mb-1.5 relative flex items-center justify-center">
              <img src="images/celt.jpg" alt="Celt" class="h-full w-full object-cover group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">Enlarge</div>
            </div>
            <div class="font-bold text-white truncate">Polished Celt</div>
            <div class="text-[10px] text-cyan-400">Neolithic</div>
          </div>

          <div onclick="openLightboxArtifact('hathnora')" class="bg-slate-950 border border-slate-800 hover:border-amber-500 p-2 rounded-xl text-center cursor-pointer transition group">
            <div class="h-20 rounded bg-slate-900 overflow-hidden mb-1.5 relative flex items-center justify-center">
              <img src="images/hathnora.jpg" alt="Hathnora" class="h-full w-full object-cover group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">Enlarge</div>
            </div>
            <div class="font-bold text-white truncate">Narmada Skull</div>
            <div class="text-[10px] text-rose-400">Hathnora Fossil</div>
          </div>

          <div onclick="openLightboxArtifact('bhimbetka')" class="bg-slate-950 border border-slate-800 hover:border-amber-500 p-2 rounded-xl text-center cursor-pointer transition group">
            <div class="h-20 rounded bg-slate-900 overflow-hidden mb-1.5 relative flex items-center justify-center">
              <img src="images/bhimbetka.jpg" alt="Bhimbetka" class="h-full w-full object-cover group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">Enlarge</div>
            </div>
            <div class="font-bold text-white truncate">Rock Art</div>
            <div class="text-[10px] text-amber-400">Bhimbetka Cave</div>
          </div>

        </div>
      </div>

      <!-- Tab 2: Geology -->
      <div id="art-tab-geology" class="art-tab-content hidden grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-rose-400 font-bold uppercase text-[10px]">Early Pleistocene (2.58 – 0.78 Ma)</div>
          <div class="text-white font-bold">Matuyama Reversed Chron</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            Northern Hemisphere glaciation, Siwalik Pinjor turnover. Early Acheulian stone tools emerge in peninsular India (Attirampakkam 1.5 Ma, Isampur 1.2 Ma).
          </p>
        </div>
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-amber-400 font-bold uppercase text-[10px]">Middle Pleistocene (780 – 126 ka)</div>
          <div class="text-white font-bold">Brunhes Normal Chron</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            Acheulian handaxes & cleavers climax. Hathnora hominin calvarium (*Narmada Man*) positioned in the Surajkund Formation (~250–300 ka).
          </p>
        </div>
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-purple-400 font-bold uppercase text-[10px]">Late Pleistocene (126 – 11.7 ka)</div>
          <div class="text-white font-bold">Toba Tephra & Blade-Burin</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            Middle to Upper Palaeolithic transition. Youngest Toba Tuff eruption (74 ka) documented at Jwalapuram with lithic continuity.
          </p>
        </div>
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-emerald-400 font-bold uppercase text-[10px]">Holocene Epoch (11.7 ka – Present)</div>
          <div class="text-white font-bold">Post-Glacial Warm Optimum</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            Southwest monsoon intensification, Mesolithic geometric microliths, rock art, and emergence of Neolithic agriculture.
          </p>
        </div>
      </div>

      <!-- Tab 3: Evolution -->
      <div id="art-tab-evolution" class="art-tab-content hidden grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-rose-400 font-bold uppercase text-[10px]">Hathnora Calvarium (Narmada Man)</div>
          <div class="text-white font-bold">Arun Sonakia Discovery (1982)</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            Found in cemented basal gravels of Surajkund Formation, Narmada River (Sehore district, MP). Cranial capacity ~1,155–1,421 cc. Archaic *Homo sapiens* / advanced *Homo erectus*.
          </p>
        </div>
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-amber-400 font-bold uppercase text-[10px]">Post-Cranial Clavicle</div>
          <div class="text-white font-bold">A.A. Sankhyan Discovery (1997)</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            Right clavicle fragment suggesting a diminutive female individual (~130–140 cm stature), indicating polymorphic Middle Pleistocene hominin populations in India.
          </p>
        </div>
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-emerald-400 font-bold uppercase text-[10px]">Modern Human Dispersal & Burials</div>
          <div class="text-white font-bold">Homo sapiens sapiens Evidence</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            Jwalapuram (Toba ash continuity), Kurnool cave bone tools, Ganga Valley burials (Sarai-Nahar Rai, Mahadaha with complete skeletons), and engraved ostrich eggshell beads (Patne).
          </p>
        </div>
      </div>

      <!-- Tab 4: Palaeoenv -->
      <div id="art-tab-palaeoenv" class="art-tab-content hidden grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-amber-400 font-bold uppercase text-[10px]">Pleistocene Mammalian Megafauna</div>
          <div class="text-white font-bold">Extinct Central & Peninsular Fauna</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            *Bos namadicus* (giant wild cattle), *Elephas namadicus* & *E. hysudricus*, *Hexaprotodon palaeindicus* (six-incisor hippo), *Stegodon namadicus*, and *Equus namadicus*.
          </p>
        </div>
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-emerald-400 font-bold uppercase text-[10px]">Holocene Faunal Turnover</div>
          <div class="text-white font-bold">Savannah & Wetland Wildlife</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            Extinction of *Hexaprotodon* and *Stegodon*; replaced by modern Indian Gaur (*Bos gaurus*), Blackbuck (*Antilope cervicapra*), Chital (*Axis axis*), and Wild Boar (*Sus scrofa*).
          </p>
        </div>
        <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-1.5">
          <div class="text-cyan-400 font-bold uppercase text-[10px]">Prehistoric Flora & Cultivation</div>
          <div class="text-white font-bold">Rice, Barley & Pollen Records</div>
          <p class="text-slate-400 text-[11px] leading-relaxed">
            Early wild & domestic rice (*Oryza sativa*) at Chopani-Mando, Koldihwa, and Lahuradewa. Barley and wheat at Mehrgarh. Lake pollen cores (Didwana, Sambhar) show Holocene monsoon intensification.
          </p>
        </div>
      </div>
    </section>

    <!-- INTERACTIVE CONTROLS BAR -->
    <section class="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-xl space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
        <div class="md:col-span-5 relative">
          <input 
            type="text" 
            id="searchInput" 
            placeholder="Search site, river valley, state, tool typology, excavator..." 
            class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500 transition"
          >
        </div>

        <div class="md:col-span-4">
          <select id="zoneSelect" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
            <option value="ALL">All Geographical Zones</option>
            <option value="The Himalayan">The Himalayan Context (Soan, Beas, Sirsa)</option>
            <option value="Western India">Western India (Didwana, Luni, Thar)</option>
            <option value="Central India">Central India (Narmada-Son Basin)</option>
            <option value="Peninsular India">Peninsular India (Deccan Craton)</option>
            <option value="Eastern India">Eastern India (Chota Nagpur Plateau)</option>
            <option value="Ganga Valley">Ganga Valley & Vindhyas</option>
          </select>
        </div>

        <div class="md:col-span-3">
          <select id="adaptationSelect" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
            <option value="ALL">All Landscape Adaptations</option>
            <option value="Alluvial plain adaptation">Alluvial Plain Adaptation</option>
            <option value="Horse-shoe lake sites">Horse-shoe Lake (Oxbow) Sites</option>
            <option value="Sand dune landscape">Sand Dune Landscape</option>
            <option value="Plateau occupation">Plateau Occupation</option>
            <option value="Cave & Rock Shelter">Cave & Rock Shelter Occupation</option>
            <option value="Ashmound">Ashmound Settlement</option>
          </select>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-2 pt-1 border-t border-slate-800/80">
        <span class="text-xs font-semibold text-slate-400 mr-2">Filter Period:</span>
        <button onclick="setPeriodFilter('ALL')" id="pill-ALL" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-amber-500 text-slate-950 transition">All (104)</button>
        <button onclick="setPeriodFilter('Lower Paleolithic')" id="pill-LP" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-rose-300 hover:bg-slate-700 transition">Lower Palaeo (27)</button>
        <button onclick="setPeriodFilter('Middle Paleolithic')" id="pill-MP" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-amber-300 hover:bg-slate-700 transition">Middle Palaeo (12)</button>
        <button onclick="setPeriodFilter('Upper Paleolithic')" id="pill-UP" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-purple-300 hover:bg-slate-700 transition">Upper Palaeo (12)</button>
        <button onclick="setPeriodFilter('Mesolithic')" id="pill-MESO" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-emerald-300 hover:bg-slate-700 transition">Mesolithic (18)</button>
        <button onclick="setPeriodFilter('Neolithic')" id="pill-NEO" class="period-pill px-3 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-cyan-300 hover:bg-slate-700 transition">Neolithic (35)</button>

        <div class="ml-auto flex items-center gap-2">
          <label class="flex items-center gap-1.5 text-xs text-slate-300 cursor-pointer bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800">
            <input type="checkbox" id="rockArtOnly" class="rounded bg-slate-800 border-slate-700 text-amber-500 focus:ring-0">
            <span>Rock Art Localities</span>
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
            <p class="text-xs text-slate-400">South Asia Projection (66°E–96°E, 8°N–35°N). Click pin to inspect site details.</p>
          </div>
          <div class="flex items-center gap-3 text-[11px]">
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span> Lower P.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span> Mid P.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-purple-500 inline-block"></span> Upper P.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Meso.</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-cyan-500 inline-block"></span> Neo.</span>
          </div>
        </div>

        <div class="relative bg-slate-950 rounded-xl border border-slate-800/80 overflow-hidden flex items-center justify-center p-2">
          <svg id="subcontinentMap" viewBox="0 0 660 700" class="w-full h-auto max-h-[620px] select-none">
            <defs>
              <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.7" stroke-dasharray="2,2"/>
              </pattern>
            </defs>
            <rect width="660" height="700" fill="#0b0f19" />
            <rect width="660" height="700" fill="url(#grid)" />

            <path d="M 120,40 L 260,35 L 360,65 L 430,110 L 530,140 L 610,190 L 620,270 L 570,300 L 520,330 L 480,335 L 485,380 L 460,420 L 415,480 L 350,560 L 330,620 L 310,635 L 290,620 L 275,540 L 260,470 L 220,410 L 195,380 L 160,380 L 140,320 L 120,280 L 105,210 L 95,140 Z" 
                  fill="#111827" stroke="#1e293b" stroke-width="1.5" />
            
            <ellipse cx="360" cy="625" rx="16" ry="24" fill="#111827" stroke="#1e293b" stroke-width="1.5" />

            <!-- Rivers -->
            <path d="M 280,60 Q 210,100 190,160 T 150,260 T 140,330" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.45" stroke-linecap="round"/>
            <text x="145" y="240" fill="#38bdf8" font-size="9" opacity="0.6">Indus</text>
            
            <path d="M 260,140 Q 320,170 380,210 T 500,270 T 560,310" fill="none" stroke="#0369a1" stroke-width="1.8" opacity="0.45" stroke-linecap="round"/>
            <text x="390" y="205" fill="#38bdf8" font-size="9" opacity="0.6">Ganga</text>
            
            <path d="M 440,300 Q 340,310 240,315" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.45" stroke-linecap="round"/>
            <text x="320" y="305" fill="#38bdf8" font-size="9" opacity="0.6">Narmada</text>
            
            <path d="M 250,370 Q 340,385 435,405" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.45" stroke-linecap="round"/>
            <text x="320" y="375" fill="#38bdf8" font-size="9" opacity="0.6">Godavari</text>
            
            <path d="M 260,430 Q 330,445 420,460" fill="none" stroke="#0369a1" stroke-width="1.5" opacity="0.45" stroke-linecap="round"/>
            <text x="330" y="435" fill="#38bdf8" font-size="9" opacity="0.6">Krishna</text>

            <text x="175" y="80" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">HIMALAYAN (SOAN)</text>
            <text x="140" y="200" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">THAR DESERT (DIDWANA)</text>
            <text x="310" y="270" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">VINDHYAS (BHIMBETKA)</text>
            <text x="260" y="480" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">DECCAN (HUNSGI-ISAMPUR)</text>
            <text x="310" y="585" fill="#64748b" font-size="10" font-weight="bold" opacity="0.6">KORTALLAYAR (ATTIRAMPAKKAM)</text>

            <g id="siteMarkersLayer"></g>
          </svg>

          <div id="mapTooltip" class="absolute pointer-events-none hidden bg-slate-900/95 border border-slate-700 text-xs rounded-lg px-3 py-2 shadow-2xl z-20 max-w-xs backdrop-blur"></div>
        </div>

        <div class="mt-3 flex items-center justify-between text-xs text-slate-400">
          <span>Click any pin to inspect complete stratigraphy, tools & dates.</span>
          <button onclick="resetFiltersArtifact()" class="text-amber-400 hover:text-amber-300 font-medium">Reset All Filters</button>
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

        <div id="dossierContent" class="space-y-4 text-xs overflow-y-auto max-h-[580px] pr-2">
          <div class="text-center py-16 space-y-3">
            <div class="w-16 h-16 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center mx-auto text-2xl text-amber-400">
              ⛏️
            </div>
            <h3 class="text-base font-bold text-slate-200">Select an Archaeological Site</h3>
            <p class="text-slate-400 max-w-xs mx-auto text-xs leading-relaxed">
              Click on any marker on the South Asian map or select a site from the table below to inspect its photographic lithic plates, stratigraphy, and chronology.
            </p>
          </div>
        </div>
      </div>

    </div>

    <!-- MASTER DATA REGISTRY TABLE -->
    <section class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <h3 class="text-base font-bold text-white">Master Archaeological Registry</h3>
          <p class="text-xs text-slate-400">Complete searchable and sortable inventory of all 104 sites across the Subcontinent.</p>
        </div>
        <div class="text-xs text-slate-400">
          Showing <span id="tableSummary" class="text-white font-bold">104 of 104 archaeological sites</span>
        </div>
      </div>

      <div class="overflow-x-auto rounded-xl border border-slate-800 max-h-[500px] overflow-y-auto">
        <table class="w-full text-left text-xs text-slate-300">
          <thead class="bg-slate-950 text-slate-400 uppercase tracking-wider sticky top-0 z-10 border-b border-slate-800 text-[11px]">
            <tr>
              <th class="px-3 py-3 font-semibold">Site Name</th>
              <th class="px-3 py-3 font-semibold">Period</th>
              <th class="px-3 py-3 font-semibold">State / Region</th>
              <th class="px-3 py-3 font-semibold">River Valley</th>
              <th class="px-3 py-3 font-semibold">Excavator(s)</th>
              <th class="px-3 py-3 font-semibold">Year</th>
              <th class="px-3 py-3 font-semibold">Coordinates</th>
              <th class="px-3 py-3 font-semibold text-center">Action</th>
            </tr>
          </thead>
          <tbody id="sitesTableBody" class="divide-y divide-slate-800/80 bg-slate-900/40">
          </tbody>
        </table>
      </div>
    </section>

  </main>

  <!-- LIGHTBOX MODAL FOR IN-ARTIFACT DASHBOARD -->
  <div id="art-lightbox-modal" class="fixed inset-0 bg-black/90 backdrop-blur-md z-[100] hidden flex items-center justify-center p-4">
    <div class="relative max-w-3xl w-full bg-slate-950 border border-slate-800 rounded-2xl shadow-2xl flex flex-col max-h-[90vh] overflow-hidden">
      <div class="p-3.5 border-b border-slate-800 flex items-center justify-between bg-slate-900/60">
        <div>
          <span id="art-lightbox-badge" class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-500/20 text-rose-300"></span>
          <h3 id="art-lightbox-title" class="text-sm font-bold text-white mt-1"></h3>
        </div>
        <button onclick="closeLightboxArtifact()" class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition">
          ✕
        </button>
      </div>
      <div class="flex-1 bg-black flex items-center justify-center p-3 max-h-[55vh] overflow-hidden">
        <img id="art-lightbox-img" src="" alt="Enlarged specimen" class="max-h-[50vh] max-w-full w-auto object-contain rounded border border-slate-800">
      </div>
      <div class="p-3.5 border-t border-slate-800 bg-slate-900/80 text-xs space-y-1.5">
        <p id="art-lightbox-desc" class="text-slate-300 text-[11px] leading-relaxed"></p>
        <div class="text-[11px] text-amber-300 pt-1 border-t border-slate-800">
          <strong>Key Sites:</strong> <span id="art-lightbox-sites"></span>
        </div>
      </div>
    </div>
  </div>

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

  <!-- JAVASCRIPT LOGIC -->
  <script>
    const SITES_DATA = {sites_json_str};

    let activeFilter = {{
      period: 'ALL',
      zone: 'ALL',
      adaptation: 'ALL',
      search: '',
      rockArtOnly: false,
      faunaOnly: false
    }};

    let selectedSiteId = null;

    const PERIOD_COLORS = {{
      'Lower Paleolithic': '#f43f5e',
      'Middle Paleolithic': '#f59e0b',
      'Upper Paleolithic': '#a855f7',
      'Mesolithic': '#10b981',
      'Neolithic': '#06b6d4',
      'Other': '#94a3b8'
    }};

    const LON_MIN = 66.0;
    const LON_MAX = 96.0;
    const LAT_MIN = 8.0;
    const LAT_MAX = 35.0;

    const TOOL_CATALOG_ART = {{
      handaxe: {{
        title: "Acheulian Bifacial Handaxe (Biface)",
        period: "Lower Palaeolithic (1.5 Ma – 120 ka)",
        image: "images/handaxe.jpg",
        desc: "Pointed or amygdaloid biface with soft-hammer step flaking, sharp bilateral cutting edges, and rounded butt.",
        sites: "Attirampakkam (TN), Isampur (KA), Bhimbetka (MP), Didwana (RJ), Hunsgi (KA)."
      }},
      cleaver: {{
        title: "Acheulian Cleaver (Transverse Bit)",
        period: "Lower Palaeolithic (1.2 Ma – 120 ka)",
        image: "images/cleaver.png",
        desc: "Bifacial tool characterized by a broad transverse cutting bit formed by the intersection of two large flake scars or tranchet blow.",
        sites: "Isampur (KA), Chirki-Nevasa (MH), Bhimbetka (MP), Attirampakkam (TN)."
      }},
      chopper: {{
        title: "Soanian Pebble Chopper",
        period: "Lower Palaeolithic (Pebble-Core)",
        image: "images/chopper.jpg",
        desc: "Massive unifacially flaked river cobble tool with natural smooth pebble cortex preserved over the butt.",
        sites: "Soan Valley (Potwar), Guler (Beas Terraces T1-T5), Nalagarh (Sirsa)."
      }},
      levallois: {{
        title: "Levallois Prepared Core & Points",
        period: "Middle Palaeolithic (385 ka – 40 ka)",
        image: "images/levallois.jpg",
        desc: "Radial centripetal flake removals on a prepared tortoise core detaching standardized points and scrapers.",
        sites: "Nevasa (MH), Samnapur (MP), Attirampakkam MP phase (TN), Didwana 16R (RJ)."
      }},
      blade: {{
        title: "Prismatic Blade & Burin",
        period: "Upper Palaeolithic (45 ka – 10 ka)",
        image: "images/blade.png",
        desc: "Elongated, parallel-sided blades with longitudinal guide ridges and specialized burin chisel edges.",
        sites: "Renigunta (AP), Baghor I (MP), Jwalapuram (AP), Patne (MH)."
      }},
      microlith: {{
        title: "Geometric Microliths & Composite Sickles",
        period: "Mesolithic (12 ka – 2500 BCE)",
        image: "images/microlith.jpg",
        desc: "Standardized lunates, trapezes, and triangles with steep blunting retouch, hafted into composite tools.",
        sites: "Bagor (RJ), Sarai-Nahar Rai (UP), Mahadaha (UP), Langhnaj (GJ)."
      }},
      celt: {{
        title: "Ground & Polished Stone Celts",
        period: "Neolithic (7000 BCE – 1000 BCE)",
        image: "images/celt.jpg",
        desc: "Hone-polished basalt celts and axes with sharp convex bits used for forest clearance and cultivation.",
        sites: "Burzahom (JK), Gufkral (JK), Sangankallu (KA), Brahmagiri (KA)."
      }},
      hathnora: {{
        title: "Hathnora Archaic Hominin Skull (Narmada Man)",
        period: "Middle Pleistocene (~250–300 ka)",
        image: "images/hathnora.jpg",
        desc: "Fossil skullcap of an archaic hominin (Homo erectus / archaic Homo sapiens) discovered by Arun Sonakia (1982) in the Narmada basal gravels.",
        sites: "Hathnora (Narmada Valley, Madhya Pradesh)."
      }},
      bhimbetka: {{
        title: "Prehistoric Rock Art (Bhimbetka)",
        period: "Mesolithic & Upper Palaeolithic",
        image: "images/bhimbetka.jpg",
        desc: "Dynamic red ochre paintings inside sandstone rockshelters depicting wild animal herds, hunters, and dances.",
        sites: "Bhimbetka (MP), Adamgarh (MP), Pachmarhi (MP)."
      }}
    }};

    function openLightboxArtifact(key) {{
      const d = TOOL_CATALOG_ART[key];
      if (!d) return;
      document.getElementById('art-lightbox-badge').innerText = d.period;
      document.getElementById('art-lightbox-title').innerText = d.title;
      document.getElementById('art-lightbox-img').src = d.image;
      document.getElementById('art-lightbox-desc').innerText = d.desc;
      document.getElementById('art-lightbox-sites').innerText = d.sites;
      document.getElementById('art-lightbox-modal').classList.remove('hidden');
    }}

    function closeLightboxArtifact() {{
      document.getElementById('art-lightbox-modal').classList.add('hidden');
    }}

    document.getElementById('art-lightbox-modal').addEventListener('click', (e) => {{
      if (e.target.id === 'art-lightbox-modal') closeLightboxArtifact();
    }});

    function projectCoords(lat, lon) {{
      const x = ((lon - LON_MIN) / (LON_MAX - LON_MIN)) * 560 + 50;
      const y = ((LAT_MAX - lat) / (LAT_MAX - LAT_MIN)) * 600 + 50;
      return {{ x, y }};
    }}

    function switchTabArtifact(tabId) {{
      document.querySelectorAll('.art-tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active', 'border-amber-500', 'text-amber-400', 'bg-amber-500/10'));
      
      const target = document.getElementById(tabId);
      if (target) target.classList.remove('hidden');

      const btn = document.getElementById(
        tabId === 'art-tab-typology' ? 'btn-art-typology' :
        tabId === 'art-tab-geology' ? 'btn-art-geology' :
        tabId === 'art-tab-evolution' ? 'btn-art-evolution' : 'btn-art-palaeoenv'
      );
      if (btn) btn.classList.add('active', 'border-amber-500', 'text-amber-400', 'bg-amber-500/10');
    }}

    function getFilteredSites() {{
      return SITES_DATA.filter(s => {{
        if (activeFilter.period !== 'ALL' && s.period !== activeFilter.period) return false;
        if (activeFilter.zone !== 'ALL' && s.geographical_zone !== activeFilter.zone) return false;
        if (activeFilter.adaptation !== 'ALL' && s.environmental_adaptation !== activeFilter.adaptation) return false;
        if (activeFilter.rockArtOnly && (!s.rock_art_details || s.rock_art_details === 'None recorded')) return false;
        if (activeFilter.faunaOnly && (!s.palaeofauna_palaeoflora || s.palaeofauna_palaeoflora === 'None reported' || s.palaeofauna_palaeoflora === 'Not preserved')) return false;
        
        if (activeFilter.search) {{
          const q = activeFilter.search.toLowerCase();
          const match = 
            (s.site_name && s.site_name.toLowerCase().includes(q)) ||
            (s.state_province && s.state_province.toLowerCase().includes(q)) ||
            (s.river_basin && s.river_basin.toLowerCase().includes(q)) ||
            (s.excavator_discoverer && s.excavator_discoverer.toLowerCase().includes(q)) ||
            (s.tool_typology && s.tool_typology.toLowerCase().includes(q)) ||
            (s.manufacturing_technique && s.manufacturing_technique.toLowerCase().includes(q));
          if (!match) return false;
        }}
        return true;
      }});
    }}

    function renderMapMarkers() {{
      const filtered = getFilteredSites();
      const container = document.getElementById('siteMarkersLayer');
      container.innerHTML = '';

      document.getElementById('mapCounter').innerText = `${{filtered.length}} / 104 Sites`;

      filtered.forEach(s => {{
        const lat = parseFloat(s.latitude);
        const lon = parseFloat(s.longitude);
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

        circle.addEventListener('mouseenter', (e) => showTooltip(e, s));
        circle.addEventListener('mousemove', (e) => moveTooltip(e));
        circle.addEventListener('mouseleave', hideTooltip);

        circle.addEventListener('click', () => {{
          selectSite(s.site_id);
        }});

        container.appendChild(circle);
      }});
    }}

    const tooltip = document.getElementById('mapTooltip');
    function showTooltip(e, site) {{
      tooltip.innerHTML = `
        <div class="font-bold text-white">${{site.site_name}}</div>
        <div class="text-[11px] text-amber-400 font-medium">${{site.period}}</div>
        <div class="text-slate-400 text-[10px] mt-0.5">${{site.district || ''}}, ${{site.state_province}} (${{site.river_basin || ''}})</div>
        <div class="text-slate-300 text-[10px] mt-1 italic">${{site.tool_typology || ''}}</div>
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

    function getToolImagePathForSite(site) {{
      const period = site.period;
      const name = (site.site_name || '').toLowerCase();
      const tools = (site.tool_typology || '').toLowerCase();

      if (name.includes('hathnora')) return 'images/hathnora.jpg';
      if (site.rock_art_details && site.rock_art_details !== 'None recorded' && (name.includes('bhimbetka') || name.includes('adamgarh') || name.includes('pachmarhi'))) {{
        return 'images/bhimbetka.jpg';
      }}

      if (period === 'Lower Paleolithic') {{
        if (tools.includes('cleaver') || name.includes('isampur')) return 'images/cleaver.png';
        if (tools.includes('chopper') || tools.includes('pebble') || name.includes('soan') || name.includes('guler')) return 'images/chopper.jpg';
        return 'images/handaxe.jpg';
      }}
      if (period === 'Middle Paleolithic') return 'images/levallois.jpg';
      if (period === 'Upper Paleolithic') return 'images/blade.png';
      if (period === 'Mesolithic') return 'images/microlith.jpg';
      return 'images/celt.jpg';
    }}

    function selectSite(siteId) {{
      selectedSiteId = siteId;
      const site = SITES_DATA.find(s => s.site_id === siteId);
      if (!site) return;

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

      const badge = document.getElementById('selectedPeriodBadge');
      badge.innerText = site.period;
      badge.className = `text-xs font-semibold px-2.5 py-0.5 rounded-full border ${{
        site.period === 'Lower Paleolithic' ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' :
        site.period === 'Middle Paleolithic' ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' :
        site.period === 'Upper Paleolithic' ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' :
        site.period === 'Mesolithic' ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' :
        'bg-cyan-500/20 text-cyan-300 border-cyan-500/30'
      }}`;

      const imgPath = getToolImagePathForSite(site);

      // Determine tool key for clicking to enlarge from dossier
      let toolKey = 'handaxe';
      for (const k of ['cleaver', 'chopper', 'levallois', 'blade', 'microlith', 'celt', 'hathnora', 'bhimbetka']) {{
        if (imgPath.includes(k)) {{
          toolKey = k;
          break;
        }}
      }}

      const dossier = document.getElementById('dossierContent');
      dossier.innerHTML = `
        <div class="space-y-4 animate-fade-in">
          <!-- Tool Image Card (Click to Enlarge) -->
          <div onclick="openLightboxArtifact('${{toolKey}}')" class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center gap-3 cursor-pointer hover:border-amber-500 transition group" title="Click to enlarge image">
            <div class="w-24 h-24 rounded-lg bg-slate-900 border border-slate-800 overflow-hidden flex-shrink-0 relative flex items-center justify-center">
              <img src="${{imgPath}}" alt="${{site.site_name}}" class="w-full h-full object-cover group-hover:scale-105 transition">
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-[10px] text-white font-semibold">🔍 Enlarge</div>
            </div>
            <div>
              <div class="text-[10px] text-amber-400 font-bold uppercase flex items-center gap-1">
                <span>Diagnostic Specimen</span> • <span class="underline">Click to Enlarge</span>
              </div>
              <div class="text-white font-bold text-xs mt-0.5">${{site.period}} Assemblage</div>
              <div class="text-[11px] text-slate-400 mt-1 leading-snug">${{site.tool_typology}}</div>
            </div>
          </div>

          <div>
            <h3 class="text-xl font-black text-white">${{site.site_name}}</h3>
            <div class="text-xs text-slate-400 mt-0.5">
              ${{site.alternative_names ? `<em>Alt: ${{site.alternative_names}}</em> • ` : ''}}
              ${{site.district || ''}}, <strong class="text-slate-200">${{site.state_province}}</strong>, ${{site.country}}
            </div>
            <div class="mt-2 flex flex-wrap items-center gap-1.5">
              <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono">${{site.latitude}}°N, ${{site.longitude}}°E</span>
              <span class="px-2 py-0.5 rounded bg-slate-800 text-amber-300 text-[10px]">${{site.river_basin || '-'}}</span>
              <span class="px-2 py-0.5 rounded bg-slate-800 text-indigo-300 text-[10px]">${{site.geographical_zone || '-'}}</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2 text-xs">
            <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <div class="text-[10px] text-slate-500 uppercase font-semibold">Excavator(s)</div>
              <div class="text-slate-200 font-medium mt-0.5">${{site.excavator_discoverer || '-'}}</div>
            </div>
            <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800">
              <div class="text-[10px] text-slate-500 uppercase font-semibold">Discovery Year</div>
              <div class="text-slate-200 font-medium mt-0.5">${{site.year_of_discovery || 'Various'}}</div>
            </div>
          </div>

          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-2">
            <div class="text-[10px] text-amber-400 uppercase font-bold tracking-wider">Lithic Industry & Technology</div>
            <div>
              <span class="text-slate-400 font-medium">Tool Typology:</span> 
              <span class="text-slate-200 font-semibold">${{site.tool_typology}}</span>
            </div>
            <div>
              <span class="text-slate-400 font-medium">Manufacturing Technique:</span> 
              <span class="text-emerald-300 font-mono text-[11px]">${{site.manufacturing_technique}}</span>
            </div>
            <div class="grid grid-cols-2 gap-2 pt-1 border-t border-slate-900">
              <div>
                <span class="text-slate-400">Raw Material:</span>
                <div class="text-slate-300 font-medium">${{site.primary_raw_materials}}</div>
              </div>
              <div>
                <span class="text-slate-400">Size Bounds:</span>
                <div class="text-slate-300 font-mono text-[11px]">L: ${{site.length_min_mm}}-${{site.length_max_mm}}mm</div>
              </div>
            </div>
          </div>

          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-1.5">
            <div class="text-[10px] text-slate-500 uppercase font-semibold">Ecological & Cultural Evidence</div>
            <div class="text-slate-200"><strong class="text-slate-400">Landscape Adaptation:</strong> ${{site.environmental_adaptation}}</div>
            <div class="text-slate-200"><strong class="text-slate-400">Fauna / Flora:</strong> ${{site.palaeofauna_palaeoflora}}</div>
            <div class="text-slate-200"><strong class="text-slate-400">Rock Art:</strong> <span class="${{site.rock_art_details && site.rock_art_details !== 'None recorded' ? 'text-amber-400 font-bold' : 'text-slate-500'}}">${{site.rock_art_details}}</span></div>
          </div>

          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-[11px]">
            <div class="text-[10px] text-slate-500 uppercase font-semibold">Publications & Citations</div>
            <div class="text-slate-400 mt-1 italic">${{site.key_references}}</div>
            <div class="mt-2 pt-2 border-t border-slate-900 flex items-center gap-2">
              <a href="https://archive.org/search?query=%22Indian+Archaeology%22+%22A+Review%22" target="_blank" rel="noopener noreferrer" class="text-amber-400 hover:text-amber-300 underline font-medium">
                Internet Archive (IAR Volumes)
              </a>
              <span class="text-slate-600">•</span>
              <a href="https://asi.nic.in/" target="_blank" rel="noopener noreferrer" class="text-sky-400 hover:text-sky-300 underline font-medium">
                Official ASI Portal
              </a>
            </div>
          </div>
        </div>
      `;

      document.querySelectorAll('#sitesTableBody tr').forEach(row => {{
        row.classList.remove('bg-amber-500/10', 'border-l-4', 'border-l-amber-500');
      }});
      const tableRow = document.getElementById(`row-${{siteId}}`);
      if (tableRow) {{
        tableRow.classList.add('bg-amber-500/10', 'border-l-4', 'border-l-amber-500');
        tableRow.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }}
    }}

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
          <td class="px-3 py-2.5 text-slate-400 whitespace-nowrap">${{s.river_basin || '-'}}</td>
          <td class="px-3 py-2.5 text-slate-300 max-w-xs truncate" title="${{s.excavator_discoverer}}">${{s.excavator_discoverer}}</td>
          <td class="px-3 py-2.5 text-slate-400 whitespace-nowrap">${{s.year_of_discovery}}</td>
          <td class="px-3 py-2.5 font-mono text-[11px] text-slate-400 whitespace-nowrap">${{s.latitude}}°, ${{s.longitude}}°</td>
          <td class="px-3 py-2.5 text-center whitespace-nowrap">
            <button onclick="selectSite('${{s.site_id}}')" class="px-2.5 py-1 rounded-md bg-slate-800 hover:bg-amber-500 hover:text-slate-950 text-slate-200 font-medium transition text-[11px]">
              Inspect
            </button>
          </td>
        `;

        tr.addEventListener('click', (e) => {{
          if (e.target.tagName !== 'BUTTON') selectSite(s.site_id);
        }});

        tbody.appendChild(tr);
      }});
    }}

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

    function resetFiltersArtifact() {{
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

    function updateKPICardsArtifact() {{
      const filtered = getFilteredSites();
      const counts = {{
        'Total': filtered.length,
        'Lower Paleolithic': 0,
        'Middle Paleolithic': 0,
        'Upper Paleolithic': 0,
        'Mesolithic': 0,
        'Neolithic': 0
      }};

      filtered.forEach(s => {{
        if (counts[s.period] !== undefined) counts[s.period]++;
      }});

      document.getElementById('kpiTotal').innerText = counts['Total'];
      document.getElementById('kpiLP').innerText = counts['Lower Paleolithic'];
      document.getElementById('kpiMP').innerText = counts['Middle Paleolithic'];
      document.getElementById('kpiUP').innerText = counts['Upper Paleolithic'];
      document.getElementById('kpiMeso').innerText = counts['Mesolithic'];
      document.getElementById('kpiNeo').innerText = counts['Neolithic'];
    }}

    function updateView() {{
      renderMapMarkers();
      renderTable();
      updateKPICardsArtifact();
    }}

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

    window.addEventListener('DOMContentLoaded', () => {{
      updateView();
      const featured = SITES_DATA.find(s => s.site_name.includes('Bhimbetka')) || SITES_DATA[0];
      if (featured) selectSite(featured.site_id);

      window.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape') closeLightboxArtifact();
      }});
    }});
  </script>
</body>
</html>
"""

    out_artifact = r"C:\Users\DuDu-PC\.gemini\antigravity\brain\56c9ba5d-fc02-4acf-a11e-3bc90cf38fd5\prehistoric_dashboard.html"
    with open(out_artifact, "w", encoding="utf-8") as f:
        f.write(artifact_html)
    print(f"Updated prehistoric_dashboard.html at {out_artifact}")

if __name__ == "__main__":
    update()
