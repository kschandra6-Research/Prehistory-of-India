import os
import re

def get_foundations_tabs(is_art=False):
    prefix = "art-" if is_art else ""
    fn_open = f"openFoundationsModalArtifact" if is_art else "openFoundationsModal"
    badge_bg = "bg-slate-950" if is_art else "bg-gray-950"
    border_color = "border-slate-800" if is_art else "border-gray-800"
    border_hover_amber = "hover:border-amber-500/80"
    border_hover_rose = "hover:border-rose-500/80"
    border_hover_emerald = "hover:border-emerald-500/80"
    text_muted = "text-slate-400" if is_art else "text-gray-400"
    text_sub = "text-slate-300" if is_art else "text-gray-300"

    html = f"""      <!-- TAB 2: GEOLOGICAL TIME SCALE -->
      <div id="{prefix}tab-geology" class="{prefix}tab-content hidden space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-xl {badge_bg} border {border_color}">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-amber-400 font-bold uppercase text-[11px] tracking-wider">Chronostratigraphy & Quaternary Geochronology</span>
              <span class="text-[10px] text-gray-400 font-mono">1.5 Ma – 1000 BCE</span>
            </div>
            <p class="text-xs {text_muted} mt-0.5">Glacial/interglacial correlations, geomagnetic chrons, and diagnostic Indian lithic industries.</p>
          </div>
          <button onclick="{fn_open}('geology')" class="px-4 py-2 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-semibold flex items-center gap-1.5 transition shadow">
            <i data-lucide="maximize-2" class="w-3.5 h-3.5"></i> 🔍 Click to Enlarge Geological Time Scale
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
          <div onclick="{fn_open}('geology')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_amber} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <span class="text-rose-400 font-bold uppercase tracking-wider text-[11px]">Lower / Early Pleistocene</span>
              <span class="text-amber-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <div class="text-gray-400 font-mono text-[10px]">2.58 – 0.78 Ma</div>
            <h3 class="text-white font-bold text-sm">Matuyama Reversed Chron</h3>
            <p class="{text_muted} leading-relaxed">
              Onset of Northern Hemisphere glaciation; Siwalik Pinjor faunal turnover. Early Acheulian stone tools emerge in peninsular India (Attirampakkam 1.51 Ma; Isampur 1.27 Ma).
            </p>
            <div class="pt-2 text-[11px] text-amber-300 font-medium">MIS Stages 63 to 19 • Attirampakkam 1.51 Ma • Isampur</div>
          </div>

          <div onclick="{fn_open}('geology')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_amber} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <span class="text-amber-400 font-bold uppercase tracking-wider text-[11px]">Middle Pleistocene</span>
              <span class="text-amber-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <div class="text-gray-400 font-mono text-[10px]">780 – 126 ka</div>
            <h3 class="text-white font-bold text-sm">Brunhes Normal Chron</h3>
            <p class="{text_muted} leading-relaxed">
              Climax of Acheulian tradition (handaxes & cleavers); hominin occupation in Narmada, Hunsgi, and Kortallayar basins. Hathnora cranial calvarium (*Narmada Man*) in Surajkund gravels (~250–300 ka).
            </p>
            <div class="pt-2 text-[11px] text-amber-300 font-medium">MIS Stages 19 to 6 • Acheulian & Archaic Hominins</div>
          </div>

          <div onclick="{fn_open}('geology')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_amber} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <span class="text-purple-400 font-bold uppercase tracking-wider text-[11px]">Late / Upper Pleistocene</span>
              <span class="text-amber-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <div class="text-gray-400 font-mono text-[10px]">126 – 11.7 ka</div>
            <h3 class="text-white font-bold text-sm">Last Glacial Cycle & Toba</h3>
            <p class="{text_muted} leading-relaxed">
              Transition from Middle Palaeolithic (Levallois, scrapers) to Upper Palaeolithic blade-burin industries. Catastrophic Youngest Toba Tuff (74 ka) ash event with continuous human occupation at Jwalapuram.
            </p>
            <div class="pt-2 text-[11px] text-amber-300 font-medium">MIS Stages 5 to 2 • Toba Tephra (74 ka) • LGM (21 ka)</div>
          </div>

          <div onclick="{fn_open}('geology')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_amber} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <span class="text-emerald-400 font-bold uppercase tracking-wider text-[11px]">Holocene Epoch</span>
              <span class="text-amber-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <div class="text-gray-400 font-mono text-[10px]">11.7 ka – Present</div>
            <h3 class="text-white font-bold text-sm">Post-Glacial Warm Optimum</h3>
            <p class="{text_muted} leading-relaxed">
              Intensification of southwest monsoon; emergence of intensive Mesolithic foraging, geometric microliths, rock art (Bhimbetka), followed by early Neolithic agriculture (Mehrgarh, Belan Valley, Kashmir).
            </p>
            <div class="pt-2 text-[11px] text-amber-300 font-medium">MIS Stage 1 • Holocene Climatic Optimum • Farming</div>
          </div>
        </div>
      </div>

      <!-- TAB 3: HUMAN EVOLUTION -->
      <div id="{prefix}tab-evolution" class="{prefix}tab-content hidden space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-xl {badge_bg} border {border_color}">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-rose-400 font-bold uppercase text-[11px] tracking-wider">Palaeoanthropology & Hominin Evolution</span>
              <span class="text-[10px] text-gray-400 font-mono">Archaic to AMH</span>
            </div>
            <p class="text-xs {text_muted} mt-0.5">The Hathnora hominin calvarium (*Narmada Man*), Toba ash AMH continuity, and Mesolithic osteology.</p>
          </div>
          <button onclick="{fn_open}('evolution')" class="px-4 py-2 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/40 text-xs font-semibold flex items-center gap-1.5 transition shadow">
            <i data-lucide="maximize-2" class="w-3.5 h-3.5"></i> 🔍 Click to Enlarge Human Evolution
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div onclick="{fn_open}('evolution')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_rose} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2 text-rose-400 font-bold uppercase text-[11px]">
                <i data-lucide="skull" class="w-4 h-4"></i> The Hathnora Hominin Calvarium
              </div>
              <span class="text-rose-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <h3 class="text-white font-bold text-sm">Arun Sonakia Discovery (Dec 5, 1982)</h3>
            <p class="{text_muted} leading-relaxed">
              Discovered at Hathnora on northern bank of Narmada River (Sehore district, MP). Stratigraphically embedded in cemented boulder conglomerate (Surajkund Formation). Classified as archaic *Homo sapiens* / advanced *Homo erectus*.
            </p>
            <div class="bg-black/40 p-2.5 rounded-lg border {border_color} text-[11px] space-y-1 {text_sub}">
              <div><strong>Cranial Capacity:</strong> 1,155 – 1,421 cc (robust encephalization)</div>
              <div><strong>Morphology:</strong> Continuous prominent supraorbital torus, thick vault</div>
              <div><strong>Associated Finds:</strong> Acheulian bifaces, fossil *Bos namadicus*</div>
            </div>
          </div>

          <div onclick="{fn_open}('evolution')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_rose} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2 text-amber-400 font-bold uppercase text-[11px]">
                <i data-lucide="bone" class="w-4 h-4"></i> Post-Cranial Clavicle & Anatomy
              </div>
              <span class="text-rose-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <h3 class="text-white font-bold text-sm">A.A. Sankhyan Discovery (1997)</h3>
            <p class="{text_muted} leading-relaxed">
              Discovery of complete right human clavicle and rib fragment at Hathnora. Morphometric analysis suggests a diminutive female individual (~130–140 cm in stature), indicating anatomical polymorphism in Middle Pleistocene Indian hominins.
            </p>
            <div class="bg-black/40 p-2.5 rounded-lg border {border_color} text-[11px] space-y-1 {text_sub}">
              <div><strong>Skeletal Evidence:</strong> Human clavicle and second rib fragment</div>
              <div><strong>Chronology:</strong> Middle to early Late Pleistocene (~250–150 ka)</div>
              <div><strong>Palaeopathology:</strong> Robust muscular insertions, no trauma</div>
            </div>
          </div>

          <div onclick="{fn_open}('evolution')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_rose} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2 text-emerald-400 font-bold uppercase text-[11px]">
                <i data-lucide="activity" class="w-4 h-4"></i> Modern Human Dispersal & Burials
              </div>
              <span class="text-rose-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <h3 class="text-white font-bold text-sm">Homo sapiens sapiens Dispersal</h3>
            <p class="{text_muted} leading-relaxed">
              Behavioral and osteological evidence of anatomically modern humans:
            </p>
            <ul class="space-y-1.5 {text_sub} text-[11px]">
              <li>• <strong>Jwalapuram (AP):</strong> Lithic tool continuity across the 74 ka Toba ash event.</li>
              <li>• <strong>Kurnool Caves (AP):</strong> Upper Palaeolithic bone implements and awls.</li>
              <li>• <strong>Ganga Valley Burials:</strong> Sarai-Nahar Rai, Mahadaha, Damdama: complete Mesolithic skeletons, extended burials, bone ornaments, tall stature (~180 cm).</li>
              <li>• <strong>Symbolic Expression:</strong> Engraved ostrich eggshells at Patne & Mehtakheri (25–40 ka).</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- TAB 4: PALAEOENVIRONMENT (FLORA & FAUNA) -->
      <div id="{prefix}tab-palaeoenv" class="{prefix}tab-content hidden space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-xl {badge_bg} border {border_color}">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-emerald-400 font-bold uppercase text-[11px] tracking-wider">Palaeoenvironment, Flora & Fauna</span>
              <span class="text-[10px] text-gray-400 font-mono">Pleistocene to Holocene</span>
            </div>
            <p class="text-xs {text_muted} mt-0.5">Pleistocene mammalian megafauna, post-glacial faunal turnovers, and origins of agriculture.</p>
          </div>
          <button onclick="{fn_open}('palaeoenv')" class="px-4 py-2 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 text-xs font-semibold flex items-center gap-1.5 transition shadow">
            <i data-lucide="maximize-2" class="w-3.5 h-3.5"></i> 🔍 Click to Enlarge Prehistoric Flora & Fauna
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div onclick="{fn_open}('palaeoenv')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_emerald} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2 text-amber-400 font-bold uppercase text-[11px]">
                <i data-lucide="binary" class="w-4 h-4"></i> Pleistocene Mammalian Megafauna
              </div>
              <span class="text-emerald-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <h3 class="text-white font-bold text-sm">Extinct Fauna of Central & Peninsular India</h3>
            <p class="{text_muted} leading-relaxed">
              Fossil beds in Godavari, Narmada, Krishna, and Manjra alluvial valleys reveal heavy savannah and perennial riparian ecosystems:
            </p>
            <div class="space-y-1 {text_sub} text-[11px]">
              <div>• <strong>Bos namadicus:</strong> Extinct giant wild ox with 1.5–2.0 m horn cores.</div>
              <div>• <strong>Elephas namadicus:</strong> Straight-tusked archaic elephant with frontal crest.</div>
              <div>• <strong>Hexaprotodon palaeindicus:</strong> Six-incisor river hippopotamus.</div>
              <div>• <strong>Stegodon namadicus:</strong> Archaic proboscidean with transverse enamel ridges.</div>
              <div>• <strong>Equus namadicus:</strong> Large Pleistocene wild horse.</div>
            </div>
          </div>

          <div onclick="{fn_open}('palaeoenv')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_emerald} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2 text-emerald-400 font-bold uppercase text-[11px]">
                <i data-lucide="paw-print" class="w-4 h-4"></i> Holocene Ecological Shift
              </div>
              <span class="text-emerald-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <h3 class="text-white font-bold text-sm">Post-Glacial Faunal Turnover</h3>
            <p class="{text_muted} leading-relaxed">
              Extinction of swamp-dwelling *Hexaprotodon* and *Stegodon* at the Pleistocene-Holocene boundary, replaced by agile open-woodland and grassland species:
            </p>
            <div class="space-y-1 {text_sub} text-[11px]">
              <div>• <strong>Bos gaurus (Indian Gaur):</strong> Maintained in central highlands.</div>
              <div>• <strong>Antilope cervicapra (Blackbuck) & Gazella:</strong> Thar & Deccan.</div>
              <div>• <strong>Axis axis (Chital) & Rucervus:</strong> Ganga lake margins.</div>
              <div>• <strong>Sus scrofa (Wild Boar):</strong> Universal prey in Mesolithic middens.</div>
              <div>• <strong>Early Domesticates:</strong> Cattle, sheep, goat emerging in Neolithic.</div>
            </div>
          </div>

          <div onclick="{fn_open}('palaeoenv')" class="{badge_bg} p-4 rounded-xl border {border_color} {border_hover_emerald} hover:scale-[1.01] transition group cursor-pointer space-y-2 relative">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2 text-cyan-400 font-bold uppercase text-[11px]">
                <i data-lucide="sprout" class="w-4 h-4"></i> Prehistoric Flora & Cultivation
              </div>
              <span class="text-emerald-400 font-mono text-[10px] group-hover:underline flex items-center gap-1">🔍 Enlarge</span>
            </div>
            <h3 class="text-white font-bold text-sm">Pollen Profiles & Early Cultivation</h3>
            <p class="{text_muted} leading-relaxed">
              Macrobotanical, phytolith, and palynological studies reveal ancient vegetation and transitions to farming:
            </p>
            <div class="space-y-1.5 {text_sub} text-[11px]">
              <div>• <strong>Rice (Oryza sativa & O. nivara):</strong> Belan Valley (Chopani-Mando, Koldihwa, Lahuradewa) early exploitation & 7th–6th millennium BCE cultivated grains.</div>
              <div>• <strong>Barley (Hordeum) & Wheat:</strong> Mehrgarh (Baluchistan) and Burzahom (Kashmir) show early winter-crop agricultural packages.</div>
              <div>• <strong>Palynology:</strong> Didwana and Sambhar lake cores document heightened monsoon rainfall and freshwater vegetation 9000–5000 BP.</div>
            </div>
          </div>
        </div>
      </div>"""
    return html

print("get_foundations_tabs defined successfully.")
def get_foundations_modal(is_art=False):
    prefix = "art-" if is_art else ""
    modal_id = f"{prefix}foundations-enlarge-modal"
    fn_close = f"closeFoundationsModalArtifact" if is_art else "closeFoundationsModal"
    fn_switch = f"switchFoundationsModalSectionArtifact" if is_art else "switchFoundationsModalSection"
    fn_lightbox = f"openLightboxArtifact" if is_art else "openImageLightbox"
    badge_bg = "bg-slate-950" if is_art else "bg-gray-950"
    card_bg = "bg-slate-900/90" if is_art else "bg-gray-900/90"
    border_color = "border-slate-800" if is_art else "border-gray-800"
    text_muted = "text-slate-400" if is_art else "text-gray-400"
    text_sub = "text-slate-300" if is_art else "text-gray-300"

    html = f"""  <!-- PREHISTORIC FOUNDATIONS & PALAEOENVIRONMENTAL ENLARGE MODAL -->
  <div id="{modal_id}" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden flex items-center justify-center p-3 md:p-6 animate-in fade-in duration-200">
    <div class="{badge_bg} border {border_color} w-full max-w-6xl max-h-[92vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden text-slate-200">
      
      <!-- Sticky Modal Header -->
      <div class="p-4 md:px-6 border-b {border_color} flex flex-wrap items-center justify-between gap-3 bg-black/50 backdrop-blur">
        <div>
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wider uppercase bg-amber-500/20 text-amber-300 border border-amber-500/30">Archaeological Research Archive</span>
            <span class="text-xs text-gray-400 font-mono">1.5 Ma – 1000 BCE</span>
          </div>
          <h2 class="text-base md:text-lg font-bold font-display text-white mt-1">Prehistoric Foundations & Palaeoenvironmental Archive</h2>
          <p class="text-xs {text_muted}">High-Resolution Reading & Comprehensive Scientific Compendium of South Asian Prehistory</p>
        </div>

        <!-- Modal Navigation Tabs -->
        <div class="flex items-center gap-1.5 {badge_bg} p-1 rounded-xl border {border_color}">
          <button id="{prefix}btn-modal-geology" onclick="{fn_switch}('geology')" class="{prefix}foundations-modal-tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold border transition flex items-center gap-1.5 whitespace-nowrap bg-amber-500/20 border-amber-500 text-amber-300">
            <i data-lucide="layers" class="w-3.5 h-3.5"></i> Geological Time Scale
          </button>
          <button id="{prefix}btn-modal-evolution" onclick="{fn_switch}('evolution')" class="{prefix}foundations-modal-tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold border transition flex items-center gap-1.5 whitespace-nowrap border-transparent {text_muted} hover:text-white">
            <i data-lucide="skull" class="w-3.5 h-3.5"></i> Human Evolution
          </button>
          <button id="{prefix}btn-modal-palaeoenv" onclick="{fn_switch}('palaeoenv')" class="{prefix}foundations-modal-tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold border transition flex items-center gap-1.5 whitespace-nowrap border-transparent {text_muted} hover:text-white">
            <i data-lucide="trees" class="w-3.5 h-3.5"></i> Prehistoric Flora & Fauna
          </button>
        </div>

        <!-- Close Button -->
        <button onclick="{fn_close}()" class="px-3.5 py-1.5 rounded-xl bg-gray-900 hover:bg-rose-900/60 text-gray-300 hover:text-rose-200 border {border_color} hover:border-rose-700/50 transition text-xs font-semibold flex items-center gap-1.5 shadow">
          <i data-lucide="x" class="w-4 h-4"></i> Close
        </button>
      </div>

      <!-- Scrollable Modal Content Container -->
      <div class="flex-1 overflow-y-auto p-5 md:p-8 space-y-8 text-sm leading-relaxed">
        
        <!-- ========================================== -->
        <!-- SECTION 1: GEOLOGICAL TIME SCALE           -->
        <!-- ========================================== -->
        <div id="{prefix}foundations-modal-geology" class="{prefix}foundations-modal-section space-y-6">
          <div class="border-b {border_color} pb-4">
            <div class="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-wider mb-1">
              <i data-lucide="layers" class="w-4 h-4"></i> Chronostratigraphy & Quaternary Geochronology
            </div>
            <h3 class="text-xl md:text-2xl font-bold font-display text-white">Geological Time Scale of South Asian Prehistory</h3>
            <p class="text-sm {text_sub} mt-1 max-w-4xl leading-relaxed">
              Quaternary stratigraphy in the Indian Subcontinent is correlated through continental river terraces, alluvial deposits, lacustrine pollen cores, palaeomagnetic chrons (Matuyama/Brunhes boundary), and absolute numerical dating methods ($^{{26}}\\text{{Al}}/ 10Be\\text{{Be}}$ cosmogenic burial, OSL, ESR, and $^{{14}}\\text{{C}}$).
            </p>
          </div>

          <!-- Chronological Pillars -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="{card_bg} p-4 rounded-xl border border-rose-500/30 space-y-2">
              <div class="flex items-center justify-between">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-rose-500/20 text-rose-300 border border-rose-500/30">Lower Pleistocene</span>
                <span class="text-xs font-mono text-gray-400 font-bold">2.58 – 0.78 Ma</span>
              </div>
              <h4 class="text-white font-bold text-sm">Matuyama Reversed Chron</h4>
              <p class="text-xs {text_sub} leading-relaxed">
                Northern Hemisphere Glaciation onset, Siwalik Pinjor-Tatrot faunal turnover. Early Acheulian stone tools emerge in peninsular India (Attirampakkam dated to 1.51 Ma; Isampur quarry 1.27 Ma).
              </p>
              <div class="pt-2 border-t {border_color} text-[11px] text-amber-400 font-medium">
                MIS 63 to 19 • Attirampakkam 1.51 Ma • Isampur
              </div>
            </div>

            <div class="{card_bg} p-4 rounded-xl border border-amber-500/30 space-y-2">
              <div class="flex items-center justify-between">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-amber-500/20 text-amber-300 border border-amber-500/30">Middle Pleistocene</span>
                <span class="text-xs font-mono text-gray-400 font-bold">780 – 126 ka</span>
              </div>
              <h4 class="text-white font-bold text-sm">Brunhes Normal Chron</h4>
              <p class="text-xs {text_sub} leading-relaxed">
                Climax of Acheulian tradition (bifacial thinning, handaxes & cleavers). Hathnora cranial calvarium (*Narmada Man*) found in basal gravels of Surajkund Formation (~250–300 ka) with *Bos namadicus*.
              </p>
              <div class="pt-2 border-t {border_color} text-[11px] text-amber-400 font-medium">
                MIS 19 to 6 • Hathnora Calvarium • Hunsgi Climax
              </div>
            </div>

            <div class="{card_bg} p-4 rounded-xl border border-purple-500/30 space-y-2">
              <div class="flex items-center justify-between">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-purple-500/20 text-purple-300 border border-purple-500/30">Late Pleistocene</span>
                <span class="text-xs font-mono text-gray-400 font-bold">126 – 11.7 ka</span>
              </div>
              <h4 class="text-white font-bold text-sm">Last Glacial Cycle & Toba</h4>
              <p class="text-xs {text_sub} leading-relaxed">
                Nevasan flake industry transition to Upper Palaeolithic blade-burins. Catastrophic Youngest Toba Tuff (74 ka) ash event documented with continuous human occupation at Jwalapuram (AP).
              </p>
              <div class="pt-2 border-t {border_color} text-[11px] text-amber-400 font-medium">
                MIS 5 to 2 • Toba Tephra (74 ka) • LGM (21 ka)
              </div>
            </div>

            <div class="{card_bg} p-4 rounded-xl border border-emerald-500/30 space-y-2">
              <div class="flex items-center justify-between">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Holocene Epoch</span>
                <span class="text-xs font-mono text-gray-400 font-bold">11.7 ka – Present</span>
              </div>
              <h4 class="text-white font-bold text-sm">Post-Glacial Warm Optimum</h4>
              <p class="text-xs {text_sub} leading-relaxed">
                Monsoon intensification; emergence of intensive Mesolithic geometric microliths, rock art (Bhimbetka), followed by early Neolithic agriculture (Mehrgarh, Belan/Ganga, Kashmir, Ashmounds).
              </p>
              <div class="pt-2 border-t {border_color} text-[11px] text-amber-400 font-medium">
                MIS 1 • Microliths & Rock Art • Early Farming
              </div>
            </div>
          </div>

          <!-- Master Table -->
          <div class="{card_bg} rounded-xl border {border_color} overflow-hidden space-y-3 p-4">
            <div class="flex items-center justify-between">
              <h4 class="text-white font-bold text-sm flex items-center gap-2">
                <i data-lucide="table" class="w-4 h-4 text-amber-400"></i> Master Chronostratigraphic Correlation Table of South Asia
              </h4>
              <span class="text-[11px] text-gray-400 font-mono">Stratigraphy & Industrial Succession</span>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead>
                  <tr class="{badge_bg} text-gray-300 border-b {border_color} font-semibold">
                    <th class="p-3">Epoch / Sub-Epoch</th>
                    <th class="p-3">Numerical Age</th>
                    <th class="p-3">Palaeomagnetic & MIS</th>
                    <th class="p-3">Palaeoclimate Dynamics</th>
                    <th class="p-3">Diagnostic Lithic Industry</th>
                    <th class="p-3">Geological Horizons & Formations</th>
                    <th class="p-3">Benchmark Sites</th>
                  </tr>
                </thead>
                <tbody class="divide-y {border_color} {text_sub}">
                  <tr class="hover:bg-white/5 transition">
                    <td class="p-3 font-bold text-rose-400">Lower / Early Pleistocene</td>
                    <td class="p-3 font-mono text-gray-300">2.58 – 0.78 Ma</td>
                    <td class="p-3">Matuyama Chron (Reversed)<br><span class="text-gray-400 text-[11px]">MIS 63 – MIS 19</span></td>
                    <td class="p-3">Onset of Northern Glaciation cycles, alternating semi-arid & humid phases</td>
                    <td class="p-3 font-medium text-white">Early Acheulian (Large Flake Acheulian, thick bifaces) & Pebble Choppers</td>
                    <td class="p-3">Boulder Conglomerate (Siwalik), Ferricrete basal gravels (Kortallayar)</td>
                    <td class="p-3 text-amber-300 font-semibold">Attirampakkam (1.51 Ma), Isampur (1.27 Ma), Soan Valley</td>
                  </tr>
                  <tr class="hover:bg-white/5 transition">
                    <td class="p-3 font-bold text-amber-400">Middle Pleistocene</td>
                    <td class="p-3 font-mono text-gray-300">780 – 126 ka</td>
                    <td class="p-3">Brunhes Chron (Normal)<br><span class="text-gray-400 text-[11px]">MIS 19 – MIS 6</span></td>
                    <td class="p-3">100-kyr orbital glacial-interglacial cycles, strong monsoonal pulses</td>
                    <td class="p-3 font-medium text-white">Late Acheulian (symmetric ovates, soft-hammer handaxes, cleavers)</td>
                    <td class="p-3">Surajkund Formation (Narmada), Pravara gravels (Chirki-Nevasa)</td>
                    <td class="p-3 text-amber-300 font-semibold">Hathnora (~250 ka), Hunsgi-Baichbal, Bhimbetka III F-23, Didwana</td>
                  </tr>
                  <tr class="hover:bg-white/5 transition">
                    <td class="p-3 font-bold text-purple-400">Late / Upper Pleistocene</td>
                    <td class="p-3 font-mono text-gray-300">126 – 11.7 ka</td>
                    <td class="p-3">Last Glacial Cycle<br><span class="text-gray-400 text-[11px]">MIS 5 – MIS 2 (LGM 21 ka)</span></td>
                    <td class="p-3">Progressive aridity peaking at LGM; Youngest Toba Tuff ashfall at 74 ka</td>
                    <td class="p-3 font-medium text-white">Middle Palaeolithic (Nevasan, Levallois flakes) to Upper Palaeolithic (blades, burins, bone tools)</td>
                    <td class="p-3">Jurreru alluvial silt & Toba ash (Jwalapuram), Patne loessic silt</td>
                    <td class="p-3 text-amber-300 font-semibold">Jwalapuram (74 ka), Nevasa, Patne, Kurnool Caves, Mehtakheri</td>
                  </tr>
                  <tr class="hover:bg-white/5 transition">
                    <td class="p-3 font-bold text-emerald-400">Holocene Epoch</td>
                    <td class="p-3 font-mono text-gray-300">11.7 ka – Present</td>
                    <td class="p-3">Holocene Interglacial<br><span class="text-gray-400 text-[11px]">MIS 1</span></td>
                    <td class="p-3">Post-glacial monsoon optimum (9–5 ka BP), lacustrine wetland expansion</td>
                    <td class="p-3 font-medium text-white">Mesolithic geometric microliths, rock art, followed by Neolithic polished celts & pottery</td>
                    <td class="p-3">Oxbow lake marls (Ganga), Sand dunes / Teri sites, Ashmounds (Deccan)</td>
                    <td class="p-3 text-amber-300 font-semibold">Sarai-Nahar Rai, Damdama, Bagor, Mehrgarh, Koldihwa, Lahuradewa</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Detailed Analytical Insights -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs leading-relaxed">
            <div class="{card_bg} p-4 rounded-xl border {border_color} space-y-2">
              <h5 class="text-white font-bold text-sm flex items-center gap-1.5 text-amber-300">
                <i data-lucide="bookmark" class="w-4 h-4"></i> The Cosmogenic Dating Revolution at Attirampakkam
              </h5>
              <p class="{text_sub}">
                Prior to the application of cosmogenic nuclide burial dating ($^{{26}}\\text{{Al}}/ 10Be\\text{{Be}}$) by Shanti Pappu and colleagues (Science, 2011), the Indian Lower Palaeolithic was widely viewed as a late Middle Pleistocene phenomenon. Measurements of quartz tools and embedding ferricrete gravels at Attirampakkam established an Acheulian presence at $1.51 \\pm 0.07\\text{{ Ma}}$, proving that hominins carrying Large Flake Acheulian bifacial technologies dispersed across South Asia almost simultaneously with the earliest Acheulian dispersals in East Africa and the Levant.
              </p>
            </div>

            <div class="{card_bg} p-4 rounded-xl border {border_color} space-y-2">
              <h5 class="text-white font-bold text-sm flex items-center gap-1.5 text-purple-300">
                <i data-lucide="flame" class="w-4 h-4"></i> The 74,000 BP Youngest Toba Tuff (YTT) Marker
              </h5>
              <p class="{text_sub}">
                The super-eruption of Mount Toba (Sumatra) at ~74 ka ejected ~2,800 $\\text{{km}}^3$ of magma, blanketing the Indian subcontinent in an extensive tephra deposit. Excavations at Jwalapuram in the Jurreru Valley (Petraglia et al., 2007) discovered hominin lithic tool assemblages directly beneath and above the thick volcanic ash layer. The continuous industrial traits show that human populations in South Asia survived this massive environmental crisis without catastrophic extinction or technological collapse.
              </p>
            </div>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- SECTION 2: HUMAN EVOLUTION (HATHNORA)      -->
        <!-- ========================================== -->
        <div id="{prefix}foundations-modal-evolution" class="{prefix}foundations-modal-section hidden space-y-6">
          <div class="border-b {border_color} pb-4">
            <div class="flex items-center gap-2 text-rose-400 text-xs font-bold uppercase tracking-wider mb-1">
              <i data-lucide="skull" class="w-4 h-4"></i> Palaeoanthropology & Hominin Evolution
            </div>
            <h3 class="text-xl md:text-2xl font-bold font-display text-white">Human Evolution & Skeletal Record in South Asia</h3>
            <p class="text-sm {text_sub} mt-1 max-w-4xl leading-relaxed">
              From the Middle Pleistocene Hathnora hominin calvarium (*Narmada Man*) to anatomically modern human (AMH) dispersals across the Toba ash horizon and the rich Mesolithic skeletal populations of the Ganga Valley.
            </p>
          </div>

          <!-- Hathnora Spotlight with Image -->
          <div class="{card_bg} rounded-2xl border {border_color} p-5 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            <div class="lg:col-span-4 flex flex-col items-center">
              <div class="relative group rounded-xl overflow-hidden border border-gray-700 bg-black/60 shadow-xl max-w-xs w-full cursor-pointer" onclick="{fn_lightbox}('hathnora')">
                <img src="images/hathnora.jpg" alt="Hathnora Skull Specimen" class="w-full h-56 object-cover object-center group-hover:scale-105 transition duration-300">
                <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-1.5 text-xs font-semibold text-white">
                  <i data-lucide="zoom-in" class="w-4 h-4"></i> Click to Enlarge Specimen
                </div>
                <div class="absolute bottom-2 left-2 bg-black/80 px-2 py-0.5 rounded text-[10px] text-amber-300 font-mono">
                  Specimen Cast • GSI Calcutta
                </div>
              </div>
              <button onclick="{fn_lightbox}('hathnora')" class="mt-3 px-3 py-1.5 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-semibold flex items-center gap-1.5 transition">
                🔍 Enlarge Hathnora Skull Photo
              </button>
            </div>

            <div class="lg:col-span-8 space-y-3">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-rose-500/20 text-rose-300 border border-rose-500/30">Middle Pleistocene Archaic Hominin</span>
                <span class="text-xs text-gray-400 font-mono">250,000 – 300,000 BP</span>
              </div>
              <h4 class="text-lg md:text-xl font-bold text-white font-display">The Hathnora Cranial Calvarium (*Narmada Man*)</h4>
              <p class="text-xs {text_sub} leading-relaxed">
                Discovered on December 5, 1982, by Arun Sonakia (Geological Survey of India) on the northern bank of the Narmada River at Hathnora, Sehore District, Madhya Pradesh. The calvarium was stratigraphically cemented inside the basal boulder conglomerate of the Surajkund Formation, directly associated with late Acheulian bifaces, cleavers, and fossilized bones of *Bos namadicus*.
              </p>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs pt-2 border-t {border_color}">
                <div class="{badge_bg} p-3 rounded-lg border {border_color} space-y-1">
                  <span class="text-gray-400 font-semibold">Cranial Capacity & Vault:</span>
                  <p class="text-amber-300 font-mono font-medium">1,155 – 1,421 cc (robust encephalization)</p>
                  <p class="{text_muted} text-[11px]">Substantially exceeds Asian *Homo erectus* (850–1050 cc), overlapping with early archaic *Homo sapiens*.</p>
                </div>
                <div class="{badge_bg} p-3 rounded-lg border {border_color} space-y-1">
                  <span class="text-gray-400 font-semibold">Anatomical Traits:</span>
                  <p class="text-gray-200">Continuous prominent supraorbital torus, post-orbital constriction, thick vault bones, sagittal keeling.</p>
                  <p class="{text_muted} text-[11px]">Reclassified by Kenneth Kennedy and Lumley as archaic *Homo sapiens* / *Homo heidelbergensis*.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Additional Evolutionary Landmarks -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="{card_bg} p-4 rounded-xl border {border_color} space-y-2">
              <div class="flex items-center gap-2 text-amber-400 font-bold uppercase text-[11px]">
                <i data-lucide="bone" class="w-4 h-4"></i> Sankhyan's Clavicle Discovery (1997)
              </div>
              <h5 class="text-white font-bold text-sm">Post-Cranial Skeletal Evidence</h5>
              <p class="{text_sub} leading-relaxed">
                A.A. Sankhyan (ASI) recovered a complete right human clavicle and a rib fragment from the same Hathnora basal gravel layer. Morphometry indicates a diminutive female individual (~130–140 cm in stature), revealing pronounced body-size polymorphism and sexual dimorphism in South Asian Middle Pleistocene hominin populations.
              </p>
            </div>

            <div class="{card_bg} p-4 rounded-xl border {border_color} space-y-2">
              <div class="flex items-center gap-2 text-purple-400 font-bold uppercase text-[11px]">
                <i data-lucide="activity" class="w-4 h-4"></i> AMH Dispersal & Toba Continuity
              </div>
              <h5 class="text-white font-bold text-sm">Jwalapuram & Kurnool Bone Tools</h5>
              <p class="{text_sub} leading-relaxed">
                Excavations at Jwalapuram (Petraglia et al.) prove that modern humans were present in South Asia before 74 ka and survived the volcanic winter. At Muchchatla Chintamanu Gavi (Kurnool Caves, AP), over 200 Upper Palaeolithic bone implements (awls, spatulae, points) provide clear evidence of complex specialized tool technology.
              </p>
            </div>

            <div class="{card_bg} p-4 rounded-xl border {border_color} space-y-2">
              <div class="flex items-center gap-2 text-emerald-400 font-bold uppercase text-[11px]">
                <i data-lucide="users" class="w-4 h-4"></i> Ganga Valley Mesolithic Skeletons
              </div>
              <h5 class="text-white font-bold text-sm">Sarai-Nahar Rai, Mahadaha, Damdama</h5>
              <p class="{text_sub} leading-relaxed">
                Over 80 excavated human burials (Allahabad University). Anthropological analysis by K.A.R. Kennedy indicates tall, robust athletic populations (males ~175–182 cm), low dental caries (<2%), roasted bone ornaments, and double burials interring male and female together.
              </p>
            </div>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- SECTION 3: PREHISTORIC FLORA & FAUNA       -->
        <!-- ========================================== -->
        <div id="{prefix}foundations-modal-palaeoenv" class="{prefix}foundations-modal-section hidden space-y-6">
          <div class="border-b {border_color} pb-4">
            <div class="flex items-center gap-2 text-emerald-400 text-xs font-bold uppercase tracking-wider mb-1">
              <i data-lucide="trees" class="w-4 h-4"></i> Palaeoecology & Archaeobotany
            </div>
            <h3 class="text-xl md:text-2xl font-bold font-display text-white">Prehistoric Flora, Fauna & Environmental Dynamics</h3>
            <p class="text-sm {text_sub} mt-1 max-w-4xl leading-relaxed">
              Quaternary palaeoenvironments of South Asia: Extinct Pleistocene mammalian megafauna, the Holocene post-glacial faunal turnover, Thar Desert lacustrine palynology, and archaeobotanical evidence for the origins of rice, wheat, and barley agriculture.
            </p>
          </div>

          <!-- Megafauna Master Table -->
          <div class="{card_bg} rounded-xl border {border_color} overflow-hidden space-y-3 p-4">
            <div class="flex items-center justify-between">
              <h4 class="text-white font-bold text-sm flex items-center gap-2">
                <i data-lucide="table" class="w-4 h-4 text-amber-400"></i> Pleistocene Mammalian Megafauna of Peninsular & Central India
              </h4>
              <span class="text-[11px] text-gray-400 font-mono">Fossil Mammalian Record</span>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead>
                  <tr class="{badge_bg} text-gray-300 border-b {border_color} font-semibold">
                    <th class="p-3">Taxon (Scientific Name)</th>
                    <th class="p-3">Common Name / Niche</th>
                    <th class="p-3">Chronological Range</th>
                    <th class="p-3">Diagnostic Skeletal & Dental Hallmarks</th>
                    <th class="p-3">Key Indian River Basins & Sites</th>
                  </tr>
                </thead>
                <tbody class="divide-y {border_color} {text_sub}">
                  <tr class="hover:bg-white/5 transition">
                    <td class="p-3 font-bold text-amber-300 italic">Bos namadicus</td>
                    <td class="p-3">Giant Extinct Wild Ox</td>
                    <td class="p-3 font-mono">Middle to Late Pleistocene</td>
                    <td class="p-3">Enormous horn cores spanning 1.5–2.0 meters; progenitor of Indian domestic Zebu cattle (*Bos indicus*).</td>
                    <td class="p-3 text-gray-300 font-medium">Narmada (Hathnora), Godavari (Nevasa), Manjra, Krishna</td>
                  </tr>
                  <tr class="hover:bg-white/5 transition">
                    <td class="p-3 font-bold text-amber-300 italic">Elephas namadicus</td>
                    <td class="p-3">Straight-Tusked Elephant</td>
                    <td class="p-3 font-mono">Middle to Late Pleistocene</td>
                    <td class="p-3">Massive cranial fronto-parietal crest, long straight tusks; heavy browser and woodland grazer.</td>
                    <td class="p-3 text-gray-300 font-medium">Central Narmada Basin, Belan Valley, Siwaliks</td>
                  </tr>
                  <tr class="hover:bg-white/5 transition">
                    <td class="p-3 font-bold text-amber-300 italic">Stegodon namadicus</td>
                    <td class="p-3">Archaic Proboscidean</td>
                    <td class="p-3 font-mono">Early to Late Pleistocene</td>
                    <td class="p-3">Low-crowned molars with distinctive roof-shaped transverse enamel ridges.</td>
                    <td class="p-3 text-gray-300 font-medium">Narmada gravels, Upper Siwaliks, Mahanadi Valley</td>
                  </tr>
                  <tr class="hover:bg-white/5 transition">
                    <td class="p-3 font-bold text-amber-300 italic">Hexaprotodon palaeindicus</td>
                    <td class="p-3">Extinct Indian River Hippo</td>
                    <td class="p-3 font-mono">Early to Late Pleistocene</td>
                    <td class="p-3">Six incisors in upper and lower jaws; definitive bio-indicator of deep, sluggish perennial river channels.</td>
                    <td class="p-3 text-gray-300 font-medium">Narmada (Surajkund Fm), Godavari, Krishna Basin</td>
                  </tr>
                  <tr class="hover:bg-white/5 transition">
                    <td class="p-3 font-bold text-amber-300 italic">Equus namadicus</td>
                    <td class="p-3">Pleistocene Wild Horse</td>
                    <td class="p-3 font-mono">Middle to Late Pleistocene</td>
                    <td class="p-3">Large stenonid equid with specialized molar enamel folds adapted for dry savannah grasses.</td>
                    <td class="p-3 text-gray-300 font-medium">Hathnora, Chirki-Nevasa, Kortallayar Basin</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Holocene Turnover & Agriculture -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs leading-relaxed">
            <div class="{card_bg} p-4 rounded-xl border {border_color} space-y-2">
              <div class="flex items-center gap-2 text-emerald-400 font-bold uppercase text-[11px]">
                <i data-lucide="paw-print" class="w-4 h-4"></i> The Holocene Faunal Turnover
              </div>
              <h5 class="text-white font-bold text-sm">Extinction of Megafauna & Modern Wildlife</h5>
              <p class="{text_sub}">
                At the Pleistocene-Holocene boundary (~11,700 BP), the extinction of specialized giant swamp mammals (*Hexaprotodon*, *Stegodon*, *Elephas namadicus*) coincided with post-glacial warming. They were replaced by modern open-woodland and grassland ungulates: Indian Gaur (*Bos gaurus*), Blackbuck (*Antilope cervicapra*), Chinkara (*Gazella bennettii*), Spotted Deer (*Axis axis*), Sambar (*Rusa unicolor*), and Wild Boar (*Sus scrofa*), which formed the primary subsistence base for Mesolithic hunting populations at Bagor, Langhnaj, and Damdama.
              </p>
            </div>

            <div class="{card_bg} p-4 rounded-xl border {border_color} space-y-2">
              <div class="flex items-center gap-2 text-cyan-400 font-bold uppercase text-[11px]">
                <i data-lucide="sprout" class="w-4 h-4"></i> Prehistoric Flora & Agricultural Origins
              </div>
              <h5 class="text-white font-bold text-sm">Rice, Barley, Wheat & Lake Palynology</h5>
              <p class="{text_sub}">
                Palynological cores from Lake Didwana and Sambhar (Gurdip Singh) record intense monsoon rainfall between 9000 and 5000 BP. Archaeobotanical finds document two distinct agricultural trajectories:
              </p>
              <ul class="space-y-1 {text_sub} pt-1 text-[11px]">
                <li>• <strong>Rice (*Oryza sativa*):</strong> Indigenous domestication from wild *Oryza nivara* at Chopani-Mando (9th mill. BCE), Koldihwa (6th mill. BCE), and Lahuradewa (~7000–6000 BCE).</li>
                <li>• <strong>Wheat & Barley:</strong> Mehrgarh (Baluchistan, Period I, ~7000–6000 BCE) six-row barley (*Hordeum vulgare*) and emmer wheat stored in granaries.</li>
                <li>• <strong>Deccan Millets & Pulses:</strong> Southern Ashmound sites (Utnur, Kupgal) cultivating horsegram and browntop millet alongside cattle pastoralism.</li>
              </ul>
            </div>
          </div>
        </div>

      </div>
      
      <!-- Modal Footer -->
      <div class="p-3 md:px-6 border-t {border_color} bg-black/60 flex items-center justify-between text-xs {text_muted}">
        <div class="flex items-center gap-2">
          <span>Idea & Design by K.S.Chandra 2026</span>
          <span>•</span>
          <span class="text-amber-400">Prehistory of the Indian Subcontinent</span>
        </div>
        <div class="text-[11px] font-mono text-gray-500">
          Press Esc to close • Switch sections using top tabs
        </div>
      </div>

    </div>
  </div>"""
    return html

print("get_foundations_modal defined successfully.")
def get_foundations_js(is_art=False):
    if is_art:
        return """
    // Foundations Deep-Dive Modal Controls (Artifact)
    function openFoundationsModalArtifact(sectionKey) {
      const modal = document.getElementById('art-foundations-enlarge-modal');
      if (!modal) return;
      modal.classList.remove('hidden');
      switchFoundationsModalSectionArtifact(sectionKey || 'geology');
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    function closeFoundationsModalArtifact() {
      const modal = document.getElementById('art-foundations-enlarge-modal');
      if (modal) modal.classList.add('hidden');
    }

    function switchFoundationsModalSectionArtifact(sectionKey) {
      const sections = ['geology', 'evolution', 'palaeoenv'];
      sections.forEach(k => {
        const sec = document.getElementById(`art-foundations-modal-${k}`);
        if (sec) sec.classList.add('hidden');
        const btn = document.getElementById(`art-btn-modal-${k}`);
        if (btn) {
          btn.classList.remove('bg-amber-500/20', 'border-amber-500', 'text-amber-300',
                               'bg-rose-500/20', 'border-rose-500', 'text-rose-300',
                               'bg-emerald-500/20', 'border-emerald-500', 'text-emerald-300');
          btn.classList.add('border-transparent', 'text-slate-400');
        }
      });

      const targetSec = document.getElementById(`art-foundations-modal-${sectionKey}`);
      if (targetSec) targetSec.classList.remove('hidden');

      const targetBtn = document.getElementById(`art-btn-modal-${sectionKey}`);
      if (targetBtn) {
        targetBtn.classList.remove('border-transparent', 'text-slate-400');
        if (sectionKey === 'geology') {
          targetBtn.classList.add('bg-amber-500/20', 'border-amber-500', 'text-amber-300');
        } else if (sectionKey === 'evolution') {
          targetBtn.classList.add('bg-rose-500/20', 'border-rose-500', 'text-rose-300');
        } else {
          targetBtn.classList.add('bg-emerald-500/20', 'border-emerald-500', 'text-emerald-300');
        }
      }
    }
"""
    else:
        return """
    // Foundations Deep-Dive Modal Controls
    function openFoundationsModal(sectionKey) {
      const modal = document.getElementById('foundations-enlarge-modal');
      if (!modal) return;
      modal.classList.remove('hidden');
      switchFoundationsModalSection(sectionKey || 'geology');
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    function closeFoundationsModal() {
      const modal = document.getElementById('foundations-enlarge-modal');
      if (modal) modal.classList.add('hidden');
    }

    function switchFoundationsModalSection(sectionKey) {
      const sections = ['geology', 'evolution', 'palaeoenv'];
      sections.forEach(k => {
        const sec = document.getElementById(`foundations-modal-${k}`);
        if (sec) sec.classList.add('hidden');
        const btn = document.getElementById(`btn-modal-${k}`);
        if (btn) {
          btn.classList.remove('bg-amber-500/20', 'border-amber-500', 'text-amber-300',
                               'bg-rose-500/20', 'border-rose-500', 'text-rose-300',
                               'bg-emerald-500/20', 'border-emerald-500', 'text-emerald-300');
          btn.classList.add('border-transparent', 'text-gray-400');
        }
      });

      const targetSec = document.getElementById(`foundations-modal-${sectionKey}`);
      if (targetSec) targetSec.classList.remove('hidden');

      const targetBtn = document.getElementById(`btn-modal-${sectionKey}`);
      if (targetBtn) {
        targetBtn.classList.remove('border-transparent', 'text-gray-400');
        if (sectionKey === 'geology') {
          targetBtn.classList.add('bg-amber-500/20', 'border-amber-500', 'text-amber-300');
        } else if (sectionKey === 'evolution') {
          targetBtn.classList.add('bg-rose-500/20', 'border-rose-500', 'text-rose-300');
        } else {
          targetBtn.classList.add('bg-emerald-500/20', 'border-emerald-500', 'text-emerald-300');
        }
      }
    }
"""

def update_index_file():
    index_path = r"C:\Users\DuDu-PC\.gemini\antigravity\scratch\prehistoric_gis_database\index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace tabs 2-4
    pattern_tabs = re.compile(r'<!-- TAB 2: GEOLOGICAL TIME SCALE -->.*?<!-- FILTER CONTROL BAR -->', re.DOTALL)
    new_tabs = get_foundations_tabs(is_art=False) + "\n    </div>\n\n    <!-- FILTER CONTROL BAR -->"
    content, count = pattern_tabs.subn(new_tabs, content, count=1)
    print("Replaced tabs in index.html:", count)

    # 2. Add modal if not already present
    if 'id="foundations-enlarge-modal"' not in content:
        modal_html = get_foundations_modal(is_art=False)
        # insert before id="image-lightbox-modal"
        target = '<div id="image-lightbox-modal"'
        content = content.replace(target, modal_html + "\n\n  " + target)
        print("Inserted foundations modal in index.html")

    # 3. Add JS functions
    if 'function openFoundationsModal' not in content:
        js_code = get_foundations_js(is_art=False)
        target = 'function openImageLightbox'
        content = content.replace(target, js_code + "\n    " + target)
        print("Inserted foundations JS in index.html")

    # 4. Update click outside & escape listeners
    if "if (e.target.id === 'foundations-enlarge-modal') closeFoundationsModal();" not in content:
        target = "if (e.target.id === 'image-lightbox-modal') closeImageLightbox();"
        replacement = target + "\n      if (e.target.id === 'foundations-enlarge-modal') closeFoundationsModal();"
        content = content.replace(target, replacement)

    if "closeFoundationsModal();" not in content.split("if (e.key === 'Escape')")[1].split("}")[0]:
        target = "if (e.key === 'Escape') {"
        replacement = target + "\n        closeFoundationsModal();"
        content = content.replace(target, replacement)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Saved updated index.html")

def update_artifact_file():
    art_path = r"C:\Users\DuDu-PC\.gemini\antigravity\brain\56c9ba5d-fc02-4acf-a11e-3bc90cf38fd5\prehistoric_dashboard.html"
    with open(art_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace tabs 2-4
    pattern_tabs = re.compile(r'<!-- Tab 2: Geology -->.*?</section>\s*<!-- INTERACTIVE CONTROLS BAR -->', re.DOTALL)
    new_tabs = get_foundations_tabs(is_art=True) + "\n    </section>\n\n    <!-- INTERACTIVE CONTROLS BAR -->"
    content, count = pattern_tabs.subn(new_tabs, content, count=1)
    print("Replaced tabs in prehistoric_dashboard.html:", count)

    # 2. Add modal if not already present
    if 'id="art-foundations-enlarge-modal"' not in content:
        modal_html = get_foundations_modal(is_art=True)
        # insert before id="art-lightbox-modal"
        target = '<div id="art-lightbox-modal"'
        content = content.replace(target, modal_html + "\n\n  " + target)
        print("Inserted foundations modal in prehistoric_dashboard.html")

    # 3. Add JS functions
    if 'function openFoundationsModalArtifact' not in content:
        js_code = get_foundations_js(is_art=True)
        target = 'function openLightboxArtifact'
        content = content.replace(target, js_code + "\n    " + target)
        print("Inserted foundations JS in prehistoric_dashboard.html")

    # 4. Update click outside & escape listeners
    if "if (e.target.id === 'art-foundations-enlarge-modal') closeFoundationsModalArtifact();" not in content:
        target = "if (e.target.id === 'art-lightbox-modal') closeLightboxArtifact();"
        replacement = target + "\n      if (e.target.id === 'art-foundations-enlarge-modal') closeFoundationsModalArtifact();"
        content = content.replace(target, replacement)

    if "closeFoundationsModalArtifact();" not in content.split("if (e.key === 'Escape')")[1].split("}")[0]:
        target = "if (e.key === 'Escape') {"
        replacement = target + "\n        closeFoundationsModalArtifact();"
        content = content.replace(target, replacement)

    with open(art_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Saved updated prehistoric_dashboard.html")

if __name__ == '__main__':
    update_index_file()
    update_artifact_file()
