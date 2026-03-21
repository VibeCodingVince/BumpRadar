#!/usr/bin/env python3
"""Populate pregnancy safety database with 300+ food-related ingredients."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'pregnancy_safety.db')

# Each entry: (name, safety_level, category, description, why_flagged, safe_alternatives, source, confidence_score, aliases)
FOOD_INGREDIENTS = [
    # ============================================================
    # FOOD ADDITIVES - Preservatives, colors, flavor enhancers
    # ============================================================
    ("Sodium Nitrite", "caution", "food_additive",
     "Preservative commonly used in cured and processed meats.",
     "Forms nitrosamines which are potentially carcinogenic; linked to methemoglobinemia. Limit intake during pregnancy.",
     "Fresh uncured meats, celery-powder-cured alternatives", "fda_guidance", 0.8,
     ["E250", "Nitrite"]),

    ("Sodium Nitrate", "caution", "food_additive",
     "Preservative used in cured meats and some cheeses.",
     "Converts to nitrite in the body; same concerns as sodium nitrite regarding nitrosamine formation.",
     "Fresh meats, uncured options", "fda_guidance", 0.8,
     ["E251"]),

    ("BHA", "caution", "food_additive",
     "Butylated hydroxyanisole, a synthetic antioxidant preservative.",
     "Classified as possibly carcinogenic by IARC. Limited data on pregnancy safety.",
     "Vitamin E (tocopherols) as natural antioxidant", "fda_guidance", 0.7,
     ["Butylated Hydroxyanisole", "E320"]),

    ("BHT", "caution", "food_additive",
     "Butylated hydroxytoluene, a synthetic antioxidant preservative.",
     "Limited pregnancy safety data; some animal studies show developmental concerns at high doses.",
     "Vitamin E (tocopherols), rosemary extract", "fda_guidance", 0.7,
     ["Butylated Hydroxytoluene", "E321"]),

    ("MSG", "safe", "food_additive",
     "Monosodium glutamate, a flavor enhancer. FDA considers it generally recognized as safe (GRAS).",
     None, None, "fda_guidance", 0.85,
     ["Monosodium Glutamate", "E621", "Glutamate"]),

    ("Sodium Benzoate", "caution", "food_additive",
     "Preservative used in acidic foods and beverages.",
     "Can form benzene when combined with ascorbic acid (vitamin C). Keep intake moderate during pregnancy.",
     "Fresh foods without preservatives", "fda_guidance", 0.7,
     ["E211"]),

    ("Potassium Sorbate", "safe", "food_additive",
     "Common preservative in foods, generally recognized as safe by FDA.",
     None, None, "fda_guidance", 0.85,
     ["E202", "Sorbic Acid Potassium Salt"]),

    ("Carrageenan", "caution", "food_additive",
     "Thickener and stabilizer derived from seaweed.",
     "Some studies link degraded carrageenan to gastrointestinal inflammation. Debated safety profile.",
     "Guar gum, xanthan gum", "curated_medical_literature", 0.6,
     ["E407", "Irish Moss Extract"]),

    ("Xanthan Gum", "safe", "food_additive",
     "Common food thickener and stabilizer, generally recognized as safe.",
     None, None, "fda_guidance", 0.9,
     ["E415"]),

    ("Guar Gum", "safe", "food_additive",
     "Natural thickener from guar beans, widely used in food products.",
     None, None, "fda_guidance", 0.9,
     ["E412"]),

    ("Red Dye No. 3", "caution", "food_additive",
     "Synthetic food coloring (Erythrosine).",
     "FDA banned in cosmetics due to thyroid tumor risk in animals. Still allowed in food but being phased out. Avoid during pregnancy as precaution.",
     "Beet juice, paprika extract for natural red color", "fda_guidance", 0.8,
     ["Erythrosine", "E127", "FD&C Red No. 3", "Red 3"]),

    ("Red Dye No. 40", "caution", "food_additive",
     "Most commonly used food dye in the US.",
     "Some studies suggest behavioral effects in children. Limited pregnancy-specific data. Moderate intake likely fine.",
     "Beet juice, tomato-based colorings", "fda_guidance", 0.6,
     ["Allura Red", "E129", "FD&C Red No. 40", "Red 40"]),

    ("Yellow No. 5", "caution", "food_additive",
     "Synthetic food dye (Tartrazine).",
     "Can cause allergic reactions in sensitive individuals. Limited pregnancy data; moderate intake as precaution.",
     "Turmeric, annatto for natural yellow color", "fda_guidance", 0.6,
     ["Tartrazine", "E102", "FD&C Yellow No. 5", "Yellow 5"]),

    ("Yellow No. 6", "caution", "food_additive",
     "Synthetic food dye (Sunset Yellow).",
     "Some concern about hypersensitivity reactions. Limited pregnancy-specific studies.",
     "Turmeric, saffron for natural color", "fda_guidance", 0.6,
     ["Sunset Yellow", "E110", "FD&C Yellow No. 6", "Yellow 6"]),

    ("Blue No. 1", "caution", "food_additive",
     "Synthetic food dye (Brilliant Blue).",
     "Generally considered low risk but limited pregnancy-specific safety data. Moderate intake.",
     "Spirulina extract for natural blue", "fda_guidance", 0.6,
     ["Brilliant Blue", "E133", "FD&C Blue No. 1", "Blue 1"]),

    ("Blue No. 2", "caution", "food_additive",
     "Synthetic food dye (Indigo Carmine).",
     "Limited pregnancy safety data for synthetic dyes as a class.",
     "Butterfly pea flower, blueberry extract", "fda_guidance", 0.6,
     ["Indigo Carmine", "E132", "FD&C Blue No. 2", "Blue 2"]),

    ("Titanium Dioxide", "caution", "food_additive",
     "White colorant used in candies, chewing gum, and supplements.",
     "Banned as food additive in EU (2022). Nanoparticle concerns for gut absorption. Avoid during pregnancy as precaution.",
     "Foods without whitening agents", "fda_guidance", 0.7,
     ["E171", "TiO2"]),

    ("Sodium Sulfite", "caution", "food_additive",
     "Preservative used in dried fruits and wine.",
     "Can trigger asthma and allergic reactions. May cause issues in sulfite-sensitive individuals during pregnancy.",
     "Unsulfured dried fruits, sulfite-free wines", "fda_guidance", 0.75,
     ["E221", "Sulfites", "Sulphites"]),

    ("Calcium Propionate", "safe", "food_additive",
     "Preservative used in bread and baked goods, generally recognized as safe.",
     None, None, "fda_guidance", 0.85,
     ["E282"]),

    ("Phosphoric Acid", "caution", "food_additive",
     "Acidulant used in cola drinks.",
     "High intake may affect calcium absorption, important during pregnancy for fetal bone development.",
     "Water, natural fruit juices", "curated_medical_literature", 0.7,
     ["E338"]),

    ("Citric Acid", "safe", "food_additive",
     "Natural acid found in citrus fruits, widely used as flavoring and preservative.",
     None, None, "fda_guidance", 0.95,
     ["E330"]),

    ("Lecithin", "safe", "food_additive",
     "Emulsifier derived from soybeans or eggs. Provides choline which is beneficial in pregnancy.",
     None, None, "fda_guidance", 0.9,
     ["Soy Lecithin", "E322"]),

    ("Polysorbate 80", "caution", "food_additive",
     "Emulsifier used in ice cream and other processed foods.",
     "Some animal studies suggest potential gut microbiome disruption. Limited human pregnancy data.",
     "Foods without emulsifiers, homemade versions", "curated_medical_literature", 0.6,
     ["E433", "Tween 80"]),

    ("Sodium Aluminum Phosphate", "caution", "food_additive",
     "Leavening agent in baking powders and processed cheese.",
     "Contains aluminum; high aluminum intake should be avoided during pregnancy due to potential neurotoxicity.",
     "Aluminum-free baking powder", "curated_medical_literature", 0.7,
     ["E541"]),

    ("Annatto", "safe", "food_additive",
     "Natural food coloring derived from achiote seeds.",
     None, None, "fda_guidance", 0.85,
     ["E160b", "Achiote"]),

    ("Acesulfame Potassium", "caution", "food_additive",
     "Artificial sweetener often blended with other sweeteners.",
     "Crosses the placenta. Limited long-term pregnancy outcome data. FDA considers it safe but use in moderation.",
     "Small amounts of sugar, stevia", "fda_guidance", 0.7,
     ["Acesulfame K", "Ace-K", "E950"]),

    ("High Fructose Corn Syrup", "caution", "food_additive",
     "Common sweetener in processed foods and beverages.",
     "Excessive intake linked to gestational diabetes, excessive weight gain, and metabolic issues during pregnancy.",
     "Moderate amounts of regular sugar, honey, maple syrup", "curated_medical_literature", 0.8,
     ["HFCS", "Corn Sugar", "Glucose-Fructose Syrup"]),

    ("Sodium Erythorbate", "safe", "food_additive",
     "Antioxidant used in processed meats, isomer of ascorbic acid.",
     None, None, "fda_guidance", 0.85,
     ["E316"]),

    ("TBHQ", "caution", "food_additive",
     "Tert-butylhydroquinone, a synthetic antioxidant preservative.",
     "High doses shown to cause stomach tumors in animal studies. Limited pregnancy data; use moderation.",
     "Foods preserved with vitamin E, rosemary extract", "fda_guidance", 0.7,
     ["Tert-Butylhydroquinone", "E319"]),

    ("Propylene Glycol", "caution", "food_additive",
     "Humectant and solvent used in food and drinks.",
     "Generally recognized as safe in small amounts, but large doses may cause lactic acidosis. Moderate intake during pregnancy.",
     "Foods without this additive", "fda_guidance", 0.7,
     ["E1520", "PG"]),

    # ============================================================
    # SWEETENERS
    # ============================================================
    ("Aspartame", "caution", "sweetener",
     "Artificial sweetener found in diet sodas and sugar-free products.",
     "Contains phenylalanine — dangerous for those with PKU. FDA says safe for general population but moderate use advised during pregnancy.",
     "Stevia, small amounts of sugar", "fda_guidance", 0.8,
     ["NutraSweet", "Equal", "E951"]),

    ("Saccharin", "avoid", "sweetener",
     "Artificial sweetener (Sweet'N Low).",
     "Crosses the placenta and is slowly cleared by the fetus. ACOG and many guidelines recommend avoiding during pregnancy.",
     "Stevia, sucralose in moderation, small amounts of sugar", "acog_guidelines", 0.85,
     ["Sweet'N Low", "E954"]),

    ("Sucralose", "caution", "sweetener",
     "Artificial sweetener (Splenda).",
     "Generally considered safe during pregnancy by FDA, but some studies suggest potential effects on gut microbiome and glucose metabolism. Use in moderation.",
     "Stevia, small amounts of sugar or honey", "fda_guidance", 0.75,
     ["Splenda", "E955"]),

    ("Stevia", "safe", "sweetener",
     "Natural sweetener derived from the Stevia rebaudiana plant. High-purity steviol glycosides are FDA-approved.",
     None, None, "fda_guidance", 0.85,
     ["Steviol Glycosides", "Reb A", "Rebaudioside A", "E960", "Truvia", "PureVia"]),

    ("Erythritol", "safe", "sweetener",
     "Sugar alcohol naturally found in some fruits. Well-tolerated and does not affect blood sugar.",
     None, None, "fda_guidance", 0.8,
     ["E968"]),

    ("Xylitol", "safe", "sweetener",
     "Sugar alcohol used in gum and dental products. Safe during pregnancy in normal food amounts.",
     None, None, "fda_guidance", 0.85,
     ["E967", "Birch Sugar"]),

    ("Sorbitol", "safe", "sweetener",
     "Sugar alcohol found naturally in fruits. Safe in moderate amounts; excess may cause GI discomfort.",
     None, None, "fda_guidance", 0.85,
     ["E420", "Glucitol"]),

    ("Monk Fruit Extract", "safe", "sweetener",
     "Natural sweetener from monk fruit (luo han guo). No known safety concerns during pregnancy.",
     None, None, "fda_guidance", 0.8,
     ["Luo Han Guo", "Mogrosides", "Monk Fruit Sweetener"]),

    ("Mannitol", "safe", "sweetener",
     "Sugar alcohol used as sweetener. Safe in food amounts during pregnancy.",
     None, None, "fda_guidance", 0.85,
     ["E421"]),

    ("Neotame", "caution", "sweetener",
     "Artificial sweetener, derivative of aspartame but more potent.",
     "FDA-approved but very limited pregnancy-specific safety data. Use with caution.",
     "Stevia, small amounts of sugar", "fda_guidance", 0.65,
     ["E961"]),

    ("Advantame", "caution", "sweetener",
     "Newest FDA-approved artificial sweetener.",
     "Very limited pregnancy-specific safety data despite FDA GRAS status.",
     "Stevia, monk fruit", "fda_guidance", 0.6,
     ["E969"]),

    ("Allulose", "safe", "sweetener",
     "Rare sugar found naturally in figs and raisins. Low-calorie, does not raise blood sugar.",
     None, None, "fda_guidance", 0.75,
     ["D-Allulose", "D-Psicose"]),

    ("Cyclamate", "avoid", "sweetener",
     "Artificial sweetener banned in the US since 1969.",
     "Banned by FDA due to cancer concerns. Still used in some countries. Avoid during pregnancy.",
     "Stevia, monk fruit, erythritol", "fda_guidance", 1.0,
     ["E952", "Sodium Cyclamate"]),

    # ============================================================
    # HERBS & SPICES
    # ============================================================
    ("Blue Cohosh", "avoid", "herb",
     "Herbal supplement historically used to induce labor.",
     "Can cause uterine contractions, premature labor, and serious fetal heart defects. Strongly contraindicated in pregnancy.",
     "Consult healthcare provider for labor induction", "acog_guidelines", 1.0,
     ["Caulophyllum Thalictroides"]),

    ("Black Cohosh", "avoid", "herb",
     "Herbal supplement used for menopausal symptoms.",
     "May stimulate uterine contractions leading to preterm labor or miscarriage. Avoid throughout pregnancy.",
     "Consult healthcare provider for symptom management", "acog_guidelines", 0.95,
     ["Cimicifuga Racemosa", "Actaea Racemosa"]),

    ("Pennyroyal", "avoid", "herb",
     "Herb historically used as an abortifacient.",
     "Highly toxic. Can cause liver failure, seizures, and death. Known abortifacient. Absolutely avoid during pregnancy.",
     "Peppermint tea (safe alternative for mint flavor)", "curated_medical_literature", 1.0,
     ["Mentha Pulegium", "Pennyroyal Oil", "Squaw Mint"]),

    ("Dong Quai", "avoid", "herb",
     "Chinese herb used in traditional medicine.",
     "Acts as a uterine stimulant and may cause contractions. Also has blood-thinning properties. Avoid during pregnancy.",
     "Consult healthcare provider for alternatives", "acog_guidelines", 0.95,
     ["Angelica Sinensis", "Female Ginseng", "Chinese Angelica"]),

    ("Mugwort", "avoid", "herb",
     "Herb used in traditional medicine and cooking.",
     "Contains thujone which can stimulate the uterus and potentially cause miscarriage.",
     "Safe culinary herbs like basil or thyme", "curated_medical_literature", 0.9,
     ["Artemisia Vulgaris", "Common Wormwood"]),

    ("Wormwood", "avoid", "herb",
     "Herb used to flavor absinthe and in traditional medicine.",
     "Contains thujone, a neurotoxin that can cause seizures and stimulate uterine contractions.",
     "Safe herbs for flavoring", "curated_medical_literature", 0.95,
     ["Artemisia Absinthium", "Absinthe Wormwood"]),

    ("Tansy", "avoid", "herb",
     "Herb historically used as an abortifacient.",
     "Contains thujone; can cause uterine contractions, liver damage, and is potentially fatal in large doses.",
     "Safe culinary herbs", "curated_medical_literature", 0.95,
     ["Tanacetum Vulgare"]),

    ("Rue", "avoid", "herb",
     "Herb used in some traditional cuisines and folk medicine.",
     "Strong uterine stimulant; can cause miscarriage. Also causes phototoxic skin reactions.",
     "Other culinary herbs for flavoring", "curated_medical_literature", 0.9,
     ["Ruta Graveolens", "Common Rue"]),

    ("Comfrey", "avoid", "herb",
     "Herb used in traditional medicine for wound healing.",
     "Contains pyrrolizidine alkaloids which are hepatotoxic and potentially carcinogenic. FDA advises against internal use.",
     "Consult healthcare provider for wound care", "fda_guidance", 0.9,
     ["Symphytum Officinale"]),

    ("Saw Palmetto", "avoid", "herb",
     "Herbal supplement used for prostate issues.",
     "Has anti-androgenic effects that could interfere with fetal sexual development.",
     "Not needed during pregnancy; consult provider", "curated_medical_literature", 0.85,
     ["Serenoa Repens"]),

    ("Ephedra", "avoid", "herb",
     "Stimulant herb banned by FDA in dietary supplements.",
     "Can cause hypertension, heart attack, stroke. Banned by FDA. Absolutely avoid during pregnancy.",
     "No safe alternative needed; avoid entirely", "fda_guidance", 1.0,
     ["Ma Huang", "Ephedra Sinica"]),

    ("Goldenseal", "avoid", "herb",
     "Herb sometimes combined with echinacea for cold remedies.",
     "Contains berberine which can cross the placenta and may cause jaundice in newborns. Can stimulate uterine contractions.",
     "Consult healthcare provider for cold remedies", "curated_medical_literature", 0.85,
     ["Hydrastis Canadensis"]),

    ("Sassafras", "avoid", "herb",
     "Root bark traditionally used for tea and root beer flavoring.",
     "Contains safrole, classified as carcinogenic. FDA banned its use in food. Avoid during pregnancy.",
     "Sarsaparilla (for flavor), other safe teas", "fda_guidance", 0.9,
     ["Sassafras Albidum", "Safrole"]),

    ("Kava", "avoid", "herb",
     "Herbal supplement used for anxiety relief.",
     "Linked to severe liver damage. Sedative effects may be harmful to fetal development. Avoid during pregnancy.",
     "Chamomile tea, consult provider for anxiety management", "fda_guidance", 0.9,
     ["Kava Kava", "Piper Methysticum"]),

    ("Ginger", "safe", "herb",
     "Common spice. Evidence supports safety and efficacy for pregnancy-related nausea and vomiting.",
     None, None, "acog_guidelines", 0.95,
     ["Zingiber Officinale", "Ginger Root", "Fresh Ginger"]),

    ("Turmeric", "safe", "herb",
     "Common culinary spice. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     ["Curcuma Longa", "Curcumin"]),

    ("Cinnamon", "safe", "herb",
     "Common spice safe in culinary amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Cinnamomum", "Ceylon Cinnamon", "Cassia Cinnamon"]),

    ("Basil", "safe", "herb",
     "Common culinary herb. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Sweet Basil", "Ocimum Basilicum"]),

    ("Oregano", "safe", "herb",
     "Common culinary herb. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Origanum Vulgare"]),

    ("Thyme", "safe", "herb",
     "Common culinary herb. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Thymus Vulgaris"]),

    ("Rosemary", "safe", "herb",
     "Common culinary herb. Safe in food amounts. Avoid medicinal/concentrated doses.",
     None, None, "curated_medical_literature", 0.85,
     ["Rosmarinus Officinalis", "Salvia Rosmarinus"]),

    ("Garlic", "safe", "herb",
     "Common culinary ingredient. Safe in food amounts during pregnancy. May help with blood pressure.",
     None, None, "curated_medical_literature", 0.9,
     ["Allium Sativum"]),

    ("Parsley", "safe", "herb",
     "Common culinary herb. Safe in food amounts. Avoid large medicinal doses which may stimulate uterus.",
     None, None, "curated_medical_literature", 0.85,
     ["Petroselinum Crispum"]),

    ("Sage", "safe", "herb",
     "Culinary herb safe in food amounts. Avoid concentrated sage oil during pregnancy.",
     None, None, "curated_medical_literature", 0.8,
     ["Salvia Officinalis", "Common Sage"]),

    ("Peppermint", "safe", "herb",
     "Common herb used in food and tea. Safe during pregnancy and may help with nausea.",
     None, None, "curated_medical_literature", 0.9,
     ["Mentha Piperita", "Peppermint Tea", "Peppermint Leaf"]),

    ("Chamomile", "safe", "herb",
     "Herbal tea ingredient. Generally considered safe in moderate tea amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.8,
     ["Matricaria Chamomilla", "German Chamomile", "Chamomile Tea"]),

    ("Fenugreek", "caution", "herb",
     "Herb used in cooking and as a galactagogue.",
     "May stimulate uterine contractions in large amounts. Safe in culinary quantities but avoid supplements during pregnancy.",
     "Use only in culinary amounts", "curated_medical_literature", 0.8,
     ["Trigonella Foenum-Graecum", "Methi"]),

    ("Licorice Root", "caution", "herb",
     "Herb used in candy and traditional medicine.",
     "Contains glycyrrhizin which can raise blood pressure and is associated with preterm birth and lower IQ in some studies. Avoid large amounts.",
     "Anise or fennel for similar flavor", "curated_medical_literature", 0.85,
     ["Glycyrrhiza Glabra", "Liquorice"]),

    ("Echinacea", "caution", "herb",
     "Herbal supplement used for immune support.",
     "Limited but generally reassuring pregnancy safety data. Some healthcare providers advise caution due to immune-modulating effects.",
     "Vitamin C-rich foods, adequate rest", "curated_medical_literature", 0.65,
     ["Echinacea Purpurea", "Purple Coneflower"]),

    ("Ginseng", "caution", "herb",
     "Herbal supplement used for energy and vitality.",
     "Some animal studies suggest potential teratogenic effects. Limited human data. Avoid during pregnancy as precaution.",
     "Adequate rest, balanced diet", "curated_medical_literature", 0.75,
     ["Panax Ginseng", "Asian Ginseng", "Korean Ginseng"]),

    ("St. John's Wort", "avoid", "herb",
     "Herbal supplement used for depression.",
     "Interacts with many medications. May reduce effectiveness of prenatal medications. Animal studies show potential birth defects.",
     "Consult healthcare provider for safe depression treatment", "curated_medical_literature", 0.85,
     ["Hypericum Perforatum"]),

    ("Valerian", "caution", "herb",
     "Herbal supplement used for sleep and anxiety.",
     "Insufficient safety data during pregnancy. Some animal studies suggest potential concerns.",
     "Good sleep hygiene, consult provider for insomnia", "curated_medical_literature", 0.7,
     ["Valeriana Officinalis", "Valerian Root"]),

    ("Evening Primrose Oil", "avoid", "herb",
     "Supplement sometimes used to ripen the cervix.",
     "Can stimulate uterine contractions and potentially cause premature rupture of membranes. Avoid during pregnancy.",
     "Consult healthcare provider for cervical ripening", "acog_guidelines", 0.85,
     ["EPO", "Oenothera Biennis"]),

    ("Raspberry Leaf", "caution", "herb",
     "Traditional herbal tea used in late pregnancy.",
     "May stimulate uterine contractions. Generally advised to avoid in first trimester. Some providers allow in third trimester.",
     "Peppermint or ginger tea", "curated_medical_literature", 0.75,
     ["Red Raspberry Leaf", "Rubus Idaeus"]),

    ("Fennel", "safe", "herb",
     "Culinary herb and spice. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     ["Foeniculum Vulgare", "Fennel Seed"]),

    ("Dill", "safe", "herb",
     "Common culinary herb. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Anethum Graveolens"]),

    ("Cumin", "safe", "herb",
     "Common culinary spice. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Cuminum Cyminum"]),

    ("Coriander", "safe", "herb",
     "Common culinary herb/spice. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Cilantro", "Coriandrum Sativum", "Chinese Parsley"]),

    ("Black Pepper", "safe", "herb",
     "Common spice. Safe in normal culinary amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Piper Nigrum"]),

    ("Nutmeg", "caution", "herb",
     "Common baking spice.",
     "Safe in small culinary amounts. Large doses (>1 tablespoon) can be hallucinogenic and toxic, potentially causing contractions.",
     "Use only in small recipe amounts", "curated_medical_literature", 0.8,
     ["Myristica Fragrans"]),

    ("Saffron", "safe", "herb",
     "Expensive spice used in cooking. Safe in culinary amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     ["Crocus Sativus"]),

    ("Cardamom", "safe", "herb",
     "Common spice used in baking and cooking. Safe in food amounts.",
     None, None, "curated_medical_literature", 0.9,
     ["Elettaria Cardamomum"]),

    ("Clove", "safe", "herb",
     "Common spice. Safe in culinary amounts. Avoid clove oil supplements during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     ["Syzygium Aromaticum", "Cloves"]),

    ("Star Anise", "safe", "herb",
     "Spice used in cooking. Chinese star anise is safe; Japanese star anise is toxic and should be avoided.",
     None, None, "curated_medical_literature", 0.8,
     ["Illicium Verum", "Chinese Star Anise"]),

    ("Lemongrass", "safe", "herb",
     "Culinary herb used in Asian cooking. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     ["Cymbopogon"]),

    ("Hibiscus", "caution", "herb",
     "Herb used for tea and flavoring.",
     "May have emmenagogue effects (stimulate menstruation) and lower blood pressure. Some studies suggest it may affect estrogen levels. Avoid in large amounts.",
     "Peppermint tea, rooibos tea", "curated_medical_literature", 0.75,
     ["Hibiscus Sabdariffa", "Roselle", "Hibiscus Tea"]),

    ("Nettle Leaf", "caution", "herb",
     "Herbal tea ingredient.",
     "May stimulate uterine contractions in early pregnancy. Some midwives recommend in late pregnancy for mineral content, but evidence is mixed.",
     "Pregnancy-safe herbal teas", "curated_medical_literature", 0.7,
     ["Stinging Nettle", "Urtica Dioica"]),

    ("Aloe Vera", "caution", "herb",
     "Plant used in food and beverages.",
     "Aloe latex (found under the skin) contains anthraquinones which can cause uterine contractions. Inner gel in small amounts is likely safe.",
     "Other hydrating beverages", "curated_medical_literature", 0.8,
     ["Aloe Barbadensis"]),

    ("Neem", "avoid", "herb",
     "Herb used in traditional medicine and some foods.",
     "Has anti-fertility properties. Can cause miscarriage and has been used as a contraceptive in traditional medicine.",
     "Consult healthcare provider for alternatives", "curated_medical_literature", 0.85,
     ["Azadirachta Indica", "Neem Oil", "Neem Leaf"]),

    ("Papaya (Unripe)", "avoid", "herb",
     "Unripe or semi-ripe papaya fruit.",
     "Contains papain and latex which can stimulate uterine contractions. Ripe papaya is safe to eat.",
     "Ripe papaya, mango, other tropical fruits", "curated_medical_literature", 0.85,
     ["Green Papaya", "Raw Papaya"]),

    # ============================================================
    # SEAFOOD
    # ============================================================
    ("Shark", "avoid", "seafood",
     "Large predatory fish with very high mercury levels.",
     "Contains dangerously high levels of methylmercury which can damage fetal brain and nervous system development.",
     "Salmon, tilapia, shrimp, pollock", "fda_guidance", 1.0,
     ["Shark Meat", "Shark Fin"]),

    ("Swordfish", "avoid", "seafood",
     "Large predatory fish with very high mercury levels.",
     "Contains dangerously high mercury levels. FDA advises pregnant women to avoid entirely.",
     "Salmon, cod, tilapia", "fda_guidance", 1.0,
     ["Broadbill"]),

    ("King Mackerel", "avoid", "seafood",
     "Large mackerel species with very high mercury levels.",
     "Contains very high mercury levels. FDA advises pregnant women to avoid entirely.",
     "Atlantic mackerel (lower mercury), salmon", "fda_guidance", 1.0,
     ["Kingfish"]),

    ("Tilefish (Gulf of Mexico)", "avoid", "seafood",
     "Tilefish from the Gulf of Mexico has very high mercury levels.",
     "Among the highest mercury levels of any commercial fish. FDA advises pregnant women to avoid.",
     "Cod, pollock, catfish", "fda_guidance", 1.0,
     ["Golden Snapper", "Golden Tilefish"]),

    ("Bigeye Tuna", "avoid", "seafood",
     "Large tuna species with high mercury levels.",
     "Contains high mercury levels. FDA advises pregnant women to avoid.",
     "Canned light tuna, skipjack tuna, salmon", "fda_guidance", 0.95,
     ["Ahi Tuna"]),

    ("Marlin", "avoid", "seafood",
     "Large predatory fish with high mercury levels.",
     "Contains high mercury levels due to bioaccumulation in large predatory fish.",
     "Salmon, trout, sardines", "fda_guidance", 0.95,
     ["Blue Marlin", "White Marlin"]),

    ("Orange Roughy", "avoid", "seafood",
     "Deep-sea fish known for very high mercury levels.",
     "Contains high mercury and is extremely long-lived (can reach 150 years), accumulating more toxins.",
     "Cod, haddock, pollock", "fda_guidance", 0.9,
     ["Deep Sea Perch"]),

    ("Albacore Tuna", "caution", "seafood",
     "White tuna with moderate mercury levels.",
     "Contains more mercury than light tuna. FDA advises limiting to 6 oz (1 serving) per week during pregnancy.",
     "Canned light tuna, salmon, sardines", "fda_guidance", 0.95,
     ["White Tuna", "Canned White Tuna"]),

    ("Canned Light Tuna", "safe", "seafood",
     "Lower-mercury tuna option. FDA recommends up to 2-3 servings per week during pregnancy.",
     None, None, "fda_guidance", 0.9,
     ["Skipjack Tuna", "Chunk Light Tuna"]),

    ("Salmon", "safe", "seafood",
     "Excellent source of omega-3 fatty acids (DHA/EPA) with low mercury. Highly recommended during pregnancy when cooked.",
     None, None, "fda_guidance", 0.95,
     ["Atlantic Salmon", "Wild Salmon", "Sockeye Salmon", "Pink Salmon"]),

    ("Sardines", "safe", "seafood",
     "Small fish very low in mercury and high in omega-3s, calcium, and vitamin D. Excellent during pregnancy.",
     None, None, "fda_guidance", 0.95,
     ["Pilchards"]),

    ("Anchovies", "safe", "seafood",
     "Very small fish with very low mercury levels. Good source of omega-3s.",
     None, None, "fda_guidance", 0.95,
     []),

    ("Herring", "safe", "seafood",
     "Small fish with low mercury. Rich in omega-3 fatty acids.",
     None, None, "fda_guidance", 0.9,
     ["Kipper"]),

    ("Shrimp", "safe", "seafood",
     "Low-mercury shellfish. Safe and nutritious during pregnancy when cooked.",
     None, None, "fda_guidance", 0.95,
     ["Prawns"]),

    ("Cod", "safe", "seafood",
     "Low-mercury white fish. Safe during pregnancy when fully cooked.",
     None, None, "fda_guidance", 0.9,
     ["Atlantic Cod", "Pacific Cod"]),

    ("Pollock", "safe", "seafood",
     "Low-mercury white fish commonly used in fish sticks and imitation crab.",
     None, None, "fda_guidance", 0.9,
     ["Alaska Pollock", "Walleye Pollock"]),

    ("Catfish", "safe", "seafood",
     "Low-mercury freshwater fish. Safe during pregnancy when cooked.",
     None, None, "fda_guidance", 0.9,
     []),

    ("Tilapia", "safe", "seafood",
     "Low-mercury farmed fish. Safe during pregnancy when cooked.",
     None, None, "fda_guidance", 0.9,
     []),

    ("Trout", "safe", "seafood",
     "Low-mercury freshwater fish rich in omega-3s.",
     None, None, "fda_guidance", 0.9,
     ["Rainbow Trout"]),

    ("Halibut", "caution", "seafood",
     "Larger fish with moderate mercury levels.",
     "Contains moderate mercury. Limit to 1 serving per week during pregnancy.",
     "Cod, pollock, salmon", "fda_guidance", 0.85,
     ["Pacific Halibut", "Atlantic Halibut"]),

    ("Sea Bass", "caution", "seafood",
     "Some species contain moderate to high mercury levels.",
     "Chilean sea bass (Patagonian toothfish) has higher mercury. Limit consumption during pregnancy.",
     "Cod, tilapia, salmon", "fda_guidance", 0.8,
     ["Chilean Sea Bass", "Patagonian Toothfish"]),

    ("Grouper", "caution", "seafood",
     "Large reef fish with moderate to high mercury levels.",
     "Contains moderate mercury levels due to size and predatory nature. Limit during pregnancy.",
     "Snapper (smaller species), cod, mahi-mahi", "fda_guidance", 0.8,
     []),

    ("Mahi-Mahi", "safe", "seafood",
     "Moderate-sized fish with relatively low mercury levels. Safe in moderation during pregnancy.",
     None, None, "fda_guidance", 0.85,
     ["Dolphinfish", "Dorado"]),

    ("Raw Fish / Sushi", "avoid", "seafood",
     "Any raw or undercooked fish or shellfish.",
     "Risk of parasites (Anisakis), bacteria (Listeria, Salmonella, Vibrio), and viruses. Can cause serious infections during pregnancy.",
     "Cooked sushi rolls, fully cooked fish, vegetable sushi", "acog_guidelines", 1.0,
     ["Sashimi", "Raw Sushi", "Ceviche", "Poke"]),

    ("Raw Oysters", "avoid", "seafood",
     "Uncooked oysters and other raw shellfish.",
     "High risk of Vibrio, norovirus, and hepatitis A. Can cause severe illness during pregnancy.",
     "Cooked oysters, cooked shrimp", "fda_guidance", 1.0,
     ["Raw Shellfish", "Raw Clams", "Raw Mussels"]),

    ("Smoked Salmon (Cold)", "caution", "seafood",
     "Cold-smoked or lox-style salmon.",
     "Risk of Listeria contamination as it is not fully cooked. Heat to 165°F/74°C before eating or choose shelf-stable versions.",
     "Canned salmon, cooked salmon, hot-smoked salmon", "fda_guidance", 0.85,
     ["Lox", "Nova", "Cold Smoked Salmon", "Gravlax"]),

    ("Crab", "safe", "seafood",
     "Shellfish low in mercury. Safe during pregnancy when fully cooked.",
     None, None, "fda_guidance", 0.9,
     ["Crab Meat", "King Crab", "Snow Crab", "Dungeness Crab"]),

    ("Lobster", "safe", "seafood",
     "Shellfish with low mercury levels. Safe during pregnancy when fully cooked.",
     None, None, "fda_guidance", 0.9,
     []),

    ("Scallops", "safe", "seafood",
     "Low-mercury shellfish. Safe during pregnancy when cooked thoroughly.",
     None, None, "fda_guidance", 0.9,
     ["Sea Scallops", "Bay Scallops"]),

    ("Calamari", "safe", "seafood",
     "Squid — low mercury seafood. Safe during pregnancy when cooked.",
     None, None, "fda_guidance", 0.9,
     ["Squid"]),

    ("Clams", "safe", "seafood",
     "Shellfish with low mercury. Safe when fully cooked during pregnancy.",
     None, None, "fda_guidance", 0.9,
     ["Littleneck Clams", "Cherrystone Clams"]),

    ("Fish Oil Supplement", "safe", "seafood",
     "Purified fish oil supplements are safe and beneficial during pregnancy for DHA/EPA.",
     None, None, "acog_guidelines", 0.9,
     ["Omega-3 Supplement", "DHA Supplement", "EPA Supplement"]),

    # ============================================================
    # DAIRY
    # ============================================================
    ("Raw Milk", "avoid", "dairy",
     "Unpasteurized milk from cows, goats, or sheep.",
     "Can contain Listeria, Salmonella, E. coli, and Campylobacter. Listeriosis is 10x more likely in pregnant women and can cause miscarriage.",
     "Pasteurized milk", "fda_guidance", 1.0,
     ["Unpasteurized Milk", "Farm Fresh Milk"]),

    ("Brie", "caution", "dairy",
     "Soft cheese traditionally made from unpasteurized milk.",
     "Soft cheeses are at higher risk for Listeria if made with unpasteurized milk. Safe if made with pasteurized milk and eaten before expiry.",
     "Hard cheeses like cheddar, pasteurized brie", "fda_guidance", 0.85,
     []),

    ("Camembert", "caution", "dairy",
     "Soft-ripened cheese similar to brie.",
     "Risk of Listeria if made with unpasteurized milk. Check labels for pasteurized versions.",
     "Hard cheeses, pasteurized Camembert", "fda_guidance", 0.85,
     []),

    ("Feta Cheese", "caution", "dairy",
     "Soft brined cheese.",
     "Safe if made with pasteurized milk (most US commercial feta is). Risk of Listeria if unpasteurized.",
     "Pasteurized feta, ricotta", "fda_guidance", 0.8,
     ["Feta"]),

    ("Blue Cheese", "caution", "dairy",
     "Mold-ripened cheese.",
     "Higher risk of Listeria due to mold-ripening process and moisture content, especially if unpasteurized. Some pasteurized versions are safer.",
     "Hard cheeses like cheddar or Parmesan", "fda_guidance", 0.8,
     ["Gorgonzola", "Roquefort", "Stilton", "Danish Blue"]),

    ("Queso Fresco", "caution", "dairy",
     "Fresh Mexican-style cheese.",
     "Frequently linked to Listeria outbreaks due to unpasteurized milk use and high moisture content. Verify pasteurization.",
     "Pasteurized queso fresco, pasteurized Monterey Jack", "fda_guidance", 0.85,
     ["Queso Blanco", "Panela Cheese"]),

    ("Cheddar Cheese", "safe", "dairy",
     "Hard aged cheese. Safe during pregnancy due to low moisture and aging process.",
     None, None, "fda_guidance", 0.95,
     ["Cheddar"]),

    ("Parmesan", "safe", "dairy",
     "Hard aged cheese. Very low Listeria risk due to long aging and low moisture.",
     None, None, "fda_guidance", 0.95,
     ["Parmigiano-Reggiano", "Parmigiano"]),

    ("Swiss Cheese", "safe", "dairy",
     "Hard cheese safe during pregnancy.",
     None, None, "fda_guidance", 0.95,
     ["Emmental", "Gruyère"]),

    ("Mozzarella", "safe", "dairy",
     "Semi-soft cheese. Commercial pasteurized mozzarella is safe during pregnancy.",
     None, None, "fda_guidance", 0.9,
     ["Fresh Mozzarella"]),

    ("Ricotta", "safe", "dairy",
     "Soft cheese made from pasteurized whey. Safe during pregnancy when pasteurized.",
     None, None, "fda_guidance", 0.9,
     []),

    ("Cottage Cheese", "safe", "dairy",
     "Fresh cheese. Safe during pregnancy when pasteurized and consumed before expiry.",
     None, None, "fda_guidance", 0.9,
     []),

    ("Cream Cheese", "safe", "dairy",
     "Soft fresh cheese made from pasteurized milk. Safe during pregnancy.",
     None, None, "fda_guidance", 0.9,
     ["Philadelphia Cream Cheese"]),

    ("Pasteurized Milk", "safe", "dairy",
     "Heat-treated milk that is safe during pregnancy. Important source of calcium and vitamin D.",
     None, None, "fda_guidance", 0.95,
     ["Whole Milk", "Skim Milk", "2% Milk"]),

    ("Yogurt", "safe", "dairy",
     "Fermented dairy product. Pasteurized yogurt is safe and provides probiotics and calcium.",
     None, None, "fda_guidance", 0.95,
     ["Greek Yogurt", "Plain Yogurt"]),

    ("Goat Cheese (Soft)", "caution", "dairy",
     "Soft fresh goat cheese (chèvre).",
     "Risk of Listeria if made with unpasteurized milk. Pasteurized versions are safe. Aged/hard goat cheese is safer.",
     "Pasteurized goat cheese, hard goat cheese", "fda_guidance", 0.8,
     ["Chèvre"]),

    ("Ice Cream", "safe", "dairy",
     "Commercial ice cream made with pasteurized ingredients. Safe during pregnancy.",
     None, None, "fda_guidance", 0.9,
     []),

    ("Soft Serve Ice Cream", "caution", "dairy",
     "Machine-dispensed soft serve ice cream.",
     "Risk of Listeria from improperly cleaned soft serve machines. Commercial chains with proper hygiene are generally safe.",
     "Pre-packaged ice cream", "curated_medical_literature", 0.7,
     ["Soft Serve", "Mr. Whippy"]),

    # ============================================================
    # MEAT
    # ============================================================
    ("Deli Meat", "caution", "meat",
     "Pre-sliced, ready-to-eat lunch meats.",
     "Risk of Listeria contamination. Heat to steaming (165°F/74°C) before eating during pregnancy.",
     "Freshly cooked and sliced meat, heated deli meat", "acog_guidelines", 0.9,
     ["Lunch Meat", "Cold Cuts", "Sliced Turkey", "Sliced Ham", "Bologna", "Salami"]),

    ("Hot Dogs", "caution", "meat",
     "Pre-cooked processed meat.",
     "Risk of Listeria. Must be reheated until steaming hot (165°F/74°C) before eating during pregnancy.",
     "Freshly grilled meats, heated hot dogs", "fda_guidance", 0.9,
     ["Frankfurters", "Wieners"]),

    ("Pâté", "avoid", "meat",
     "Refrigerated meat or liver spreads.",
     "Refrigerated pâté has high risk of Listeria contamination. Also, liver pâté is very high in vitamin A (retinol) which can cause birth defects.",
     "Canned/shelf-stable pâté, hummus, other spreads", "fda_guidance", 0.9,
     ["Liver Pâté", "Meat Spread"]),

    ("Liver", "avoid", "meat",
     "Organ meat extremely high in preformed vitamin A (retinol).",
     "Excessive vitamin A (retinol) intake is teratogenic — can cause birth defects. One serving of liver can contain 10x the safe upper limit.",
     "Lean meats like chicken breast, beef steak", "acog_guidelines", 0.95,
     ["Beef Liver", "Chicken Liver", "Liver and Onions"]),

    ("Raw or Undercooked Meat", "avoid", "meat",
     "Any meat not cooked to safe internal temperature.",
     "Risk of Toxoplasma gondii, Salmonella, E. coli, and other pathogens. Toxoplasmosis can cause severe birth defects.",
     "Fully cooked meat to safe internal temperatures", "acog_guidelines", 1.0,
     ["Rare Steak", "Steak Tartare", "Beef Carpaccio", "Raw Meat"]),

    ("Raw or Undercooked Eggs", "avoid", "meat",
     "Raw eggs or foods containing raw eggs.",
     "Risk of Salmonella which can cause severe illness during pregnancy. Avoid homemade mayo, Caesar dressing, raw cookie dough.",
     "Pasteurized eggs, fully cooked eggs, commercial pasteurized egg products", "fda_guidance", 1.0,
     ["Raw Eggs", "Runny Eggs", "Soft-Boiled Eggs"]),

    ("Cooked Chicken", "safe", "meat",
     "Fully cooked poultry. Safe and excellent protein source during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Chicken Breast", "Roasted Chicken"]),

    ("Cooked Beef", "safe", "meat",
     "Fully cooked beef (to safe internal temp of 160°F/71°C for ground, 145°F/63°C for whole cuts with rest).",
     None, None, "curated_medical_literature", 0.95,
     ["Beef Steak (Well Done)", "Ground Beef (Cooked)"]),

    ("Cooked Pork", "safe", "meat",
     "Fully cooked pork (to 145°F/63°C with 3-minute rest). Good protein source during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Pork Loin", "Pork Chop (Cooked)"]),

    ("Bacon", "safe", "meat",
     "Cooked bacon is safe during pregnancy. Contains nitrates but in acceptable amounts when consumed occasionally.",
     None, None, "curated_medical_literature", 0.85,
     ["Cooked Bacon"]),

    ("Jerky", "caution", "meat",
     "Dried meat snack.",
     "Commercial jerky may not reach temperatures high enough to kill Toxoplasma. Also high in sodium and nitrates.",
     "Freshly cooked meat, commercial jerky from reputable brands", "curated_medical_literature", 0.7,
     ["Beef Jerky", "Turkey Jerky"]),

    ("Prosciutto", "caution", "meat",
     "Italian dry-cured ham, typically eaten uncooked.",
     "As a cured but uncooked meat, it carries risk of Toxoplasma and Listeria. Cook or heat before eating during pregnancy.",
     "Cooked ham, heated prosciutto", "curated_medical_literature", 0.8,
     ["Parma Ham"]),

    ("Pepperoni", "caution", "meat",
     "Cured sausage commonly used on pizza.",
     "When eaten uncooked (e.g., on charcuterie), carries Listeria and Toxoplasma risk. Safe when heated on pizza to steaming.",
     "Cooked/heated pepperoni on pizza", "curated_medical_literature", 0.8,
     []),

    ("Chorizo (Cured)", "caution", "meat",
     "Spanish-style cured sausage eaten without cooking.",
     "Uncooked cured meats carry risk of Toxoplasma and Listeria during pregnancy.",
     "Cooked Mexican-style chorizo, other cooked meats", "curated_medical_literature", 0.8,
     ["Spanish Chorizo"]),

    ("Ground Turkey", "safe", "meat",
     "Ground poultry. Safe when cooked to internal temperature of 165°F/74°C.",
     None, None, "curated_medical_literature", 0.95,
     ["Cooked Ground Turkey"]),

    # ============================================================
    # BEVERAGES
    # ============================================================
    ("Alcohol", "avoid", "beverage",
     "All alcoholic beverages including beer, wine, and spirits.",
     "No safe amount of alcohol during pregnancy. Causes Fetal Alcohol Spectrum Disorders (FASD), birth defects, intellectual disabilities, and growth restriction.",
     "Mocktails, sparkling water, non-alcoholic beer", "acog_guidelines", 1.0,
     ["Beer", "Wine", "Liquor", "Spirits", "Ethanol"]),

    ("Caffeine", "caution", "beverage",
     "Stimulant found in coffee, tea, chocolate, and energy drinks.",
     "ACOG recommends limiting to 200mg/day (about one 12oz coffee). High intake linked to increased miscarriage risk and low birth weight.",
     "Decaf coffee, herbal tea, water", "acog_guidelines", 0.95,
     ["Coffee", "Espresso"]),

    ("Green Tea", "caution", "beverage",
     "Tea containing caffeine and catechins.",
     "Contains caffeine (25-50mg per cup) — count toward 200mg daily limit. High catechin intake may reduce folate absorption.",
     "Decaffeinated green tea, peppermint tea, rooibos tea", "curated_medical_literature", 0.8,
     ["Matcha"]),

    ("Black Tea", "caution", "beverage",
     "Tea with moderate caffeine content.",
     "Contains caffeine (40-70mg per cup). Count toward 200mg daily caffeine limit. Tannins may reduce iron absorption.",
     "Decaf black tea, rooibos tea", "curated_medical_literature", 0.85,
     ["English Breakfast Tea", "Earl Grey", "Chai Tea"]),

    ("Herbal Tea (General)", "caution", "beverage",
     "Teas made from various herbs, flowers, and plants.",
     "Some herbal teas are safe (peppermint, ginger), but many lack safety data during pregnancy. Avoid teas with medicinal herb claims.",
     "Peppermint tea, ginger tea, rooibos tea", "acog_guidelines", 0.8,
     []),

    ("Rooibos Tea", "safe", "beverage",
     "Caffeine-free tea from South African red bush plant. Generally considered safe during pregnancy.",
     None, None, "curated_medical_literature", 0.8,
     ["Red Bush Tea", "Redbos"]),

    ("Ginger Tea", "safe", "beverage",
     "Tea made from ginger root. Safe and may help with pregnancy nausea.",
     None, None, "acog_guidelines", 0.9,
     ["Ginger Infusion"]),

    ("Energy Drinks", "avoid", "beverage",
     "Highly caffeinated beverages often containing other stimulants.",
     "Often contain 200-300mg+ caffeine per serving plus guarana, taurine, and other stimulants with unknown pregnancy effects.",
     "Water, sparkling water with fruit", "acog_guidelines", 0.95,
     ["Red Bull", "Monster Energy", "Rockstar Energy"]),

    ("Kombucha", "caution", "beverage",
     "Fermented tea beverage.",
     "Contains small amounts of alcohol (typically <0.5%), caffeine, and unpasteurized varieties may harbor harmful bacteria.",
     "Pasteurized sparkling beverages, sparkling water", "curated_medical_literature", 0.75,
     []),

    ("Unpasteurized Juice", "avoid", "beverage",
     "Fresh-squeezed or cold-pressed juices that have not been pasteurized.",
     "Can contain E. coli, Salmonella, and Cryptosporidium. FDA requires warning labels on unpasteurized juices.",
     "Pasteurized juice, whole fruits", "fda_guidance", 0.95,
     ["Fresh Squeezed Juice", "Cold Pressed Juice", "Raw Juice"]),

    ("Pasteurized Juice", "safe", "beverage",
     "Heat-treated juice safe during pregnancy. Good source of vitamins.",
     None, None, "fda_guidance", 0.95,
     ["Orange Juice", "Apple Juice"]),

    ("Water", "safe", "beverage",
     "Essential for hydration during pregnancy. Aim for 8-12 cups daily.",
     None, None, "curated_medical_literature", 1.0,
     ["Drinking Water", "Filtered Water", "Mineral Water"]),

    ("Sparkling Water", "safe", "beverage",
     "Carbonated water is safe during pregnancy. May help with nausea.",
     None, None, "curated_medical_literature", 0.95,
     ["Seltzer", "Club Soda", "Carbonated Water"]),

    ("Coconut Water", "safe", "beverage",
     "Natural hydrating beverage rich in electrolytes. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Diet Soda", "caution", "beverage",
     "Sugar-free carbonated beverages containing artificial sweeteners.",
     "Contains artificial sweeteners and caffeine. No nutritional value. Limit intake and count caffeine toward daily limit.",
     "Sparkling water with fruit, water", "curated_medical_literature", 0.75,
     ["Diet Coke", "Diet Pepsi", "Sugar-Free Soda"]),

    ("Regular Soda", "caution", "beverage",
     "Sugar-sweetened carbonated beverages.",
     "High sugar content can contribute to excessive weight gain and gestational diabetes. Some contain caffeine.",
     "Sparkling water with fruit, water, diluted juice", "curated_medical_literature", 0.8,
     ["Cola", "Pop", "Soft Drink"]),

    ("Milk (Pasteurized)", "safe", "beverage",
     "Pasteurized cow's milk. Excellent source of calcium, vitamin D, and protein during pregnancy.",
     None, None, "acog_guidelines", 0.95,
     []),

    ("Wheatgrass Juice", "caution", "beverage",
     "Fresh juice from wheatgrass.",
     "Often unpasteurized and grown in moist conditions favorable to mold and bacteria. Risk of contamination.",
     "Pasteurized green juices, cooked leafy greens", "curated_medical_literature", 0.7,
     ["Wheatgrass Shot"]),

    ("Licorice Tea", "caution", "beverage",
     "Herbal tea made from licorice root.",
     "Contains glycyrrhizin which in high amounts is associated with preterm birth, lower birth weight, and hormonal effects.",
     "Peppermint tea, ginger tea", "curated_medical_literature", 0.8,
     []),

    # ============================================================
    # SUPPLEMENTS
    # ============================================================
    ("Folic Acid", "safe", "supplement",
     "Essential B vitamin (B9). Critical for preventing neural tube defects. All pregnant women should take 400-800mcg daily.",
     None, None, "acog_guidelines", 1.0,
     ["Folate", "Vitamin B9", "Methylfolate", "5-MTHF"]),

    ("Iron Supplement", "safe", "supplement",
     "Essential mineral. Many pregnant women need supplementation to prevent anemia. Take as directed by provider.",
     None, None, "acog_guidelines", 0.95,
     ["Ferrous Sulfate", "Ferrous Gluconate", "Iron Pills"]),

    ("Prenatal Vitamin", "safe", "supplement",
     "Multivitamin formulated for pregnancy with appropriate levels of key nutrients.",
     None, None, "acog_guidelines", 1.0,
     ["Prenatal Multivitamin"]),

    ("Vitamin D", "safe", "supplement",
     "Important for calcium absorption and bone health. 600 IU daily recommended during pregnancy.",
     None, None, "acog_guidelines", 0.95,
     ["Cholecalciferol", "Vitamin D3"]),

    ("Calcium", "safe", "supplement",
     "Essential for fetal bone development. 1000mg daily recommended. Supplement if dietary intake is insufficient.",
     None, None, "acog_guidelines", 0.95,
     ["Calcium Carbonate", "Calcium Citrate"]),

    ("DHA (Docosahexaenoic Acid)", "safe", "supplement",
     "Omega-3 fatty acid crucial for fetal brain and eye development. 200-300mg daily recommended.",
     None, None, "acog_guidelines", 0.9,
     ["Omega-3 DHA", "Algal DHA"]),

    ("Vitamin A (Retinol)", "caution", "supplement",
     "Preformed vitamin A from animal sources.",
     "Excessive retinol (>10,000 IU/day) is teratogenic — causes birth defects. Most prenatal vitamins use beta-carotene form instead.",
     "Beta-carotene (provitamin A), prenatal vitamins with safe levels", "acog_guidelines", 0.95,
     ["Retinol", "Retinyl Palmitate"]),

    ("Vitamin A (Beta-Carotene)", "safe", "supplement",
     "Plant-based provitamin A. Body converts only what it needs, so toxicity risk is minimal.",
     None, None, "acog_guidelines", 0.9,
     ["Beta-Carotene", "Provitamin A"]),

    ("Vitamin C", "safe", "supplement",
     "Important antioxidant. 85mg daily recommended during pregnancy. Safe in recommended amounts.",
     None, None, "acog_guidelines", 0.9,
     ["Ascorbic Acid"]),

    ("Vitamin E", "safe", "supplement",
     "Antioxidant vitamin. Safe in recommended amounts (15mg/day) during pregnancy.",
     None, None, "acog_guidelines", 0.85,
     ["Alpha-Tocopherol"]),

    ("Vitamin B6", "safe", "supplement",
     "B vitamin that may help with morning sickness. 10-25mg up to 3x daily recommended by ACOG for nausea.",
     None, None, "acog_guidelines", 0.95,
     ["Pyridoxine"]),

    ("Vitamin B12", "safe", "supplement",
     "Essential for nervous system development. Important supplement for vegetarian/vegan pregnant women.",
     None, None, "acog_guidelines", 0.95,
     ["Cobalamin", "Cyanocobalamin", "Methylcobalamin"]),

    ("Zinc", "safe", "supplement",
     "Essential mineral for fetal growth and immune function. 11mg daily recommended during pregnancy.",
     None, None, "acog_guidelines", 0.9,
     ["Zinc Gluconate", "Zinc Picolinate"]),

    ("Iodine", "safe", "supplement",
     "Essential for fetal thyroid function and brain development. 220mcg daily recommended during pregnancy.",
     None, None, "acog_guidelines", 0.9,
     ["Potassium Iodide"]),

    ("Magnesium", "safe", "supplement",
     "Important mineral for pregnancy. May help with leg cramps and preeclampsia prevention.",
     None, None, "acog_guidelines", 0.9,
     ["Magnesium Citrate", "Magnesium Glycinate"]),

    ("Probiotics", "safe", "supplement",
     "Beneficial bacteria supplements. Generally considered safe during pregnancy and may help with GI issues.",
     None, None, "curated_medical_literature", 0.8,
     ["Lactobacillus", "Bifidobacterium"]),

    ("Collagen Supplement", "caution", "supplement",
     "Protein supplement for skin, joints, and connective tissue.",
     "Generally considered safe but limited pregnancy-specific research. Source quality varies. Consult provider.",
     "Protein from whole foods like eggs, meat, beans", "curated_medical_literature", 0.6,
     ["Collagen Peptides", "Hydrolyzed Collagen"]),

    ("Melatonin", "caution", "supplement",
     "Hormone supplement used for sleep.",
     "Crosses the placenta and may affect fetal circadian rhythm development. Limited pregnancy safety data.",
     "Sleep hygiene practices, consult provider", "curated_medical_literature", 0.7,
     []),

    ("Activated Charcoal", "caution", "supplement",
     "Supplement marketed for detox purposes.",
     "Can bind to and reduce absorption of prenatal vitamins and medications. Not recommended during pregnancy.",
     "Consult healthcare provider", "curated_medical_literature", 0.75,
     ["Charcoal Supplement"]),

    ("Bitter Melon Extract", "avoid", "supplement",
     "Herbal supplement from Momordica charantia.",
     "Has abortifacient properties in animal studies. Can stimulate uterine contractions and menstruation.",
     "Consult healthcare provider for blood sugar management", "curated_medical_literature", 0.8,
     ["Momordica Charantia", "Karela"]),

    ("Choline", "safe", "supplement",
     "Essential nutrient for fetal brain development. 450mg daily recommended during pregnancy.",
     None, None, "acog_guidelines", 0.9,
     ["Choline Bitartrate"]),

    # ============================================================
    # PRODUCE
    # ============================================================
    ("Raw Sprouts", "avoid", "produce",
     "All types of raw sprouts including alfalfa, bean, clover, and radish sprouts.",
     "Warm, humid growing conditions are ideal for Salmonella, E. coli, and Listeria. FDA advises pregnant women to avoid raw sprouts entirely.",
     "Cooked sprouts, other vegetables", "fda_guidance", 1.0,
     ["Alfalfa Sprouts", "Bean Sprouts", "Clover Sprouts", "Mung Bean Sprouts", "Radish Sprouts"]),

    ("Unwashed Produce", "avoid", "produce",
     "Any fruits or vegetables that have not been thoroughly washed.",
     "Can harbor Toxoplasma gondii, Listeria, and pesticide residues. Always wash produce thoroughly, even organic.",
     "Thoroughly washed and/or peeled produce", "fda_guidance", 0.95,
     ["Unwashed Fruits", "Unwashed Vegetables"]),

    ("Pre-Cut Fruit (Store-Bought)", "caution", "produce",
     "Pre-cut melon and other pre-cut fruit from stores or delis.",
     "Higher risk of bacterial growth due to cut surfaces and extended storage. Linked to Listeria and Salmonella outbreaks.",
     "Whole fruits washed and cut at home", "fda_guidance", 0.8,
     ["Pre-Cut Melon", "Fruit Salad (Pre-Made)"]),

    ("Spinach", "safe", "produce",
     "Leafy green vegetable rich in folate, iron, and fiber. Excellent for pregnancy when washed properly.",
     None, None, "curated_medical_literature", 0.95,
     ["Baby Spinach"]),

    ("Kale", "safe", "produce",
     "Nutrient-dense leafy green rich in vitamins A, C, K and folate. Excellent during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Curly Kale", "Lacinato Kale"]),

    ("Sweet Potatoes", "safe", "produce",
     "Root vegetable rich in beta-carotene, fiber, and potassium. Excellent during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Yams"]),

    ("Avocado", "safe", "produce",
     "Fruit rich in healthy fats, folate, and potassium. Highly beneficial during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     []),

    ("Bananas", "safe", "produce",
     "Fruit rich in potassium and vitamin B6. May help with morning sickness and leg cramps.",
     None, None, "curated_medical_literature", 0.95,
     ["Banana"]),

    ("Berries", "safe", "produce",
     "Rich in antioxidants, vitamin C, and fiber. Excellent during pregnancy when washed thoroughly.",
     None, None, "curated_medical_literature", 0.95,
     ["Blueberries", "Strawberries", "Raspberries", "Blackberries"]),

    ("Oranges", "safe", "produce",
     "Citrus fruit rich in vitamin C and folate. Beneficial during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Orange", "Tangerines", "Clementines", "Mandarins"]),

    ("Broccoli", "safe", "produce",
     "Cruciferous vegetable rich in folate, fiber, calcium, and vitamin C.",
     None, None, "curated_medical_literature", 0.95,
     []),

    ("Carrots", "safe", "produce",
     "Root vegetable rich in beta-carotene. Safe and nutritious during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     []),

    ("Tomatoes", "safe", "produce",
     "Fruit/vegetable rich in lycopene, vitamin C, and potassium. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Tomato"]),

    ("Lentils", "safe", "produce",
     "Legume excellent source of folate, iron, and protein. Highly recommended during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Red Lentils", "Green Lentils", "Brown Lentils"]),

    ("Beans", "safe", "produce",
     "Legumes rich in protein, fiber, iron, and folate. Excellent during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Black Beans", "Kidney Beans", "Chickpeas", "Navy Beans", "Pinto Beans"]),

    ("Edamame", "safe", "produce",
     "Young soybeans. Good source of protein, folate, and fiber. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Young Soybeans"]),

    ("Ripe Papaya", "safe", "produce",
     "Ripe papaya fruit is safe and nutritious during pregnancy. Rich in vitamin C and folate.",
     None, None, "curated_medical_literature", 0.85,
     []),

    ("Pineapple", "safe", "produce",
     "Tropical fruit. Safe during pregnancy despite myths. Would need enormous amounts for any uterine effect.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Mango", "safe", "produce",
     "Tropical fruit rich in vitamins A and C. Safe and nutritious during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     []),

    ("Asparagus", "safe", "produce",
     "Vegetable rich in folate. Excellent food choice during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     []),

    ("Bell Peppers", "safe", "produce",
     "Vegetable rich in vitamin C. Safe and nutritious during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Sweet Peppers", "Capsicum"]),

    ("Mushrooms (Cooked)", "safe", "produce",
     "Edible mushrooms are safe when cooked. Good source of vitamin D and B vitamins.",
     None, None, "curated_medical_literature", 0.9,
     ["Button Mushrooms", "Shiitake", "Portobello"]),

    ("Dates", "safe", "produce",
     "Dried fruit rich in fiber and natural sugars. Some evidence supports consumption in late pregnancy for easier labor.",
     None, None, "curated_medical_literature", 0.85,
     ["Medjool Dates"]),

    # ============================================================
    # GRAINS
    # ============================================================
    ("Fortified Cereals", "safe", "grain",
     "Breakfast cereals fortified with folic acid, iron, and B vitamins. Helpful for meeting pregnancy nutrient needs.",
     None, None, "curated_medical_literature", 0.9,
     ["Fortified Breakfast Cereal"]),

    ("Whole Wheat", "safe", "grain",
     "Whole grain rich in fiber, B vitamins, and iron. Excellent during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Whole Wheat Bread", "Whole Wheat Pasta"]),

    ("Brown Rice", "safe", "grain",
     "Whole grain rice. Good source of fiber and nutrients during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Oats", "safe", "grain",
     "Whole grain rich in fiber, iron, and B vitamins. Excellent during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Oatmeal", "Rolled Oats", "Steel-Cut Oats"]),

    ("Quinoa", "safe", "grain",
     "Complete protein pseudo-grain. Rich in iron, folate, and fiber. Excellent during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     []),

    ("White Rice", "safe", "grain",
     "Refined grain. Safe during pregnancy but less nutritious than brown rice.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Barley", "safe", "grain",
     "Whole grain rich in fiber. Safe and nutritious during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Corn", "safe", "grain",
     "Common grain/vegetable. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Maize", "Sweet Corn", "Corn on the Cob"]),

    ("Millet", "safe", "grain",
     "Ancient grain, gluten-free. Safe and nutritious during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Buckwheat", "safe", "grain",
     "Gluten-free pseudo-grain rich in rutin and minerals. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Soba"]),

    ("Flaxseed", "safe", "grain",
     "Seed rich in omega-3 (ALA) and fiber. Safe in food amounts during pregnancy.",
     None, None, "curated_medical_literature", 0.8,
     ["Linseed", "Ground Flaxseed", "Flax Meal"]),

    ("Chia Seeds", "safe", "grain",
     "Seeds rich in omega-3, fiber, and calcium. Safe and beneficial during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     ["Chia"]),

    ("Wheat Germ", "safe", "grain",
     "Nutrient-dense part of wheat kernel rich in folate, vitamin E, and zinc.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("White Flour", "safe", "grain",
     "Refined wheat flour. Safe but less nutritious than whole grain alternatives. Often enriched with folic acid.",
     None, None, "curated_medical_literature", 0.9,
     ["All-Purpose Flour", "Enriched Flour"]),

    # ============================================================
    # CONDIMENTS
    # ============================================================
    ("Soy Sauce", "safe", "condiment",
     "Fermented condiment. Safe during pregnancy in normal culinary amounts. Watch sodium intake.",
     None, None, "curated_medical_literature", 0.9,
     ["Shoyu", "Tamari"]),

    ("Vinegar", "safe", "condiment",
     "Acidic condiment. All types (white, apple cider, balsamic) safe during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Apple Cider Vinegar", "Balsamic Vinegar", "White Vinegar", "Rice Vinegar"]),

    ("Commercial Mayonnaise", "safe", "condiment",
     "Store-bought mayo made with pasteurized eggs. Safe during pregnancy.",
     None, None, "fda_guidance", 0.9,
     ["Mayo", "Hellmann's", "Best Foods"]),

    ("Homemade Mayonnaise", "avoid", "condiment",
     "Mayonnaise made with raw, unpasteurized eggs.",
     "Contains raw eggs which can harbor Salmonella. Avoid unless made with pasteurized eggs.",
     "Commercial mayonnaise, mayo made with pasteurized eggs", "fda_guidance", 0.95,
     ["Raw Egg Mayo"]),

    ("Hot Sauce", "safe", "condiment",
     "Spicy condiment. Safe during pregnancy though may worsen heartburn/reflux.",
     None, None, "curated_medical_literature", 0.9,
     ["Sriracha", "Tabasco", "Frank's Red Hot", "Chili Sauce"]),

    ("Mustard", "safe", "condiment",
     "Common condiment. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Yellow Mustard", "Dijon Mustard", "Whole Grain Mustard"]),

    ("Ketchup", "safe", "condiment",
     "Common tomato-based condiment. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Catsup", "Tomato Ketchup"]),

    ("Salsa", "safe", "condiment",
     "Tomato-based condiment. Commercial pasteurized salsa is safe. Fresh salsa should use washed ingredients.",
     None, None, "curated_medical_literature", 0.9,
     ["Pico de Gallo"]),

    ("Hummus", "safe", "condiment",
     "Chickpea spread. Commercial refrigerated hummus is safe. Consume before expiration date.",
     None, None, "curated_medical_literature", 0.85,
     []),

    ("Peanut Butter", "safe", "condiment",
     "Nut butter. Safe during pregnancy and good protein source. No evidence that avoiding prevents allergies in baby.",
     None, None, "curated_medical_literature", 0.9,
     ["PB"]),

    ("Honey", "safe", "condiment",
     "Natural sweetener. Safe for pregnant women (botulism risk is only for infants under 1 year, not adults/fetuses).",
     None, None, "curated_medical_literature", 0.9,
     ["Raw Honey", "Manuka Honey"]),

    ("Maple Syrup", "safe", "condiment",
     "Natural sweetener. Safe during pregnancy in moderation.",
     None, None, "curated_medical_literature", 0.95,
     ["Pure Maple Syrup"]),

    ("Fish Sauce", "safe", "condiment",
     "Fermented condiment used in Asian cooking. Safe in culinary amounts. High in sodium.",
     None, None, "curated_medical_literature", 0.9,
     ["Nam Pla", "Nuoc Mam"]),

    ("Worcestershire Sauce", "safe", "condiment",
     "Fermented condiment. Safe during pregnancy in normal amounts.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Miso", "safe", "condiment",
     "Fermented soybean paste. Safe during pregnancy. High in sodium so moderate intake.",
     None, None, "curated_medical_literature", 0.9,
     ["Miso Paste"]),

    ("Tahini", "safe", "condiment",
     "Sesame seed paste. Safe and nutritious during pregnancy. Good source of calcium.",
     None, None, "curated_medical_literature", 0.9,
     ["Sesame Paste"]),

    ("Aioli", "caution", "condiment",
     "Garlic mayonnaise, traditionally made with raw eggs.",
     "Traditional recipe uses raw eggs — risk of Salmonella. Commercial versions with pasteurized eggs are safe.",
     "Commercial aioli with pasteurized eggs", "curated_medical_literature", 0.8,
     ["Garlic Aioli"]),

    ("Hollandaise Sauce", "caution", "condiment",
     "Butter sauce traditionally made with raw or lightly cooked egg yolks.",
     "May contain undercooked eggs — risk of Salmonella. Safe if made with pasteurized eggs or heated properly.",
     "Hollandaise made with pasteurized eggs", "curated_medical_literature", 0.8,
     ["Béarnaise Sauce"]),

    ("Caesar Dressing", "caution", "condiment",
     "Salad dressing traditionally made with raw eggs and anchovies.",
     "Traditional recipe uses raw egg yolks — Salmonella risk. Most commercial versions use pasteurized eggs and are safe.",
     "Commercial Caesar dressing, vinaigrette", "curated_medical_literature", 0.8,
     ["Caesar Salad Dressing"]),

    ("Teriyaki Sauce", "safe", "condiment",
     "Japanese-style sweet soy sauce glaze. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     []),

    # ============================================================
    # OILS
    # ============================================================
    ("Olive Oil", "safe", "oil",
     "Healthy monounsaturated cooking oil. Excellent choice during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Extra Virgin Olive Oil", "EVOO"]),

    ("Coconut Oil", "safe", "oil",
     "Cooking oil with medium-chain triglycerides. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Virgin Coconut Oil"]),

    ("Avocado Oil", "safe", "oil",
     "Heart-healthy cooking oil with high smoke point. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Canola Oil", "safe", "oil",
     "Common cooking oil low in saturated fat. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Rapeseed Oil"]),

    ("Sunflower Oil", "safe", "oil",
     "Common cooking oil. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Sesame Oil", "safe", "oil",
     "Cooking oil used in Asian cuisine. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Flaxseed Oil", "safe", "oil",
     "Oil rich in omega-3 (ALA). Safe during pregnancy in food amounts. Do not heat.",
     None, None, "curated_medical_literature", 0.8,
     ["Linseed Oil"]),

    ("Pennyroyal Essential Oil", "avoid", "oil",
     "Essential oil from the pennyroyal plant.",
     "Extremely toxic. Known abortifacient. Can cause liver failure and death even in small amounts. Never ingest or apply.",
     "Peppermint essential oil (for aromatherapy only, topical/diffused)", "curated_medical_literature", 1.0,
     ["Pennyroyal Oil"]),

    ("Clary Sage Essential Oil", "avoid", "oil",
     "Essential oil sometimes used in aromatherapy.",
     "May stimulate uterine contractions. Sometimes used by midwives during labor but avoid during pregnancy.",
     "Lavender essential oil (with provider guidance)", "curated_medical_literature", 0.85,
     ["Clary Sage Oil"]),

    ("Rosemary Essential Oil", "caution", "oil",
     "Essential oil from rosemary plant.",
     "In concentrated form, may stimulate uterine contractions and raise blood pressure. Culinary rosemary is fine.",
     "Lavender essential oil, lemon essential oil (diffused only)", "curated_medical_literature", 0.75,
     ["Rosemary Oil"]),

    ("Cinnamon Essential Oil", "avoid", "oil",
     "Concentrated essential oil from cinnamon bark.",
     "May stimulate uterine contractions in concentrated form. Also a skin irritant. Culinary cinnamon is safe.",
     "Culinary cinnamon, vanilla essential oil", "curated_medical_literature", 0.8,
     ["Cinnamon Bark Oil", "Cassia Oil"]),

    ("Wintergreen Essential Oil", "avoid", "oil",
     "Essential oil containing methyl salicylate.",
     "Contains methyl salicylate (aspirin-like compound). Can be absorbed through skin. Risk of bleeding and fetal effects.",
     "Consult provider for pain management", "curated_medical_literature", 0.9,
     ["Methyl Salicylate"]),

    ("Lavender Essential Oil", "safe", "oil",
     "Common aromatherapy oil. Generally considered safe when diffused or used topically in diluted form during pregnancy.",
     None, None, "curated_medical_literature", 0.8,
     ["Lavender Oil"]),

    ("Tea Tree Essential Oil", "caution", "oil",
     "Essential oil used for its antimicrobial properties.",
     "Limited pregnancy safety data. Topical use in small diluted amounts probably safe. Avoid ingestion.",
     "Consult provider for antimicrobial alternatives", "curated_medical_literature", 0.7,
     ["Tea Tree Oil", "Melaleuca Oil"]),

    ("Eucalyptus Essential Oil", "caution", "oil",
     "Aromatic essential oil.",
     "Limited pregnancy safety data. Can be irritating. Brief diffusion likely safe; avoid direct application and ingestion.",
     "Steam inhalation with hot water (no oils)", "curated_medical_literature", 0.7,
     ["Eucalyptus Oil"]),

    ("Juniper Essential Oil", "avoid", "oil",
     "Essential oil from juniper berries.",
     "May stimulate uterine contractions and has potential nephrotoxic effects. Avoid during pregnancy.",
     "Lavender or chamomile essential oil", "curated_medical_literature", 0.8,
     ["Juniper Berry Oil"]),

    ("Peppermint Essential Oil", "caution", "oil",
     "Concentrated essential oil from peppermint.",
     "Generally safe when diffused. Avoid topical use on chest when breastfeeding (may reduce milk supply). Do not ingest.",
     "Lemon or lavender essential oil", "curated_medical_literature", 0.75,
     ["Peppermint Oil"]),

    ("Butter", "safe", "oil",
     "Dairy fat. Safe during pregnancy in moderate amounts as part of balanced diet.",
     None, None, "curated_medical_literature", 0.95,
     ["Unsalted Butter", "Salted Butter"]),

    ("Margarine", "safe", "oil",
     "Plant-based spread. Modern versions without trans fats are safe during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     []),

    ("Trans Fats", "avoid", "oil",
     "Partially hydrogenated oils / artificial trans fats.",
     "Increase inflammation, raise bad cholesterol, cross the placenta. FDA has largely banned artificial trans fats. Avoid any remaining sources.",
     "Olive oil, avocado oil, natural butter", "fda_guidance", 0.95,
     ["Partially Hydrogenated Oil", "Partially Hydrogenated Vegetable Oil", "PHO"]),

    # ============================================================
    # ADDITIONAL FOOD ITEMS (miscellaneous categories to reach 300+)
    # ============================================================
    ("Tofu", "safe", "produce",
     "Soy-based protein. Safe during pregnancy. Good plant-based protein source.",
     None, None, "curated_medical_literature", 0.9,
     ["Bean Curd"]),

    ("Tempeh", "safe", "produce",
     "Fermented soybean product. Safe and nutritious during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     []),

    ("Sauerkraut (Pasteurized)", "safe", "condiment",
     "Fermented cabbage. Pasteurized versions are safe. Good source of probiotics if unpasteurized but check freshness.",
     None, None, "curated_medical_literature", 0.85,
     ["Kimchi (Pasteurized)"]),

    ("Kimchi", "safe", "condiment",
     "Korean fermented vegetables. Safe during pregnancy if fresh and properly prepared. Watch sodium content.",
     None, None, "curated_medical_literature", 0.8,
     []),

    ("Soy Milk", "safe", "beverage",
     "Plant-based milk alternative. Safe during pregnancy. Choose calcium-fortified versions.",
     None, None, "curated_medical_literature", 0.9,
     ["Soymilk"]),

    ("Almond Milk", "safe", "beverage",
     "Plant-based milk alternative. Safe during pregnancy. Choose calcium-fortified versions.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Oat Milk", "safe", "beverage",
     "Plant-based milk alternative. Safe during pregnancy. Choose calcium-fortified versions.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Eggs (Cooked)", "safe", "meat",
     "Fully cooked eggs are an excellent protein source during pregnancy. Rich in choline for fetal brain development.",
     None, None, "curated_medical_literature", 0.95,
     ["Hard-Boiled Eggs", "Scrambled Eggs", "Fried Eggs"]),

    ("Peanuts", "safe", "produce",
     "Legume/nut. Safe during pregnancy unless allergic. Current guidelines do NOT recommend avoidance for allergy prevention.",
     None, None, "acog_guidelines", 0.9,
     ["Groundnuts"]),

    ("Tree Nuts", "safe", "produce",
     "Almonds, walnuts, cashews, etc. Safe during pregnancy unless allergic. Good source of healthy fats.",
     None, None, "curated_medical_literature", 0.9,
     ["Almonds", "Walnuts", "Cashews", "Pecans", "Pistachios"]),

    ("Dark Chocolate", "caution", "food_additive",
     "Chocolate with high cocoa content.",
     "Contains caffeine and theobromine. Count caffeine toward daily 200mg limit. Small amounts are fine.",
     "Carob, white chocolate (less caffeine)", "curated_medical_literature", 0.8,
     ["Cacao", "Cocoa"]),

    ("Licorice Candy", "caution", "food_additive",
     "Candy made with real licorice root extract.",
     "Contains glycyrrhizin. Studies link high intake to preterm birth and developmental effects. Avoid large amounts.",
     "Other candy without licorice root", "curated_medical_literature", 0.8,
     ["Black Licorice"]),

    ("Raw Cookie Dough", "avoid", "meat",
     "Uncooked dough containing raw eggs and raw flour.",
     "Risk of Salmonella from raw eggs and E. coli from raw flour. FDA advises against consuming any raw dough.",
     "Edible cookie dough made with heat-treated flour and no eggs, baked cookies", "fda_guidance", 0.95,
     ["Raw Dough", "Raw Batter"]),

    ("Cassava (Raw)", "avoid", "produce",
     "Raw cassava root.",
     "Contains cyanogenic glycosides (linamarin) that release cyanide. Must be properly prepared (soaked, cooked) before eating.",
     "Properly prepared and cooked cassava, other root vegetables", "curated_medical_literature", 0.9,
     ["Raw Tapioca Root", "Yuca (Raw)"]),

    ("Cassava (Cooked)", "safe", "produce",
     "Properly prepared and cooked cassava. Safe when thoroughly cooked.",
     None, None, "curated_medical_literature", 0.85,
     ["Tapioca", "Yuca (Cooked)"]),

    ("Seaweed", "caution", "produce",
     "Marine algae used in cooking (nori, kelp, wakame).",
     "Can be very high in iodine, especially kelp. Excessive iodine can affect fetal thyroid function. Small amounts are fine.",
     "Small portions of nori, limit kelp consumption", "curated_medical_literature", 0.75,
     ["Nori", "Kelp", "Wakame", "Dulse", "Kombu"]),

    ("Moringa", "caution", "herb",
     "Nutrient-dense plant used as supplement and food.",
     "Moringa bark, root, and flowers may have anti-fertility properties. Moringa leaf powder in food amounts is likely safe but data is limited.",
     "Other leafy greens, prenatal vitamins", "curated_medical_literature", 0.7,
     ["Moringa Oleifera", "Drumstick Tree"]),

    ("Turmeric Supplement", "caution", "supplement",
     "High-dose turmeric/curcumin capsules.",
     "Culinary turmeric is safe, but concentrated supplements may stimulate the uterus and have blood-thinning effects.",
     "Culinary turmeric in cooking", "curated_medical_literature", 0.75,
     ["Curcumin Supplement", "Turmeric Capsules"]),

    ("Elderberry", "caution", "herb",
     "Berry used in syrups and supplements for immune support.",
     "Cooked elderberries are safe in food amounts. Raw elderberries are toxic. Limited safety data for elderberry supplements during pregnancy.",
     "Vitamin C from citrus fruits, consult provider", "curated_medical_literature", 0.65,
     ["Sambucus", "Elderberry Syrup"]),

    ("Garlic Supplement", "caution", "supplement",
     "Concentrated garlic pills or extract.",
     "High doses may increase bleeding risk due to antiplatelet effects. Culinary garlic is safe.",
     "Garlic in cooking", "curated_medical_literature", 0.75,
     ["Garlic Pills", "Garlic Extract"]),

    ("Vitamin K", "safe", "supplement",
     "Fat-soluble vitamin important for blood clotting. Safe at recommended levels during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     ["Phytonadione", "Vitamin K1", "Vitamin K2"]),

    ("Biotin", "safe", "supplement",
     "B vitamin (B7). Safe during pregnancy at recommended levels. Found in many prenatal vitamins.",
     None, None, "curated_medical_literature", 0.85,
     ["Vitamin B7", "Vitamin H"]),

    ("Pantothenic Acid", "safe", "supplement",
     "B vitamin (B5). Safe during pregnancy. Found in many foods and prenatal vitamins.",
     None, None, "curated_medical_literature", 0.85,
     ["Vitamin B5"]),

    ("Riboflavin", "safe", "supplement",
     "B vitamin (B2). Safe and important during pregnancy for energy metabolism and fetal development.",
     None, None, "curated_medical_literature", 0.9,
     ["Vitamin B2"]),

    ("Thiamine", "safe", "supplement",
     "B vitamin (B1). Essential during pregnancy for fetal brain development.",
     None, None, "curated_medical_literature", 0.9,
     ["Vitamin B1"]),

    ("Niacin", "safe", "supplement",
     "B vitamin (B3). Safe at recommended levels during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     ["Vitamin B3", "Nicotinic Acid"]),

    ("Selenium", "safe", "supplement",
     "Trace mineral important for thyroid function. Safe at recommended levels (60mcg/day) during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     []),

    ("Copper", "safe", "supplement",
     "Trace mineral. Safe at recommended levels during pregnancy (1mg/day).",
     None, None, "curated_medical_literature", 0.85,
     []),

    ("Chromium", "safe", "supplement",
     "Trace mineral involved in blood sugar regulation. Safe at recommended levels during pregnancy.",
     None, None, "curated_medical_literature", 0.85,
     ["Chromium Picolinate"]),

    ("Gelatin", "safe", "food_additive",
     "Protein derived from animal collagen. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Gelatine"]),

    ("Pectin", "safe", "food_additive",
     "Natural gelling agent from fruits. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Fruit Pectin"]),

    ("Glucosamine", "caution", "supplement",
     "Joint health supplement.",
     "Limited pregnancy safety data. Some concern about potential effects on fetal cartilage development. Consult provider.",
     "Consult healthcare provider for joint pain management", "curated_medical_literature", 0.6,
     ["Glucosamine Sulfate"]),

    ("Hemp Seeds", "safe", "produce",
     "Nutritious seeds rich in omega-3 and protein. Safe during pregnancy. Contains negligible THC.",
     None, None, "curated_medical_literature", 0.85,
     ["Hemp Hearts"]),

    ("Sunflower Seeds", "safe", "produce",
     "Nutritious seeds rich in vitamin E and folate. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     []),

    ("Pumpkin Seeds", "safe", "produce",
     "Seeds rich in iron, zinc, and magnesium. Excellent during pregnancy.",
     None, None, "curated_medical_literature", 0.95,
     ["Pepitas"]),

    ("Cottonseed Oil", "safe", "oil",
     "Cooking oil. Safe during pregnancy in normal culinary use.",
     None, None, "curated_medical_literature", 0.85,
     []),

    ("Ghee", "safe", "oil",
     "Clarified butter used in cooking. Safe during pregnancy in moderation.",
     None, None, "curated_medical_literature", 0.9,
     ["Clarified Butter"]),

    ("Soybean Oil", "safe", "oil",
     "Common cooking oil. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Vegetable Oil"]),

    ("Corn Oil", "safe", "oil",
     "Common cooking oil. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Grapeseed Oil", "safe", "oil",
     "Light cooking oil. Safe during pregnancy.",
     None, None, "curated_medical_literature", 0.9,
     ["Grape Seed Oil"]),

    ("Walnut Oil", "safe", "oil",
     "Nut oil rich in omega-3. Safe during pregnancy. Best used unheated.",
     None, None, "curated_medical_literature", 0.9,
     []),

    ("Jasmine Essential Oil", "caution", "oil",
     "Aromatic essential oil.",
     "May stimulate uterine contractions. Avoid during pregnancy, especially first trimester. Some midwives use during labor.",
     "Lavender essential oil", "curated_medical_literature", 0.75,
     ["Jasmine Oil"]),

    ("CBD Oil", "avoid", "supplement",
     "Cannabidiol oil derived from cannabis plant.",
     "FDA strongly advises against use during pregnancy. May affect fetal brain development, interact with medications, and contains unregulated contaminants.",
     "Consult healthcare provider for anxiety/pain management", "fda_guidance", 0.9,
     ["Cannabidiol", "Hemp CBD Oil"]),

    ("Raw Flour", "avoid", "grain",
     "Uncooked flour of any type.",
     "Can contain E. coli from contamination during growing/milling. Always cook or bake flour before consuming.",
     "Cooked/baked flour products, heat-treated flour for no-bake recipes", "fda_guidance", 0.9,
     ["Uncooked Flour"]),

    ("Tonic Water", "caution", "beverage",
     "Carbonated water containing quinine.",
     "Contains quinine which in high doses has been associated with birth defects and other adverse effects. Small amounts in tonic water are likely safe but limit intake.",
     "Sparkling water, club soda", "curated_medical_literature", 0.75,
     ["Quinine Water"]),

    ("Protein Powder", "caution", "supplement",
     "Concentrated protein supplement.",
     "Quality and contamination vary widely. Some contain heavy metals, added herbs, or artificial ingredients. Choose third-party tested brands if using.",
     "Whole food protein sources: eggs, chicken, beans, Greek yogurt", "curated_medical_literature", 0.7,
     ["Whey Protein", "Plant Protein Powder"]),

    ("Apple Cider Vinegar Supplement", "caution", "supplement",
     "Concentrated apple cider vinegar in pill or liquid supplement form.",
     "Pasteurized ACV in cooking is safe. Unpasteurized supplements may contain harmful bacteria. High acidity may damage teeth and throat.",
     "Pasteurized apple cider vinegar in cooking", "curated_medical_literature", 0.7,
     ["ACV Pills", "ACV Gummies"]),

    ("Spirulina", "caution", "supplement",
     "Blue-green algae supplement.",
     "Can be contaminated with heavy metals and microcystins depending on source. Quality control varies. Not regulated as a drug.",
     "Iron-rich foods, prenatal vitamins", "curated_medical_literature", 0.65,
     ["Blue-Green Algae"]),

    ("Chlorella", "caution", "supplement",
     "Green algae supplement.",
     "Limited pregnancy safety data. Risk of contamination with heavy metals depending on source.",
     "Leafy greens, prenatal vitamins", "curated_medical_literature", 0.6,
     []),

    ("Digestive Bitters", "avoid", "supplement",
     "Herbal supplement containing various bitter herbs.",
     "Often contains herbs contraindicated in pregnancy (wormwood, gentian). May stimulate uterine contractions.",
     "Ginger tea for digestive support, consult provider", "curated_medical_literature", 0.8,
     ["Herbal Bitters"]),

    ("Black Seed Oil", "caution", "supplement",
     "Oil from Nigella sativa seeds.",
     "Some animal studies suggest it may slow uterine contractions. Limited human pregnancy data. Avoid supplements; small culinary use is likely fine.",
     "Culinary use only in small amounts", "curated_medical_literature", 0.65,
     ["Nigella Sativa Oil", "Kalonji Oil", "Black Cumin Seed Oil"]),

    ("Raw Honey", "safe", "condiment",
     "Unpasteurized honey. Safe for pregnant women (botulism risk is only for infants under 1, not pregnant women or fetuses).",
     None, None, "curated_medical_literature", 0.9,
     []),
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check existing categories to avoid duplicating food items already there
    cur.execute("SELECT name_normalized FROM ingredients")
    existing = {row[0] for row in cur.fetchall()}

    inserted_count = 0
    alias_count = 0
    skipped = 0

    for item in FOOD_INGREDIENTS:
        name, safety, category, desc, why, alts, source, confidence, aliases = item
        normalized = name.lower()

        if normalized in existing:
            skipped += 1
            continue

        cur.execute("""
            INSERT INTO ingredients (name, name_normalized, safety_level, category, description, why_flagged, safe_alternatives, source, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, normalized, safety, category, desc, why, alts, source, confidence))

        ingredient_id = cur.lastrowid
        existing.add(normalized)
        inserted_count += 1

        for alias in aliases:
            alias_norm = alias.lower()
            cur.execute("""
                INSERT INTO ingredient_aliases (ingredient_id, alias, alias_normalized)
                VALUES (?, ?, ?)
            """, (ingredient_id, alias, alias_norm))
            alias_count += 1

    conn.commit()

    # Print results
    print(f"\n{'='*60}")
    print(f"INSERTION COMPLETE")
    print(f"{'='*60}")
    print(f"New ingredients inserted: {inserted_count}")
    print(f"Skipped (already existed): {skipped}")
    print(f"New aliases inserted: {alias_count}")

    # Total counts
    cur.execute("SELECT COUNT(*) FROM ingredients")
    total_ingredients = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM ingredient_aliases")
    total_aliases = cur.fetchone()[0]

    print(f"\n{'='*60}")
    print(f"DATABASE TOTALS")
    print(f"{'='*60}")
    print(f"Total ingredients: {total_ingredients}")
    print(f"Total aliases: {total_aliases}")

    # By category
    print(f"\n--- Breakdown by Category ---")
    cur.execute("SELECT category, COUNT(*) FROM ingredients GROUP BY category ORDER BY COUNT(*) DESC")
    for row in cur.fetchall():
        print(f"  {row[0]:25s} {row[1]:4d}")

    # By safety level
    print(f"\n--- Breakdown by Safety Level ---")
    cur.execute("SELECT safety_level, COUNT(*) FROM ingredients GROUP BY safety_level ORDER BY COUNT(*) DESC")
    for row in cur.fetchall():
        print(f"  {row[0]:25s} {row[1]:4d}")

    # Food categories only
    food_cats = ('food_additive','herb','seafood','dairy','meat','beverage','sweetener','supplement','produce','grain','condiment','oil')
    placeholders = ','.join('?' * len(food_cats))
    cur.execute(f"SELECT COUNT(*) FROM ingredients WHERE category IN ({placeholders})", food_cats)
    food_total = cur.fetchone()[0]
    print(f"\nTotal FOOD ingredients (target categories): {food_total}")

    conn.close()

if __name__ == '__main__':
    main()
