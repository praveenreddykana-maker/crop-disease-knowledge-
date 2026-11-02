"""
Crop Disease Knowledge Base - Built-in agricultural knowledge
Used to seed the vector store with structured disease information.
"""

CROP_DISEASE_DATA = [
    # ─── RICE DISEASES ───────────────────────────────────────────────────────
    {
        "crop": "Rice",
        "disease": "Rice Blast",
        "pathogen": "Magnaporthe oryzae (fungus)",
        "symptoms": (
            "Diamond-shaped lesions with gray centers and brown borders on leaves. "
            "Lesions may coalesce causing large dead areas. Infected panicles turn brown "
            "causing 'neck rot' or 'panicle blast', leading to empty grains. "
            "Nodes may also be infected (node blast), causing the stem to break."
        ),
        "causes": (
            "Caused by the fungus Magnaporthe oryzae. Spreads via airborne conidia. "
            "High humidity (>90%), temperatures between 24–28°C, and excessive nitrogen "
            "fertilization favor disease development."
        ),
        "favorable_conditions": (
            "Cool nights (below 20°C), warm days, high humidity, heavy dew, "
            "prolonged leaf wetness, dense crop canopy, and high soil nitrogen."
        ),
        "prevention": (
            "Use certified blast-resistant rice varieties. Maintain balanced nitrogen "
            "fertilization — avoid excessive use. Ensure proper field drainage. "
            "Remove infected plant debris after harvest. Practice crop rotation."
        ),
        "management": (
            "Apply recommended fungicides at early disease onset. Drain fields periodically "
            "to reduce humidity. Remove and destroy severely infected plants. "
            "Consult local agricultural extension for approved fungicide recommendations "
            "as chemical options vary by region."
        ),
        "source": "FAO Rice Crop Disease Management Guidelines"
    },
    {
        "crop": "Rice",
        "disease": "Bacterial Leaf Blight (BLB)",
        "pathogen": "Xanthomonas oryzae pv. oryzae (bacterium)",
        "symptoms": (
            "Water-soaked to yellowish stripes along leaf margins that turn pale yellow "
            "to white and then straw-colored. Leaves wilt and roll. Severe infections "
            "cause complete yellowing and death of leaves. Kresek phase in young seedlings "
            "causes wilting and death of entire plant."
        ),
        "causes": (
            "Caused by Xanthomonas oryzae pv. oryzae. Enters plant through wounds and "
            "natural openings (hydathodes). Spreads through rain splash, irrigation water, "
            "and contaminated tools."
        ),
        "favorable_conditions": (
            "High temperatures (25–34°C), high humidity, frequent rainfall, "
            "flooding, strong winds causing leaf injuries, excessive nitrogen application."
        ),
        "prevention": (
            "Plant resistant varieties. Use certified disease-free seeds. Avoid excessive "
            "nitrogen fertilization. Maintain proper spacing for air circulation. "
            "Avoid working in fields when leaves are wet. Use clean irrigation water."
        ),
        "management": (
            "There are no effective chemical controls for BLB once established. "
            "Remove infected plant material. Drain flooded fields. "
            "Apply copper-based bactericides as preventive measures in some regions. "
            "Consult local agricultural authorities for region-specific management."
        ),
        "source": "IRRI Rice Knowledge Bank"
    },
    {
        "crop": "Rice",
        "disease": "Sheath Blight",
        "pathogen": "Rhizoctonia solani (fungus)",
        "symptoms": (
            "Oval to elliptical lesions with grayish-green to white centers and "
            "dark brown borders on leaf sheaths. Lesions may spread to leaves. "
            "Affected tissues dry out and plants lodge easily."
        ),
        "causes": (
            "Caused by Rhizoctonia solani. Survives in soil as sclerotia. "
            "Spread by infected plant debris and water. Favored by dense planting "
            "and high nitrogen."
        ),
        "favorable_conditions": (
            "High temperatures (28–32°C), high humidity, dense canopy from close planting, "
            "high soil nitrogen, and continuous flooding."
        ),
        "prevention": (
            "Use wide row spacing. Reduce nitrogen fertilizer rates. "
            "Remove and destroy crop residue. Use resistant varieties where available. "
            "Rotate with non-host crops."
        ),
        "management": (
            "Apply fungicides to lower canopy at early infection stages. "
            "Drain fields to reduce humidity. Remove infected stubble after harvest. "
            "Consult local extension services for approved fungicide programs."
        ),
        "source": "IRRI Rice Knowledge Bank"
    },

    # ─── WHEAT DISEASES ──────────────────────────────────────────────────────
    {
        "crop": "Wheat",
        "disease": "Wheat Rust (Stem Rust / Black Rust)",
        "pathogen": "Puccinia graminis f. sp. tritici (fungus)",
        "symptoms": (
            "Reddish-brown, oval to elongated pustules on stems, leaves, and leaf sheaths. "
            "Pustules are surrounded by yellow halos and rupture to release masses of "
            "rust-colored spores. Severely infected plants show premature death."
        ),
        "causes": (
            "Caused by Puccinia graminis. Spreads via airborne urediniospores over "
            "long distances. Alternate host is barberry (Berberis spp.)."
        ),
        "favorable_conditions": (
            "Temperatures of 15–35°C (optimum 25°C), high humidity, dew, "
            "dense plant stands, and susceptible varieties."
        ),
        "prevention": (
            "Grow resistant varieties. Plant early to avoid peak spore seasons. "
            "Eradicate alternate barberry hosts near fields. "
            "Monitor fields regularly for early detection."
        ),
        "management": (
            "Apply fungicides at early signs of infection. "
            "Harvest early if infection is severe to reduce yield losses. "
            "Consult local agricultural extension for approved fungicide schedules."
        ),
        "source": "CIMMYT Wheat Disease Management Manual"
    },
    {
        "crop": "Wheat",
        "disease": "Yellow Rust (Stripe Rust)",
        "pathogen": "Puccinia striiformis f. sp. tritici (fungus)",
        "symptoms": (
            "Bright yellow to orange pustules arranged in stripes along leaf veins. "
            "Infected leaves turn yellow, wither, and die. Severe infections reduce "
            "grain filling and cause shriveled grains."
        ),
        "causes": (
            "Caused by Puccinia striiformis. Spreads by wind-borne spores. "
            "Favored by cool, moist conditions."
        ),
        "favorable_conditions": (
            "Cool temperatures (2–15°C optimal), high humidity, prolonged leaf wetness, "
            "and susceptible varieties."
        ),
        "prevention": (
            "Use stripe rust-resistant varieties. Avoid dense planting. "
            "Monitor crops regularly, especially in cool, wet seasons."
        ),
        "management": (
            "Fungicide applications are effective when applied early. "
            "Consult extension officers for locally approved fungicide recommendations."
        ),
        "source": "CIMMYT Wheat Disease Management Manual"
    },
    {
        "crop": "Wheat",
        "disease": "Powdery Mildew",
        "pathogen": "Blumeria graminis f. sp. tritici (fungus)",
        "symptoms": (
            "White, fluffy, powdery patches on leaves, stems, and heads. "
            "Infected tissues may turn yellow and die. Severe infections reduce "
            "photosynthesis and grain yield."
        ),
        "causes": "Caused by Blumeria graminis. Spreads by airborne spores.",
        "favorable_conditions": (
            "Moderate temperatures (15–22°C), high humidity, dense canopy, "
            "excessive nitrogen, and overcast conditions."
        ),
        "prevention": (
            "Use resistant varieties. Maintain proper plant spacing. "
            "Balance nitrogen fertilization."
        ),
        "management": (
            "Apply fungicides when disease first appears. "
            "Remove infected plant material."
        ),
        "source": "FAO Wheat Production and Protection Guidelines"
    },

    # ─── TOMATO DISEASES ─────────────────────────────────────────────────────
    {
        "crop": "Tomato",
        "disease": "Tomato Leaf Curl",
        "pathogen": "Tomato Yellow Leaf Curl Virus (TYLCV) - transmitted by whiteflies",
        "symptoms": (
            "Leaves curl upward and become small and yellow. Plant growth is stunted. "
            "Flowers drop, leading to poor fruit set. Young plants show severe stunting; "
            "older plants may survive but with greatly reduced yield."
        ),
        "causes": (
            "Caused by Tomato Yellow Leaf Curl Virus (TYLCV), a begomovirus. "
            "Transmitted by the silverleaf whitefly (Bemisia tabaci). "
            "Not transmitted by contact or tools — only by whitefly vectors."
        ),
        "favorable_conditions": (
            "Warm temperatures (25–35°C), high whitefly populations, "
            "absence of resistant varieties, and proximity to infected plants."
        ),
        "prevention": (
            "Use TYLCV-resistant or tolerant varieties. Apply reflective mulches "
            "to repel whiteflies. Install insect-proof screens in nurseries. "
            "Remove and destroy infected plants promptly. "
            "Use yellow sticky traps to monitor and reduce whitefly populations."
        ),
        "management": (
            "There is no cure once a plant is infected. Remove infected plants. "
            "Control whitefly vectors with approved insecticides. "
            "Consult local agricultural authorities for approved insecticide options."
        ),
        "source": "FAO Integrated Pest Management Guidelines"
    },
    {
        "crop": "Tomato",
        "disease": "Early Blight",
        "pathogen": "Alternaria solani (fungus)",
        "symptoms": (
            "Dark brown to black circular spots with concentric rings (target-board pattern) "
            "on older leaves. Spots are surrounded by yellow halos. Leaves turn yellow "
            "and die. Stem cankers may also appear."
        ),
        "causes": (
            "Caused by Alternaria solani. Spreads through infected plant debris, soil, "
            "and airborne spores. Infection favored by warm temperatures and rain."
        ),
        "favorable_conditions": (
            "Temperatures of 24–29°C, alternating wet and dry periods, "
            "plant stress from nutrient deficiency, and overcrowding."
        ),
        "prevention": (
            "Use certified disease-free seeds and transplants. "
            "Avoid overhead irrigation. Maintain proper plant spacing. "
            "Remove infected leaves and plant debris. Crop rotation with non-solanaceous crops."
        ),
        "management": (
            "Apply approved fungicides at first sign of disease. "
            "Remove heavily infected leaves. Maintain plant nutrition. "
            "Consult extension services for locally available fungicide options."
        ),
        "source": "FAO Integrated Pest Management Guidelines"
    },
    {
        "crop": "Tomato",
        "disease": "Late Blight",
        "pathogen": "Phytophthora infestans (oomycete)",
        "symptoms": (
            "Water-soaked patches on leaves that rapidly turn dark brown. "
            "White mold appears on undersides of leaves in humid conditions. "
            "Stems show dark brown lesions. Fruits develop firm, brown, greasy-looking rots."
        ),
        "causes": (
            "Caused by Phytophthora infestans. Spreads rapidly via airborne sporangia. "
            "Can devastate entire crops within days under favorable conditions."
        ),
        "favorable_conditions": "Cool temperatures (10–25°C), high humidity, foggy conditions, and rain.",
        "prevention": (
            "Use resistant varieties. Avoid overhead irrigation. "
            "Remove and destroy infected plant material. Do not compost infected debris."
        ),
        "management": (
            "Apply protective fungicides before infection occurs during high-risk weather. "
            "Remove infected plants immediately. Consult local agricultural extension "
            "for approved oomycide/fungicide recommendations."
        ),
        "source": "FAO Integrated Pest Management Guidelines"
    },

    # ─── POTATO DISEASES ─────────────────────────────────────────────────────
    {
        "crop": "Potato",
        "disease": "Late Blight",
        "pathogen": "Phytophthora infestans (oomycete)",
        "symptoms": (
            "Dark brown water-soaked lesions on leaves and stems that spread rapidly. "
            "White sporulation on leaf undersides in humid weather. "
            "Tubers show reddish-brown granular rot extending from the skin."
        ),
        "causes": (
            "Caused by Phytophthora infestans. Infected tubers and plant debris are "
            "primary inoculum sources. Spreads rapidly by windborne sporangia."
        ),
        "favorable_conditions": (
            "Cool (10–20°C), humid conditions, prolonged leaf wetness, and rain."
        ),
        "prevention": (
            "Use certified disease-free seed potatoes. Plant resistant varieties. "
            "Avoid overhead irrigation. Hilling soil around plants reduces tuber infection. "
            "Remove volunteer potato plants."
        ),
        "management": (
            "Apply protective fungicides before infection. Destroy infected plant debris. "
            "Harvest tubers in dry conditions. Do not store infected tubers. "
            "Consult extension services for locally approved fungicide schedules."
        ),
        "source": "International Potato Center (CIP) Disease Management Guide"
    },
    {
        "crop": "Potato",
        "disease": "Common Scab",
        "pathogen": "Streptomyces scabies (bacterium)",
        "symptoms": (
            "Rough, corky, raised or pitted lesions on tuber surfaces. "
            "Does not affect internal tuber quality but reduces marketability."
        ),
        "causes": (
            "Caused by Streptomyces scabies. Survives in soil for many years. "
            "Enters tuber through lenticels and wounds."
        ),
        "favorable_conditions": "Dry, alkaline soils (pH above 5.5), sandy soils, and warm soil temperatures.",
        "prevention": (
            "Use resistant or tolerant varieties. Maintain soil pH between 5.0–5.2. "
            "Irrigate adequately during tuber initiation. Rotate with non-host crops for 3–4 years."
        ),
        "management": (
            "Avoid liming fields before potato planting. Use certified scab-free seed potatoes. "
            "Practice long-term crop rotation."
        ),
        "source": "International Potato Center (CIP) Disease Management Guide"
    },

    # ─── COTTON DISEASES ─────────────────────────────────────────────────────
    {
        "crop": "Cotton",
        "disease": "Cotton Leaf Curl Virus",
        "pathogen": "Cotton Leaf Curl Virus (CLCuV) - transmitted by whiteflies",
        "symptoms": (
            "Leaf curling (upward or downward), vein thickening, leaf enation (leaf-like "
            "structures on veins), and stunted plant growth. Severely infected plants "
            "produce no viable bolls."
        ),
        "causes": (
            "Caused by Cotton Leaf Curl Virus (CLCuV), a begomovirus, "
            "transmitted by Bemisia tabaci whiteflies. Does not spread through soil or contact."
        ),
        "favorable_conditions": "High whitefly populations, warm temperatures, and susceptible varieties.",
        "prevention": (
            "Plant resistant or tolerant cotton varieties. "
            "Monitor and control whitefly populations using sticky traps and biological controls. "
            "Remove and destroy infected plants early. "
            "Avoid planting near alternative whitefly host crops."
        ),
        "management": (
            "No cure exists once plants are infected. Control whitefly vectors. "
            "Remove severely infected plants. Consult local cotton advisory services "
            "for approved vector control options."
        ),
        "source": "ICAC Cotton Production and Protection Guidelines"
    },
    {
        "crop": "Cotton",
        "disease": "Fusarium Wilt",
        "pathogen": "Fusarium oxysporum f. sp. vasinfectum (fungus)",
        "symptoms": (
            "Yellowing and wilting of leaves, starting from lower leaves. "
            "Brown discoloration of vascular tissue visible when stem is cut. "
            "Plants die prematurely."
        ),
        "causes": (
            "Caused by Fusarium oxysporum. Soilborne pathogen that persists for many years. "
            "Enters roots and spreads through vascular system."
        ),
        "favorable_conditions": "Sandy soils, high soil temperatures, and susceptible varieties.",
        "prevention": (
            "Use resistant cotton varieties. Practice long crop rotation. "
            "Improve soil drainage. Avoid root damage during cultivation."
        ),
        "management": (
            "No effective chemical control once established in soil. "
            "Remove and destroy infected plants. Improve soil health with organic matter."
        ),
        "source": "ICAC Cotton Production and Protection Guidelines"
    },

    # ─── MAIZE DISEASES ──────────────────────────────────────────────────────
    {
        "crop": "Maize",
        "disease": "Maize Lethal Necrosis (MLN)",
        "pathogen": "Combination of Maize Chlorotic Mottle Virus (MCMV) and cereals viruses",
        "symptoms": (
            "Chlorotic (yellow) mottling of leaves. Premature drying and death of leaves "
            "from the tips. Plant stunting and reduced ear development. "
            "Complete crop failure in severe cases."
        ),
        "causes": (
            "Caused by co-infection of MCMV and other cereal viruses. "
            "Spread by thrips, aphids, beetles, and contaminated equipment."
        ),
        "favorable_conditions": "Warm, dry conditions with high insect vector populations.",
        "prevention": (
            "Use MLN-resistant or tolerant maize varieties. "
            "Control insect vectors. Remove and destroy infected plants. "
            "Avoid moving equipment from infected fields without cleaning."
        ),
        "management": (
            "There is no cure. Roguing (removing infected plants) early can slow spread. "
            "Control insect vectors. Plant resistant varieties in subsequent seasons."
        ),
        "source": "CIMMYT Maize Disease Management Guidelines"
    },
    {
        "crop": "Maize",
        "disease": "Gray Leaf Spot",
        "pathogen": "Cercospora zeae-maydis (fungus)",
        "symptoms": (
            "Long, rectangular, tan to gray lesions with parallel edges running parallel "
            "to leaf veins. Lesions may coalesce causing leaf blighting."
        ),
        "causes": "Caused by Cercospora zeae-maydis. Survives in crop debris.",
        "favorable_conditions": "High humidity, warm temperatures (25–30°C), prolonged dew, and dense canopy.",
        "prevention": (
            "Use resistant hybrids. Practice crop rotation. Remove crop residue. "
            "Ensure proper plant spacing."
        ),
        "management": (
            "Apply fungicides at early tassel stage in severe cases. "
            "Practice conservation tillage carefully to manage residue."
        ),
        "source": "CIMMYT Maize Disease Management Guidelines"
    },

    # ─── GROUNDNUT DISEASES ──────────────────────────────────────────────────
    {
        "crop": "Groundnut",
        "disease": "Early Leaf Spot",
        "pathogen": "Cercospora arachidicola (fungus)",
        "symptoms": (
            "Circular to irregular dark brown spots on upper leaf surfaces, "
            "with yellow halos. Spots appear earlier in the season than late leaf spot."
        ),
        "causes": "Caused by Cercospora arachidicola. Spreads by rain splash and wind.",
        "favorable_conditions": "Warm, humid conditions and prolonged leaf wetness.",
        "prevention": (
            "Use resistant varieties. Practice crop rotation. "
            "Remove infected plant debris."
        ),
        "management": (
            "Apply fungicides starting 30–40 days after planting and repeat every 14 days "
            "during high-risk periods. Consult local extension for approved products."
        ),
        "source": "ICRISAT Groundnut Disease Management Guidelines"
    },
    {
        "crop": "Groundnut",
        "disease": "Groundnut Rosette Virus",
        "pathogen": "Groundnut Rosette Virus (GRV) - transmitted by aphids",
        "symptoms": (
            "Severe stunting, rosette appearance with crowded, small, chlorotic leaves. "
            "Plants produce few or no pods. Mosaic or chlorotic patterns on leaves."
        ),
        "causes": "Caused by Groundnut Rosette Virus, transmitted by Aphis craccivora aphids.",
        "favorable_conditions": "High aphid populations, late planting, and susceptible varieties.",
        "prevention": (
            "Plant early to avoid peak aphid activity. "
            "Use tolerant varieties. Apply reflective mulch to repel aphids. "
            "Remove infected plants promptly."
        ),
        "management": (
            "No cure once infected. Control aphid vectors. Remove infected plants. "
            "Consult local advisory services for approved aphid control methods."
        ),
        "source": "ICRISAT Groundnut Disease Management Guidelines"
    },

    # ─── GENERAL FUNGAL INFECTION MANAGEMENT ────────────────────────────────
    {
        "crop": "All Crops",
        "disease": "General Fungal Infection Management",
        "pathogen": "Various fungal pathogens",
        "symptoms": (
            "Common signs of fungal infections include: spots or lesions on leaves, "
            "stems, or fruits; powdery or downy mold growth; wilting; discoloration; "
            "and premature death of plant parts."
        ),
        "causes": (
            "Fungal diseases are caused by various fungal organisms including Alternaria, "
            "Fusarium, Rhizoctonia, Puccinia, and others. They spread through spores "
            "carried by wind, water, insects, and infected plant material."
        ),
        "favorable_conditions": (
            "High humidity, wet conditions, poor air circulation, plant stress, "
            "and warm temperatures generally favor fungal disease development."
        ),
        "prevention": (
            "Use resistant varieties whenever possible. "
            "Ensure proper plant spacing for good air circulation. "
            "Avoid overhead irrigation; use drip irrigation where possible. "
            "Practice crop rotation to reduce soilborne inoculum. "
            "Remove and destroy infected plant debris. "
            "Use certified disease-free seeds and planting material. "
            "Monitor crops regularly for early detection."
        ),
        "management": (
            "Contact local agricultural extension services or plant disease clinics "
            "for diagnosis and approved fungicide recommendations specific to your region. "
            "Always follow label instructions on any pesticide product. "
            "Integrated disease management combining cultural, biological, and "
            "chemical methods is most effective and sustainable."
        ),
        "source": "FAO Integrated Pest Management Principles"
    }
]


def format_disease_document(disease_data: dict) -> str:
    """Format a disease entry as a text document for embedding."""
    text = f"""
CROP DISEASE INFORMATION
========================
Crop: {disease_data['crop']}
Disease: {disease_data['disease']}
Pathogen/Cause: {disease_data['pathogen']}

SYMPTOMS:
{disease_data['symptoms']}

CAUSES AND TRANSMISSION:
{disease_data['causes']}

FAVORABLE CONDITIONS:
{disease_data['favorable_conditions']}

PREVENTION METHODS:
{disease_data['prevention']}

MANAGEMENT RECOMMENDATIONS:
{disease_data['management']}

Source: {disease_data['source']}
========================
"""
    return text.strip()

