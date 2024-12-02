examples = [
    {
        "url": "https://www.apple.com/leadership/",
        "json_schema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Board Member Information Extractor",
            "description": "Schema for extracting information about board members from a company website.",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "title": "Full Name",
                    "description": "The full name of the board member.",
                },
                "position": {
                    "type": "string",
                    "title": "Position on the Board",
                    "description": "The position or title of the board member on the board within the company.",
                },
            },
        },
        "output": [
            {"name": "Arthur D. Levinson", "position": "Chairman of the Board"},
            {"name": "Wanda Austin, Ph.D.", "position": "Board Member"},
            {"name": "Tim Cook", "position": "CEO and Board Member"},
            {"name": "Alex Gorsky", "position": "Board Member"},
            {"name": "Andrea Jung", "position": "Board Member"},
            {"name": "Monica Lozano", "position": "Board Member"},
            {"name": "Ronald D. Sugar, Ph.D.", "position": "Board Member"},
            {"name": "Susan L. Wagner", "position": "Board Member"},
        ],
    },
    {
        "url": "https://www.cdc.gov/antimicrobial-resistance/programs/AR-investment-map.html",
        "json_schema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "CDC Investments in 2017 BAA Projects",
            "description": "Schema about 2017 BAA Project CDC investments.",
            "type": "object",
            "properties": {
                "recipient_name": {
                    "type": "string",
                    "title": "Recipient Name",
                    "description": "The name of the recipient of the CDC investment in the research project.",
                },
                "investment_amount": {
                    "type": "number",
                    "title": "Investment Amount",
                    "description": "The amount of investment made by CDC in the research project recipient.",
                },
                "project_title": {
                    "type": "string",
                    "title": "Project Title",
                    "description": "The title of the research project funded by CDC.",
                },
            },
        },
        "output": [
            {
                "project_title": "Cross-validation of human fecal minibioreactor arrays and humanized microbiota mice as complementary pre-clinical models of the gastrointestinal microbiome",
                "recipient_name": "Baylor College of Medicine",
                "investment_amount": None,
            },
            {
                "project_title": "Rapid assays to detect Neisseria gonorrhea antibiotic resistance at the point of care",
                "recipient_name": "Children's Hospital Oakland Research Institute (CHORI) at the University of California San Francisco",
                "investment_amount": None,
            },
            {
                "project_title": "Natural history of C. difficile colonization",
                "recipient_name": "Cleveland VA Medical Research and Education Foundation",
                "investment_amount": None,
            },
            {
                "project_title": "Prenatal antibiotic use and body weight in children",
                "recipient_name": "Department of Research & Evaluation, Kaiser Permanente Southern California",
                "investment_amount": None,
            },
            {
                "project_title": "Computational methods for culture-independent disambiguation of wgMLST types in biological samples with multiple related bacterial strains",
                "recipient_name": "Emory University",
                "investment_amount": None,
            },
            {
                "project_title": "Antibiotic resistance in concentrated poultry feeding operations: Impacts on environmental waters",
                "recipient_name": "Georgia Tech Applied Research Corporation (GTARC)",
                "investment_amount": None,
            },
            {
                "project_title": "Optimization of therapeutic strategies to manage polymicrobial CF lung infections: Clinical assessment",
                "recipient_name": "Georgia Tech Applied Research Corporation (GTARC)",
                "investment_amount": None,
            },
            {
                "project_title": "The Leaders in Epidemiology, Antimicrobial stewardship and Public health, or LEAP, Fellowship are Infectious Diseases Fellowships to drive innovative education and approaches in antibiotic resistance, antibiotic stewardship and public health",
                "recipient_name": "Infectious Diseases Society of America (IDSA)",
                "investment_amount": None,
            },
            {
                "project_title": "Improved bioinformatics tools for detection and characterization of antimicrobial resistance in public health",
                "recipient_name": "J. Craig Venter Institute (JCVI)",
                "investment_amount": None,
            },
            {
                "project_title": "Highly accessible system for infection control and antimicrobial stewardship in resource limited settings",
                "recipient_name": "OpGen, Inc.",
                "investment_amount": None,
            },
            {
                "project_title": "Microbiome disruption and Enterobacterales dominance as a risk factor for sepsis in intensive care patients",
                "recipient_name": "Regents of the University of Michigan",
                "investment_amount": None,
            },
            {
                "project_title": "Rapid identification and analysis of transmission of the emerging pathogen Candida auris",
                "recipient_name": "Rutgers, The State University of New Jersey",
                "investment_amount": None,
            },
            {
                "project_title": "Perinatal antibiotics and weight gain in childhood",
                "recipient_name": "The Children's Hospital of Philadelphia (CHOP)",
                "investment_amount": None,
            },
            {
                "project_title": "Preventing the dissemination of CRE from healthcare facilities into surface waters in the US (continuation request)",
                "recipient_name": "The Ohio State University",
                "investment_amount": None,
            },
            {
                "project_title": "Understanding the microbiologic dynamics of Carbapenemase-producing organisms in hospital wastewater premise plumbing",
                "recipient_name": "The Rector and Visitors of the University of Virginia",
                "investment_amount": None,
            },
            {
                "project_title": "The prevalence and diversity of antibiotic resistant bacteria in a mixed-use watershed",
                "recipient_name": "The University of Georgia",
                "investment_amount": None,
            },
            {
                "project_title": "Considering homologous and non-homologous recombination in outbreak analysis",
                "recipient_name": "Translational Genomics Research Institute (TGen)",
                "investment_amount": None,
            },
            {
                "project_title": "Sentinel surveillance for Macrolide-resistant Mycoplasma pneumoniae at select sites in the U.S.",
                "recipient_name": "University of Alabama at Birmingham",
                "investment_amount": None,
            },
            {
                "project_title": "Reducing antibacterial use in patients with coccidioidomycosis",
                "recipient_name": "University of Arizona",
                "investment_amount": None,
            },
            {
                "project_title": "Azole resistance in agricultural settings",
                "recipient_name": "University of Georgia Research Foundation, Inc.",
                "investment_amount": None,
            },
            {
                "project_title": "Implementation of a novel strategy to prevent Staphylococcus aureus (SA) acquisition in community-based nursing homes to prevent invasive SA infection: Feasibility and pilot to guide a multicenter stepped wedge cluster trial",
                "recipient_name": "University of Maryland, Baltimore",
                "investment_amount": None,
            },
            {
                "project_title": "Comparison of methods for detecting recombination in bacterial whole genome sequences",
                "recipient_name": "University of Mississippi Medical Center",
                "investment_amount": None,
            },
            {
                "project_title": "Double blinded, randomized controlled Trial of Oral vancomycin versus placebo in hospitalized patients with diarrhea and stool toXin NEGative but nucleic acid amplification test positive for toxigenic C. difficile (TOX NEG trial)",
                "recipient_name": "Washington University",
                "investment_amount": None,
            },
        ],
    },
    {
        "url": "https://www.food.com/recipe/balsamic-chicken-and-mushrooms-54726",
        "json_schema": {
            "title": "Recipe Ingredients Extractor without Unit or Quantity",
            "description": "Schema for extracting ingredients from a recipe text without unit or quantity.",
            "type": "object",
            "properties": {
                "ingredient_name": {
                    "title": "Ingredient Name",
                    "description": "The name of the ingredient in the recipe.",
                    "type": "string",
                }
            },
        },
        "output": [
            {"ingredient_name": "vegetable oil"},
            {"ingredient_name": "balsamic vinegar"},
            {"ingredient_name": "Dijon mustard"},
            {"ingredient_name": "garlic"},
            {"ingredient_name": "chicken breasts"},
            {"ingredient_name": "mushrooms"},
            {"ingredient_name": "chicken broth or white wine"},
            {"ingredient_name": "dried thyme leaves"},
        ],
    },
    {
        "url": "https://mufon.com/2021/05/14/aurora-tx-crash-1897/",
        "json_schema": {
            "type": "object",
            "title": "UFO Sighting Extractor",
            "properties": {
                "date": {
                    "type": "string",
                    "title": "Date",
                    "format": "date",
                    "description": "The date when the UFO sighting took place. YYYY-MM-DD format.",
                },
                "location": {
                    "type": "string",
                    "title": "Location",
                    "description": "The location where the UFO sighting occurred.",
                },
                "description": {
                    "type": "string",
                    "title": "Description",
                    "description": "A description of the UFO sighting.",
                },
            },
            "description": "Schema for extracting information related to UFO sightings.",
        },
        "output": [
            {
                "date": "1897-04-17",
                "location": "Aurora, Texas",
                "description": "A UFO sighting involving a cigar-shaped mystery airship that crashed on the property of Judge J.S. Proctor. The pilot, described as 'not of this world' and a 'Martian', did not survive the crash and was buried at the nearby Aurora Cemetery with Christian rites. Wreckage from the crash site was dumped into a nearby well, and some ended up with the alien in the grave. The incident is marked by a Texas Historical Commission marker at the cemetery.",
            }
        ],
    },
    {
        "url": "https://www.hauntedplaces.org/item/eunice-williams-covered-bridge-pumping-station-bridge/",
        "json_schema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Haunted Location Extractor",
            "description": "Schema for extracting information about haunted locations from text.",
            "type": "object",
            "properties": {
                "location_name": {
                    "type": "string",
                    "title": "Location Name",
                    "description": "The name of the haunted location.",
                },
                "ghosts": {
                    "type": "array",
                    "title": "Ghosts",
                    "description": "List of ghosts or spirits reported to haunt the location.",
                    "items": {"type": "string"},
                },
            },
        },
        "output": (
            [
                {
                    "ghosts": ["Eunice Williams"],
                    "location_name": "Eunice Williams Covered Bridge - Pumping Station Bridge",
                }
            ],
        ),
    },
    {
        "url": "https://phys.org/news/2024-10-super-neptune-exoplanet.html",
        "json_schema": {
            "title": "Exoplanet Information Extractor",
            "description": "Schema for extracting information about exoplanets from text.",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "title": "Name",
                    "description": "The name of the exoplanet.",
                },
                "discovery_method": {
                    "type": "string",
                    "title": "Discovery Method",
                    "description": "The method used to discover the exoplanet.",
                },
                "discovery_year": {
                    "type": "integer",
                    "title": "Discovery Year",
                    "description": "The year in which the exoplanet was discovered.",
                },
                "mass": {
                    "type": "number",
                    "title": "Mass",
                    "description": "The mass of the exoplanet in Earth masses.",
                },
                "radius": {
                    "type": "number",
                    "title": "Radius",
                    "description": "The radius of the exoplanet in Earth radii.",
                },
                "orbital_period": {
                    "type": "number",
                    "title": "Orbital Period",
                    "description": "The orbital period of the exoplanet in days.",
                },
            },
        },
        "output": [
            {
                "mass": 32.7,
                "name": "TOI-5005 b",
                "radius": 6.25,
                "discovery_year": 2024,
                "orbital_period": 6.31,
                "discovery_method": "Transit",
            }
        ],
    },
    {
        "url": "https://science.nasa.gov/exoplanet-catalog/toi-5005-b/",
        "json_schema": {
            "title": "Exoplanet Information Extractor",
            "description": "Schema for extracting information about exoplanets from text.",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "title": "Name",
                    "description": "The name of the exoplanet.",
                },
                "discovery_method": {
                    "type": "string",
                    "title": "Discovery Method",
                    "description": "The method used to discover the exoplanet.",
                },
                "discovery_year": {
                    "type": "integer",
                    "title": "Discovery Year",
                    "description": "The year in which the exoplanet was discovered.",
                },
                "mass": {
                    "type": "number",
                    "title": "Mass",
                    "description": "The mass of the exoplanet in Earth masses.",
                },
                "radius": {
                    "type": "number",
                    "title": "Radius",
                    "description": "The radius of the exoplanet in Earth radii.",
                },
                "orbital_period": {
                    "type": "number",
                    "title": "Orbital Period",
                    "description": "The orbital period of the exoplanet in days.",
                },
            },
        },
        "output": [
            {
                "mass": 32.7,
                "name": "TOI-5005 b",
                "radius": 6.25,
                "discovery_year": 2024,
                "orbital_period": 6.3,
                "discovery_method": "Transit",
            }
        ],
    },
    {
        "url": "https://sites.pitt.edu/~dash/japan.html",
        "json_schema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Legend Extractor",
            "description": "Extracts the name of a legend and the names of characters from text.",
            "type": "object",
            "properties": {
                "legend_name": {
                    "type": "string",
                    "title": "Legend Name",
                    "description": "The name of the legend mentioned in the text.",
                },
                "character_names": {
                    "type": "array",
                    "title": "Character Names",
                    "description": "An array of names of characters associated with the legend. Each name is a string.",
                    "items": {"type": "string"},
                },
            },
        },
        "output": [
            {
                "legend_name": "The Two Frogs",
                "characters": ["Osaka frog", "Kyoto frog"],
            },
            {
                "legend_name": "The Mirror of Matsuyama",
                "characters": ["man", "wife", "little girl", "stepmother"],
            },
            {
                "characters": ["Visu", "Old Priest", "Visu's wife", "Old woman"],
                "legend_name": "Visu the Woodsman",
            },
            {
                "legend_name": "The Adventures of Little Peachling",
                "characters": [
                    "Little Peachling",
                    "old woodcutter",
                    "old woodcutter's wife",
                    "monkey",
                    "pheasant",
                    "dog",
                    "ogres",
                    "ogres' king",
                ],
            },
            {
                "legend_name": "A Woman and the Bell of Miidera",
                "characters": ["priests", "woman"],
            },
            {
                "legend_name": "The Stonecutter",
                "character_names": ["The Stonecutter", "The Mountain Spirit"],
            },
            {
                "legend_name": "Danzayémon, Chief of the Etas",
                "character_names": [
                    "Danzayémon",
                    "Minamoto no Yoritomo",
                    "Minamoto no Yoshitomo",
                    "Taira no Kiyomori",
                    "Tokiwa",
                    "Munémori",
                    "Hojo",
                ],
            },
        ],
    },
    {
        "url": "https://sites.pitt.edu/~dash/japan.html",
        "json_schema": {
            "title": "Conspiracy Theory Extractor",
            "description": "Schema for extracting information related to conspiracy theories from text.",
            "type": "object",
            "properties": {
                "title": {
                    "title": "Conspiracy Theory",
                    "description": "The conspiracy theory mentioned in the text.",
                    "type": "string",
                },
                "geography_location": {
                    "title": "Geography Location",
                    "description": "The geographical location associated with the conspiracy theory.",
                    "type": "string",
                },
                "origin_year": {
                    "title": "Origin Year",
                    "description": "The year when the conspiracy theory originated.",
                    "type": "number",
                },
                "status": {
                    "title": "Status",
                    "description": "The current status or validity of the conspiracy theory.",
                    "type": "string",
                    "enum": ["unverified", "debunked", "confirmed"],
                },
            },
        },
        "output": [],
    },
    {
        "url": "https://www.factcheck.org/2021/07/scicheck-spoof-video-furthers-microchip-conspiracy-theory/",
        "json_schema": {
            "title": "Conspiracy Theory Extractor",
            "description": "Schema for extracting information related to conspiracy theories from text.",
            "type": "object",
            "properties": {
                "title": {
                    "title": "Conspiracy Theory",
                    "description": "The conspiracy theory mentioned in the text.",
                    "type": "string",
                },
                "geography_location": {
                    "title": "Geography Location",
                    "description": "The geographical location associated with the conspiracy theory.",
                    "type": "string",
                },
                "origin_year": {
                    "title": "Origin Year",
                    "description": "The year when the conspiracy theory originated.",
                    "type": "number",
                },
                "status": {
                    "title": "Status",
                    "description": "The current status or validity of the conspiracy theory.",
                    "type": "string",
                    "enum": ["unverified", "debunked", "confirmed"],
                },
            },
        },
        "output": [
            {
                "title": "Conspiracy theories about microchips in COVID-19 vaccines",
                "status": "debunked",
                "origin_year": 2020,
                "geography_location": "United States",
            }
        ],
    },
]

if __name__ == "__main__":
    from langsmith import Client

    client = Client()
    dataset_name = "Webpage Extraction Dataset"

    # Storing inputs in a dataset lets us
    # run chains and LLMs over a shared set of examples.
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Extract specific data from a given webpage.",
    )

    # Prepare inputs, outputs, and metadata for bulk creation
    inputs = [
        {"json_schema": record["json_schema"], "url": record["url"]}
        for record in examples
    ]
    outputs = [{"output": record["output"]} for record in examples]

    client.create_examples(
        inputs=inputs,
        outputs=outputs,
        dataset_id=dataset.id,
    )
