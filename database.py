"""
=============================================================================
Prakriti: Nature & Belief Explorer - Database Module
=============================================================================
This file handles:
1. SQLite connection management
2. Creation of database tables (elements, beliefs, festivals, quiz_questions)
3. Initial seeding with accurate cultural and ecological content
4. Data access functions for the Flask application and Admin interface
=============================================================================
"""

import sqlite3
import os

# Define database file path in the same directory as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "prakriti.db")


def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    Configures row_factory so query results can be accessed like dictionaries.
    """
    conn = sqlite3.connect(DB_PATH)
    # Enable access to columns by name instead of only numerical tuple indexes
    conn.row_factory = sqlite3.Row
    # Enforce foreign key constraints in SQLite
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Initializes database tables if they do not already exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Elements table: stores nature elements honored across Indian tradition
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
    """)

    # 2. Beliefs table: stores cultural belief vs scientific explanation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS beliefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            element_id INTEGER NOT NULL,
            belief_text TEXT NOT NULL,
            science_text TEXT NOT NULL,
            FOREIGN KEY (element_id) REFERENCES elements(id) ON DELETE CASCADE
        )
    """)

    # 3. Festivals table: stores festivals linked to nature elements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS festivals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            month TEXT NOT NULL,
            element_id INTEGER,
            description TEXT NOT NULL,
            FOREIGN KEY (element_id) REFERENCES elements(id) ON DELETE SET NULL
        )
    """)

    # 4. Quiz Questions table: tests understanding of traditional wisdom and science
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """
    Seeds the database with at least 12 elements, 12 beliefs, 8 festivals,
    and 10 quiz questions if the database is currently empty.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if elements table already has data
    cursor.execute("SELECT COUNT(*) FROM elements")
    element_count = cursor.fetchone()[0]

    if element_count > 0:
        conn.close()
        return  # Already seeded

    print("Seeding Prakriti database with rich cultural and scientific content...")

    # =========================================================================
    # SEED 1: ELEMENTS (12 Elements)
    # =========================================================================
    elements_data = [
        (
            1,
            "Surya (The Sun)",
            "Celestial Bodies",
            "Revered as the visible Supreme Divinity (Pratyaksha Devata) and the soul of all living and moving beings. Worshiped at dawn through Surya Namaskar and water offerings (Arghya).",
            "/static/images/surya.svg"
        ),
        (
            2,
            "Maa Ganga & Sacred Rivers",
            "Water Bodies",
            "Personified as the divine mother descending from Shiva's locks to nourish the land and liberate ancestral spirits. Revered as living goddesses across India.",
            "/static/images/ganga.svg"
        ),
        (
            3,
            "Tulsi (Holy Basil)",
            "Flora & Sacred Plants",
            "Considered the earthly manifestation of Vrinda and Goddess Lakshmi. Planted at the heart of the courtyard (Tulsi Chaura) as a guardian of health and spiritual sanctity.",
            "/static/images/tulsi.svg"
        ),
        (
            4,
            "Peepal Tree (Ashvattha / Ficus religiosa)",
            "Flora & Sacred Plants",
            "Regarded as the King of Trees where the cosmic Trinity abides: Brahma at the roots, Vishnu in the trunk, and Shiva in the leaves. Cutting a living Peepal is taboo.",
            "/static/images/peepal.svg"
        ),
        (
            5,
            "Nag (Serpents / Snakes)",
            "Fauna & Sacred Animals",
            "Adorned around Lord Shiva's neck as Vasuki and serving as the bed of Lord Vishnu as Sheshnaga. Revered as guardians of subterranean realms, fertility, and waters.",
            "/static/images/nag.svg"
        ),
        (
            6,
            "Gomata (Indigenous Cow)",
            "Fauna & Sacred Animals",
            "Venerated as Kamadhenu, the wish-granting mother embodying selfless giving and non-violence (Ahimsa). Believed to harbor millions of divine energies.",
            "/static/images/cow.svg"
        ),
        (
            7,
            "Agni (Sacred Fire)",
            "Elemental Forces",
            "The cosmic priest and mediator (Havyavahana) who carries oblations to heaven and bears witness to sacred vows (Saptapadi). Revered in Havana and daily cooking.",
            "/static/images/agni.svg"
        ),
        (
            8,
            "Govardhan & Sacred Mountains",
            "Earth & Landforms",
            "Revered as living protectors of watersheds and weather cycles. Lord Krishna famously held Govardhan hill on his little finger to honor local ecology over ritual sacrifice.",
            "/static/images/govardhan.svg"
        ),
        (
            9,
            "Chandra (The Moon)",
            "Celestial Bodies",
            "Revered as the sovereign lord of medicinal herbs (Oshadhinam Adhipati) and ruler of the human mind (Manas). Associated with cooling nectar and tranquility.",
            "/static/images/chandra.svg"
        ),
        (
            10,
            "Prithvi / Bhumi (Mother Earth)",
            "Earth & Landforms",
            "Worshiped as Bhumi Devi, embodying unconditional tolerance and sustenance. Devotees ask forgiveness each morning for stepping upon her sacred body.",
            "/static/images/prithvi.svg"
        ),
        (
            11,
            "Vata (The Sacred Banyan Tree)",
            "Flora & Sacred Plants",
            "Known as Akshaya Vata (the Undying Tree), symbolizing eternal life, sheltering wisdom, and resilience. Revered during Vat Savitri for enduring longevity.",
            "/static/images/banyan.svg"
        ),
        (
            12,
            "Neem (Margosa Tree)",
            "Flora & Sacred Plants",
            "Regarded as an incarnation of Goddess Shitala and Mariamman, guardians against disease and pestilence. Sprigs are hung at doorways during new year celebrations.",
            "/static/images/neem.svg"
        )
    ]

    cursor.executemany("""
        INSERT INTO elements (id, name, category, description, image_url)
        VALUES (?, ?, ?, ?, ?)
    """, elements_data)

    # =========================================================================
    # SEED 2: BELIEFS (12 Beliefs - Tradition vs Science)
    # =========================================================================
    beliefs_data = [
        (
            1,
            "Offering water (Arghya) to Surya at sunrise while looking through droplets honors the cosmic creator who sustains life, dispels darkness, and blesses humanity with radiant vitality.",
            "Morning sunlight has gentle UV rays that stimulate Vitamin D synthesis without sunburn risk, sets our circadian rhythm, and triggers serotonin production. The prism effect of water droplets softens solar glare while stimulating optic pathways."
        ),
        (
            2,
            "Rivers are living mothers whose sacred waters wash away karmic impurities. Ganga Jal is kept in copper vessels for years without spoiling and offered during every rite of passage.",
            "River basins sustain over 500 million people and provide crucial alluvial soil for agriculture. Scientific studies by microbiologists show Ganga contains unique bacteriophages ('Ganga Factor') that destroy harmful bacteria and keep dissolved oxygen levels remarkably high."
        ),
        (
            3,
            "Tulsi is beloved of Lord Vishnu and is honored as Goddess Vrinda. Lighting a lamp beside Tulsi at twilight brings spiritual purity, peace, and protects the household from misfortune.",
            "Tulsi (Ocimum sanctum) is a powerhouse adaptogen and natural insect repellent. It releases volatile terpenes, eugenol, and caryophyllene that purify courtyard air, deter mosquitoes, and combat airborne pathogens."
        ),
        (
            4,
            "Lord Krishna in the Bhagavad Gita declared: 'Among all trees, I am the Ashvattha (Peepal)'. It is considered the dwelling place of Brahma, Vishnu, and Shiva; chopping it brings spiritual peril.",
            "The Peepal tree has an exceptionally vast canopy with high stomatal density that cools surrounding microclimates. It exhibits Crassulacean Acid Metabolism (CAM), absorbing CO2 and releasing oxygen over extended diurnal periods, and serves as a keystone host for hundreds of avian and insect species."
        ),
        (
            5,
            "Snakes are worshiped as representatives of the subterranean Nagas who guard fertility, subterranean waters, and agricultural bounty. Nag Panchami reminds humans to revere them with milk and flowers.",
            "Snakes are nature's most effective biological pest controllers. A single rat snake consumes hundreds of rodents annually, saving grain silos from decimation and containing fatal rodent-borne epidemics such as leptospirosis and plague."
        ),
        (
            6,
            "The cow is revered as Gomata, the embodiment of selfless motherhood and gentle nature. Feeding cows and worshiping them is believed to atone for sins and foster non-violent stewardship.",
            "Indigenous cattle (Bos indicus) are the cornerstone of regenerative zero-budget natural farming. Cow dung and urine contain billions of beneficial nitrogen-fixing and phosphate-solubilizing bacteria (Jeevamrit) that rejuvenate depleted topsoil without chemical fertilizers."
        ),
        (
            7,
            "Agni is the divine messenger who accepts offerings made into the sacrificial fire and delivers them to cosmic energies. Agni cleanses physical spaces and validates holy vows as a divine witness.",
            "Controlled combustion of dry aromatic woods, cow ghee, camphor, and medicinal herbs during Hawan disperses micronized therapeutic aerosols into the atmosphere, which significantly reduces bacterial colony counts in indoor and courtyard air."
        ),
        (
            8,
            "Krishna taught the Braj community that mountains with their forests, grazing pastures, and perennial streams directly sustain human and bovine life, deserving far greater gratitude than abstract rituals.",
            "Mountains serve as vital water towers and watershed shields. Govardhan's vegetation prevented soil runoff during torrential monsoons, while the greater Himalayan mountain barrier traps monsoon clouds to feed perennial river networks across South Asia."
        ),
        (
            9,
            "Chandra rules over night, the ocean tides, and plant sap. On Sharad Purnima, dishes like kheer are kept under moonlight to absorb divine healing ambrosia (Amrita) from the full moon.",
            "The Moon's gravitational pull governs marine tides and biological rhythms. Full moonlight combined with autumn nocturnal dew causes rapid cooling and condensation, while lunar illumination influences plant hormone circulation and nocturnal pollinators."
        ),
        (
            10,
            "Mother Earth (Bhumi Devi) provides boundless patience, water, minerals, and grain. Devotees recite the morning prayer: 'O ocean-robed Goddess, forgive the touch of my feet upon your sacred body'.",
            "Healthy topsoil is a living ecosystem harboring billions of microorganisms, fungal mycorrhizae, and organic carbon. Recognizing the ground as sacred prevents reckless soil compaction, erosion, and over-exploitation."
        ),
        (
            11,
            "The Banyan tree is named Akshaya Vata because its roots drop from branches to form new trunks, creating an immortal forest that never dies. Married women circumambulate it for the longevity of family bonds.",
            "The extensive aerial prop roots of the Banyan anchor expansive hillsides against flash floods and mudslides. A single mature Banyan tree creates a self-contained forest that shelters over 500 species of birds, bats, insects, and epiphytic flora."
        ),
        (
            12,
            "Neem is worshiped as Goddess Mariamman / Shitala, representing immunity against pox, measles, and seasonal viral outbreaks. Doorways are lined with fresh neem leaves to protect the home.",
            "Neem (Azadirachta indica) produces over 140 active compounds including azadirachtin and nimbin. It is scientifically proven to possess potent antibacterial, antiviral, antifungal, and insect-repellent properties, acting as an organic pesticide and immune booster."
        )
    ]

    cursor.executemany("""
        INSERT INTO beliefs (element_id, belief_text, science_text)
        VALUES (?, ?, ?)
    """, beliefs_data)

    # =========================================================================
    # SEED 3: FESTIVALS (10 Festivals)
    # =========================================================================
    festivals_data = [
        (
            1,
            "Chhath Puja",
            "Kartika (October - November)",
            1,  # Surya
            "A four-day festival dedicated to Surya Dev and Chhathi Maiya. Devotees stand waist-deep in natural water bodies at dusk and dawn to offer Arghya, expressing supreme gratitude for sunlight and ecological bounty."
        ),
        (
            2,
            "Makar Sankranti & Pongal",
            "Magha (January)",
            1,  # Surya
            "Marks the transition of the Sun into the zodiac sign of Makara (Capricorn) and the northward journey (Uttarayan). Celebrates the first harvest with sesame seeds, jaggery, and community bonfires."
        ),
        (
            3,
            "Nag Panchami",
            "Shravana (July - August)",
            5,  # Nag
            "Celebrated during peak monsoon when heavy rains flood snake burrows, driving them into human habitats. Rather than killing snakes in fear, people offer prayers, milk, and seek coexistence."
        ),
        (
            4,
            "Ganga Dussehra",
            "Jyeshtha (May - June)",
            2,  # Ganga
            "Commemorates the day the celestial river Ganga descended to Earth. Devotees assemble at riverbanks at the start of summer to clean ghats, bathe, and pledge protection of freshwater sources."
        ),
        (
            5,
            "Tulsi Vivah",
            "Kartika (November)",
            3,  # Tulsi
            "The ceremonial wedding of the Tulsi plant to Shaligram (Lord Vishnu), marking the end of the monsoon and the beginning of the auspicious winter wedding and herbal harvesting season."
        ),
        (
            6,
            "Govardhan Puja (Annakut)",
            "Kartika (October - November)",
            8,  # Govardhan
            "Celebrated the day after Diwali, where communities build symbolic replicas of Mount Govardhan using cow dung and prepare a mountain of 56 organic food offerings (Chhappan Bhog) in gratitude to nature."
        ),
        (
            7,
            "Vat Purnima (Vat Savitri)",
            "Jyeshtha (May - June)",
            11, # Vata / Banyan
            "Women tie sacred red and yellow threads around the trunks of massive Banyan trees and circumambulate them, commemorating Savitri's triumph and honoring the eternal sheltering canopy of the tree."
        ),
        (
            8,
            "Sharad Purnima",
            "Ashvin (October)",
            9,  # Chandra
            "A harvest moon festival celebrating the brightest full moon of autumn. Devotees prepare rice pudding (kheer) and place it under the moonlight all night to absorb therapeutic lunar dew."
        ),
        (
            9,
            "Holika Dahan & Lohri",
            "Phalguna & Pausha (March & January)",
            7,  # Agni
            "Community bonfires ignited to celebrate the victory of devotion over malice, marking the changing seasons from cold winter to warm spring while burning agricultural harvest residues in a celebratory circle."
        ),
        (
            10,
            "Raja Parba (Earth Menstruation Festival)",
            "Ashadha (June)",
            10, # Prithvi
            "A celebrated 3-day festival in Odisha honoring Mother Earth. All agricultural activities, tilling, digging, and tree-felling cease completely to give the soil time to rest and rejuvenate before the arrival of the monsoon rains."
        )
    ]

    cursor.executemany("""
        INSERT INTO festivals (id, name, month, element_id, description)
        VALUES (?, ?, ?, ?, ?)
    """, festivals_data)

    # =========================================================================
    # SEED 4: QUIZ QUESTIONS (10 Questions - Superstition or Science?)
    # =========================================================================
    quiz_data = [
        (
            1,
            "Why did ancient Indian ecological ethics strictly prohibit the cutting down of the Peepal tree (Ashvattha)?",
            "Because spirits would haunt whoever chops down a Peepal tree.",
            "Because its extensive canopy provides prolonged oxygen release and acts as a keystone ecological shelter for diverse fauna.",
            "Because Peepal wood is completely toxic and cannot be used for any household furniture.",
            "Because it was reserved exclusively for royal woodcutters.",
            "B",
            "The Peepal tree (Ficus religiosa) releases oxygen over extended periods due to Crassulacean Acid Metabolism (CAM) and hosts hundreds of bird, insect, and epiphyte species. Coding its protection into sacred duty ensured communities preserved these vital ecosystem anchors."
        ),
        (
            2,
            "What is the ecological purpose behind celebrating Nag Panchami during the monsoon month of Shravana?",
            "To promote keeping venomous snakes as domestic pets in households.",
            "Because snakes multiply exclusively on this single day.",
            "Because flooded burrows drive snakes above ground, and the festival instills restraint against harming these crucial rodent predators.",
            "To gather snake venom for making temple dyes.",
            "C",
            "During the heavy monsoon, snake burrows flood, forcing reptiles into agricultural fields and villages. Nag Panchami teaches reverence rather than panic, protecting snakes who keep crop-destroying rodent populations under control."
        ),
        (
            3,
            "In traditional Indian house architecture, why was the Tulsi plant placed in the center of the inner courtyard (Angan)?",
            "To cast a shadow across the roof during solar eclipses.",
            "Because Tulsi leaves naturally ward off lightning strikes.",
            "Because it emits volatile essential oils that repel mosquitoes and purify the air circulating through living quarters.",
            "To serve solely as a decorative centerpiece for visiting guests.",
            "C",
            "Tulsi (Ocimum sanctum) releases volatile terpenes like eugenol and camphor that act as potent natural mosquito repellents and airborne antimicrobial agents, ensuring clean air circulation throughout traditional central-courtyard homes."
        ),
        (
            4,
            "What scientific property explains why water from the River Ganga traditionally remained fresh in vessels for years?",
            "It is naturally carbonated by volcanic vents in the Himalayas.",
            "The presence of unique, self-purifying bacteriophages ('Ganga Factor') and high dissolved oxygen levels that suppress putrefaction.",
            "Heavy metals added by temple priests act as chemical preservatives.",
            "The water boils naturally in underground hot springs before reaching the plains.",
            "B",
            "Extensive microbiological research has confirmed that Ganga water harbors specialized bacteriophages—viruses that specifically destroy harmful bacteria—along with unusual mineral sediment that helps maintain high dissolved oxygen."
        ),
        (
            5,
            "During Chhath Puja, why do devotees stand waist-deep in water facing the rising and setting Sun?",
            "To demonstrate physical stamina and withstand cold river temperatures.",
            "Morning and evening sunlight offers safe, oblique UV rays that stimulate Vitamin D and regulate circadian health without retina damage.",
            "Because the Sun is only visible when standing in flowing river water.",
            "To cool down the body before eating spicy festival delicacies.",
            "B",
            "At dawn and dusk, the Sun's rays traverse a thicker atmospheric layer, filtering out harsh UV radiation while providing the ideal wavelength for synthesizing Vitamin D, balancing melatonin, and resetting the master circadian clock."
        ),
        (
            6,
            "Why has indigenous cow dung (Gomaya) been revered as sacred in Indian agrarian tradition?",
            "Because it contains precious metals that can be extracted through alchemy.",
            "It is rich in beneficial nitrogen-fixing and phosphate-solubilizing microbes that regenerate depleted topsoil organically.",
            "Because it emits an aroma that directly attracts rain clouds.",
            "It was the only building material allowed by ancient construction guilds.",
            "B",
            "Desi cow dung and urine contain diverse colonies of beneficial soil microbes, enzymes, and organic matter. Formulations like Jeevamrit and Panchagavya nourish soil microbiology, enhancing moisture retention and plant immunity."
        ),
        (
            7,
            "What profound ecological shift did Lord Krishna introduce during the Govardhan Puja narrative?",
            "He encouraged clearing mountain forests to build larger royal palaces.",
            "He advised communities to stop traveling to distant temples.",
            "He redirected reverence away from distant celestial deities toward the local mountain ecosystem that sustains life with pasture and water.",
            "He proved that stone mountains could be easily broken for gravel.",
            "C",
            "Krishna challenged blind ritualism by pointing out that the Braj community's cattle and people were directly nurtured by the pastures, trees, and streams of Mount Govardhan. He taught that real divinity resides in protecting local ecology."
        ),
        (
            8,
            "On Ugadi and Gudi Padwa, why is it customary to eat a paste of bitter Neem leaves mixed with sweet Jaggery?",
            "To prove one's ability to tolerate unpleasant medicinal flavors.",
            "To kickstart immunity, kill intestinal parasites, and philosophically acknowledge life's balance of bitter trials and sweet blessings.",
            "Because winter crops are completely unavailable during this month.",
            "To temporarily numb the tongue before festival banquets.",
            "B",
            "Transitioning from spring to summer brings seasonal illnesses. Neem provides powerful bitter anthelmintic, antiviral, and hepatic cleansing properties, while jaggery provides instant iron and energy, harmonizing tradition with seasonal preventative medicine."
        ),
        (
            9,
            "Why does the Raja Parba festival in Odisha prohibit all tilling, digging, and ploughing of the soil for three consecutive days?",
            "Because farm cattle are taken on an annual interstate migration.",
            "To allow the soil to rest, recover, and prepare organically for the arrival of the life-giving summer monsoon rains.",
            "Because iron farming tools were believed to invite lightning strikes in June.",
            "To compel farmers to spend all three days shopping in local village markets.",
            "B",
            "Raja Parba celebrates the Earth's fertility cycle right before the onset of the monsoon. Halting all tilling gives the topsoil time to aerate and regenerate without mechanical disturbance, embodying sustainable soil conservation."
        ),
        (
            10,
            "How do the hanging prop roots of the Sacred Banyan Tree (Vata) help protect village ecosystems?",
            "They attract lightning away from residential thatched roofs.",
            "They drop into the ground to create massive secondary trunks that anchor fragile soil against flash floods and create expansive wildlife habitats.",
            "They absorb toxic gases from the clouds and convert them into salt.",
            "They prevent all other trees in the vicinity from growing.",
            "B",
            "The aerial roots of Ficus benghalensis extend downward to form auxiliary trunks, spreading across acres. This root matrix prevents severe bank erosion during monsoon floods while forming a sanctuary for countless birds, mammals, and pollinators."
        )
    ]

    cursor.executemany("""
        INSERT INTO quiz_questions (
            id, question, option_a, option_b, option_c, option_d, correct_option, explanation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, quiz_data)

    conn.commit()
    conn.close()
    print("Database seeding completed successfully!")


# =============================================================================
# DATA ACCESS & QUERY FUNCTIONS
# =============================================================================

def get_all_elements(category=None, search=None, festival_id=None):
    """
    Retrieves elements with optional filtering by category, search query, or linked festival.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT e.*, b.belief_text, b.science_text,
               GROUP_CONCAT(f.name, ', ') AS festival_names
        FROM elements e
        LEFT JOIN beliefs b ON e.id = b.element_id
        LEFT JOIN festivals f ON e.id = f.element_id
        WHERE 1=1
    """
    params = []

    if category and category != "All":
        query += " AND e.category = ?"
        params.append(category)

    if search:
        query += " AND (e.name LIKE ? OR e.description LIKE ? OR b.belief_text LIKE ? OR b.science_text LIKE ?)"
        wildcard = f"%{search}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])

    if festival_id:
        query += " AND f.id = ?"
        params.append(festival_id)

    query += " GROUP BY e.id ORDER BY e.id ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_element_by_id(element_id):
    """
    Retrieves a single element by its ID along with its belief and linked festivals.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.*, b.id AS belief_id, b.belief_text, b.science_text
        FROM elements e
        LEFT JOIN beliefs b ON e.id = b.element_id
        WHERE e.id = ?
    """, (element_id,))
    element = cursor.fetchone()

    if not element:
        conn.close()
        return None

    # Fetch associated festivals
    cursor.execute("SELECT * FROM festivals WHERE element_id = ? ORDER BY id ASC", (element_id,))
    festivals = cursor.fetchall()

    # Fetch previous and next element IDs for navigation
    cursor.execute("SELECT id FROM elements WHERE id < ? ORDER BY id DESC LIMIT 1", (element_id,))
    prev_row = cursor.fetchone()
    prev_id = prev_row["id"] if prev_row else None

    cursor.execute("SELECT id FROM elements WHERE id > ? ORDER BY id ASC LIMIT 1", (element_id,))
    next_row = cursor.fetchone()
    next_id = next_row["id"] if next_row else None

    conn.close()
    return {
        "element": element,
        "festivals": festivals,
        "prev_id": prev_id,
        "next_id": next_id
    }


def get_all_festivals():
    """
    Retrieves all festivals along with the name and category of the element they honor.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.*, e.name AS element_name, e.category AS element_category, e.image_url AS element_image
        FROM festivals f
        LEFT JOIN elements e ON f.element_id = e.id
        ORDER BY f.id ASC
    """)
    festivals = cursor.fetchall()
    conn.close()
    return festivals


def get_festival_by_id(festival_id):
    """
    Retrieves a single festival by ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM festivals WHERE id = ?", (festival_id,))
    festival = cursor.fetchone()
    conn.close()
    return festival


def get_categories():
    """
    Retrieves unique categories of elements.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM elements ORDER BY category ASC")
    categories = [row["category"] for row in cursor.fetchall()]
    conn.close()
    return categories


def get_quiz_questions(limit=None):
    """
    Retrieves quiz questions.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if limit:
        cursor.execute("SELECT * FROM quiz_questions ORDER BY id ASC LIMIT ?", (limit,))
    else:
        cursor.execute("SELECT * FROM quiz_questions ORDER BY id ASC")
    questions = cursor.fetchall()
    conn.close()
    return questions


def get_quiz_question_by_id(question_id):
    """
    Retrieves a single quiz question by ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_questions WHERE id = ?", (question_id,))
    question = cursor.fetchone()
    conn.close()
    return question


def get_stats():
    """
    Returns counts of all major entities for the admin dashboard and home hero.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM elements")
    element_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM beliefs")
    belief_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM festivals")
    festival_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM quiz_questions")
    quiz_count = cursor.fetchone()[0]

    conn.close()
    return {
        "elements": element_count,
        "beliefs": belief_count,
        "festivals": festival_count,
        "quiz_questions": quiz_count
    }


# =============================================================================
# ADMIN CRUD FUNCTIONS
# =============================================================================

# --- Elements ---
def add_element(name, category, description, image_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO elements (name, category, description, image_url)
        VALUES (?, ?, ?, ?)
    """, (name, category, description, image_url))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_element(element_id, name, category, description, image_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE elements
        SET name = ?, category = ?, description = ?, image_url = ?
        WHERE id = ?
    """, (name, category, description, image_url, element_id))
    conn.commit()
    conn.close()


def delete_element(element_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM elements WHERE id = ?", (element_id,))
    conn.commit()
    conn.close()


# --- Beliefs ---
def get_all_beliefs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.*, e.name AS element_name
        FROM beliefs b
        LEFT JOIN elements e ON b.element_id = e.id
        ORDER BY b.id ASC
    """)
    beliefs = cursor.fetchall()
    conn.close()
    return beliefs


def get_belief_by_id(belief_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM beliefs WHERE id = ?", (belief_id,))
    belief = cursor.fetchone()
    conn.close()
    return belief


def add_belief(element_id, belief_text, science_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO beliefs (element_id, belief_text, science_text)
        VALUES (?, ?, ?)
    """, (element_id, belief_text, science_text))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_belief(belief_id, element_id, belief_text, science_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE beliefs
        SET element_id = ?, belief_text = ?, science_text = ?
        WHERE id = ?
    """, (element_id, belief_text, science_text, belief_id))
    conn.commit()
    conn.close()


def delete_belief(belief_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM beliefs WHERE id = ?", (belief_id,))
    conn.commit()
    conn.close()


# --- Festivals ---
def add_festival(name, month, element_id, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO festivals (name, month, element_id, description)
        VALUES (?, ?, ?, ?)
    """, (name, month, element_id, description))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_festival(festival_id, name, month, element_id, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE festivals
        SET name = ?, month = ?, element_id = ?, description = ?
        WHERE id = ?
    """, (name, month, element_id, description, festival_id))
    conn.commit()
    conn.close()


def delete_festival(festival_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM festivals WHERE id = ?", (festival_id,))
    conn.commit()
    conn.close()


# --- Quiz Questions ---
def add_quiz_question(question, option_a, option_b, option_c, option_d, correct_option, explanation):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_questions (
            question, option_a, option_b, option_c, option_d, correct_option, explanation
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (question, option_a, option_b, option_c, option_d, correct_option.upper(), explanation))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_quiz_question(question_id, question, option_a, option_b, option_c, option_d, correct_option, explanation):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE quiz_questions
        SET question = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?,
            correct_option = ?, explanation = ?
        WHERE id = ?
    """, (question, option_a, option_b, option_c, option_d, correct_option.upper(), explanation, question_id))
    conn.commit()
    conn.close()


def delete_quiz_question(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quiz_questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()


# Initialize and seed on direct script execution or module load
if __name__ == "__main__":
    init_db()
    seed_db()
    print("Database ready. Element count:", get_stats()["elements"])
