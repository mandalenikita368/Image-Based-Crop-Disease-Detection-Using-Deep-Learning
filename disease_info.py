# ✅ disease_info.py
# This file provides details for all detected plant diseases matching your model’s class names.

disease_database = {
    # 🌶️ Pepper (Bell)
    "Pepper__bell___Bacterial_spot": {
        "name": "Pepper Bell Bacterial Spot",
        "crop": "Pepper (Bell)",
        "pathogen": "Xanthomonas campestris pv. vesicatoria",
        "symptoms": [
            "Small water-soaked spots on leaves",
            "Yellow halos around lesions",
            "Fruit spots causing rot"
        ],
        "treatment": [
            "Use certified disease-free seeds",
            "Apply copper-based bactericides",
            "Avoid overhead irrigation"
        ],
        "prevention": [
            "Rotate crops with non-hosts",
            "Destroy infected debris",
            "Avoid handling plants when wet"
        ]
    },
    "Pepper__bell___healthy": {
        "name": "Healthy Pepper Leaf",
        "crop": "Pepper (Bell)",
        "pathogen": "None",
        "symptoms": ["No visible disease symptoms"],
        "treatment": ["No treatment needed"],
        "prevention": ["Maintain good irrigation and nutrition"]
    },

    # 🥔 Potato
    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "crop": "Potato",
        "pathogen": "Alternaria solani",
        "symptoms": [
            "Dark brown concentric spots on lower leaves",
            "Leaves turn yellow and drop early",
            "Reduced tuber yield"
        ],
        "treatment": [
            "Apply Mancozeb or Chlorothalonil fungicides",
            "Use disease-free certified seed potatoes"
        ],
        "prevention": [
            "Crop rotation (2-3 years)",
            "Avoid overhead irrigation",
            "Remove and destroy infected plants"
        ]
    },
    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "crop": "Potato",
        "pathogen": "Phytophthora infestans",
        "symptoms": [
            "Water-soaked dark lesions on leaves",
            "White fungal growth under leaves in humid weather",
            "Tuber rot with foul odor"
        ],
        "treatment": [
            "Use systemic fungicides like Metalaxyl",
            "Remove infected foliage before harvest"
        ],
        "prevention": [
            "Avoid water stagnation",
            "Plant resistant varieties",
            "Ensure good field drainage"
        ]
    },
    "Potato___healthy": {
        "name": "Healthy Potato Leaf",
        "crop": "Potato",
        "pathogen": "None",
        "symptoms": ["No visible spots or mold on leaves"],
        "treatment": ["No treatment needed"],
        "prevention": ["Maintain optimal soil moisture and nutrition"]
    },

    # 🍅 Tomato
    "Tomato_Bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "crop": "Tomato",
        "pathogen": "Xanthomonas campestris pv. vesicatoria",
        "symptoms": [
            "Small brown water-soaked spots on leaves",
            "Yellow halos around spots",
            "Fruit lesions causing cracking"
        ],
        "treatment": [
            "Apply copper fungicides weekly",
            "Remove and destroy infected leaves"
        ],
        "prevention": [
            "Use pathogen-free seeds",
            "Rotate crops every 2 years"
        ]
    },
    "Tomato_Early_blight": {
        "name": "Tomato Early Blight",
        "crop": "Tomato",
        "pathogen": "Alternaria solani",
        "symptoms": [
            "Brown concentric rings on leaves",
            "Yellowing and defoliation",
            "Dark stem lesions near soil line"
        ],
        "treatment": [
            "Spray fungicides like Mancozeb or Azoxystrobin",
            "Remove lower infected leaves"
        ],
        "prevention": [
            "Avoid overhead irrigation",
            "Rotate with non-host crops"
        ]
    },
    "Tomato_Late_blight": {
        "name": "Tomato Late Blight",
        "crop": "Tomato",
        "pathogen": "Phytophthora infestans",
        "symptoms": [
            "Water-soaked gray-green spots on leaves",
            "White mold growth under leaves",
            "Fruit rot and softening"
        ],
        "treatment": [
            "Use Metalaxyl-based fungicides",
            "Destroy infected debris"
        ],
        "prevention": [
            "Avoid overcrowding plants",
            "Use resistant varieties"
        ]
    },
    "Tomato_Leaf_Mold": {
        "name": "Tomato Leaf Mold",
        "crop": "Tomato",
        "pathogen": "Passalora fulva",
        "symptoms": [
            "Pale yellow spots on upper leaf surfaces",
            "Olive-green mold on undersides",
            "Leaves curl and drop prematurely"
        ],
        "treatment": [
            "Use chlorothalonil-based sprays",
            "Increase greenhouse ventilation"
        ],
        "prevention": [
            "Avoid leaf wetness for long periods",
            "Space plants properly"
        ]
    },
    "Tomato_Septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "crop": "Tomato",
        "pathogen": "Septoria lycopersici",
        "symptoms": [
            "Tiny circular spots with dark borders",
            "Premature leaf yellowing",
            "Reduced yield and fruit exposure to sunscald"
        ],
        "treatment": [
            "Apply fungicides such as Chlorothalonil",
            "Remove infected leaves"
        ],
        "prevention": [
            "Use drip irrigation",
            "Avoid working with wet plants"
        ]
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "name": "Tomato Spider Mite Infestation",
        "crop": "Tomato",
        "pathogen": "Tetranychus urticae (mite)",
        "symptoms": [
            "Fine webbing on leaf undersides",
            "Tiny yellow speckles on leaves",
            "Leaves curl and dry out"
        ],
        "treatment": [
            "Spray neem oil or miticide",
            "Use predatory mites for control"
        ],
        "prevention": [
            "Maintain humidity",
            "Avoid water stress"
        ]
    },
    "Tomato__Target_Spot": {
        "name": "Tomato Target Spot",
        "crop": "Tomato",
        "pathogen": "Corynespora cassiicola",
        "symptoms": [
            "Circular spots with concentric rings on leaves",
            "Spots enlarge and cause defoliation"
        ],
        "treatment": [
            "Use preventive fungicides",
            "Remove infected debris"
        ],
        "prevention": [
            "Avoid continuous tomato cropping",
            "Use resistant hybrids"
        ]
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "name": "Tomato Yellow Leaf Curl Virus",
        "crop": "Tomato",
        "pathogen": "Begomovirus (transmitted by whitefly)",
        "symptoms": [
            "Upward curling of leaves",
            "Yellowing and stunted growth",
            "Reduced fruit set"
        ],
        "treatment": [
            "Control whitefly population",
            "Remove infected plants"
        ],
        "prevention": [
            "Use virus-resistant varieties",
            "Apply insect netting"
        ]
    },
    "Tomato__Tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus",
        "crop": "Tomato",
        "pathogen": "Tobamovirus",
        "symptoms": [
            "Mosaic mottling of leaves",
            "Stunted and deformed plants"
        ],
        "treatment": [
            "Remove infected plants immediately"
        ],
        "prevention": [
            "Avoid tobacco handling before touching plants",
            "Disinfect tools regularly"
        ]
    },
    "Tomato_healthy": {
        "name": "Healthy Tomato Leaf",
        "crop": "Tomato",
        "pathogen": "None",
        "symptoms": ["No disease symptoms"],
        "treatment": ["No treatment required"],
        "prevention": ["Maintain balanced fertilization and irrigation"]
    },

    # 🌽 Corn (Maize)
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "name": "Corn Gray Leaf Spot",
        "crop": "Corn (Maize)",
        "pathogen": "Cercospora zeae-maydis",
        "symptoms": [
            "Rectangular gray lesions on leaves",
            "Premature drying of foliage"
        ],
        "treatment": [
            "Apply strobilurin fungicides",
            "Plant resistant hybrids"
        ],
        "prevention": [
            "Rotate crops yearly",
            "Destroy corn residues"
        ]
    },
    "Corn_(maize)___Common_rust": {
        "name": "Corn Common Rust",
        "crop": "Corn (Maize)",
        "pathogen": "Puccinia sorghi",
        "symptoms": [
            "Reddish-brown pustules on leaves",
            "Reduced photosynthesis and growth"
        ],
        "treatment": [
            "Use fungicides during early infection",
            "Grow resistant varieties"
        ],
        "prevention": [
            "Avoid dense planting",
            "Monitor for early signs"
        ]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "name": "Corn Northern Leaf Blight",
        "crop": "Corn (Maize)",
        "pathogen": "Exserohilum turcicum",
        "symptoms": [
            "Cigar-shaped gray-green lesions on leaves",
            "Premature leaf death"
        ],
        "treatment": [
            "Apply fungicides if necessary",
            "Use resistant hybrids"
        ],
        "prevention": [
            "Rotate with non-corn crops",
            "Destroy infected residues"
        ]
    },
    "Corn_(maize)___healthy": {
        "name": "Healthy Corn Leaf",
        "crop": "Corn (Maize)",
        "pathogen": "None",
        "symptoms": ["No visible disease symptoms"],
        "treatment": ["No treatment required"],
        "prevention": ["Follow good field hygiene"]
    },
}


# ✅ Function to get disease details safely
def get_disease_info(predicted_class: str):
    if not predicted_class:
        return {
            "name": "Unknown Disease",
            "crop": "Unknown",
            "pathogen": "Unknown",
            "symptoms": ["Information not available"],
            "treatment": ["Consult an agricultural expert"],
            "prevention": ["Follow general plant health practices"]
        }

    info = disease_database.get(predicted_class)
    if info:
        return info

    # fallback normalization
    normalized = predicted_class.replace("__", "___")
    return disease_database.get(normalized, {
        "name": "Unknown Disease",
        "crop": "Unknown",
        "pathogen": "Unknown",
        "symptoms": ["Information not available"],
        "treatment": ["Consult an agricultural expert"],
        "prevention": ["Follow general plant health practices"]
    })


# ✅ Function to extract readable names
def parse_disease_name(predicted_class: str):
    if not predicted_class or not isinstance(predicted_class, str):
        return ("Unknown", "Unknown")

    name = predicted_class.replace("___", " ").replace("__", " ").replace("_", " ")
    parts = name.split()
    if len(parts) > 1:
        return (parts[0].capitalize(), " ".join(parts[1:]).capitalize())
    return ("Unknown", name.capitalize())
