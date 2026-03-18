"""
Seed database with initial ingredient safety data.
Sources: FDA, American College of Obstetricians and Gynecologists, peer-reviewed literature.

Run: python seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, init_db
from app.models.ingredient import Ingredient, IngredientAlias

def normalize(name: str) -> str:
    return name.lower().strip()

# Format: (name, safety_level, category, why_flagged, safe_alternatives, aliases)
INGREDIENTS = [
    # ===== AVOID =====
    ("Retinol", "avoid", "active",
     "Vitamin A derivative linked to birth defects (teratogenic). All retinoids are contraindicated during pregnancy.",
     "Bakuchiol, Niacinamide, Vitamin C",
     ["Retinyl Palmitate", "Retinaldehyde", "Retinoic Acid", "Tretinoin", "Adapalene", "Tazarotene", "Retinyl Acetate", "Vitamin A"]),

    ("Salicylic Acid", "avoid", "active",
     "High-dose salicylic acid (BHA) is related to aspirin and may pose risks. Low concentrations (<2%) in wash-off products may be acceptable — consult your provider.",
     "Glycolic Acid (low concentration), Azelaic Acid",
     ["BHA", "Beta Hydroxy Acid", "2-Hydroxybenzoic Acid"]),

    ("Hydroquinone", "avoid", "active",
     "Skin-lightening agent with high systemic absorption (35-45%). Not recommended during pregnancy.",
     "Vitamin C, Azelaic Acid, Niacinamide, Arbutin",
     ["Hydroquinol", "1,4-Benzenediol"]),

    ("Formaldehyde", "avoid", "preservative",
     "Known carcinogen and teratogen. Banned or restricted in cosmetics in many countries.",
     "Phenoxyethanol, Sodium Benzoate",
     ["Formalin", "Methanal", "Methylene Oxide"]),

    ("Formaldehyde-Releasing Preservatives", "avoid", "preservative",
     "Release formaldehyde over time. Includes DMDM Hydantoin, Quaternium-15, Diazolidinyl Urea, Imidazolidinyl Urea.",
     "Phenoxyethanol, Potassium Sorbate",
     ["DMDM Hydantoin", "Quaternium-15", "Diazolidinyl Urea", "Imidazolidinyl Urea", "Bronopol", "2-Bromo-2-Nitropropane-1,3-Diol"]),

    ("Phthalates", "avoid", "fragrance",
     "Endocrine disruptors linked to reproductive harm and developmental issues. Often hidden in 'fragrance'.",
     "Phthalate-free fragrance, Essential oils (select safe ones)",
     ["Diethyl Phthalate", "DEP", "DBP", "Dibutyl Phthalate", "DEHP"]),

    ("Toluene", "avoid", "solvent",
     "Toxic solvent found in nail polish. Linked to developmental damage and reproductive harm.",
     "Ethyl Acetate, Water-based nail polish",
     ["Methylbenzene", "Toluol"]),

    ("Chemical Sunscreens - Oxybenzone", "avoid", "active",
     "Endocrine disruptor with high skin absorption. Associated with low birth weight in studies.",
     "Zinc Oxide, Titanium Dioxide (mineral sunscreen)",
     ["Oxybenzone", "Benzophenone-3", "BP-3"]),

    ("Avobenzone", "caution", "active",
     "Chemical UV filter with some endocrine disruption concerns. Mineral sunscreens are preferred during pregnancy.",
     "Zinc Oxide, Titanium Dioxide",
     ["Butyl Methoxydibenzoylmethane"]),

    ("Octinoxate", "avoid", "active",
     "Chemical UV filter and endocrine disruptor. Banned in Hawaii for coral reef damage. Avoid during pregnancy.",
     "Zinc Oxide, Titanium Dioxide",
     ["Octyl Methoxycinnamate", "Ethylhexyl Methoxycinnamate", "OMC"]),

    ("Homosalate", "caution", "active",
     "Chemical UV filter that may disrupt hormones at high concentrations. Prefer mineral sunscreens.",
     "Zinc Oxide, Titanium Dioxide",
     ["HMS"]),

    ("Camphor", "avoid", "active",
     "Can be toxic if absorbed systemically. Avoid topical camphor products during pregnancy.",
     "Menthol (in small amounts), cool compresses",
     []),

    ("Parabens", "caution", "preservative",
     "Weak estrogen mimics. While low concentrations may be low-risk, many experts recommend avoiding during pregnancy as a precaution.",
     "Phenoxyethanol, Potassium Sorbate, Sodium Benzoate",
     ["Methylparaben", "Ethylparaben", "Propylparaben", "Butylparaben", "Isobutylparaben"]),

    ("Thioglycolic Acid", "avoid", "active",
     "Used in chemical hair removers and perms. Can be absorbed through skin. Avoid during pregnancy.",
     "Shaving, waxing, sugaring",
     ["Mercaptoacetic Acid"]),

    ("Lead Acetate", "avoid", "colorant",
     "Heavy metal — neurotoxic. Found in some progressive hair dyes. Absolutely avoid during pregnancy.",
     "Henna, plant-based dyes",
     []),

    ("Mercury", "avoid", "active",
     "Neurotoxic heavy metal. Found in some skin-lightening creams. Extremely dangerous during pregnancy.",
     "Vitamin C, Niacinamide, Azelaic Acid",
     ["Thimerosal", "Mercurous Chloride", "Calomel"]),

    ("Diethanolamine", "avoid", "emulsifier",
     "Can react with other ingredients to form carcinogenic nitrosamines. Skin irritant with absorption concerns.",
     "Cocamidopropyl Betaine",
     ["DEA", "Cocamide DEA", "Lauramide DEA"]),

    ("Triclosan", "avoid", "preservative",
     "Endocrine disruptor and antibiotic. FDA banned it from consumer antiseptic washes. Avoid during pregnancy.",
     "Regular soap and water",
     []),

    # ===== CAUTION =====
    ("Benzoyl Peroxide", "caution", "active",
     "Limited studies in pregnancy. Low systemic absorption but consult your provider. Short-contact use may be acceptable.",
     "Azelaic Acid (preferred for pregnancy acne)",
     ["BPO"]),

    ("Glycolic Acid", "caution", "active",
     "AHA with generally low risk at low concentrations (<10%). High-concentration peels should be avoided.",
     "Lactic Acid (gentler AHA)",
     ["AHA", "Alpha Hydroxy Acid", "Hydroxyacetic Acid"]),

    ("Lactic Acid", "caution", "active",
     "AHA — generally considered safe at low concentrations in skincare. Avoid high-concentration peels.",
     None,
     ["Alpha Hydroxy Acid"]),

    ("Azelaic Acid", "safe", "active",
     None,
     None,
     ["Nonanedioic Acid"]),

    ("Essential Oils - Tea Tree", "caution", "fragrance",
     "Tea tree oil has hormonal properties. Use sparingly and diluted if at all during pregnancy.",
     "Fragrance-free products",
     ["Tea Tree Oil", "Melaleuca Alternifolia Oil"]),

    ("Essential Oils - Rosemary", "caution", "fragrance",
     "May stimulate uterine contractions in concentrated forms. Avoid in first trimester.",
     "Lavender (generally safer)",
     ["Rosemary Oil", "Rosmarinus Officinalis Leaf Oil"]),

    ("Essential Oils - Clary Sage", "avoid", "fragrance",
     "Known uterotonic — can stimulate contractions. Avoid throughout pregnancy.",
     "Lavender essential oil",
     ["Clary Sage Oil", "Salvia Sclarea Oil"]),

    ("Fragrance", "caution", "fragrance",
     "Synthetic fragrances may contain undisclosed phthalates or allergens. Choose fragrance-free when possible.",
     "Fragrance-free products, products scented with safe essential oils",
     ["Parfum", "Aroma", "Synthetic Fragrance"]),

    ("Aluminum Chlorohydrate", "caution", "active",
     "Found in antiperspirants. Limited pregnancy data. Natural deodorants are a safer choice.",
     "Aluminum-free deodorants",
     ["Aluminum Chloride", "Aluminium Chlorohydrate"]),

    # ===== SAFE =====
    ("Water", "safe", "solvent", None, None,
     ["Aqua", "Eau", "Purified Water", "Deionized Water"]),

    ("Glycerin", "safe", "humectant", None, None,
     ["Glycerol", "Vegetable Glycerin"]),

    ("Hyaluronic Acid", "safe", "humectant", None, None,
     ["Sodium Hyaluronate", "HA", "Hyaluronan"]),

    ("Niacinamide", "safe", "active", None, None,
     ["Nicotinamide", "Vitamin B3"]),

    ("Vitamin C", "safe", "antioxidant", None, None,
     ["Ascorbic Acid", "L-Ascorbic Acid", "Sodium Ascorbyl Phosphate", "Ascorbyl Glucoside", "Magnesium Ascorbyl Phosphate"]),

    ("Vitamin E", "safe", "antioxidant", None, None,
     ["Tocopherol", "Tocopheryl Acetate", "Alpha-Tocopherol"]),

    ("Zinc Oxide", "safe", "active", None, None, []),

    ("Titanium Dioxide", "safe", "active", None, None, ["TiO2"]),

    ("Shea Butter", "safe", "emollient", None, None,
     ["Butyrospermum Parkii Butter", "Butyrospermum Parkii"]),

    ("Cocoa Butter", "safe", "emollient", None, None,
     ["Theobroma Cacao Seed Butter"]),

    ("Jojoba Oil", "safe", "emollient", None, None,
     ["Simmondsia Chinensis Seed Oil"]),

    ("Coconut Oil", "safe", "emollient", None, None,
     ["Cocos Nucifera Oil"]),

    ("Aloe Vera", "safe", "emollient", None, None,
     ["Aloe Barbadensis Leaf Juice", "Aloe Barbadensis Leaf Extract"]),

    ("Centella Asiatica", "safe", "active", None, None,
     ["Cica", "Gotu Kola", "Madecassoside", "Asiaticoside"]),

    ("Ceramides", "safe", "emollient", None, None,
     ["Ceramide NP", "Ceramide AP", "Ceramide EOP", "Phytosphingosine", "Sphingolipids"]),

    ("Squalane", "safe", "emollient", None, None,
     ["Squalene"]),

    ("Panthenol", "safe", "humectant", None, None,
     ["Provitamin B5", "D-Panthenol", "Dexpanthenol"]),

    ("Allantoin", "safe", "emollient", None, None, []),

    ("Colloidal Oatmeal", "safe", "emollient", None, None,
     ["Avena Sativa Kernel Flour"]),

    ("Petrolatum", "safe", "emollient", None, None,
     ["Petroleum Jelly", "Vaseline", "White Petrolatum"]),

    ("Dimethicone", "safe", "emollient", None, None,
     ["Polydimethylsiloxane", "PDMS"]),

    ("Phenoxyethanol", "safe", "preservative", None, None, []),

    ("Sodium Benzoate", "safe", "preservative", None, None, []),

    ("Potassium Sorbate", "safe", "preservative", None, None, []),

    ("Citric Acid", "safe", "ph_adjuster", None, None, []),

    ("Sodium Hydroxide", "safe", "ph_adjuster", None, None,
     ["Lye", "NaOH"]),

    ("Stearic Acid", "safe", "emulsifier", None, None, []),

    ("Cetyl Alcohol", "safe", "emollient", None, None, []),

    ("Cetearyl Alcohol", "safe", "emollient", None, None, []),

    ("Caprylic/Capric Triglyceride", "safe", "emollient", None, None,
     ["MCT Oil"]),

    ("Green Tea Extract", "safe", "antioxidant", None, None,
     ["Camellia Sinensis Leaf Extract", "EGCG"]),

    ("Chamomile Extract", "safe", "emollient", None, None,
     ["Matricaria Chamomilla", "Bisabolol", "Chamomilla Recutita"]),

    ("Bakuchiol", "safe", "active", None, None, []),

    ("Arbutin", "safe", "active", None, None,
     ["Alpha-Arbutin", "Beta-Arbutin"]),

    ("Tranexamic Acid", "caution", "active",
     "Topical use likely low risk, but it's also used as an oral medication. Discuss with your provider for topical use.",
     "Vitamin C, Niacinamide, Arbutin",
     []),

    ("Kojic Acid", "safe", "active", None, None, ["Kojic Dipalmitate"]),

    ("Licorice Root Extract", "safe", "active", None, None,
     ["Glycyrrhiza Glabra Root Extract", "Glabridin"]),

    ("Rosehip Oil", "safe", "emollient", None, None,
     ["Rosa Canina Seed Oil", "Rosa Mosqueta Oil"]),

    ("Argan Oil", "safe", "emollient", None, None,
     ["Argania Spinosa Kernel Oil"]),

    ("Marula Oil", "safe", "emollient", None, None,
     ["Sclerocarya Birrea Seed Oil"]),

    ("Sunflower Seed Oil", "safe", "emollient", None, None,
     ["Helianthus Annuus Seed Oil"]),

    ("Olive Oil", "safe", "emollient", None, None,
     ["Olea Europaea Fruit Oil"]),

    ("Witch Hazel", "safe", "active", None, None,
     ["Hamamelis Virginiana"]),

    ("Calendula Extract", "safe", "emollient", None, None,
     ["Calendula Officinalis Flower Extract"]),

    ("Peptides", "safe", "active", None, None,
     ["Palmitoyl Tripeptide", "Palmitoyl Tetrapeptide", "Copper Peptides", "Matrixyl", "Argireline"]),

    ("Sodium PCA", "safe", "humectant", None, None, []),

    ("Urea", "safe", "humectant", None, None, ["Carbamide"]),

    ("Propylene Glycol", "safe", "humectant", None, None, ["PG"]),

    ("Butylene Glycol", "safe", "humectant", None, None, ["BG", "1,3-Butanediol"]),

    ("Xanthan Gum", "safe", "thickener", None, None, []),

    ("Carbomer", "safe", "thickener", None, None, ["Carbopol"]),

    ("Polysorbate 20", "safe", "emulsifier", None, None, ["Tween 20"]),

    ("Polysorbate 80", "safe", "emulsifier", None, None, ["Tween 80"]),

    ("Sodium Lauryl Sulfate", "safe", "surfactant", None, None, ["SLS"]),

    ("Sodium Laureth Sulfate", "safe", "surfactant", None, None, ["SLES"]),

    ("Cocamidopropyl Betaine", "safe", "surfactant", None, None, []),

    ("Tocopheryl Acetate", "safe", "antioxidant", None, None, ["Vitamin E Acetate"]),

    ("Ethylhexylglycerin", "safe", "preservative", None, None, []),

    ("Caprylyl Glycol", "safe", "preservative", None, None, []),

    ("EDTA", "safe", "other", None, None,
     ["Disodium EDTA", "Tetrasodium EDTA"]),

    ("Mineral Oil", "safe", "emollient", None, None,
     ["Paraffinum Liquidum", "Liquid Paraffin"]),

    ("Lanolin", "safe", "emollient", None, None, []),

    ("Beeswax", "safe", "emollient", None, None,
     ["Cera Alba"]),

    ("Iron Oxides", "safe", "colorant", None, None,
     ["CI 77491", "CI 77492", "CI 77499"]),

    ("Mica", "safe", "colorant", None, None, ["CI 77019"]),
]


def seed():
    init_db()
    db = SessionLocal()

    added = 0
    skipped = 0

    for item in INGREDIENTS:
        name, safety, category, why_flagged, alternatives, aliases = item
        norm = normalize(name)

        existing = db.query(Ingredient).filter(Ingredient.name_normalized == norm).first()
        if existing:
            skipped += 1
            continue

        ing = Ingredient(
            name=name,
            name_normalized=norm,
            safety_level=safety,
            category=category,
            why_flagged=why_flagged,
            safe_alternatives=alternatives,
            source="curated_medical_literature",
            confidence_score=1.0,
        )
        db.add(ing)
        db.flush()

        for alias_name in aliases:
            alias = IngredientAlias(
                ingredient_id=ing.id,
                alias=alias_name,
                alias_normalized=normalize(alias_name),
            )
            db.add(alias)

        added += 1

    db.commit()
    db.close()

    print(f"✅ Seeded {added} ingredients ({skipped} already existed)")
    print(f"📊 Total unique ingredients: {added}")

    # Count aliases
    db = SessionLocal()
    alias_count = db.query(IngredientAlias).count()
    ing_count = db.query(Ingredient).count()
    db.close()
    print(f"📊 Total ingredients in DB: {ing_count}")
    print(f"📊 Total aliases: {alias_count}")


if __name__ == "__main__":
    seed()
