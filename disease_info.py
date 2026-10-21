"""General, non-prescriptive disease information shown in the web app.

This is educational guidance only. It deliberately contains no pesticide
names or doses: those depend on country, crop stage and local regulation.
Always verify with a local agricultural extension office / KVK.
Extend INFO with more entries if your final class list needs them.
"""
import re

HEALTHY = {
    "description": "The model predicts that this leaf looks like a healthy leaf of the supported crop.",
    "symptoms": ["No obvious spots, lesions, mould, curling or discolouration in the image."],
    "prevention": [
        "Keep monitoring the crop regularly, including the undersides of leaves.",
        "Use good field hygiene: remove crop debris and weeds.",
        "Avoid overhead irrigation late in the day; water at the base of plants.",
        "Maintain balanced nutrition and adequate plant spacing for airflow.",
    ],
    "management": ["No treatment is suggested by the model. A healthy prediction does not rule out problems that are not visible in one photo."],
}

# Each entry: keys (normalised substrings matched against the disease name), plus text.
INFO = [
    {"keys": ["early blight"], "title": "Early blight",
     "description": "A fungal leaf disease (Alternaria species) common on tomato and potato, favoured by warm, humid conditions and stressed plants.",
     "symptoms": ["Dark brown spots with concentric 'target-like' rings, usually on older leaves first.", "Yellowing around lesions; leaves may drop.", "Dark, sunken lesions can also appear on stems or fruit."],
     "prevention": ["Rotate crops; avoid planting solanaceous crops in the same field year after year.", "Use disease-free seed/seedlings and resistant varieties where available.", "Mulch and avoid wetting foliage; space plants for airflow."],
     "management": ["Remove and destroy badly affected leaves and crop debris.", "Keep plants well fed and watered to reduce stress.", "If the problem is spreading, ask a local agricultural officer which registered fungicide is suitable."]},
    {"keys": ["late blight"], "title": "Late blight",
     "description": "A fast-spreading disease caused by the oomycete Phytophthora infestans, affecting tomato and potato in cool, wet weather.",
     "symptoms": ["Large, irregular water-soaked patches that turn brown/black.", "White fuzzy growth on the underside of leaves in humid conditions.", "Brown rot on stems, tubers or fruit."],
     "prevention": ["Plant certified disease-free seed tubers or seedlings.", "Avoid dense planting and overhead irrigation.", "Destroy volunteer plants and cull piles."],
     "management": ["Act quickly: this disease can destroy a crop within days in suitable weather.", "Remove and safely dispose of infected plants; do not compost them.", "Contact a local agricultural expert promptly for locally approved control options."]},
    {"keys": ["leaf mold"], "title": "Leaf mould (tomato)",
     "description": "A fungal disease (Passalora fulva) mostly seen in humid, poorly ventilated conditions such as greenhouses.",
     "symptoms": ["Pale green/yellow patches on the upper leaf surface.", "Olive-green to brown velvety mould on the underside.", "Leaves curl, wither and may drop."],
     "prevention": ["Improve ventilation and reduce humidity.", "Avoid leaf wetness; water at soil level.", "Use resistant varieties and clean up debris after harvest."],
     "management": ["Remove affected leaves.", "Prune to open the canopy.", "Seek local advice if it keeps spreading."]},
    {"keys": ["septoria"], "title": "Septoria leaf spot",
     "description": "A fungal disease (Septoria lycopersici) of tomato spread by water splash.",
     "symptoms": ["Many small circular spots with grey/white centres and dark borders.", "Tiny black dots (fruiting bodies) in the centre of spots.", "Lower leaves yellow and drop first."],
     "prevention": ["Rotate crops and remove old plant debris.", "Mulch to reduce soil splash; avoid overhead watering.", "Stake plants for airflow."],
     "management": ["Remove infected lower leaves early.", "Consult a local expert about suitable treatment if infection is widespread."]},
    {"keys": ["bacterial spot"], "title": "Bacterial spot",
     "description": "A bacterial disease (Xanthomonas species) affecting tomato and pepper, spread by rain splash, tools and infected seed.",
     "symptoms": ["Small, dark, water-soaked spots that may have yellow halos.", "Spots can dry and fall out, giving a 'shot-hole' look.", "Raised scabby spots on fruit."],
     "prevention": ["Use clean seed and healthy transplants.", "Avoid working in wet fields; disinfect tools.", "Rotate with non-host crops."],
     "management": ["Remove and destroy infected plant material.", "Avoid overhead irrigation.", "Ask a local agricultural officer about approved options; bacterial diseases are hard to cure once established."]},
    {"keys": ["target spot"], "title": "Target spot",
     "description": "A fungal disease (Corynespora cassiicola) of tomato favoured by warm, humid weather.",
     "symptoms": ["Brown spots with concentric rings and a yellow halo.", "Lesions may merge, causing leaf drop.", "Spots can appear on fruit."],
     "prevention": ["Improve airflow and avoid prolonged leaf wetness.", "Remove crop residue after harvest.", "Rotate crops."],
     "management": ["Remove infected leaves.", "Consult local experts if disease pressure is high."]},
    {"keys": ["spider mite"], "title": "Spider mite damage",
     "description": "Tiny sap-feeding mites (e.g. two-spotted spider mite) that thrive in hot, dry conditions. This is a pest problem rather than a pathogen.",
     "symptoms": ["Fine yellow stippling on leaves.", "Fine webbing on the underside of leaves or between stems.", "Leaves turn bronze/dry and drop in heavy infestations."],
     "prevention": ["Avoid water stress and dusty conditions.", "Inspect leaf undersides regularly.", "Conserve natural enemies such as predatory mites."],
     "management": ["Wash plants with a strong water spray where practical.", "Remove heavily infested leaves.", "Ask a local expert about miticide options; wrong products can make mites worse."]},
    {"keys": ["yellow leaf curl"], "title": "Tomato yellow leaf curl virus",
     "description": "A virus spread mainly by whiteflies. There is no cure once a plant is infected.",
     "symptoms": ["Upward curling and yellowing of leaf edges.", "Stunted plants with small leaves.", "Reduced flowering and fruit set."],
     "prevention": ["Control whiteflies; use insect-proof nets for nurseries.", "Use resistant/tolerant varieties.", "Remove weeds that host whiteflies."],
     "management": ["Remove and destroy infected plants to limit spread.", "Seek local advice on integrated whitefly management."]},
    {"keys": ["mosaic virus"], "title": "Mosaic virus",
     "description": "A viral disease spread by contaminated hands/tools, seed and sometimes insects. There is no cure for infected plants.",
     "symptoms": ["Light and dark green mottling or mosaic pattern.", "Distorted, curled or narrow leaves.", "Stunted growth."],
     "prevention": ["Use certified seed and resistant varieties.", "Wash hands and disinfect tools.", "Control weeds and insect vectors."],
     "management": ["Remove and destroy infected plants.", "Do not handle healthy plants after infected ones without washing."]},
    {"keys": ["northern leaf blight"], "title": "Northern leaf blight (maize)",
     "description": "A fungal disease (Exserohilum turcicum) of maize favoured by moderate temperatures and long periods of leaf wetness.",
     "symptoms": ["Long, cigar-shaped grey-green to tan lesions on leaves.", "Lesions merge and can blight large leaf areas."],
     "prevention": ["Plant resistant hybrids.", "Rotate crops and manage residue (tillage).", "Avoid very dense planting."],
     "management": ["Monitor fields, especially before and around tasselling.", "Consult a local expert if lesions reach upper leaves early."]},
    {"keys": ["gray leaf spot", "grey leaf spot", "cercospora"], "title": "Gray leaf spot (maize)",
     "description": "A fungal disease (Cercospora zeae-maydis) of maize favoured by warm, humid weather and maize residue.",
     "symptoms": ["Narrow, rectangular tan to grey lesions running parallel to leaf veins.", "Lesions may merge and kill large leaf areas."],
     "prevention": ["Rotate away from maize; manage residue.", "Use tolerant hybrids.", "Improve airflow through suitable plant spacing."],
     "management": ["Scout fields regularly in humid weather.", "Consult local experts if infection is spreading to upper leaves."]},
    {"keys": ["common rust"], "title": "Common rust (maize)",
     "description": "A fungal disease (Puccinia sorghi) producing rust-coloured pustules, favoured by cool, humid conditions.",
     "symptoms": ["Small, circular to elongated reddish-brown pustules on both leaf surfaces.", "Pustules release powdery rust-coloured spores.", "Leaves may yellow and dry out in severe cases."],
     "prevention": ["Plant resistant hybrids.", "Avoid late planting where rust pressure is high."],
     "management": ["Monitor fields; severe early infection is more damaging.", "Seek local advice if pustules are widespread."]},
    {"keys": ["cedar apple rust"], "title": "Cedar apple rust",
     "description": "A fungal disease of apple that needs both apple and juniper/cedar hosts to complete its life cycle.",
     "symptoms": ["Bright yellow-orange spots on leaves, often with small dark centres.", "Tube-like structures may develop on the underside of leaves."],
     "prevention": ["Choose resistant apple varieties.", "Remove nearby juniper/cedar hosts where practical."],
     "management": ["Remove affected leaves where feasible.", "Consult local horticultural experts about protection timing."]},
    {"keys": ["apple scab", "scab"], "title": "Apple scab",
     "description": "A fungal disease (Venturia inaequalis) of apple favoured by cool, wet spring weather.",
     "symptoms": ["Olive-green to brown velvety spots on leaves.", "Scabby, cracked lesions on fruit.", "Premature leaf drop."],
     "prevention": ["Rake and remove fallen leaves in autumn.", "Prune for airflow.", "Use scab-resistant varieties."],
     "management": ["Remove infected leaves and fruit.", "Consult local experts about timing of protective measures."]},
    {"keys": ["black rot"], "title": "Black rot",
     "description": "A fungal disease affecting apple and grape, favoured by warm, wet weather; overwinters on mummified fruit and infected wood.",
     "symptoms": ["Brown leaf spots with darker borders (apple 'frogeye' leaf spot).", "Dark, shrivelled, rotting fruit.", "Tiny black fruiting bodies on lesions."],
     "prevention": ["Remove mummified fruit and prune out infected wood.", "Improve canopy airflow.", "Practise sanitation after harvest."],
     "management": ["Remove infected plant parts and dispose of them away from the orchard/vineyard.", "Consult local experts for region-specific protection plans."]},
    {"keys": ["esca", "black measles"], "title": "Esca (black measles) of grape",
     "description": "A complex trunk disease of grapevine caused by several fungi; symptoms can appear suddenly in warm weather.",
     "symptoms": ["Yellow or brown 'tiger-stripe' patterns between leaf veins.", "Dark spots on berries; shrivelled fruit.", "Internal wood decay in older vines."],
     "prevention": ["Protect pruning wounds and avoid large wounds.", "Use clean planting material."],
     "management": ["Mark and monitor affected vines; remove severely diseased wood.", "Consult viticulture specialists; options are limited once established."]},
    {"keys": ["leaf blight", "isariopsis"], "title": "Leaf blight (grape)",
     "description": "A fungal leaf disease (Isariopsis/Pseudocercospora) of grape typically appearing late in the season.",
     "symptoms": ["Irregular dark brown spots on leaves.", "Premature leaf drop in heavy infection."],
     "prevention": ["Ensure good canopy airflow and sanitation.", "Remove fallen leaves."],
     "management": ["Remove affected leaves where practical.", "Consult local experts if the disease progresses."]},
    {"keys": ["powdery mildew"], "title": "Powdery mildew",
     "description": "A fungal disease producing a white powdery coating; it thrives in moderate temperatures and humid air, and does not need free water on leaves.",
     "symptoms": ["White to grey powdery patches on leaves and shoots.", "Leaf distortion, yellowing or premature drop."],
     "prevention": ["Provide airflow and light penetration through pruning and spacing.", "Choose resistant varieties."],
     "management": ["Remove badly infected parts.", "Consult local experts about suitable options."]},
    {"keys": ["leaf scorch"], "title": "Leaf scorch",
     "description": "Browning of leaf margins and tips that can be caused by fungal infection but also by drought, heat or salt stress, so it is hard to be sure from a photo.",
     "symptoms": ["Brown, dry leaf edges or irregular scorched patches.", "Dark purple-brown spots (strawberry) in fungal forms."],
     "prevention": ["Maintain even irrigation and good drainage.", "Remove infected leaves after harvest."],
     "management": ["Check watering and soil conditions first.", "Consult a local expert to confirm the cause."]},
    {"keys": ["haunglongbing", "huanglongbing", "citrus greening"], "title": "Citrus greening (Huanglongbing)",
     "description": "A serious bacterial disease of citrus spread by psyllid insects. There is no cure.",
     "symptoms": ["Blotchy yellow mottling of leaves, often asymmetric.", "Small, lopsided, bitter fruit that stays partly green.", "Twig dieback and tree decline."],
     "prevention": ["Control psyllid vectors.", "Plant certified disease-free nursery stock."],
     "management": ["Report suspected cases to local plant-health authorities; confirmation needs laboratory testing."]},
]

_GENERIC = {
    "description": "Detailed information for this class has not been added to the application yet.",
    "symptoms": ["Not available."],
    "prevention": ["Practise crop rotation, field hygiene and avoid prolonged leaf wetness.", "Use healthy seed/planting material."],
    "management": ["Consult a local agricultural extension officer for diagnosis and treatment advice."],
}


def normalise(text: str) -> str:
    text = re.sub(r"\(.*?\)", " ", text.lower())
    text = text.replace("_", " ")
    return re.sub(r"[^a-z0-9 ]+", " ", text).strip()


def split_class_name(class_name: str):
    """'Tomato___Early_blight' -> ('Tomato', 'Early blight'). Falls back gracefully."""
    if "___" in class_name:
        crop, disease = class_name.split("___", 1)
    elif "__" in class_name:
        crop, disease = class_name.split("__", 1)
    else:
        crop, disease = "Unknown", class_name
    clean = lambda s: re.sub(r"\s+", " ", s.replace("_", " ")).strip(" ,")
    return clean(crop), clean(disease)


def is_healthy(disease_name: str) -> bool:
    return "healthy" in normalise(disease_name)


def get_disease_info(disease_name: str) -> dict:
    if is_healthy(disease_name):
        return {"title": "Healthy", **HEALTHY}
    norm = normalise(disease_name)
    candidates = []
    for entry in INFO:
        for key in entry["keys"]:
            if key in norm:
                candidates.append((len(key), entry))
    if candidates:
        return max(candidates, key=lambda c: c[0])[1]
    return {"title": disease_name, **_GENERIC}
