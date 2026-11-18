import json
import os

print("Building complete interactive dashboard with 1,588 archaeological sites...")

base_dir = r"G:\Updated Profile KSC\Prehistory-of-India"
json_path = os.path.join(base_dir, "sites_data.json")
index_path = os.path.join(base_dir, "index.html")

with open(json_path, 'r', encoding='utf-8') as f:
    sites = json.load(f)

sites_json_str = json.dumps(sites, ensure_ascii=False)

# Collect all unique states and volumes for dropdown filters
all_states = sorted(list(set(s.get('state_province', '').strip() for s in sites if s.get('state_province'))))
all_volumes = sorted(list(set(s.get('iar_volume', '').strip() for s in sites if s.get('iar_volume'))), key=lambda x: str(x))

state_options_html = '\n'.join([f'<option value="{st}">{st}</option>' for st in all_states])
volume_options_html = '\n'.join([f'<option value="{v}">IAR {v}</option>' for v in all_volumes])

html_content = f"""<!DOCTYPE html>
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
      width: 8px;
      height: 8px;
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

    .dataset-btn.active {{
      background-color: #f59e0b;
      color: #000000;
      font-weight: 700;
      border-color: #f59e0b;
    }}

    .custom-tooltip {{
      background-color: rgba(17, 24, 39, 0.95) !important;
      border: 1px solid #374151 !important;
      border-radius: 0.5rem !important;
      color: #f3f4f6 !important;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5) !important;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- TOP NAVIGATION HEADER -->
  <header class="border-b border-gray-800 bg-gray-900/90 backdrop-blur sticky top-0 z-50 px-6 py-4">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="h-12 w-12 rounded-xl bg-gradient-to-tr from-amber-500 to-rose-600 flex items-center justify-center text-white shadow-lg shadow-amber-500/20 flex-shrink-0">
          <i data-lucide="compass" class="w-6 h-6"></i>
        </div>
        <div>
          <div class="flex flex-wrap items-center gap-2">
            <h1 class="text-xl md:text-2xl font-bold font-display tracking-tight text-white">
              Prehistory of India
            </h1>
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-400 font-sans border border-amber-500/30 font-semibold">
              1,588 Geo-Indexed Sites
            </span>
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-rose-500/20 text-rose-300 font-sans border border-rose-500/30">
              1,484 IAR Survey
            </span>
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-sans border border-cyan-500/30">
              104 Syllabus Landmarks
            </span>
          </div>
          <p class="text-xs text-gray-400 mt-0.5">National Archaeological Survey Compendium (1953–1976) & University Curriculum GIS</p>
          <div class="mt-1 flex flex-wrap items-center gap-2 text-xs text-amber-400 font-medium">
            <span class="flex items-center gap-1"><i data-lucide="sparkles" class="w-3.5 h-3.5"></i> Idea & Design by <strong>K.S.Chandra 2026</strong></span>
            <span class="text-gray-600">•</span>
            <a href="mailto:kavikondalaschandra@gmail.com" class="text-sky-400 hover:text-sky-300 underline underline-offset-2">kavikondalaschandra@gmail.com</a>
            <span class="text-gray-600">•</span>
            <span class="text-gray-400 text-[11px]">Aligned with: <em>Prehistory of India – Origin & Evolution of Man in Indian Subcontinent</em></span>
          </div>
        </div>
      </div>

      <!-- Header Right: Quick Reset -->
      <div class="flex items-center gap-2">
        <button onclick="resetFilters()" class="px-3.5 py-2 rounded-xl bg-rose-950/40 hover:bg-rose-900/60 text-xs font-semibold text-rose-300 border border-rose-800/40 flex items-center gap-1.5 transition">
          <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i> Reset Filters
        </button>
      </div>
    </div>

    <!-- PEER-REVIEWED CITATION BANNER -->
    <div class="max-w-7xl mx-auto mt-3 pt-2.5 border-t border-gray-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
      <div class="flex items-start sm:items-center gap-2 text-gray-300">
        <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold uppercase text-[10px] tracking-wider whitespace-nowrap">
          Peer-Reviewed Citation
        </span>
        <span class="text-gray-400">
          <strong>Vidyarthi, V. & Chauhan, P. (2025).</strong> <em>Mapping the Indian Palaeolithic.</em> Journal of Computer Applications in Archaeology, 8(1): 78–93.
        </span>
      </div>
      <div class="flex items-center gap-3 flex-shrink-0">
        <a href="https://doi.org/10.5334/jcaa.148" target="_blank" rel="noopener noreferrer" class="text-sky-400 hover:text-sky-300 font-mono text-[11px] flex items-center gap-1 underline underline-offset-2">
          <span>DOI: 10.5334/jcaa.148</span>
          <i data-lucide="external-link" class="w-3 h-3"></i>
        </a>
        <button onclick="copyCitation()" class="px-2 py-1 rounded bg-gray-800 hover:bg-gray-700 text-gray-300 text-[11px] font-medium flex items-center gap-1 transition" title="Copy APA Citation to Clipboard">
          <i data-lucide="copy" class="w-3 h-3"></i> Copy Citation
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
        <div class="text-2xl font-bold font-display text-white" id="stat-total-sites">1,588</div>
        <span class="text-[10px] text-gray-400 mt-1">Across 22 States/UTs</span>
      </div>

      <div class="bg-gray-900/90 border border-rose-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-rose-800/50 transition">
        <div class="flex items-center justify-between text-rose-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Lower Palaeo</span>
          <span class="pulse-dot bg-rose-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-rose-300" id="stat-lp-sites">985</div>
        <span class="text-[10px] text-gray-400 mt-1">Acheulian & Soanian</span>
      </div>

      <div class="bg-gray-900/90 border border-amber-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-amber-800/50 transition">
        <div class="flex items-center justify-between text-amber-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Middle Palaeo</span>
          <span class="pulse-dot bg-amber-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-amber-300" id="stat-mp-sites">426</div>
        <span class="text-[10px] text-gray-400 mt-1">Levallois & Series II</span>
      </div>

      <div class="bg-gray-900/90 border border-purple-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-purple-800/50 transition">
        <div class="flex items-center justify-between text-purple-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Upper Palaeo</span>
          <span class="pulse-dot bg-purple-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-purple-300" id="stat-up-sites">38</div>
        <span class="text-[10px] text-gray-400 mt-1">Blade & Burin Series III</span>
      </div>

      <div class="bg-gray-900/90 border border-emerald-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-emerald-800/50 transition">
        <div class="flex items-center justify-between text-emerald-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Mesolithic</span>
          <span class="pulse-dot bg-emerald-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-emerald-300" id="stat-meso-sites">98</div>
        <span class="text-[10px] text-gray-400 mt-1">Microliths & Late Stone Age</span>
      </div>

      <div class="bg-gray-900/90 border border-cyan-900/30 p-3.5 rounded-xl flex flex-col justify-between hover:border-cyan-800/50 transition">
        <div class="flex items-center justify-between text-cyan-400 mb-1">
          <span class="text-xs uppercase tracking-wider font-semibold">Neolithic</span>
          <span class="pulse-dot bg-cyan-500"></span>
        </div>
        <div class="text-2xl font-bold font-display text-cyan-300" id="stat-neo-sites">41</div>
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
          <p class="text-xs text-gray-400">Essential chronological, environmental, technological, and peer-reviewed mapping archive.</p>
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
          <button onclick="switchTab('tab-reference')" id="btn-tab-reference" class="tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold border border-transparent transition flex items-center gap-1.5 whitespace-nowrap text-amber-400 hover:text-amber-300">
            <i data-lucide="file-text" class="w-3.5 h-3.5"></i> Mapping Methodology (Vidyarthi & Chauhan 2025)
          </button>
        </div>
      </div>

      <!-- TAB 1: TOOL TYPOLOGY GALLERY -->
      <div id="tab-typology" class="tab-content space-y-4">
        <p class="text-xs text-gray-400 leading-relaxed">
          Diagnostic stone tool forms spanning Lower Paleolithic Acheulian bifaces to Neolithic ground celts. Click any card to inspect high-resolution lithic plates with full technological descriptions.
        </p>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-9 gap-2.5">
          <button onclick="selectAndEnlargeTool('handaxe')" class="p-2.5 rounded-xl bg-gray-950/60 border border-rose-900/30 hover:border-rose-500/60 text-left transition group">
            <div class="h-20 w-full rounded-lg bg-gray-900 overflow-hidden mb-2 relative">
              <img src="images/handaxe.jpg" alt="Acheulian Handaxe" class="w-full h-full object-cover group-hover:scale-105 transition duration-300" onerror="this.src='https://commons.wikimedia.org/wiki/Special:FilePath/Biface_Attirampakkam.jpg'"/>
              <span class="absolute bottom-1 right-1 text-[9px] px-1 py-0.5 rounded bg-black/80 text-rose-300">Lower Pal</span>
            </div>
            <div class="text-[11px] font-bold text-white group-hover:text-rose-400 transition truncate">Bifacial Handaxe</div>
            <div class="text-[10px] text-gray-400 truncate">Acheulian Pointed Biface</div>
          </button>

          <button onclick="selectAndEnlargeTool('cleaver')" class="p-2.5 rounded-xl bg-gray-950/60 border border-rose-900/30 hover:border-rose-500/60 text-left transition group">
            <div class="h-20 w-full rounded-lg bg-gray-900 overflow-hidden mb-2 relative">
              <img src="images/cleaver.png" alt="Acheulian Cleaver" class="w-full h-full object-cover group-hover:scale-105 transition duration-300" onerror="this.src='https://commons.wikimedia.org/wiki/Special:FilePath/Acheulian_Cleaver_Isampur.jpg'"/>
              <span class="absolute bottom-1 right-1 text-[9px] px-1 py-0.5 rounded bg-black/80 text-rose-300">Lower Pal</span>
            </div>
            <div class="text-[11px] font-bold text-white group-hover:text-rose-400 transition truncate">Acheulian Cleaver</div>
            <div class="text-[10px] text-gray-400 truncate">Transverse Bit Kombewa</div>
          </button>

          <button onclick="selectAndEnlargeTool('chopper')" class="p-2.5 rounded-xl bg-gray-950/60 border border-rose-900/30 hover:border-rose-500/60 text-left transition group">
            <div class="h-20 w-full rounded-lg bg-gray-900 overflow-hidden mb-2 relative">
              <img src="images/chopper.jpg" alt="Soanian Chopper" class="w-full h-full object-cover group-hover:scale-105 transition duration-300"/>
              <span class="absolute bottom-1 right-1 text-[9px] px-1 py-0.5 rounded bg-black/80 text-rose-300">Soanian</span>
            </div>
            <div class="text-[11px] font-bold text-white group-hover:text-rose-400 transition truncate">Pebble Chopper</div>
            <div class="text-[10px] text-gray-400 truncate">Unifacial Flaked Cobble</div>
          </button>

          <button onclick="selectAndEnlargeTool('levallois')" class="p-2.5 rounded-xl bg-gray-950/60 border border-amber-900/30 hover:border-amber-500/60 text-left transition group">
            <div class="h-20 w-full rounded-lg bg-gray-900 overflow-hidden mb-2 relative">
              <img src="images/levallois.jpg" alt="Levallois Core" class="w-full h-full object-cover group-hover:scale-105 transition duration-300"/>
              <span class="absolute bottom-1 right-1 text-[9px] px-1 py-0.5 rounded bg-black/80 text-amber-300">Middle Pal</span>
            </div>
            <div class="text-[11px] font-bold text-white group-hover:text-amber-400 transition truncate">Levallois Core</div>
            <div class="text-[10px] text-gray-400 truncate">Prepared Tortoise Core</div>
          </button>

          <button onclick="selectAndEnlargeTool('blade')" class="p-2.5 rounded-xl bg-gray-950/60 border border-purple-900/30 hover:border-purple-500/60 text-left transition group">
            <div class="h-20 w-full rounded-lg bg-gray-900 overflow-hidden mb-2 relative">
              <img src="images/blade.png" alt="Upper Paleolithic Blade" class="w-full h-full object-cover group-hover:scale-105 transition duration-300"/>
              <span class="absolute bottom-1 right-1 text-[9px] px-1 py-0.5 rounded bg-black/80 text-purple-300">Upper Pal</span>
            </div>
            <div class="text-[11px] font-bold text-white group-hover:text-purple-400 transition truncate">Prismatic Blade</div>
            <div class="text-[10px] text-gray-400 truncate">Punch Blade & Burins</div>
          </button>

          <button onclick="selectAndEnlargeTool('microlith')" class="p-2.5 rounded-xl bg-gray-950/60 border border-emerald-900/30 hover:border-emerald-500/60 text-left transition group">
            <div class="h-20 w-full rounded-lg bg-gray-900 overflow-hidden mb-2 relative">
              <img src="images/microlith.jpg" alt="Mesolithic Microliths" class="w-full h-full object-cover group-hover:scale-105 transition duration-300"/>
              <span class="absolute bottom-1 right-1 text-[9px] px-1 py-0.5 rounded bg-black/80 text-emerald-300">Mesolithic</span>
            </div>
            <div class="text-[11px] font-bold text-white group-hover:text-emerald-400 transition truncate">Microliths</div>
            <div class="text-[10px] text-gray-400 truncate">Geometric Lunates & Triangles</div>
          </button>

          <button onclick="selectAndEnlargeTool('celt')" class="p-2.5 rounded-xl bg-gray-950/60 border border-cyan-900/30 hover:border-cyan-500/60 text-left transition group">
            <div class="h-20 w-full rounded-lg bg-gray-900 overflow-hidden mb-2 relative">
              <img src="images/celt.jpg" alt="Neolithic Polished Celt" class="w-full h-full object-cover group-hover:scale-105 transition duration-300"/>
              <span class="absolute bottom-1 right-1 text-[9px] px-1 py-0.5 rounded bg-black/80 text-cyan-300">Neolithic</span>
            </div>
            <div class="text-[11px] font-bold text-white group-hover:text-cyan-400 transition truncate">Polished Celt</div>
            <div class="text-[10px] text-gray-400 truncate">Ground Basalt Axe</div>
          </button>

          <button onclick="selectAndEnlargeTool('hathnora')" class="p-2.5 rounded-xl bg-gray-950/60 border border-red-900/30 hover:border-red-500/60 text-left transition group">
            <div class="h-20 w-full rounded-lg bg-gray-900 overflow-hidden mb-2 relative">
              <img src="images/hathnora.jpg" alt="Narmada Man Calvarium" class="w-full h-full object-cover group-hover:scale-105 transition duration-300"/>
              <span class="absolute bottom-1 right-1 text-[9px] px-1 py-0.5 rounded bg-black/80 text-red-300">Fossil</span>
            </div>
            <div class="text-[11px] font-bold text-white group-hover:text-red-400 transition truncate">Narmada Man</div>
            <div class="text-[10px] text-gray-400 truncate">Archaic Homo Hominin</div>
          </button>

          <button onclick="selectAndEnlargeTool('bhimbetka')" class="p-2.5 rounded-xl bg-gray-950/60 border border-orange-900/30 hover:border-orange-500/60 text-left transition group">
            <div class="h-20 w-full rounded-lg bg-gray-900 overflow-hidden mb-2 relative">
              <img src="images/bhimbetka.jpg" alt="Bhimbetka Rock Art" class="w-full h-full object-cover group-hover:scale-105 transition duration-300"/>
              <span class="absolute bottom-1 right-1 text-[9px] px-1 py-0.5 rounded bg-black/80 text-orange-300">Rock Art</span>
            </div>
            <div class="text-[11px] font-bold text-white group-hover:text-orange-400 transition truncate">Rock Art</div>
            <div class="text-[10px] text-gray-400 truncate">Bhimbetka Pictographs</div>
          </button>
        </div>

        <!-- Tool Detail Expanded Box -->
        <div id="toolDetailCard" class="p-3.5 rounded-xl bg-gray-950/90 border border-gray-800 flex flex-col md:flex-row gap-4 items-start">
          <div class="space-y-1.5 flex-1">
            <div class="flex items-center gap-2">
              <h3 id="toolDetailTitle" class="text-sm font-bold text-amber-400 font-display">Acheulian Bifacial Handaxe (Biface)</h3>
              <span id="toolDetailPeriod" class="text-[10px] px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">Lower Palaeolithic</span>
            </div>
            <p id="toolDetailDesc" class="text-xs text-gray-300 leading-relaxed">
              Bifacially flaked core/large-flake implement with pointed apex, sharp bilateral cutting edges, and thick basal butt. Multipurpose butchery, digging subterranean tubers, and wood chopping tool of Homo erectus and archaic hominins.
            </p>
            <div class="text-[11px] text-gray-400 flex flex-wrap gap-x-4 gap-y-1 pt-1 border-t border-gray-900">
              <span><strong>Manufacturing:</strong> <span id="toolDetailTech">Block-on-block anvil percussion, soft hammer billet flaking</span></span>
              <span><strong>Key Sites:</strong> <span id="toolDetailSites">Attirampakkam, Isampur, Bhimbetka, Didwana, Hunsgi, Nevasa</span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: GEOLOGICAL TIME SCALE -->
      <div id="tab-geology" class="tab-content hidden space-y-3">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800">
            <div class="text-[10px] font-mono text-amber-400 font-semibold uppercase">Early Pleistocene (2.58–0.78 Ma)</div>
            <h4 class="text-sm font-bold text-white mt-1">Matuyama Reversed Chron</h4>
            <p class="text-xs text-gray-400 mt-1.5 leading-relaxed">
              Initial hominin dispersals into the Indian Subcontinent. Characterized by early Acheulian bifaces at Attirampakkam (~1.51 Ma, 26Al/10Be) and Isampur (~1.27 Ma, ESR).
            </p>
          </div>
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800">
            <div class="text-[10px] font-mono text-rose-400 font-semibold uppercase">Middle Pleistocene (781–126 ka)</div>
            <h4 class="text-sm font-bold text-white mt-1">Brunhes Normal Chron</h4>
            <p class="text-xs text-gray-400 mt-1.5 leading-relaxed">
              Late Acheulian perfection with soft-hammer thinning and transition to Middle Palaeolithic (Attirampakkam ~385 ka). Hathnora cranial calvarium in Narmada boulder conglomerate.
            </p>
          </div>
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800">
            <div class="text-[10px] font-mono text-purple-400 font-semibold uppercase">Late Pleistocene (126–11.7 ka)</div>
            <h4 class="text-sm font-bold text-white mt-1">Last Glacial Cycle & Toba Tephra</h4>
            <p class="text-xs text-gray-400 mt-1.5 leading-relaxed">
              Youngest Toba Tuff (YTT ~74 ka) ash layers sealing Middle Palaeolithic horizons (Jwalapuram). Rapid emergence of Upper Palaeolithic blade-and-burin industries (Baghor I, Mehtakheri).
            </p>
          </div>
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800">
            <div class="text-[10px] font-mono text-emerald-400 font-semibold uppercase">Holocene (11.7 ka – Present)</div>
            <h4 class="text-sm font-bold text-white mt-1">Post-Glacial Warm Optimum</h4>
            <p class="text-xs text-gray-400 mt-1.5 leading-relaxed">
              Intensive Mesolithic hunting-foraging, Ganga Valley oxbow settlements (Sarai-Nahar Rai, Damdama), Vindhyan rock art climax, and transition to Neolithic agricultural villages.
            </p>
          </div>
        </div>
      </div>

      <!-- TAB 3: HUMAN EVOLUTION -->
      <div id="tab-evolution" class="tab-content hidden space-y-3">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800 space-y-2">
            <div class="text-[10px] font-mono text-red-400 font-semibold uppercase">Hathnora Calvarium (1982)</div>
            <h4 class="text-sm font-bold text-white">Arun Sonakia Discovery</h4>
            <p class="text-xs text-gray-400 leading-relaxed">
              Archaic hominin partial skullcap unearthed on Dec 5, 1982 from the basal cemented gravel of the Narmada River at Hathnora, Sehore District, MP. Displayed prominent supraorbital tori, brain volume ~1155–1421 cc, associated with Late Acheulian cleavers and Pleistocene mammal fossils.
            </p>
          </div>
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800 space-y-2">
            <div class="text-[10px] font-mono text-amber-400 font-semibold uppercase">Hathnora Clavicle (1997)</div>
            <h4 class="text-sm font-bold text-white">A.A. Sankhyan Discovery</h4>
            <p class="text-xs text-gray-400 leading-relaxed">
              Right hominin clavicle discovered by A.A. Sankhyan (ASI) from the same Hathnora gravel horizon, indicating a pygmy/short-statured archaic hominin phenotype contemporaneous with Middle Pleistocene megafauna.
            </p>
          </div>
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800 space-y-2">
            <div class="text-[10px] font-mono text-sky-400 font-semibold uppercase">Jwalapuram & Kurnool</div>
            <h4 class="text-sm font-bold text-white">Anatomically Modern Humans</h4>
            <p class="text-xs text-gray-400 leading-relaxed">
              Continuous lithic sequence spanning 77 ka to 38 ka at Jwalapuram Locality 22 demonstrates hominin survival across the super-eruption of Mount Toba (~74 ka), proving early modern human continuity in the Indian Subcontinent.
            </p>
          </div>
        </div>
      </div>

      <!-- TAB 4: PREHISTORIC FLORA & FAUNA -->
      <div id="tab-palaeoenv" class="tab-content hidden space-y-3">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800 space-y-1.5">
            <div class="text-[10px] font-mono text-rose-400 font-semibold uppercase">Pleistocene Megafauna</div>
            <h4 class="text-sm font-bold text-white">Extinct Large Mammals</h4>
            <p class="text-xs text-gray-400 leading-relaxed">
              Abundant in cemented gravels of Narmada, Godavari, and Pravara: <em>Bos namadicus</em> (wild cattle), <em>Elephas hysudricus / Palaeoloxodon namadicus</em> (straight-tusked elephant), <em>Equus namadicus</em> (archaic horse), and <em>Hexaprotodon palaeindicus</em> (six-incisor hippopotamus).
            </p>
          </div>
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800 space-y-1.5">
            <div class="text-[10px] font-mono text-emerald-400 font-semibold uppercase">Holocene Faunal Turnover</div>
            <h4 class="text-sm font-bold text-white">Mesolithic Wildlife</h4>
            <p class="text-xs text-gray-400 leading-relaxed">
              Shift to modern Holocene taxa in Ganga Valley oxbow settlements: <em>Rucervus duvaucelii</em> (swamp deer), <em>Antilope cervicapra</em> (blackbuck), <em>Gazella bennettii</em> (chinkara), <em>Sus scrofa</em> (wild boar), and aquatic fauna (tortoises, freshwater molluscs).
            </p>
          </div>
          <div class="p-3.5 rounded-xl bg-gray-950/60 border border-gray-800 space-y-1.5">
            <div class="text-[10px] font-mono text-amber-400 font-semibold uppercase">Palaeoflora & Domestication</div>
            <h4 class="text-sm font-bold text-white">Plant Macro-Remains</h4>
            <p class="text-xs text-gray-400 leading-relaxed">
              Wild rice (<em>Oryza nivara</em>) impressions in pottery and hearths at Chopani-Mando and Mahagara (Belan Valley); transition to domesticated barley (<em>Hordeum vulgare</em>) and wheat at Mehrgarh (Period I, ~7000 BCE).
            </p>
          </div>
        </div>
      </div>

      <!-- TAB 5: MAPPING METHODOLOGY & CITATION (NEW) -->
      <div id="tab-reference" class="tab-content hidden space-y-4">
        <div class="p-4 rounded-xl bg-gray-950/90 border border-amber-500/30 space-y-3">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 text-xs font-bold uppercase tracking-wider">
              Landmark Research Citation
            </span>
            <span class="text-xs text-gray-400">Journal of Computer Applications in Archaeology (2025)</span>
          </div>

          <div class="bg-gray-900/80 p-3 rounded-lg border border-gray-800 text-xs font-mono text-gray-200">
            Vidyarthi, V. and Chauhan, P. 2025. Mapping the Indian Palaeolithic. <em>Journal of Computer Applications in Archaeology</em>, 8(1): 78–93. DOI: <a href="https://doi.org/10.5334/jcaa.148" target="_blank" class="text-sky-400 hover:underline">https://doi.org/10.5334/jcaa.148</a>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 text-xs text-gray-300">
            <div class="space-y-2">
              <h4 class="font-bold text-white flex items-center gap-1.5">
                <i data-lucide="database" class="w-3.5 h-3.5 text-amber-400"></i>
                Methodology & Archival Data Source
              </h4>
              <p class="text-gray-400 leading-relaxed">
                This comprehensive dataset digitizes all Palaeolithic sites reported across 22 annual volumes of <em>Indian Archaeology: A Review</em> (IAR, 1953–54 to 1975–76) published by the Archaeological Survey of India (ASI). Each reported discovery was systematically codified with volume number, page citation, administrative district, reported lithic typologies, geomorphic site contexts, and investigator attributions.
              </p>
            </div>
            <div class="space-y-2">
              <h4 class="font-bold text-white flex items-center gap-1.5">
                <i data-lucide="map-pin" class="w-3.5 h-3.5 text-emerald-400"></i>
                Location Integrity & GIS Georeferencing
              </h4>
              <p class="text-gray-400 leading-relaxed">
                Sites are categorized into <strong>Precise</strong> (where exact coordinates or verified archaeological landmarks exist) and <strong>Vague</strong> (district/basin-level reports). In this platform, all 1,484 survey sites have been geocoded with high cartographic fidelity using district centroids and deterministic micro-dispersion to enable seamless multi-layer spatial analysis in Leaflet, QGIS, and ArcGIS.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- DATASET SELECTION PILL BAR -->
    <div class="bg-gray-900/90 border border-gray-800 rounded-xl p-3 flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-1">
          <i data-lucide="filter" class="w-3.5 h-3.5 text-amber-400"></i> Active Dataset:
        </span>
        <div class="flex flex-wrap items-center gap-1.5" id="dataset-filter-group">
          <button onclick="setDatasetFilter('ALL')" id="btn-dataset-all" class="dataset-btn active px-3 py-1 rounded-lg text-xs border border-gray-700 transition">
            All Sites (1,588)
          </button>
          <button onclick="setDatasetFilter('IAR')" id="btn-dataset-iar" class="dataset-btn px-3 py-1 rounded-lg text-xs border border-gray-700 text-gray-300 hover:text-white transition">
            IAR National Survey (1,484) — Vidyarthi & Chauhan (2025)
          </button>
          <button onclick="setDatasetFilter('LANDMARK')" id="btn-dataset-landmark" class="dataset-btn px-3 py-1 rounded-lg text-xs border border-gray-700 text-gray-300 hover:text-white transition">
            Syllabus Landmarks (104)
          </button>
          <button onclick="setDatasetFilter('EXCAVATED')" id="btn-dataset-excavated" class="dataset-btn px-3 py-1 rounded-lg text-xs border border-gray-700 text-gray-300 hover:text-white transition">
            Excavated Sites (45)
          </button>
        </div>
      </div>
      <div class="text-xs text-gray-400 flex items-center gap-2 font-mono">
        <span>Showing: <strong id="filtered-count" class="text-amber-400">1,588</strong> / <span id="total-count">1,588</span> sites</span>
      </div>
    </div>

    <!-- SEARCH & MULTI-FILTER CONTROL BAR -->
    <div class="bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl space-y-3">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        
        <!-- Search Input -->
        <div class="lg:col-span-2 relative">
          <i data-lucide="search" class="w-4 h-4 text-gray-500 absolute left-3 top-3"></i>
          <input type="text" id="search-input" placeholder="Search site, district, state, volume, artifacts, investigator..." class="w-full bg-gray-950 border border-gray-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-amber-500 transition"/>
        </div>

        <!-- Period Filter -->
        <div>
          <select id="period-filter" onchange="applyFilters()" class="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-xs text-gray-300 focus:outline-none focus:border-amber-500 transition">
            <option value="ALL">All Periods (Paleo to Neo)</option>
            <option value="Lower Paleolithic">Lower Paleolithic (Acheulian & Soanian)</option>
            <option value="Middle Paleolithic">Middle Paleolithic (Levallois & Series II)</option>
            <option value="Upper Paleolithic">Upper Paleolithic (Blade & Burin)</option>
            <option value="Mesolithic">Mesolithic (Microlithic)</option>
            <option value="Neolithic">Neolithic (Ground Celts)</option>
          </select>
        </div>

        <!-- State Filter -->
        <div>
          <select id="state-filter" onchange="applyFilters()" class="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-xs text-gray-300 focus:outline-none focus:border-amber-500 transition">
            <option value="ALL">All States / Provinces</option>
            {state_options_html}
          </select>
        </div>

        <!-- IAR Volume Filter -->
        <div>
          <select id="volume-filter" onchange="applyFilters()" class="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-xs text-gray-300 focus:outline-none focus:border-amber-500 transition">
            <option value="ALL">All IAR Volumes (1953–1976)</option>
            {volume_options_html}
          </select>
        </div>
      </div>

      <!-- Quick Toggles -->
      <div class="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-gray-800/80 text-xs">
        <div class="flex flex-wrap items-center gap-4 text-gray-400">
          <label class="flex items-center gap-1.5 cursor-pointer hover:text-gray-200 transition">
            <input type="checkbox" id="excavated-only" onchange="applyFilters()" class="rounded bg-gray-950 border-gray-700 text-amber-500 focus:ring-0 w-3.5 h-3.5"/>
            <span>Excavated Sites Only</span>
          </label>
          <label class="flex items-center gap-1.5 cursor-pointer hover:text-gray-200 transition">
            <input type="checkbox" id="fauna-only" onchange="applyFilters()" class="rounded bg-gray-950 border-gray-700 text-amber-500 focus:ring-0 w-3.5 h-3.5"/>
            <span>Fauna / Fossil Bone Sites Only</span>
          </label>
          <label class="flex items-center gap-1.5 cursor-pointer hover:text-gray-200 transition">
            <input type="checkbox" id="rock-art-only" onchange="applyFilters()" class="rounded bg-gray-950 border-gray-700 text-amber-500 focus:ring-0 w-3.5 h-3.5"/>
            <span>Rock Art / Cave Sites Only</span>
          </label>
          <label class="flex items-center gap-1.5 cursor-pointer hover:text-gray-200 transition">
            <input type="checkbox" id="precise-only" onchange="applyFilters()" class="rounded bg-gray-950 border-gray-700 text-amber-500 focus:ring-0 w-3.5 h-3.5"/>
            <span>Precise Coordinates Only</span>
          </label>
        </div>

        <button onclick="resetFilters()" class="text-xs text-gray-400 hover:text-amber-400 flex items-center gap-1 transition">
          <i data-lucide="refresh-cw" class="w-3 h-3"></i> Clear all search filters
        </button>
      </div>
    </div>

    <!-- MAP & REGIONAL DISTRIBUTION CHART -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Leaflet Map Container -->
      <div class="lg:col-span-2 bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl flex flex-col justify-between">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <i data-lucide="map" class="w-4 h-4 text-amber-400"></i>
            <h3 class="text-sm font-bold text-white font-display">Spatial GIS Archaeological Map (EPSG:4326 WGS84)</h3>
          </div>
          <span class="text-[11px] text-gray-400 font-mono">Esri Topo Basemap • Click marker for full dossier</span>
        </div>
        
        <div id="map" class="w-full"></div>

        <!-- Map Legend -->
        <div class="flex flex-wrap items-center justify-between gap-2 mt-3 pt-2.5 border-t border-gray-800 text-[11px] text-gray-400">
          <div class="flex flex-wrap items-center gap-3">
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Lower Palaeolithic</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Middle Palaeolithic</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span> Upper Palaeolithic</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Mesolithic</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-cyan-500"></span> Neolithic</span>
          </div>
          <div class="text-[10px] text-gray-500">
            Source: Vidyarthi & Chauhan (2025) & K.S.Chandra
          </div>
        </div>
      </div>

      <!-- State & Regional Distribution Chart -->
      <div class="bg-gray-900/90 border border-gray-800 rounded-2xl p-4 shadow-xl flex flex-col justify-between">
        <div class="flex items-center justify-between mb-3 border-b border-gray-800 pb-2">
          <div class="flex items-center gap-2">
            <i data-lucide="bar-chart-3" class="w-4 h-4 text-amber-400"></i>
            <h3 class="text-sm font-bold text-white font-display">State-wise Distribution</h3>
          </div>
          <span class="text-[10px] text-gray-400 uppercase tracking-wider">Top States</span>
        </div>

        <div class="h-[460px] w-full relative">
          <canvas id="zoneChart"></canvas>
        </div>

        <div class="text-[11px] text-gray-400 mt-2 text-center border-t border-gray-800/80 pt-2">
          Highest site densities recorded in <strong>Maharashtra</strong>, <strong>Madhya Pradesh</strong> & <strong>Andhra Pradesh</strong>.
        </div>
      </div>
    </div>

    <!-- COMPLETE SITES DATA TABLE -->
    <div class="bg-gray-900/90 border border-gray-800 rounded-2xl p-5 shadow-2xl space-y-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-gray-800 pb-3">
        <div>
          <h3 class="text-base font-bold font-display text-white flex items-center gap-2">
            <i data-lucide="table" class="w-4 h-4 text-amber-400"></i>
            <span>Archaeological Sites Database Directory</span>
          </h3>
          <p class="text-xs text-gray-400" id="table-info">Showing all 1,588 sites across the Indian Subcontinent.</p>
        </div>

        <!-- Page Size Selector -->
        <div class="flex items-center gap-2">
          <label class="text-xs text-gray-400">Show per page:</label>
          <select id="pageSizeSelect" onchange="changePageSize(this.value)" class="bg-gray-950 border border-gray-800 rounded-lg px-2.5 py-1 text-xs text-white focus:outline-none focus:border-amber-500">
            <option value="50" selected>50 sites</option>
            <option value="100">100 sites</option>
            <option value="250">250 sites</option>
            <option value="500">500 sites</option>
            <option value="1588">All (1,588 sites)</option>
          </select>
        </div>
      </div>

      <!-- Table Wrapper -->
      <div class="overflow-x-auto rounded-xl border border-gray-800">
        <table class="w-full text-left text-xs text-gray-300">
          <thead class="bg-gray-950 text-gray-400 uppercase tracking-wider text-[10px] font-semibold border-b border-gray-800">
            <tr>
              <th class="px-3.5 py-3">Site Name</th>
              <th class="px-3.5 py-3">Period / Stage</th>
              <th class="px-3.5 py-3">State</th>
              <th class="px-3.5 py-3">District</th>
              <th class="px-3.5 py-3">IAR Source / Year</th>
              <th class="px-3.5 py-3">Artifacts Reported</th>
              <th class="px-3.5 py-3">Investigator(s)</th>
              <th class="px-3.5 py-3">Context / Fossils</th>
              <th class="px-3.5 py-3 text-center">Actions</th>
            </tr>
          </thead>
          <tbody id="sites-table-body" class="divide-y divide-gray-800/60 font-sans">
            <!-- Dynamically populated -->
          </tbody>
        </table>
      </div>

      <!-- Pagination Controls -->
      <div class="flex items-center justify-between pt-2">
        <button id="prev-page" onclick="changePage(-1)" class="px-3.5 py-1.5 rounded-lg bg-gray-950 border border-gray-800 text-xs font-semibold text-gray-300 hover:text-white disabled:opacity-40 disabled:cursor-not-allowed transition flex items-center gap-1">
          <i data-lucide="chevron-left" class="w-3.5 h-3.5"></i> Previous
        </button>
        <span class="text-xs text-gray-400">Page <strong id="page-num" class="text-white">1</strong></span>
        <button id="next-page" onclick="changePage(1)" class="px-3.5 py-1.5 rounded-lg bg-gray-950 border border-gray-800 text-xs font-semibold text-gray-300 hover:text-white disabled:opacity-40 disabled:cursor-not-allowed transition flex items-center gap-1">
          Next <i data-lucide="chevron-right" class="w-3.5 h-3.5"></i>
        </button>
      </div>
    </div>

  </main>

  <!-- FOOTER -->
  <footer class="border-t border-gray-800 bg-gray-900/90 px-6 py-6 mt-12 text-xs text-gray-400">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
      <div>
        <p class="font-bold text-white text-sm font-display">Prehistoric Archaeology of the Indian Subcontinent: GIS & Academic Database</p>
        <p class="text-gray-400 mt-1">
          Idea & Design by <strong>K.S.Chandra 2026</strong> • Contact: <a href="mailto:kavikondalaschandra@gmail.com" class="text-sky-400 underline underline-offset-2">kavikondalaschandra@gmail.com</a>
        </p>
        <p class="text-gray-500 mt-0.5">
          Curriculum Alignment: University Syllabus Paper <em>Prehistory of India – Origin and Evolution of Man in Indian Subcontinent</em>.
        </p>
      </div>
      <div class="text-right space-y-1">
        <p class="text-amber-400 font-semibold">
          Primary Reference Citation:
        </p>
        <p class="text-[11px] text-gray-300 max-w-lg">
          Vidyarthi, V. and Chauhan, P. 2025. Mapping the Indian Palaeolithic. <em>Journal of Computer Applications in Archaeology</em>, 8(1): 78–93. DOI: <a href="https://doi.org/10.5334/jcaa.148" target="_blank" class="text-sky-400 underline">10.5334/jcaa.148</a>
        </p>
        <p class="text-[10px] text-gray-500">
          Source Material: Archaeological Survey of India (ASI), <em>Indian Archaeology: A Review</em> (1953–1976).
        </p>
      </div>
    </div>
  </footer>

  <!-- COMPREHENSIVE SITE DOSSIER MODAL -->
  <div id="site-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-gray-900 border border-gray-800 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl flex flex-col">
      
      <!-- Modal Header -->
      <div class="p-5 border-b border-gray-800 flex items-start justify-between bg-gray-950/60 sticky top-0 z-10 backdrop-blur">
        <div>
          <div class="flex items-center gap-2">
            <span id="modal-period-badge" class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold border">Period</span>
            <span id="modal-dataset-badge" class="px-2 py-0.5 rounded bg-gray-800 text-gray-300 text-[10px]">Dataset</span>
            <span id="modal-excavated-badge" class="px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800/40 text-[10px]">Status</span>
          </div>
          <h2 id="modal-site-name" class="text-xl font-bold font-display text-white mt-1.5">Site Name</h2>
          <p id="modal-alt-names" class="text-xs text-gray-400 font-mono mt-0.5"></p>
        </div>
        <button onclick="closeModal()" class="p-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 space-y-5 text-xs">
        
        <!-- Geography & Field Metadata Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 p-3.5 rounded-xl bg-gray-950/60 border border-gray-800">
          <div>
            <div class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold">State / Region</div>
            <div id="modal-state" class="font-semibold text-white mt-0.5">-</div>
          </div>
          <div>
            <div class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold">District</div>
            <div id="modal-district" class="font-semibold text-white mt-0.5">-</div>
          </div>
          <div>
            <div class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold">Coordinates</div>
            <div id="modal-coords" class="font-mono text-amber-400 mt-0.5">-</div>
          </div>
          <div>
            <div class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold">IAR Volume & Page</div>
            <div id="modal-year" class="font-semibold text-sky-400 mt-0.5">-</div>
          </div>
        </div>

        <!-- Cultural & Lithic Typology -->
        <div class="space-y-3">
          <div>
            <h4 class="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5 mb-1 text-amber-400">
              <i data-lucide="hammer" class="w-3.5 h-3.5"></i> Lithic Artifacts Reported
            </h4>
            <div id="modal-typology" class="p-3 rounded-lg bg-gray-950 border border-gray-800/80 text-gray-200 leading-relaxed font-sans">
              -
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <div class="text-[10px] text-gray-400 uppercase tracking-wider font-semibold mb-0.5">Manufacturing Technique</div>
              <div id="modal-technique" class="p-2.5 rounded-lg bg-gray-950/80 border border-gray-800 text-gray-300">-</div>
            </div>
            <div>
              <div class="text-[10px] text-gray-400 uppercase tracking-wider font-semibold mb-0.5">Primary Raw Materials</div>
              <div id="modal-material" class="p-2.5 rounded-lg bg-gray-950/80 border border-gray-800 text-gray-300">-</div>
            </div>
          </div>
        </div>

        <!-- Site Context & Investigators -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <div class="text-[10px] text-gray-400 uppercase tracking-wider font-semibold mb-0.5">Geomorphic Site Context</div>
            <div id="modal-adaptation" class="p-2.5 rounded-lg bg-gray-950/80 border border-gray-800 text-gray-300">-</div>
          </div>
          <div>
            <div class="text-[10px] text-gray-400 uppercase tracking-wider font-semibold mb-0.5">Investigator(s) / Team</div>
            <div id="modal-excavator" class="p-2.5 rounded-lg bg-gray-950/80 border border-gray-800 text-gray-300">-</div>
          </div>
        </div>

        <!-- Associated Features & Fauna/Flora -->
        <div class="space-y-2">
          <div>
            <div class="text-[10px] text-gray-400 uppercase tracking-wider font-semibold mb-0.5">Palaeontology (Fossils & Faunal Remains)</div>
            <div id="modal-fauna" class="p-2.5 rounded-lg bg-gray-950/80 border border-gray-800 text-gray-300">-</div>
          </div>
          <div>
            <div class="text-[10px] text-gray-400 uppercase tracking-wider font-semibold mb-0.5">Field Notes & Comments</div>
            <div id="modal-features" class="p-2.5 rounded-lg bg-gray-950/80 border border-gray-800 text-gray-300 leading-relaxed">-</div>
          </div>
        </div>

        <!-- Academic Citation Box -->
        <div class="p-3.5 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-amber-400 flex items-center gap-1.5 uppercase text-[10px] tracking-wider">
              <i data-lucide="book-marked" class="w-3.5 h-3.5"></i> Academic Citation
            </span>
            <button onclick="copySiteCitation()" class="px-2 py-0.5 rounded bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 text-[10px] font-semibold transition">
              Copy Citation
            </button>
          </div>
          <p id="modal-references" class="text-[11px] text-gray-300 font-mono leading-relaxed">-</p>
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

  <!-- LIGHTBOX MODAL -->
  <div id="image-lightbox-modal" class="fixed inset-0 z-50 bg-black/95 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="relative max-w-4xl w-full flex flex-col items-center">
      <div class="absolute -top-12 right-0 flex items-center gap-2">
        <button onclick="closeImageLightbox()" class="p-2 rounded-full bg-gray-800 hover:bg-gray-700 text-white transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="relative w-full flex items-center justify-center bg-gray-950 rounded-2xl border border-gray-800 overflow-hidden p-2">
        <img id="lightbox-img" src="images/handaxe.jpg" alt="Lithic Specimen" class="max-h-[65vh] w-auto object-contain rounded-lg"/>
        <button onclick="prevLightboxImage()" class="absolute left-3 top-1/2 -translate-y-1/2 p-2.5 rounded-full bg-gray-900/80 hover:bg-gray-800 text-white border border-gray-700 transition">
          <i data-lucide="chevron-left" class="w-5 h-5"></i>
        </button>
        <button onclick="nextLightboxImage()" class="absolute right-3 top-1/2 -translate-y-1/2 p-2.5 rounded-full bg-gray-900/80 hover:bg-gray-800 text-white border border-gray-700 transition">
          <i data-lucide="chevron-right" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="mt-4 w-full bg-gray-900 border border-gray-800 rounded-xl p-4 text-xs space-y-1.5">
        <div class="flex items-center justify-between">
          <h4 id="lightbox-title" class="text-sm font-bold text-white font-display">Tool Plate Title</h4>
          <span id="lightbox-period-badge" class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30">Period</span>
        </div>
        <p id="lightbox-caption" class="text-gray-300 leading-relaxed"></p>
        <div class="text-[11px] text-gray-400 pt-1 border-t border-gray-800 flex flex-wrap gap-x-4">
          <span><strong>Manufacturing:</strong> <span id="lightbox-tech"></span></span>
          <span><strong>Key Localities:</strong> <span id="lightbox-sites"></span></span>
        </div>
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
    let activeDataset = 'ALL';
    let filteredSites = [...SITES_DATA];
    let currentPage = 1;
    let pageSize = 50;

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
        desc: "Bifacially flaked core/large-flake implement with pointed or amygdaloid apex, sharp bilateral cutting edges, and rounded butt.",
        tech: "Direct stone hammer percussion followed by cylinder hammer billet thinning and invasive step flaking.",
        sites: "Attirampakkam (TN), Isampur (KA), Bhimbetka (MP), Didwana (RJ), Hunsgi (KA), Chirki-Nevasa (MH)."
      }},
      cleaver: {{
        title: "Acheulian Cleaver (Transverse Bit)",
        period: "Lower Palaeolithic (1.2 Ma – 120 ka)",
        desc: "Heavy-duty bifacial tool with broad, razor-sharp transverse cutting bit formed by the intersection of dorsal and ventral flake planes.",
        tech: "Prepared block-on-block quarrying, Kombewa/side-struck large flake blanks with controlled bifacial edging.",
        sites: "Isampur (KA), Chirki-Nevasa (MH), Bhimbetka (MP), Attirampakkam (TN), Hunsgi (KA)."
      }},
      chopper: {{
        title: "Soanian / Early Pebble Chopper",
        period: "Lower Palaeolithic (Pebble-Core Tradition)",
        desc: "Massive unifacially flaked river cobble tool with natural smooth pebble cortex preserved over the butt for hand grip.",
        tech: "Direct block-on-block percussion removing large flakes along one margin to create an irregular cutting edge.",
        sites: "Soan Valley (Potwar), Guler (Beas Terraces), Sirsa Valley, Kangra, Riwat."
      }},
      levallois: {{
        title: "Levallois Prepared Core & Points",
        period: "Middle Palaeolithic (385 ka – 40 ka)",
        desc: "Standardized flake, point, or blade tool detached from a deliberately pre-shaped 'tortoise' core with radial preparation.",
        tech: "Volumetric core shaping (Levallois technique) followed by a decisive strike detaching predetermined flakes.",
        sites: "Nevasa (MH), Samnapur (MP), Attirampakkam MP phase (TN), Didwana 16R (RJ), Kalpi (UP)."
      }},
      blade: {{
        title: "Prismatic Blades & Angle Burins",
        period: "Upper Palaeolithic (45 ka – 10 ka)",
        desc: "Elongated, parallel-sided blades detached from cylindrical cores. Included burins, end-scrapers, and tanged points.",
        tech: "Punch-blade indirect percussion on prepared cylindrical cores with soft antler/bone punches.",
        sites: "Renigunta (AP), Baghor I (MP), Jwalapuram (AP), Patne (MH), Mehtakheri (MP)."
      }},
      microlith: {{
        title: "Geometric Microliths & Sickles",
        period: "Mesolithic (12 ka – 2500 BCE)",
        desc: "Minute geometric tools (lunates, trapezes, triangles) with steep blunting retouch, mounted in wooden/bone hafts.",
        tech: "Micro-burin technique and pressure flaking on chalcedony, chert, and agate cores.",
        sites: "Bagor (RJ), Sarai-Nahar Rai (UP), Mahadaha (UP), Damdama (UP), Langhnaj (GJ), Paisra (BR)."
      }},
      celt: {{
        title: "Ground & Polished Stone Celts",
        period: "Neolithic (7000 BCE – 1000 BCE)",
        desc: "Heavy-duty celts, axes, and adzes ground and hone-polished over fine-grained igneous basalt or dolerite.",
        tech: "Rough flaking, battering/pecking to shape, followed by intensive wet grinding and hone polishing.",
        sites: "Sangankallu (KA), Brahmagiri (KA), Burzahom (JK), Kuchai (OD), Daojali Hading (AS)."
      }},
      hathnora: {{
        title: "Hathnora Archaic Hominin Cranial Calvarium (Narmada Man)",
        period: "Middle Pleistocene (~250–300 ka)",
        desc: "Fossil skullcap of an archaic hominin (Homo erectus / archaic Homo sapiens) discovered by Arun Sonakia (1982) in Narmada gravels.",
        tech: "Associated in situ with Late Acheulian handaxes, cleavers, and Pleistocene megafauna (Bos namadicus).",
        sites: "Hathnora (Narmada Valley, Sehore District, Madhya Pradesh)."
      }},
      bhimbetka: {{
        title: "Prehistoric Rock Art Panel (Bhimbetka)",
        period: "Mesolithic & Upper Palaeolithic",
        desc: "Dynamic red ochre and white mineral wall paintings inside sandstone rockshelters depicting communal hunting and ritual life.",
        tech: "Natural mineral pigments (hematite, manganese oxide) mixed with animal fat/water, applied with bird feather brushes.",
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

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.remove('active', 'border-amber-500', 'text-amber-400', 'bg-amber-500/10');
        btn.classList.add('text-gray-400');
      }});

      const target = document.getElementById(tabId);
      if (target) target.classList.remove('hidden');

      const btn = document.getElementById(`btn-${{tabId}}`);
      if (btn) {{
        btn.classList.add('active', 'border-amber-500', 'text-amber-400', 'bg-amber-500/10');
        btn.classList.remove('text-gray-400');
      }}
    }}

    function copyCitation() {{
      const citationText = "Vidyarthi, V. and Chauhan, P. 2025. Mapping the Indian Palaeolithic. Journal of Computer Applications in Archaeology, 8(1): 78–93. DOI: https://doi.org/10.5334/jcaa.148";
      navigator.clipboard.writeText(citationText).then(() => {{
        alert("Citation copied to clipboard:\\n\\n" + citationText);
      }});
    }}

    function copySiteCitation() {{
      const text = document.getElementById('modal-references').innerText;
      navigator.clipboard.writeText(text).then(() => {{
        alert("Site citation copied to clipboard!");
      }});
    }}

    function setDatasetFilter(type) {{
      activeDataset = type;
      document.querySelectorAll('.dataset-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById(`btn-dataset-${{type.toLowerCase()}}`);
      if (activeBtn) activeBtn.classList.add('active');
      applyFilters();
    }}

    // Leaflet Map Initialization with Canvas for high-performance 1500+ markers
    function initMap() {{
      map = L.map('map', {{
        center: [22.5, 78.5],
        zoom: 5,
        minZoom: 4,
        maxZoom: 18,
        preferCanvas: true
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
        attribution: 'Tiles &copy; Esri &mdash; Satellite Imagery'
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
        const isExcavated = site.excavation_status === 'Yes' || (site.excavation_seasons && site.excavation_seasons.includes('Excavated'));

        const marker = L.circleMarker([site.latitude, site.longitude], {{
          radius: isExcavated ? 6.5 : 4.5,
          fillColor: config.color,
          color: isExcavated ? '#ffffff' : '#1e293b',
          weight: isExcavated ? 1.5 : 0.8,
          opacity: 1,
          fillOpacity: isExcavated ? 0.95 : 0.8
        }});

        const yearLabel = site.iar_volume ? `IAR ${{site.iar_volume}}` : (site.year_of_discovery || '');
        marker.bindTooltip(`
          <div class="text-xs p-1">
            <div class="font-bold text-white">${{site.site_name}}</div>
            <div class="text-amber-400 font-semibold">${{site.period}}</div>
            <div class="text-gray-300 text-[10px]">${{site.district || ''}}, ${{site.state_province || ''}} (${{yearLabel}})</div>
            <div class="text-gray-400 text-[10px] mt-0.5 truncate max-w-[200px]">${{site.tool_typology || ''}}</div>
            <div class="text-sky-400 text-[9px] mt-0.5">${{site.dataset_source || ''}}</div>
          </div>
        `, {{ direction: 'top', offset: [0, -4], className: 'custom-tooltip' }});

        marker.on('click', () => {{
          openSiteModal(site);
        }});

        markersLayer.addLayer(marker);
      }});
    }}

    let zoneChart;

    function initCharts() {{
      const zCtx = document.getElementById('zoneChart').getContext('2d');
      const counts = {{}};
      filteredSites.forEach(s => {{
        const st = s.state_province || 'Other';
        counts[st] = (counts[st] || 0) + 1;
      }});

      // Sort and take top 12 states
      const sortedEntries = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 12);

      zoneChart = new Chart(zCtx, {{
        type: 'bar',
        data: {{
          labels: sortedEntries.map(e => e[0]),
          datasets: [{{
            label: 'Reported Sites',
            data: sortedEntries.map(e => e[1]),
            backgroundColor: [
              '#f43f5e', '#f59e0b', '#38bdf8', '#818cf8', '#10b981', '#a855f7',
              '#06b6d4', '#ec4899', '#fbbf24', '#34d399', '#60a5fa', '#94a3b8'
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
                  return ` ${{context.raw}} Documented Sites`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#9ca3af', font: {{ size: 10 }} }}, grid: {{ color: '#1f2937' }} }},
            y: {{ ticks: {{ color: '#e5e7eb', font: {{ size: 11, weight: '600' }} }}, grid: {{ display: false }} }}
          }}
        }}
      }});
    }}

    function updateCharts() {{
      if (!zoneChart) return;
      const counts = {{}};
      filteredSites.forEach(s => {{
        const st = s.state_province || 'Other';
        counts[st] = (counts[st] || 0) + 1;
      }});
      const sortedEntries = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 12);
      zoneChart.data.labels = sortedEntries.map(e => e[0]);
      zoneChart.data.datasets[0].data = sortedEntries.map(e => e[1]);
      zoneChart.update();
    }}

    function renderTable() {{
      const tbody = document.getElementById('sites-table-body');
      tbody.innerHTML = '';

      const total = filteredSites.length;
      document.getElementById('filtered-count').innerText = total.toLocaleString();
      document.getElementById('total-count').innerText = SITES_DATA.length.toLocaleString();

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
        const yearDisplay = s.iar_volume ? `IAR ${{s.iar_volume}} (p.${{s.iar_page ? s.iar_page.replace('(pdf)', '') : ''}})` : (s.year_of_discovery || '-');
        const contextDisplay = s.site_context || (s.associated_features ? s.associated_features.slice(0, 45) + '...' : '-');

        tr.innerHTML = `
          <td class="px-3 py-2.5 font-bold text-white whitespace-nowrap">
            <div class="flex items-center gap-1.5">
              <span>${{s.site_name}}</span>
              ${{s.excavation_status === 'Yes' ? '<span class="px-1.5 py-0.2 rounded text-[9px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Excavated</span>' : ''}}
            </div>
          </td>
          <td class="px-3 py-2.5 whitespace-nowrap">
            <span class="inline-flex items-center gap-1.5 font-semibold" style="color: ${{config.color}}">
              <span class="w-2 h-2 rounded-full" style="background-color: ${{config.color}}"></span>
              ${{s.period}}
            </span>
          </td>
          <td class="px-3 py-2.5 text-gray-300 whitespace-nowrap">${{s.state_province || '-'}}</td>
          <td class="px-3 py-2.5 text-gray-400 whitespace-nowrap">${{s.district || '-'}}</td>
          <td class="px-3 py-2.5 text-sky-400 whitespace-nowrap font-mono text-[11px]">${{yearDisplay}}</td>
          <td class="px-3 py-2.5 text-gray-300 max-w-xs truncate" title="${{s.tool_typology}}">${{s.tool_typology || '-'}}</td>
          <td class="px-3 py-2.5 text-gray-400 max-w-xs truncate" title="${{s.excavator_discoverer}}">${{s.excavator_discoverer || '-'}}</td>
          <td class="px-3 py-2.5 text-gray-400 max-w-xs truncate" title="${{contextDisplay}}">${{contextDisplay}}</td>
          <td class="px-3 py-2.5 text-center whitespace-nowrap">
            <button onclick="openSiteModalById(${{s.site_id}})" class="px-2.5 py-1 rounded-md bg-gray-800 hover:bg-amber-500 hover:text-black text-gray-300 text-[11px] font-semibold transition">
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
        `Showing all ${{total.toLocaleString()}} archaeological sites` :
        `Showing ${{start + 1}} to ${{Math.min(end, total)}} of ${{total.toLocaleString()}} sites (Page ${{currentPage}} of ${{maxPages}})`;

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

      document.getElementById('stat-total-sites').innerText = counts['Total'].toLocaleString();
      document.getElementById('stat-lp-sites').innerText = counts['Lower Paleolithic'].toLocaleString();
      document.getElementById('stat-mp-sites').innerText = counts['Middle Paleolithic'].toLocaleString();
      document.getElementById('stat-up-sites').innerText = counts['Upper Paleolithic'].toLocaleString();
      document.getElementById('stat-meso-sites').innerText = counts['Mesolithic'].toLocaleString();
      document.getElementById('stat-neo-sites').innerText = counts['Neolithic'].toLocaleString();
    }}

    function applyFilters() {{
      const query = document.getElementById('search-input').value.toLowerCase().trim();
      const period = document.getElementById('period-filter').value;
      const state = document.getElementById('state-filter').value;
      const volume = document.getElementById('volume-filter').value;
      const excavatedOnly = document.getElementById('excavated-only').checked;
      const faunaOnly = document.getElementById('fauna-only').checked;
      const rockArtOnly = document.getElementById('rock-art-only').checked;
      const preciseOnly = document.getElementById('precise-only').checked;

      filteredSites = SITES_DATA.filter(s => {{
        // Dataset filter
        if (activeDataset === 'IAR' && !s.iar_volume) return false;
        if (activeDataset === 'LANDMARK' && s.dataset_source !== 'Syllabus Landmark Benchmark') return false;
        if (activeDataset === 'EXCAVATED' && s.excavation_status !== 'Yes' && !(s.excavation_seasons && s.excavation_seasons.includes('Excavated'))) return false;

        // Dropdown filters
        if (period !== 'ALL' && s.period !== period) return false;
        if (state !== 'ALL' && s.state_province !== state) return false;
        if (volume !== 'ALL' && s.iar_volume !== volume) return false;

        // Checkbox filters
        if (excavatedOnly && s.excavation_status !== 'Yes' && !(s.excavation_seasons && s.excavation_seasons.includes('Excavated'))) return false;
        if (faunaOnly && (!s.palaeofauna_palaeoflora || s.palaeofauna_palaeoflora === 'None reported')) return false;
        if (rockArtOnly && (!s.rock_art_details || s.rock_art_details === 'None recorded')) return false;
        if (preciseOnly && s.location_integrity !== 'Precise') return false;

        // Text query
        if (query) {{
          const target = [
            s.site_name, s.alternative_names, s.state_province, s.district, s.river_basin,
            s.excavator_discoverer, s.tool_typology, s.primary_raw_materials, s.iar_volume,
            s.site_context, s.comments, s.associated_features
          ].filter(Boolean).join(' ').toLowerCase();
          if (!target.includes(query)) return false;
        }}
        return true;
      }});

      currentPage = 1;
      plotMarkers();
      renderTable();
      updateKPICards();
      updateCharts();
    }}

    function resetFilters() {{
      activeDataset = 'ALL';
      document.querySelectorAll('.dataset-btn').forEach(btn => btn.classList.remove('active'));
      document.getElementById('btn-dataset-all').classList.add('active');

      document.getElementById('search-input').value = '';
      document.getElementById('period-filter').value = 'ALL';
      document.getElementById('state-filter').value = 'ALL';
      document.getElementById('volume-filter').value = 'ALL';
      document.getElementById('excavated-only').checked = false;
      document.getElementById('fauna-only').checked = false;
      document.getElementById('rock-art-only').checked = false;
      document.getElementById('precise-only').checked = false;
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
      document.getElementById('modal-alt-names').innerText = site.alternative_names ? `Alternate / Citation: ${{site.alternative_names}}` : '';

      const badge = document.getElementById('modal-period-badge');
      badge.innerText = site.period;
      badge.className = `px-2.5 py-0.5 rounded-full text-[11px] font-semibold border ${{config.badge}}`;

      document.getElementById('modal-dataset-badge').innerText = site.dataset_source || 'Archaeological Record';
      
      const excBadge = document.getElementById('modal-excavated-badge');
      const isExcavated = site.excavation_status === 'Yes' || (site.excavation_seasons && site.excavation_seasons.includes('Excavated'));
      excBadge.innerText = isExcavated ? 'Excavated Site' : 'Exploration / Surface Survey';
      excBadge.className = isExcavated ? 'px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800/40 text-[10px]' : 'px-2 py-0.5 rounded bg-gray-800 text-gray-400 text-[10px]';

      document.getElementById('modal-state').innerText = site.state_province || '-';
      document.getElementById('modal-district').innerText = site.district || '-';
      document.getElementById('modal-coords').innerText = `${{site.latitude}}°N, ${{site.longitude}}°E (${{site.location_integrity || 'Centroid'}})`;

      const yearDisplay = site.iar_volume ? `IAR ${{site.iar_volume}} (${{site.iar_page || ''}})` : (site.year_of_discovery || 'Reported');
      document.getElementById('modal-year').innerText = yearDisplay;

      document.getElementById('modal-excavator').innerText = site.excavator_discoverer || 'Archaeological Survey Team';
      document.getElementById('modal-typology').innerText = site.tool_typology || 'Reported Palaeolithic stone implements';
      document.getElementById('modal-technique').innerText = site.manufacturing_technique || 'Lithic flaking technique';
      document.getElementById('modal-material').innerText = site.primary_raw_materials || 'Quartzite / Siliceous Fluvial Minerals';

      document.getElementById('modal-adaptation').innerText = site.site_context || site.environmental_adaptation || 'Fluvial terrace / alluvial bed';
      document.getElementById('modal-fauna').innerText = site.palaeofauna_palaeoflora || 'None reported';
      document.getElementById('modal-features').innerText = site.comments || site.associated_features || 'Documented in archaeological survey archives.';

      document.getElementById('modal-references').innerText = site.key_references || 'Archival report documented in Indian Archaeology: A Review.';

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

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully wrote updated application index.html ({len(html_content)} bytes) at {index_path}!")
