"""
NEPA-PRO Tradesmen — SEO content data.

Single source of truth for the per-trade copy, FAQ items, service-area
geography, and structured data used to generate /services/{trade}/index.html
pages plus the about page, sitemap, and llms.txt files.
"""

# ============================================================
# GEOGRAPHY — NEPA service area
# ============================================================
HQ = {
    'street': '14012 Orchard Drive',
    'city':   'Clarks Summit',
    'region': 'PA',
    'postal': '18411',
    'country':'US',
    'lat':    41.4906,
    'lon':    -75.7050,
    'phone':  '570-677-7971',
    'phone_e164': '+1-570-677-7971',
    'email':  'service@nepa-pro.com',
}

# Cities — used for keyword density and local-search optimization
CITIES = [
    'Scranton', 'Wilkes-Barre', 'Hazleton', 'Stroudsburg', 'East Stroudsburg',
    'Clarks Summit', 'Dunmore', 'Pittston', 'Kingston', 'Nanticoke',
    'Mount Pocono', 'Honesdale', 'Tunkhannock', 'Carbondale', 'Olyphant',
    'Moosic', 'Old Forge', 'Taylor', 'Throop', 'Plains', 'West Pittston',
    'Forty Fort', 'Edwardsville', 'Lake Ariel', 'Tobyhanna',
]

# PA counties NEPA-PRO covers
COUNTIES = [
    ('Lackawanna County', 'Scranton'),
    ('Luzerne County',    'Wilkes-Barre'),
    ('Monroe County',     'Stroudsburg'),
    ('Wayne County',      'Honesdale'),
    ('Pike County',       'Milford'),
    ('Wyoming County',    'Tunkhannock'),
    ('Susquehanna County','Montrose'),
    ('Carbon County',     'Jim Thorpe'),
    ('Schuylkill County', 'Pottsville'),
]

# ============================================================
# 15 TRADES — slug, display name, search intent, services
# ============================================================
TRADES = {
    'electricians': {
        'name':       'Electricians',
        'name_singular': 'electrician',
        'category':   'Electrical',
        'apprentice_rate': 58,
        'journeyman_rate': 78,
        'master_rate':     98,
        'naics':      '238210',
        'occ_code':   '47-2111',  # BLS occupation code
        'license_pa': 'PA Master Electrician (county/municipal); HIC PA-#######',
        'when_to_call': [
            'Service upgrade — 100A/200A/400A panel swap',
            'Sub-panel installs, generator interlocks, EV charger circuits',
            'Rough-in for new construction or whole-home rehab',
            'Resi rewires, troubleshooting, GFCI/AFCI replacements',
            'Commercial tenant fit-outs, conduit and tray work',
            'Punch-list trim-out, device finals, low-voltage clean-up',
        ],
        'tools_provided': ['hand tools', 'cordless drills/drivers', 'multimeters', 'fish tape', 'standard hand benders', 'PPE'],
        'tools_excluded': ['lifts', 'large compressors', 'utility line trucks', 'specialty conduit benders > 2"', 'wire pullers'],
        'faq': [
            ('How fast can you dispatch an electrician in NEPA?',
             'Same-week dispatch is standard across Lackawanna, Luzerne, and Monroe counties. Same-day or next-day is available subject to crew load — call 570-677-7971 to confirm.'),
            ('Are your electricians licensed in Pennsylvania?',
             'Every dispatched electrician on the platform is an independent 1099 subcontractor with active municipal/county Master Electrician credentials where required, current general liability insurance, and a clean background check on file.'),
            ('Can the electrician pull permits for our project?',
             'Master/foreman tier electricians can interface with AHJs and pull permits where their license allows. Permits, fees, and inspection coordination are not included in the booking unless added in writing — call us to scope.'),
            ('Do you handle EV charger and solar tie-ins?',
             'Yes — Level 2 EV charger circuits are routine work. Solar AC-side tie-ins, microinverter trunk drops, and rapid-shutdown coordination are master-tier scopes; ask for a master electrician at booking.'),
        ],
    },
    'plumbers': {
        'name':       'Plumbers',
        'name_singular': 'plumber',
        'category':   'Plumbing',
        'apprentice_rate': 55,
        'journeyman_rate': 75,
        'master_rate':     95,
        'naics':      '238220',
        'occ_code':   '47-2152',
        'license_pa': 'Municipal master plumber registration; HIC PA-#######',
        'when_to_call': [
            'Burst pipe, slab leak, and emergency shut-off response',
            'Rough-in DWV and water supply for new construction',
            'Whole-home repipe in copper, PEX, or hybrid runs',
            'Water heater replacement (tank or tankless)',
            'Fixture finals, drain cleaning, pressure-balance valves',
            'Sewer line repair, camera inspection, hydro-jetting',
        ],
        'tools_provided': ['hand tools', 'press tools (ProPress / MegaPress on master tier)', 'torches', 'standard pipe wrenches', 'PPE'],
        'tools_excluded': ['mainline jetters', 'sewer cameras', 'trenchers', 'excavators', 'water-jet pump rigs'],
        'faq': [
            ('Can you handle an emergency leak in Scranton today?',
             'For active leaks call 570-677-7971 immediately — we triage same-day if a journeyman or master plumber is available within range.'),
            ('Are your plumbers licensed for residential and commercial work?',
             'Every dispatched plumber is an independent 1099 subcontractor carrying current municipal master plumber registration where required, plus general liability insurance and a clean background record.'),
            ('Do you pull permits and coordinate inspections?',
             'Master/foreman plumbers can pull permits and meet AHJ inspectors. Permits and fees are billed separately; ask at booking.'),
            ('Will the plumber bring fixtures and material?',
             'Materials are not included in the labor block by default. We can pick up and pass-through at cost + 12% handling if approved in writing before the job.'),
        ],
    },
    'hvac': {
        'name':       'HVAC Technicians',
        'name_singular': 'HVAC technician',
        'category':   'HVAC',
        'apprentice_rate': 52,
        'journeyman_rate': 72,
        'master_rate':     92,
        'naics':      '238220',
        'occ_code':   '49-9021',
        'license_pa': 'EPA 608 Universal; HIC PA-#######',
        'when_to_call': [
            'Furnace and AC replacement (3-ton, 3.5-ton, 4-ton residential)',
            'Heat pump and mini-split installation and commissioning',
            'Rooftop unit (RTU) servicing and refrigerant work',
            'Ductwork modification, return-air balancing',
            'Boiler service, thermostat and zone-valve troubleshooting',
            'Indoor-air-quality and ERV/HRV installs',
        ],
        'tools_provided': ['hand tools', 'gauges', 'recovery machines', 'vacuum pumps', 'PPE'],
        'tools_excluded': ['cranes/lifts for RTU sets', 'specialty refrigerant cylinders > 50 lb', 'pipe-cutting saws > 12"'],
        'faq': [
            ('Can you replace a furnace this week in the Poconos?',
             'Same-week dispatch is standard for HVAC swaps across Monroe, Wayne, and Pike counties. Request a master tier for a same-day diagnostic + replacement quote — call 570-677-7971.'),
            ('Are your HVAC techs EPA-certified for refrigerant?',
             'Every dispatched HVAC technician on the platform holds active EPA 608 universal certification and provides a current Certificate of Insurance before any dispatch.'),
            ('Do you do mini-splits and heat pumps?',
             'Yes — mini-split and heat pump installs, including line-set, condensate, and electrical interface, are routine scopes. Master tier is recommended for full new-system commissioning.'),
            ('Will materials and equipment be included?',
             'Equipment (the unit itself) and refrigerant are typically Customer-supplied or pass-through cost + 12% handling with approval. Standard hand tools and gauges are included.'),
        ],
    },
    'commercial-hvac': {
        'name':       'Commercial HVAC',
        'name_singular': 'commercial HVAC technician',
        'category':   'HVAC',
        'apprentice_rate': 62,
        'journeyman_rate': 82,
        'master_rate':     105,
        'naics':      '238220',
        'occ_code':   '49-9021',
        'license_pa': 'EPA 608 Universal; commercial mechanical permit experience',
        'when_to_call': [
            'Rooftop unit (RTU) installs, swaps, and PMs',
            'VRF and VAV system service in offices, schools, retail',
            'Chiller troubleshooting and pump-motor servicing',
            'Make-up air units, kitchen exhaust, RTU economizers',
            'EMS / BMS thermostat and sensor commissioning',
            'Ductwork on light-commercial fit-outs',
        ],
        'tools_provided': ['hand tools', 'commercial gauges', 'recovery rigs', 'multimeters', 'PPE including arc-rated for service work'],
        'tools_excluded': ['cranes', 'aerial lifts', 'forklifts', 'specialty chiller refrigerant rigs'],
        'faq': [
            ('Do you service commercial RTUs in NEPA?',
             'Yes — light-commercial RTUs (3 to 25 tons) on flat roofs across Lackawanna, Luzerne, and Monroe counties are a routine scope. Crane or lift rentals for sets are Customer-coordinated.'),
            ('Can you cover a property manager portfolio?',
             'Recurring property-management dispatch is supported via standing weekly bookings — call 570-677-7971 to set up.'),
            ('Are your commercial techs OSHA-30 trained?',
             'Master/foreman tier commercial HVAC technicians on the platform carry OSHA-30 construction wallet cards along with EPA 608.'),
            ('Will you interface with our existing EMS / BMS?',
             'Yes, master tier — we can troubleshoot common Trane, Carrier, Honeywell, and Johnson Controls platforms at the local panel level.'),
        ],
    },
    'commercial-plumbers': {
        'name':       'Commercial Plumbers',
        'name_singular': 'commercial plumber',
        'category':   'Plumbing',
        'apprentice_rate': 62,
        'journeyman_rate': 82,
        'master_rate':     105,
        'naics':      '238220',
        'occ_code':   '47-2152',
        'license_pa': 'Municipal master plumber registration; commercial code experience',
        'when_to_call': [
            'Tenant fit-out plumbing for office and retail spaces',
            'Restaurant and food-service grease traps, FOG compliance',
            'Multifamily DWV stack work and riser drops',
            'Backflow preventer installs, testing, repair',
            'Industrial process piping in light manufacturing',
            'Storm drainage and roof drain leader work',
        ],
        'tools_provided': ['hand tools', 'press tools (ProPress / MegaPress / RIDGID)', 'standard threading dies', 'PPE'],
        'tools_excluded': ['large mainline jetters', 'sewer cameras', 'trenchers', 'crane-rated pipe rigging'],
        'faq': [
            ('Can you do commercial fit-out plumbing in NEPA?',
             'Yes — we dispatch master commercial plumbers for office, retail, restaurant, and light-industrial tenant fit-outs across NEPA. Call 570-677-7971 to scope.'),
            ('Do your commercial plumbers handle backflow testing?',
             'Backflow installation is in scope. Annual testing and PA DEP filings require a separately-certified BPAT — confirm at booking which scope you need.'),
            ('Are crews available for night and weekend shutdowns?',
             'Yes for commercial off-hour work. Night and Sunday dispatches bill at the posted overtime multipliers — typically 2.0× on Sundays and recognized holidays.'),
            ('Will you interface with the AHJ for commercial permits?',
             'Master tier commercial plumbers can pull permits and meet inspectors. Permit fees are pass-through to the Customer.'),
        ],
    },
    'welders': {
        'name':       'Welders',
        'name_singular': 'welder',
        'category':   'Welding',
        'apprentice_rate': 48,
        'journeyman_rate': 70,
        'master_rate':     98,
        'naics':      '238120',
        'occ_code':   '51-4121',
        'license_pa': 'AWS / ASME process certifications (per process and material)',
        'when_to_call': [
            'Structural fab on jobsite — beams, columns, embed plates',
            'Stick (SMAW), MIG (GMAW), and TIG (GTAW) field welding',
            'Stainless and aluminum repair on food-service or process equipment',
            'Pipe welding (carbon and stainless) for mechanical scopes',
            'Heavy-equipment repair welds on buckets, frames, undercarriages',
            'Architectural and railing fabrication',
        ],
        'tools_provided': ['hand tools', 'leathers', 'hood', 'angle grinders', 'PPE'],
        'tools_excluded': ['welder/plasma machines', 'positioners', 'cylinder packs', 'engine-drive units'],
        'faq': [
            ('Can you provide a certified welder same-week in NEPA?',
             'Same-week certified welder dispatch is routine. Specify the process (SMAW, GMAW, GTAW, FCAW), material (carbon, stainless, aluminum), and required cert (AWS / ASME) at booking.'),
            ('Do welders bring their own machines?',
             'Hand tools, hood, and PPE always. Welder/plasma machines, positioners, and cylinder packs are typically Customer-coordinated unless equipment-included staffing is quoted.'),
            ('Are your welders X-ray and code-grade qualified?',
             'Master tier welders carry current AWS / ASME certifications. State the welding code (D1.1, B31.1, B31.3, etc.) at booking and the right credential is confirmed.'),
            ('Can you do jobsite stainless welds for restaurants and food-service?',
             'Yes — stainless GTAW and pulse-MIG for food-service and process equipment is a master-tier scope.'),
        ],
    },
    'masons': {
        'name':       'Masons',
        'name_singular': 'mason',
        'category':   'Masonry',
        'apprentice_rate': 52,
        'journeyman_rate': 72,
        'master_rate':     92,
        'naics':      '238140',
        'occ_code':   '47-2021',
        'license_pa': 'HIC PA-#######',
        'when_to_call': [
            'Stone and brick veneer on residential exteriors',
            'Block foundation work on additions and outbuildings',
            'Chimney repair, repointing, and crown rebuilds',
            'Stone retaining walls and steps',
            'Fireplace installs and rebuilds',
            'Historic repointing on older NEPA brick housing stock',
        ],
        'tools_provided': ['hand tools', 'trowels', 'levels', 'mortar mixing tools', 'PPE'],
        'tools_excluded': ['mortar mixers', 'mast climbers', 'scaffolding', 'forklift / telehandler', 'block saws'],
        'faq': [
            ('Do you do chimney repointing in NEPA?',
             'Yes — chimney repointing, crown rebuilds, and minor structural rebuilds are routine masonry scopes. Scaffold/lift rentals are Customer-coordinated.'),
            ('Can you match historic mortar on older Scranton homes?',
             'Master-tier masons can spec and match historic lime-based mortars for pre-1940 brick. Specify "historic match" at booking.'),
            ('Are stone retaining walls in scope?',
             'Yes — dry-stack and mortared stone retaining walls under typical residential heights are a journeyman/master scope.'),
            ('Will the mason bring block, brick, or stone?',
             'No — masonry units, mortar, and rebar are Customer-supplied or pass-through with approval at cost + 12%.'),
        ],
    },
    'concrete': {
        'name':       'Concrete Workers',
        'name_singular': 'concrete worker',
        'category':   'Concrete',
        'apprentice_rate': 48,
        'journeyman_rate': 68,
        'master_rate':     88,
        'naics':      '238110',
        'occ_code':   '47-2051',
        'license_pa': 'HIC PA-#######',
        'when_to_call': [
            'Footings, foundation walls, slabs on grade',
            'Driveway, sidewalk, and patio pours',
            'Garage floor and basement slab work',
            'Form setting, rebar tying, anchor-bolt placement',
            'Decorative stamped, exposed-aggregate, and broom finishes',
            'Repair, mudjacking, and slab leveling',
        ],
        'tools_provided': ['hand tools', 'trowels', 'edgers', 'floats', 'screed boards', 'PPE'],
        'tools_excluded': ['concrete saws', 'power trowels (helicopters)', 'pump trucks', 'mixer trucks', 'compaction plates'],
        'faq': [
            ('Can you set forms and pour a slab same-week?',
             'Yes — most residential slabs and driveways can be scoped, formed, and poured in a single week subject to weather and concrete delivery.'),
            ('Will you arrange the concrete delivery?',
             'No — Customer typically schedules the ready-mix delivery directly. We can advise on volumes and PSI at booking.'),
            ('Do you do decorative finishes — stamped, exposed-aggregate?',
             'Yes — decorative work is master-tier. Specify finish type at booking.'),
            ('What about cold-weather pours in NEPA winters?',
             'We pour year-round subject to insulation and admixture protocols. Cold-weather extras (blankets, accelerator) are Customer-supplied or pass-through.'),
        ],
    },
    'drywall': {
        'name':       'Drywall Hangers',
        'name_singular': 'drywall hanger',
        'category':   'Drywall & Finishing',
        'apprentice_rate': 42,
        'journeyman_rate': 58,
        'master_rate':     78,
        'naics':      '238310',
        'occ_code':   '47-2081',
        'license_pa': 'HIC PA-#######',
        'when_to_call': [
            'Hang and finish — Level 4 / Level 5 finish for whole-home rehabs',
            'Patch and repair after rough-ins or water damage',
            'Hat channel, RC-1, sound-rated assemblies',
            'Curved walls, archways, and trim coordination',
            'Texture matching — knockdown, orange peel, smooth Level 5',
            'Steel-stud framing for partition walls in commercial fit-outs',
        ],
        'tools_provided': ['hand tools', 'screw guns', 'taping knives', 'mud pans', 'PPE'],
        'tools_excluded': ['lifts', 'sanders with HEPA collection', 'spray-texture rigs', 'panel lifts'],
        'faq': [
            ('Can you finish to Level 5 for high-end residential?',
             'Yes — master-tier drywall finishers can deliver Level 5 (skim-coat) finish for accent walls and high-light areas.'),
            ('Do you do steel-stud framing for commercial?',
             'Yes — light-gauge steel-stud framing for tenant fit-outs is a journeyman scope.'),
            ('Can you patch after a plumbing or electrical rough-in?',
             'Patch and finish work is exactly what same-day drywall dispatch is for — small trades-coordination patches are routine.'),
            ('Will you supply drywall and mud?',
             'No — board, mud, tape, and corner bead are Customer-supplied or pass-through cost + 12% with approval.'),
        ],
    },
    'ironworkers': {
        'name':       'Ironworkers',
        'name_singular': 'ironworker',
        'category':   'Structural',
        'apprentice_rate': 55,
        'journeyman_rate': 75,
        'master_rate':     95,
        'naics':      '238120',
        'occ_code':   '47-2221',
        'license_pa': 'OSHA-30 construction; ironworker apprenticeship credentials',
        'when_to_call': [
            'Structural steel erection — beams, columns, and joists',
            'Rebar setting, tying, and placement on commercial slabs',
            'Bolt-up and torque verification',
            'Decking install and welding',
            'Stair pans, embeds, and miscellaneous steel',
            'Bridge and elevated structure work in NEPA infrastructure',
        ],
        'tools_provided': ['hand tools', 'spud wrench', 'bull pin', 'sleever bar', 'PPE including fall arrest'],
        'tools_excluded': ['cranes', 'forklifts', 'mast climbers', 'man baskets'],
        'faq': [
            ('Do you provide ironworkers for steel erection in NEPA?',
             'Yes — ironworker dispatch for residential and light-commercial steel is a routine scope. Larger crane-served erections are coordinated with master-tier as crew chief.'),
            ('Are your ironworkers OSHA-trained for fall hazards?',
             'Yes — every ironworker on the platform carries OSHA-10 minimum, OSHA-30 at master tier, with current fall-arrest training.'),
            ('Can you do rebar tying for foundation walls and slabs?',
             'Yes — rebar setting and tying is a routine apprentice/journeyman scope.'),
            ('Will the ironworker bring rigging and tools?',
             'Spud wrench, bolt bag, and personal fall arrest yes. Rigging, beam clamps, and chokers are Customer-coordinated unless quoted as equipment-included.'),
        ],
    },
    'linemen': {
        'name':       'Linemen',
        'name_singular': 'lineman',
        'category':   'Electrical',
        'apprentice_rate': 68,
        'journeyman_rate': 95,
        'master_rate':     135,
        'naics':      '237130',
        'occ_code':   '49-9051',
        'license_pa': 'Apprenticeship-trained; OSHA-30; pole-climbing certification',
        'when_to_call': [
            'Service drop and weatherhead work on residential properties',
            'Aerial line repair and tree-clearance trim coordination',
            'Underground secondary cable and transformer pad work',
            'Storm-restoration support after PA wind/ice events',
            'Site-power for construction sites — temporary service installs',
            'Substation and switchgear support work (master tier)',
        ],
        'tools_provided': ['hand tools', 'climbers and belts', 'rubber gloves and sleeves (rated to job)', 'PPE'],
        'tools_excluded': ['line trucks', 'auger trucks', 'bucket trucks', 'wire pulling rigs'],
        'faq': [
            ('Can you supply linemen after a NEPA storm?',
             'Storm-restoration support is a master-tier scope. Call 570-677-7971 immediately after a major event — we route credentialed linemen as crew availability allows.'),
            ('Do you do residential service drops?',
             'Yes — service-drop weatherhead, mast, and meter-can work is a journeyman scope. Coordinated with the local utility on disconnect/reconnect.'),
            ('Are your linemen rated for primary voltage?',
             'Master-tier linemen on the platform carry primary-voltage glove ratings and apprenticeship-trained credentials. Specify voltage class at booking.'),
            ('Will trucks and equipment be supplied?',
             'No — line trucks, augers, and buckets are Customer-coordinated. Linemen arrive with PPE, climbers, and personal gear.'),
        ],
    },
    'heavy-equipment': {
        'name':       'Heavy Equipment Operators',
        'name_singular': 'heavy equipment operator',
        'category':   'Earthwork',
        'apprentice_rate': 58,
        'journeyman_rate': 78,
        'master_rate':     98,
        'naics':      '237310',
        'occ_code':   '47-2073',
        'license_pa': 'OSHA-30; equipment-specific operator certification',
        'when_to_call': [
            'Excavator operation — site clearing, foundation digs, utility trenching',
            'Skid-steer and compact track loader work',
            'Backhoe service for water, sewer, electrical underground',
            'Bulldozer grading and rough cuts',
            'Wheel loader yard work and material handling',
            'Roller and compactor operation for paving prep',
        ],
        'tools_provided': ['hand tools', 'safety vest', 'PPE'],
        'tools_excluded': ['the equipment itself — Customer rents or supplies machine'],
        'faq': [
            ('Do you supply the excavator or just the operator?',
             'Operator only by default. Customer rents or supplies the machine. Equipment-included staffing is available on quote — call to scope.'),
            ('What machines can your operators run?',
             'Standard: excavators (mini and full size), skid-steers, backhoes, dozers, loaders, rollers. Specialty equipment (telehandlers above 80 ft, articulated dumps) is a master-tier scope.'),
            ('Will the operator handle underground utility work?',
             'Yes — once PA One Call (811) markings are on site (Customer responsibility), operators can dig to utility scopes. Stop-work authority applies if markings are missing.'),
            ('Can I get an operator and laborer crew?',
             'Yes — operator + laborer combinations are common bookings for residential underground and small-site work. Book each role separately or call dispatch to combine.'),
        ],
    },
    'operating-engineers': {
        'name':       'Operating Engineers',
        'name_singular': 'operating engineer',
        'category':   'Heavy Mechanical',
        'apprentice_rate': 62,
        'journeyman_rate': 85,
        'master_rate':     115,
        'naics':      '237310',
        'occ_code':   '47-2073',
        'license_pa': 'IUOE-equivalent training; OSHA-30; equipment-specific cert',
        'when_to_call': [
            'Crane operation on commercial sites — mobile and tower',
            'Boilerhouse and central-plant equipment operation',
            'Compressor, generator, and large-pump operation',
            'HVAC plant and mechanical-room operation in commercial buildings',
            'Power-plant and process-plant operating support',
            'Heavy-haul rigging coordination on industrial sites',
        ],
        'tools_provided': ['hand tools', 'PPE', 'multimeter / gauges per scope'],
        'tools_excluded': ['the equipment / cranes / plant itself'],
        'faq': [
            ('Do you supply operating engineers for commercial cranes in NEPA?',
             'Yes — master-tier operating engineers for mobile crane operation are dispatchable, subject to NCCCO rating for the crane class. Specify class at booking.'),
            ('Can you cover a central plant or boiler-house shift?',
             'Yes — shift coverage in commercial central plants is a journeyman/master scope. Multi-week assignments are most efficient as weekly bookings.'),
            ('What\'s the difference between operating engineer and heavy-equipment operator?',
             'Heavy-equipment operators run earthmoving / excavation / paving machines. Operating engineers run plant equipment — cranes, compressors, generators, central-plant systems. We dispatch both as separate trades.'),
            ('Are your operators NCCCO-certified?',
             'Master-tier operating engineers on the platform hold NCCCO certifications for the crane class booked. Confirm with dispatch.'),
        ],
    },
    'millwrights': {
        'name':       'Millwrights',
        'name_singular': 'millwright',
        'category':   'Heavy Mechanical',
        'apprentice_rate': 58,
        'journeyman_rate': 80,
        'master_rate':     105,
        'naics':      '238290',
        'occ_code':   '49-9044',
        'license_pa': 'Millwright apprenticeship; OSHA-30; alignment training',
        'when_to_call': [
            'Industrial machinery installation and alignment',
            'Conveyor, shaft, and pulley assembly and PMs',
            'Pump and motor base alignment with laser tools',
            'Production-line equipment moves and re-installs',
            'Precision rigging of process equipment',
            'Bearing and gearbox replacement on heavy machines',
        ],
        'tools_provided': ['hand tools', 'precision levels', 'dial indicators', 'PPE'],
        'tools_excluded': ['laser alignment systems (master tier provides)', 'cranes', 'forklifts', 'jacks > 10 ton'],
        'faq': [
            ('Do you do industrial millwright work in NEPA?',
             'Yes — millwright dispatch for industrial installs, alignments, and equipment moves across NEPA manufacturing sites is a routine scope.'),
            ('Are laser-alignment services included?',
             'Master-tier millwrights typically bring their own laser alignment kits. Specify the precision-alignment scope at booking so the right tier is dispatched.'),
            ('Can you handle production-line moves on a weekend shutdown?',
             'Yes — weekend and shutdown work is well-suited to weekly bookings. Sunday/holiday hours bill at the posted 2.0× multiplier.'),
            ('Will rigging gear come with the millwright?',
             'Personal hand tools and dial indicators yes. Cranes, forklifts, and chain hoists are Customer-coordinated.'),
        ],
    },
    'riggers': {
        'name':       'Riggers',
        'name_singular': 'rigger',
        'category':   'Heavy Mechanical',
        'apprentice_rate': 52,
        'journeyman_rate': 72,
        'master_rate':     95,
        'naics':      '238290',
        'occ_code':   '47-2071',
        'license_pa': 'OSHA-30; rigger / signal-person certification',
        'when_to_call': [
            'Critical-pick rigging plans and execution',
            'Equipment moves — HVAC RTUs, generators, transformers',
            'Crane signaling and load coordination',
            'Tilt-up and panelized construction lifts',
            'Heavy machinery offload and set in industrial settings',
            'Steel erection rigging support',
        ],
        'tools_provided': ['hand tools', 'rigging slings on master tier (per pick)', 'PPE'],
        'tools_excluded': ['cranes', 'forklifts', 'gantries', 'hydraulic skidding systems'],
        'faq': [
            ('Do you do critical-pick rigging in NEPA?',
             'Yes — master-tier riggers can plan and execute critical picks for commercial and industrial sets. Provide load weight, pick radius, and crane spec at booking.'),
            ('Are your riggers OSHA-certified for crane signaling?',
             'Yes — master-tier riggers carry current OSHA Subpart CC qualified rigger / signal-person credentials.'),
            ('Will rigging gear be supplied?',
             'Personal slings, shackles, and tag lines on master-tier rigging engagements yes. Custom spreader bars and large-tonnage gear are Customer-coordinated unless quoted as equipment-included.'),
            ('Can riggers coordinate with the crane operator we already booked?',
             'Yes — that\'s exactly the typical setup. Our rigger pairs with your crane operator and runs the picks.'),
        ],
    },
}


# ============================================================
# About-page facts
# ============================================================
ABOUT = {
    'founded':       '2025',
    'company_legal': 'NEPA-PRO LLC',
    'state_org':     'Pennsylvania limited liability company',
    'mission': (
        'NEPA-PRO Tradesmen exists because the construction labor market in Northeast '
        'Pennsylvania runs on phone calls, hand-shake commitments, and last-minute scrambles — '
        'and that breaks down the moment a sub backs out, a crew member calls in sick, or an '
        'inspection date moves up. We built an on-demand platform that lets contractors and '
        'property owners book vetted skilled trade labor by the hour, with paperwork ready, '
        'insurance verified, and the dispatch happening in days instead of weeks.'
    ),
    'differentiators': [
        ('Veteran owned and operated',
         'Founded and led by a U.S. military veteran. We bring a service mindset to construction '
         'labor — show up, do the work, document everything, hand the site back better than we found it.'),
        ('100% vetted independent tradespeople',
         'Every tradesperson on the platform is a credentialed 1099 subcontractor with current trade '
         'license, active commercial general liability and (where applicable) workers compensation '
         'insurance, and a clean background check. We collect Certificates of Insurance before any '
         'dispatch, not after.'),
        ('Iron-clad paperwork',
         'Nine purpose-built legal documents form the backbone of the platform — six for tradespeople, '
         'three for customers. Each does one job; together they keep the model rock-solid. They live in '
         'the public Documents Hub at /docs/.'),
        ('Transparent NEPA-aligned pricing',
         'Hourly rates posted up front, aligned to NEPA wage data. Three duration blocks (4-hr, 8-hr, '
         '40-hr week) and three skill tiers (apprentice, journeyman, master/foreman) — 9 prices, 15 trades, '
         '135 SKUs total. No surprises at invoice.'),
        ('Local dispatch from Clarks Summit',
         'We dispatch from a real address in Clarks Summit, PA — not a forwarded number. Same-week '
         'dispatch is standard across nine NEPA counties. Same-day available subject to crew load.'),
    ],
    'service_summary': (
        'Skilled trade labor on demand across 15 trades — electricians, plumbers, HVAC technicians, '
        'commercial HVAC, commercial plumbers, welders, masons, concrete workers, drywall hangers, '
        'ironworkers, linemen, heavy-equipment operators, operating engineers, millwrights, and riggers. '
        'Bookable by the half-day (4 hrs), full day (8 hrs), or week (40 hrs) at apprentice, journeyman, '
        'or master/foreman skill tiers.'
    ),
}


# ============================================================
# Site-wide FAQs (for FAQPage schema)
# ============================================================
SITE_FAQS = [
    ('What is NEPA-PRO Tradesmen?',
     'NEPA-PRO Tradesmen is an on-demand skilled trade labor platform serving Northeast '
     'Pennsylvania. Contractors, property managers, and homeowners book vetted, licensed, '
     'insured 1099 subcontractor tradespeople by the half-day, full day, or week.'),
    ('What trades can I book?',
     'Fifteen trades: electricians, plumbers, HVAC technicians, commercial HVAC, commercial '
     'plumbers, welders, masons, concrete workers, drywall hangers, ironworkers, linemen, '
     'heavy-equipment operators, operating engineers, millwrights, and riggers. Each at three '
     'skill tiers — apprentice, journeyman, master/foreman.'),
    ('How fast can NEPA-PRO dispatch labor in Northeast Pennsylvania?',
     'Same-week dispatch is standard across Lackawanna, Luzerne, Monroe, Wayne, Pike, Wyoming, '
     'Susquehanna, Carbon, and Schuylkill counties. Same-day or next-day dispatch is available '
     'subject to crew load — call 570-677-7971 to confirm.'),
    ('What is the insurance and contractor status setup?',
     'Every tradesperson on the platform is an independent 1099 subcontractor who has signed '
     'NEPA-PRO\'s Subcontractor Master Agreement and provided proof of insurance — including '
     'general liability and, where applicable, their own workers compensation. NEPA-PRO LLC '
     'maintains its own general liability coverage as the staffing platform. Certificates of '
     'Insurance are collected before any dispatch and provided to customers on request.'),
    ('Where in NEPA does NEPA-PRO Tradesmen serve?',
     'Same-week dispatch across Scranton, Wilkes-Barre, Hazleton, Stroudsburg, Clarks Summit, '
     'Mount Pocono, Honesdale, Tunkhannock, Carbondale, Pittston, Kingston, and surrounding '
     'communities throughout the nine-county NEPA region.'),
    ('How does pricing work?',
     'Three flexible durations — half day (4 hours), full day (8 hours), and weekly (40 hours, '
     '8% volume rate baked in) — at three skill tiers. Hourly rates vary by trade and tier. Pay '
     'in full at Stripe checkout; overtime past 8 hours/day or 40 hours/week bills at 1.5×; '
     'Sundays and holidays at 2.0×.'),
    ('Can I book a crew, not just one tradesperson?',
     'Yes. Book multiple positions back-to-back through checkout. Crews of four or more get a '
     'dedicated dispatcher — call 570-677-7971 to coordinate.'),
    ('What about cancellations and refunds?',
     'Cancel or reschedule any booking up to 24 hours before dispatch for a full refund. Inside '
     '24 hours, half-day and full-day bookings are non-refundable but credits roll forward 90 '
     'days. Weekly bookings can be paused mid-week with prior notice.'),
    ('Is NEPA-PRO veteran-owned?',
     'Yes. NEPA-PRO LLC is a veteran-owned and operated business based in Clarks Summit, '
     'Pennsylvania, serving Northeast Pennsylvania construction labor needs.'),
]
