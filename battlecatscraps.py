from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sys
import sqlite3

ZERO = 72.222222
ONE = 91.481481
TWO = 110.740741
THREE = 130.000000
FOUR = 149.259259
FIVE = 168.518519
SIX = 187.777778
SEVEN = 207.037037
EIGHT = 226.296296
NINE = 0.962963

DATABASE_FILE = "battlecats.db"

def connect_database(database):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    return conn, cur

def number_conversion(number):
    number = float(number)
    if number == ZERO:
        return 0
    elif number == ONE:
        return 1
    elif number == TWO:
        return 2
    elif number == THREE:
        return 3
    elif number == FOUR:
        return 4
    elif number == FIVE:
        return 5
    elif number == SIX:
        return 6
    elif number == SEVEN:
        return 7
    elif number == EIGHT:
        return 8
    elif number == NINE:
        return 9

enemy_types = ["Red", "Reds", "Black", "Blacks", "Floating", "Metal", "Metals", "Angel", "Angels", "Alien", "Aliens", "Zombie", "Zombies", "Aku", "Akus", "Relic", "Relics", "Traitless"]

def type_allocate(trait):
    conn, cur = connect_database(DATABASE_FILE)
    cur.execute("SELECT type_id FROM cat_type WHERE LOWER(type_name) = ?;", (trait.lower(),))
    trait = cur.fetchone()[0]
    conn.close()
    return trait


def rarity_allocate(rarity):
    match rarity.lower():
        case "normal cat":
            return 6
        case "special cat":
            return 5
        case "rare cat":
            return 4
        case "super rare cat":
            return 3
        case "uber rare cat":
            return 2
        case "legend rare cat":
            return 1

skill_ban = ["Break", "Colossal", "Behemoth", "Eva angels", "Eva Angels", "Witches"]

def skill_allocate(skill):
    conn, cur = connect_database(DATABASE_FILE)
    if skill.lower() == "barriers" or skill.lower() == "barrier":
        skill = "barrier breaker"
    elif skill.lower() == "critical":
        skill = "critical hit"
    elif skill.lower() == "evade surge":
        skill = "immune to surge"
    elif skill.lower() == "pierce":
        skill = "shield piercing"
    elif skill.lower() == "strong":
        skill = "strong against"
    cur.execute("SELECT skill_id FROM cat_skills WHERE LOWER(skill_name) = ?;", (skill.lower(),))
    skill = cur.fetchone()[0]
    conn.close()
    return skill

def duplicate_remover(dup_list):
    return list(dict.fromkeys(dup_list))
# Cat URLs grabber
# cat_order_url = "https://battle-cats.fandom.com/wiki/Cat_Release_Order"
# page = urlopen(cat_order_url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# order_soup = BeautifulSoup(html, "html.parser")
# cat_links = order_soup.find("tbody")
# cat_links = cat_links.find_all("tr")
cat_links_table = ['https://battle-cats.fandom.com/wiki/Cat_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Tank_Cat_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Axe_Cat_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Gross_Cat_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Cow_Cat_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Bird_Cat_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Fish_Cat_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Lizard_Cat_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Titan_Cat_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Actress_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Kung_Fu_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Mr._(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Bondage_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Dom_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cats_in_a_Box_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Panties_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Moneko_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Tricycle_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Ninja_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Zombie_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Samurai_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Sumo_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Boogie_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Skirt_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Valkyrie_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Bahamut_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Kerihime_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Princess_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Capsule_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Masked_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Bodhisattva_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Delinquent_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hip_Hop_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kotatsu_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nekoluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nerd_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Swimmer_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Pogo_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Wheel_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Apple_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Bath_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Salon_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ice_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Machine_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lesser_Demon_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Maiko_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Jurassic_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Viking_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Pirate_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Thief_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Bishop_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Fortune_Teller_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shaman_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Evangelist_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Type_10_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Witch_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Archer_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Marauder_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Swordsman_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Baby_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Bronze_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sushi_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Toy_Machine_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Sports_Day_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Swordsman_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cow_Princess_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/PPT48_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Gau_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Reaper_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sleeping_Beauty_Punt_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Salaryman_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sanada_Yukimura_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Maeda_Keiji_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Oda_Nobunaga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Reindeer_Fish_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Windy_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Thundia_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Droid_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Space_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Adult_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Evil_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Doll_Cats_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Blue_Shinobi_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Sodom_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Megidora_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Vars_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kamukura_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Raiden_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rope_Jump_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nimue_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Monkey_King_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Tank_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Axe_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Gross_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Cow_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Bird_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Fish_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Lizard_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Titan_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Maiden_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Clone_Elle_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Red_Marron_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cabaret_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Koi_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kuu_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kai_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Coppermine_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Bros_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Madam_Bride_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Celesse_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nono_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Olga_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Norn_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Yoichi_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Serum_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Fuu_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Aura_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rei_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Wyvern_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Healer_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Merc_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Vacation_Queen_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Bean_Cats_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Date_Masamune_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Takeda_Shingen_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Clockwork_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Flower_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Vengeful_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gold_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ururun_Wolf_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Neneko_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kung_Fu_Cat_X_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hikakin_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Urashima_Taro_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/The_Grateful_Crane_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Momotaro_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kasa_Jizo_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nekondo_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Squish_Ball_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Tutorial_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Nurse_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Base_Mini_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Gunslinger_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Stilts_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Tin_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rocker_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mer-Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Juliet_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Weightlifter_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Figure_Skating_Cats_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Toaster_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hoop_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Chicken_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Dragon_League_Swordsman_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nubobo_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Uesugi_Kenshin_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kalisa_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Yurinchi_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Princess_Punt_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ayanok%C5%8Dji_Sh%C5%8D_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Saotome_Hikaru_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Saionji_Hitomi_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Hoshi_Guranmanie_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Shiratori_Sh%C5%8Dchikubai_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Yankee_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Asiluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kubiluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Tecoluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Balaluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Nyandam_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Baby_Mola_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mola_King_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Meowla_Meowla_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Marshmallow_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Dioramos_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mob_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Takuya_%26_Yuki_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mystery_Girl_Yuki_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Yuki_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cuckoo_Crew_12_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Kart_R_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mr._Ninja_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Hearscht_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cornelia_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Juvens_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mystica_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Alois_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Citrouille_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Titi_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Yamaoka_Minori_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Nakamura_Kanae_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Akira_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mekako_Saionji_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Catman_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Psychocat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Onmyoji_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Surfer_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Drumcorps_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Baozi_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Kachi-Kachi_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Felyne_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Sheria_-_Kirin_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Rathalos_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Rathian_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Kirin_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Tank_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Axe_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/The_White_Rabbit_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Catburger_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/HYAKUTARO_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/MARCO_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/TARMA_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/ERI_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/FIO_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/SV-001_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/ALLEN_O%27NEIL_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/MARS_PEOPLE_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/HUGE_HERMIT_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/JUPITER_KING_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/DONALD_MORDEN_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/HI-DO_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Warlock_and_Pierre_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Pumpcat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gloomy_Neneko_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hallowindy_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Spooky_Thundia_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Oden_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Junior_God_of_Light_-_Valkyrie_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Junior_God_Brynhildr_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Junior_God_Suruzu_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Goddess_of_Abundance_-_Freya_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/God_of_War_-_Odin_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Freshman_Cat_Jobs_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rich_Cat_III_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sniper_the_Recruit_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Togeluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Frosty_Kai_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Santa_Kuu_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Holy_Coppermine_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/A_Gift_of_Cats_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Gross_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Cow_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Bird_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Undead_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/C%26D_Swordsman_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Horsemen_Cavalry_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ashura_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Battle_Balloon_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Dragon_Rider_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Pretty_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cyclops_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Golem_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Thunder_God_Zeus_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Anubis_the_Protector_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Radiant_Aphrodite_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Catway_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hayabusa_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nyamusu_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Pochi_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Kuromi_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Setsuko_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Nebaaru-kun_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Catornado_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Red_Riding_Mina_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Baby_Gao_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Yuki_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shining_Amaterasu_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Splendid_Ganesha_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cheerleader_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Tropical_Kalisa_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Midsummer_Rabbit_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sunny_Neneko_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Funghi_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Tanky_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/White_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Fortressy_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Futenyan_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Awa-Odori_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Pai-Pai_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Express_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Baozi_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Strike_Unit_R.E.I._(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Little_Leaguer_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Madoka_Kaname_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Homura_Akemi_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sayaka_Miki_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mami_Tomoe_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kyoko_Sakura_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kyubey_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Madoka_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Homura_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sayaka_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mami_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kyoko_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Madoka_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kyubey_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lilith_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Food_Stall_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Kat-A-Pult_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Drednot_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Bomburr_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Vaulter_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gardener_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Neko_Hakase_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Yuletide_Nurse_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Fish_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Lizard_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Titan_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/PIKOTARO_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Wrathful_Poseidon_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/CPAC_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Miko_Mitama_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Killer_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hiroshi_Mihara_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nazousagi_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Sarukani_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Miyamoku_Musashi_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Curling_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Welterweight_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mobius_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Belial_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Happy_100_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Eggy_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Springtime_Kenshin_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Bunny_%26_Canard_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Easter_Neneko_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shadow_Gao_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Trickster_Himeyuri_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sea_Maiden_Ruri_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Queen_Reika_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/HMS_Princess_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Imagawa_Yoshimoto_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Redhead_Yuki_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lost_World_Yuki_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Maneki_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Slug_Jockey_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Orthos_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Michelia_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Todomeki_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gudetama_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Gudetama_Plate_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gudegude_Pudding_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nisetama_Army_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Twinstars_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hermit_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Slave_Chocolate_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Seashore_Kai_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Rekon_Korps_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nora_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Wolfchild_Deale_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Graveflower_Verbena_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Bora_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mizli_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Aer_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Saber_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rin_Tohsaka_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Illyasviel_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Archer_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lancer_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rider_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gilgamesh_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Saber_the_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Sakura_the_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rin_the_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Illya_the_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Shirou_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Sakura_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Coin_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Rover_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Fencer_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Dark_Mitama_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Volley_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/D%27artanyan_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Farmer_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Masked_Yulala_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Satori_Hikami_%26_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Akio_Yabe_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sairi_Nijitani_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Misaki_Konno_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ren_Katagiri_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Karin_Nekozuka_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Aoi_Hayakawa_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mizuki_Tachibana_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hijiri_Rokudo_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Saki_Nijima_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Subaru_Hoshi_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Miyabi_Oyama_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ganglion_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sakura_Sonic_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Honeyto-Kun_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Mentori_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Imoto_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Voli_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shinji_%26_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gendo_%26_Fuyutsuki_Cats_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Giraffe_Unit-01_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kaworu_%26_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Rei_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Asuka_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mari_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rei_Ayanami_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Asuka_Langley_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mari_Illustrious_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Eva_Unit-00_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Eva_Unit-01_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Eva_Unit-02_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shinji_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Moon_Operators_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Thermae_D-Lux_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Crazed_Moneko_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Pokota_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ovis_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Coco_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Moe_Uzumasa_%26_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Saki_Matsuga_%26_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Misa_Ono_%26_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rei_Uzumasa_%26_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Mecha-Bun_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Clan_Heroes_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Souma_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Otaku_Geek_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gude-Cat_Machine_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Detective_Vigler_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Betakkuma_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nekokkuma_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/White_Swordsman_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Valkyrie_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nobiluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_God_the_Great_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Waverider_Kuu_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Empress_Chronos_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Bebe_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/D%27arktanyan_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lone_Cat_and_Kitten_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Driller_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Piledriver_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cutter_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Backhoe_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Miter_Saw_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Musashi_Miyamoto_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Headmistress_Jeanne_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/High_Lord_Babel_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ushiwakamaru_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Primordial_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kitarou_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Medama-Oyaji_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Wonder_MOMOCO_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sakura_Matou_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shirou_the_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Archer_the_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rider_the_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kotomine_%26_Gilgamesh_Cats_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Legeluga_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Filibuster_Cat_X_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Kristul_Muu_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Dogumaru_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Maji_Cat_%26_Cat_Tour_Group_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Black_Zeus_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Super_Zeus_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Holy_Phoenix_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Super_Devil_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Satanmaria_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Heracrist_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Fiendish_Nero_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Prince_Yamato_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rosary_Angel_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Wakamiko_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Devil_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Nekonosuke_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Lumina_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gummy_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Neko-Musume_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Doktor_Heaven_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Benevolent_Souma_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kano_%26_Souma_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Valkyrie_Dark_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Calette_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hina_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Eva_Unit-08_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/AAA_Wunder_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Misato_Katsuragi_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ritsuko_Akagi_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rei_Ayanami_(%3F%3F%3F)_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/HAPPI_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gaia_the_Creator_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Seabreeze_Coppermine_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Matador_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Narita_Kaihime_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shakurel_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Shakurel_Lion_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Shakurel_Tiger_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Shakurel_Panda_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Bros_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Myrcia_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/2D_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Fatherly_Cat_(Shopkeeper)_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Relentless_Gladios_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Eyewaltz_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mightycat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ryu_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Chun-Li_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Akuma_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ryu_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Chun-Li_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Guile_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Zangief_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Blanka_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Dhalsim_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ken_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Akuma_Giraffe_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lasvoss_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Good-Luck_Ebisu_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Medusa_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Nymph_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Wushu_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sorakara_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kintaro_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Snow_Angel_Twinstars_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Slime_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cossack_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kasli_the_Scourge_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Herme_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Teacher_BearCat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Urs_%26_Fenrir_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Sharpshooter_Saki_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hades_the_Punisher_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hatsune_Miku_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sakura_Miku_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kagamine_Rin_%26_Len_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Miku_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rugby_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/U.F.O._Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Yakisoba_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Boy_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Kasli_the_Bane_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kyosaka_Nanaho_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Phantom_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Papaluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Night_Oracle_Rei_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/The_4th_Angel_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/The_6th_Angel_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/The_10th_Angel_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/The_9th_Angel_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kaworu_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Bakery_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Master_Uril_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Shaman_Khan_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Holy_Knight_Alibaba_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Heavenly_Jack_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Gacha_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Hell_Warden_Emma_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Megurine_Luka_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/MEIKO_%26_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Luka_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Squirtgun_Saki_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Summerluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Suntan_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lifeguard_Cats_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Li%27l_Clops_Cat_Egg_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Idi:N_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Gravi_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Skull_Rider_Vars_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/E._Honda_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Balrog_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Vega_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sagat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/M._Bison_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/C._Honda_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Balrog_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Vega_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sagat_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/M._Bison_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Stone_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hatsune_Miku:_MM2020_Osaka_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hatsune_Miku:_MM2020_Tokyo_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Baby_Garu_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Emperor_Cat_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sweet_Aphrodite_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/First-Love_Myrcia_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Valentine%27s_Neneko_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Snow_Miku_2021_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kaito_%26_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Neko_Rin_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Neko_Len_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Aethur_Ltd._(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Blooming_Kamukura_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ranma_Saotome_(M)_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Akane_Tendo_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ryoga_Hibiki_(Pig)_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shampoo_(Cat)_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mousse_(Duck)_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Happosai_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ukyo_Kuonji_(GR)_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Tatewaki_Kuno_(Gi)_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ranma_Cat_(M)_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Akane_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Panda_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Adventurer_Kanna_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Wafer_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Dark_Aegis_Garu_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Gold_Brick_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Godzilla_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Princess_Cat_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Elder_Mask_Doron_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Kaguya_of_the_Coast_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kabuto_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Kuwagata_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Summoner_Satoru_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shiro_Amakusa_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lilin_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hevijak_the_Wicked_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Aku_Researcher_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Jagando_Jr._(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Pied_Piper_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kunio-kun_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Furiluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Giraffe_Modoki_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Catnip_Tricky_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Catnip_Dragon_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Brainwashed_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Yamii_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Deth-Troy-R_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Shitakiri_Sparrow_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/White_Knight_Cyclops_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Million-Dollar_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Brainwashed_Tank_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Xiaoqiong_%26_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Nana_%26_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Emilia_%26_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ann_%26_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Iz_the_Dancer_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lucifer_the_Fallen_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Superfeline_(Normal_Cat)', 'https://battle-cats.fandom.com/wiki/Sweet_Love_Mekako_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Brainwashed_Axe_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Firecracker_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Huntress_Terun_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lovestruck_Lesser_Demon_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hattori_Hanzo_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Secret_Crush_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Tomboy_Lion_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Chalkboard_Eraser_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Elder_Beast_Naala_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Brainwashed_Gross_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Bliza_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N001_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Iz_the_Dancer_of_Grief_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N101_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N102_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Sea_Serpent_Daliasan_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Chronos_the_Bride_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Brainwashed_Cow_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N103_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N104_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N201_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Night_Beach_Lilin_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Brainwashed_Bird_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Tengu_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N003_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N202_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Ranma_Saotome_(Leotard)_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Genma_Saotome_(Panda)_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Carrowsell_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N105_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N106_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Osamu_Mikumo_%26_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Yuma_Kuga_%26_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Chika_Amatori_%26_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Sakura_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Spectral_Goth_Vega_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Count_Yukimura_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Brainwashed_Fish_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N004_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Goddess_of_Light_Sirius_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Reindeer_Terun_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Brainwashed_Lizard_Cat_(Super_Rare_Cat)','https://battle-cats.fandom.com/wiki/Child_of_Destiny_Phono_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N000_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Issun_Boshi_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/White_Butler_Vigler_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Brainwashed_Titan_Cat_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Killer_Tank_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Class_Rep_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N107_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Thunder_Jack_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Rabbit_Satoru_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N005_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Kamen_Rider_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Cat_Godzilla_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Evangelion_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ultraman_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/King_of_Doom_Phono_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N108_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N109_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Jetpack_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/One-Eyed_Asuka_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Eva_Unit-13_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Betrothed_Balaluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Kaoluga_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N203_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Coastal_Explorer_Kanna_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Mighty_Sphinx_Korps_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N111_(Super_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N110_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Maize_Cat_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Tekachi_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N006_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/High_School_Kingpin_Riki_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Hatsune_Miku_XVI_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Lightmother_Aset_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N112_(Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Ninja_Girl_Tomoe_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Medal_King_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Sol_Dae_Rokker_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Master_of_Mind_Soractes_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Ancient_Egg:_N204_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Daybreaker_Izanagi_(Legend_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Pegasa_(Uber_Rare_Cat)', 'https://battle-cats.fandom.com/wiki/Principal_Cat_(Special_Cat)', 'https://battle-cats.fandom.com/wiki/Frozen_Rose_Cat_(Uber_Rare_Cat)']
# for i in cat_links:
#     cat_link = i.find("a")
#     if cat_link is not None:
#         cat_links_table.append("https://battle-cats.fandom.com"+cat_link.attrs.get("href"))
# print(cat_links_table)
atk_type_special = {"non.metal": ["Red", "Black", "Floating", "Angel", "Alien", "Zombie", "Aku", "Relic", "Traitless"], "all.enemies": ["Red", "Black", "Floating", "Metal", "Angel", "Alien", "Zombie", "Aku", "Relic", "Traitless"], "traited.enemies": ["Red", "Black", "Floating", "Metal", "Angel", "Alien", "Zombie", "Aku", "Relic"]}
atk_modes = ["Single Target", "Area Attack", "Omni Strike"]
conn, cur = connect_database(DATABASE_FILE)
for i in cat_links_table:
    try:
        url = i
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        talents = soup.find('div', {'class': 'mw-parser-output'})
        talents = talents.find_all('ul')
        talent_tree = []
        for i in talents:
            i = i.find_all('b')
            for x in i:
                if x.find('a', {'title': 'Special Abilities'}):
                    x = x.find('a', {'title': 'Special Abilities'})
                    talent_tree.append(x.text)
                if x.find('a', title=re.compile("Category:")):
                    x = x.find_all('a', title=re.compile("Category:"))
                    for v in x:
                        talent_tree.append(v.text)
        unit_name = soup.find('span', {'class': 'mw-page-title-main'}).contents[0]
        unit_name = unit_name.replace(")", "").split("(")
        unit_rarity = unit_name[len(unit_name)-1]
        unit_cost = soup.find("div", {'class': 'mw-parser-output'})
        unit_cost = unit_cost.find_all("li")
        unit_cost_table = []
        for i in unit_cost:
            txt = i.text
            x = re.search("^Chapter.2:.", txt)
            if x:
                x = re.split("^Chapter.2:.", txt)
                x = x[1].rstrip(x[1][-1])
                unit_cost_table.append(x.replace(",", ""))
        stats = soup.find('table', class_= 'stats-table')
        forms = soup.find_all("th", {'style': 'font-size: 16px; color: white; background-color: #FF6811;border: solid #000;border-width: 1px 0;'})
        form_names = []
        for form_num, i in enumerate(forms, 1):
            if "{" not in i.text and form_num < 4:
                form_names.append(i.text.replace("\n", ""))
        stats = stats.find_all('tr', class_='bg-light3')
        stats_table = []
        for i in stats:
            fail = False
            i = i.text.replace(",", "").split("\n")
            i = list(filter(None, i))
            for x in i:
                if x in atk_modes or "{" in x:
                    fail = True
                    break
                elif len(stats_table) >= 3:
                    fail = True
                    break
            if fail:
                continue
            hp = i[0].split()[0]
            atk = i[1].split()[0]
            atk_range = i[2]
            atk_time = i[3].split("f")[0]
            if atk_time == "-":
                atk_time = 0
            speed = i[4]
            knockbacks = i[5].split()[0]
            if '~' in i[7]:
                fastest_recharge = i[7].split("~")[1].split("seconds")[0].replace(" ", "")
            else:
                fastest_recharge = i[7].split("-")[1].split("seconds")[0].replace(" ", "")
            stats_table.append([len(stats_table)+1, hp, atk, atk_range, atk_time, speed, knockbacks, fastest_recharge])
        if soup.find('td', {'style': 'font-weight:bold;border-left:1px solid black;text-align:right;'}):
            experience = soup.find('td', {'style': 'font-weight:bold;border-left:1px solid black;text-align:right;'}).text.replace(",", "").split()[0]
        else:
            experience = 0
        atk_type = soup.find('table', class_= 'stats-table')

        ability_text = atk_type.find_all('tr', class_="bg-light3")
        abilities = atk_type.find_all('a')
        atk_type = atk_type.find('a').get("href")
        atk_type = atk_type.split("#")
        atk_type = atk_type[len(atk_type)-1].split("_")
        atk_type = " ".join(atk_type)
        form1 = [atk_type,]
        form2 = []
        form3 = []
        form_type1 = []
        form_type2 = []
        form_type3 = []
        current_form = form1
        current_form_type = form1
        trueform_table = []
        for i in range(1, len(abilities)):
            current_ability = abilities[i].get("href")
            if "#" in abilities[i].get("href"):
                current_ability = current_ability.split("#")
                current_ability = current_ability[len(current_ability)-1].split("_")
                current_ability = " ".join(current_ability)
            elif ":" in abilities[i].get("href"):
                current_ability = current_ability.split(":")
                current_ability = current_ability[len(current_ability)-1].split("_")[0]
            else:
                current_ability = current_ability.split("/")
                current_ability = current_ability[len(current_ability)-1].split("_")
                current_ability = " ".join(current_ability)
            if current_ability.capitalize() in enemy_types:
                if current_form == form1:
                    current_form_type = form_type1
                elif current_form == form2:
                    current_form_type = form_type2
                elif current_form == form3:
                    current_form_type = form_type3
                current_form_type.append(current_ability.capitalize())
            if current_ability in atk_modes:
                if current_form == form1:
                    current_form = form2
                elif current_form == form2:
                    current_form = form3
                else:
                    break
            current_form.append(current_ability.capitalize())
        if "Spirit" in form1:
            form1.remove("Spirit")
        if "Spirit" in form2:
            form2.remove("Spirit")
        if "Spirit" in form3:
            form3.remove("Spirit")
        if "Shield" in form1:
            form1.remove("Shield")
        if "Shield" in form2:
            form2.remove("Shield")
        if "Shield" in form3:
            form3.remove("Shield")
        type_forms = [duplicate_remover(form_type1), duplicate_remover(form_type2), duplicate_remover(form_type3)]
        count = 0
        for i in ability_text:
            ability = i.find("td", {'style': 'text-align: left;'})
            if ability:
                if "{" not in str(ability):
                    ability = ability.text.replace("\n", "").lower()
                    for x in atk_type_special:
                        if re.search(x, ability):
                            type_forms[count] = atk_type_special[x]
                    count += 1
                            
        if soup.find('tr', class_= 'evolve-materials'):
            trueform_ing = soup.find('tr', class_= 'evolve-materials')
            trueform_ing = trueform_ing.find_all('td', {'style': "padding: 0;"})
            trueform_table = []
            for i in trueform_ing:
                more_than_one = False
                ing_amount = i.find_all('span', class_="game-numbers")
                if i.a.img.attrs.get("data-image-name") != "Blank.png":
                    for ing in ing_amount:
                        if len(ing_amount) > 1 and more_than_one is False:
                            more_than_one = True
                            number_table = [i.a.img.attrs.get("data-image-name").split(".")[0], str(number_conversion(ing.attrs["style"].split(";")[3].split("-")[2].replace("px", "").replace(" ", ""))),]
                        elif len(ing_amount) > 1:
                            number_table[1] = number_table[1]+str(number_conversion(ing.attrs["style"].split(";")[3].split("-")[2].replace("px", "").replace(" ", "")))
                        else:
                            number_table = [i.a.img.attrs.get("data-image-name").split(".")[0], str(number_conversion(ing.attrs["style"].split(";")[3].split("-")[2].replace("px", "").replace(" ", ""))),]
                    trueform_table.append(number_table)
        #print({"Name": form_names, "Rarity": unit_rarity, "Cost": unit_cost_table[0], "HP": hp, "ATK": atk, "RANGE": atk_range, "ATK_TIME": atk_time, "SPEED": speed, "KNOCKBACKS": knockbacks, "RECHARGE": fastest_recharge, "EXP": experience, "FORM 1": form1, "FORM 2": form2, "FORM 3": form3})
        
        cur.execute("SELECT cat_id FROM battle_cat WHERE cat_first=?;", (form_names[0],))
        cat_id = cur.fetchone()[0]
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(url, e, exc_tb.tb_lineno)
print("All done")
conn.close()
    # Battle_Cat table code
    # if len(form_names) >= 3:
    #     cur.execute("INSERT INTO battle_cat (cat_first, cat_second, cat_trueform, cat_rarity_id, cat_experience) VALUES (?, ?, ?, ?, ?);", (form_names[0], form_names[1], form_names[2], int(rarity_allocate(unit_rarity)), int(experience)))
    # else:
    #     cur.execute("INSERT INTO battle_cat (cat_first, cat_second, cat_rarity_id, cat_experience) VALUES (?, ?, ?, ?);", (form_names[0], form_names[1], int(rarity_allocate(unit_rarity)), int(experience)))
    # conn.commit()

    # Battle_Bride table code
    # for i in stats_table:
    #     cur.execute("INSERT INTO battle_bridge VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (cat_id, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
    #     conn.commit()

    # Cat_Cost table code
    # for i in unit_cost_table:
    #     cur.execute("INSERT INTO cat_cost VALUES (?, ?);", (cat_id, i))
    #     conn.commit()

    # Skill_Bridge table code
    # form_table = [duplicate_remover(form1), duplicate_remover(form2), duplicate_remover(form3)]
    # for form_num, i in enumerate(form_table, 1):
    #     for type in enemy_types:
    #         if type in i:
    #             i.remove(type)
    #         for skill in i:
    #             if skill in skill_ban:
    #                 i.remove(skill)
    #     for skill in i:
    #         cur.execute("INSERT INTO skill_bridge VALUES (?, ?, ?);", (cat_id, form_num, skill_allocate(skill)))
    #         conn.commit()

    # Type bridge table code
    # for count, i in enumerate(type_forms):
        #     if type_forms[count]:
        #         type_forms[count] = list(map(type_allocate, i))
        #         for enemy_type in type_forms[count]:
        #             cur.execute("INSERT INTO type_bridge VALUES (?, ?, ?);", (cat_id, count+1, enemy_type))
    # conn.commit()

    # Trueform ingredients table code
    # if trueform_table:
        #     for form in trueform_table:
        #         cur.execute("SELECT ingredient_id FROM trueform_ingredient WHERE LOWER(REPLACE(ingredient_name, ' ', '')) = ?;", (form[0].lower().replace(" ", ""),))
        #         if form[0].lower() == "goldenseed":
        #             ingredient_id = 9
        #         else:
        #             ingredient_id = cur.fetchone()[0]
        #         cur.execute("INSERT INTO trueform_bridge VALUES (?, ?, ?);", (cat_id, ingredient_id, form[1]))
    
    # Talents table code
    # if talent_tree:
        #     for i in talent_tree:
        #         cur.execute("SELECT talent_id FROM cat_talenttree WHERE talent_name = ?;", (i,))
        #         talent_id = cur.fetchone()[0]
        #         cur.execute("INSERT INTO talent_bridge VALUES (?, ?);", (cat_id, talent_id))
        #     conn.commit()
        