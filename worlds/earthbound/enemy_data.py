from typing import Dict
from logging import warning
import struct


class EarthBoundEnemy:
    def __init__(self, name, address, hp, pp, exp, money, speed, offense, defense, level, is_scaled, shield=None):
        self.name = name
        self.address = address
        self.hp = hp
        self.pp = pp
        self.exp = exp
        self.money = money
        self.speed = speed
        self.offense = offense
        self.defense = defense
        self.level = level
        self.is_scaled = is_scaled
        self.shield = shield


def initialize_enemies(world):
    world.enemies = {
        "Insane Cultist": EarthBoundEnemy("Insane Cultist", 0x1595e7, 94, 0, 353, 33, 8, 19, 25, 13, False),
        "Dept. Store Spook": EarthBoundEnemy("Dept. Store Spook", 0x159645, 610, 290, 24291, 1648, 19, 82, 135, 42, False),
        "Armored Frog": EarthBoundEnemy("Armored Frog", 0x1596a3, 202, 0, 1566, 77, 7, 37, 108, 22, False),
        "Bad Buffalo": EarthBoundEnemy("Bad Buffalo", 0x159701, 341, 0, 4108, 172, 11, 64, 104, 34, False),
        "Black Antoid": EarthBoundEnemy("Black Antoid", 0x15975f, 34, 25, 37, 7, 4, 14, 13, 7, False),
        "Red Antoid": EarthBoundEnemy("Red Antoid", 0x1597bd, 112, 30, 1175, 35, 10, 29, 27, 20, False),
        "Ramblin' Evil Mushroom": EarthBoundEnemy("Ramblin' Evil Mushroom", 0x15981b, 60, 0, 95, 15, 5, 15, 10, 7, False),
        "Struttin' Evil Mushroom": EarthBoundEnemy("Struttin' Evil Mushroom", 0x159879, 157, 0, 1492, 95, 28, 29, 22, 17, False),
        "Mobile Sprout": EarthBoundEnemy("Mobile Sprout", 0x1598d7, 79, 9, 133, 13, 6, 17, 12, 10, False),
        "Tough Mobile Sprout": EarthBoundEnemy("Tough Mobile Sprout", 0x159935, 179, 13, 1865, 119, 18, 33, 27, 21, False),
        "Enraged Fire Plug": EarthBoundEnemy("Enraged Fire Plug", 0x159993, 309, 0, 4321, 346, 14, 60, 81, 32, False),
        "Mystical Record": EarthBoundEnemy("Mystical Record", 0x1599f1, 263, 35, 2736, 310, 20, 63, 78, 33, False),
        "Atomic Power Robot": EarthBoundEnemy("Atomic Power Robot", 0x159a4f, 594, 0, 26937, 730, 25, 119, 133, 56, False),
        "Nuclear Reactor Robot": EarthBoundEnemy("Nuclear Reactor Robot", 0x159aad, 798, 0, 53142, 820, 46, 142, 185, 64, False),
        "Guardian Hieroglyph": EarthBoundEnemy("Guardian Hieroglyph", 0x159b0b, 470, 126, 13064, 470, 20, 94, 106, 48, False),
        "Lethal Asp Hieroglyph": EarthBoundEnemy("Lethal Asp Hieroglyph", 0x159b69, 458, 0, 11321, 625, 21, 89, 94, 46, False),
        "Electro Swoosh": EarthBoundEnemy("Electro Swoosh", 0x159bc7, 543, 338, 17075, 791, 40, 140, 156, 62, False),
        "Conducting Menace": EarthBoundEnemy("Conducting Menace", 0x159c25, 445, 238, 14792, 574, 20, 107, 107, 52, False),
        "Conducting Spirit": EarthBoundEnemy("Conducting Spirit", 0x159c83, 587, 329, 30390, 804, 26, 130, 139, 59, False),
        "Evil Elemental": EarthBoundEnemy("Evil Elemental", 0x159ce1, 564, 0, 35737, 853, 30, 121, 136, 57, False),
        "Ness's Nightmare": EarthBoundEnemy("Ness's Nightmare", 0x159d3f, 1654, 882, 89004, 4442, 31, 172, 253, 71, False, "psi_1"),
        "Annoying Old Party Man": EarthBoundEnemy("Annoying Old Party Man", 0x159d9d, 99, 0, 130, 32, 6, 20, 25, 13, False),
        "Annoying Reveler": EarthBoundEnemy("Annoying Reveler", 0x159dfb, 288, 0, 2373, 268, 17, 58, 77, 31, False),
        "Unassuming Local Guy": EarthBoundEnemy("Unassuming Local Guy", 0x159e59, 73, 0, 146, 19, 5, 18, 13, 9, False),
        "New Age Retro Hippie": EarthBoundEnemy("New Age Retro Hippie", 0x159eb7, 87, 0, 160, 23, 5, 19, 14, 11, False),
        "Mr. Carpainter": EarthBoundEnemy("Mr. Carpainter", 0x159f15, 262, 70, 1412, 195, 8, 33, 45, 21, False),
        "Carbon Dog": EarthBoundEnemy("Carbon Dog", 0x159f73, 1672, 0, 0, 0, 31, 159, 174, 70, False),
        "Mighty Bear": EarthBoundEnemy("Mighty Bear", 0x159fd1, 167, 0, 609, 49, 7, 29, 31, 16, False),
        "Mighty Bear Seven": EarthBoundEnemy("Mighty Bear Seven", 0x15a02f, 367, 0, 8884, 440, 11, 85, 76, 42, False),
        "Putrid Moldyman": EarthBoundEnemy("Putrid Moldyman", 0x15a08d, 203, 0, 830, 53, 9, 36, 41, 21, False),
        "Thunder Mite": EarthBoundEnemy("Thunder Mite", 0x15a0eb, 293, 200, 10798, 430, 20, 85, 83, 43, False),
        "Cranky Lady": EarthBoundEnemy("Cranky Lady", 0x15a149, 95, 0, 200, 17, 6, 16, 18, 8, False),
        "Extra Cranky Lady": EarthBoundEnemy("Extra Cranky Lady", 0x15a1a7, 277, 0, 3651, 134, 17, 48, 70, 27, False),
        "Giygas (1)": EarthBoundEnemy("Giygas (1)", 0x15a205, 3600, 0, 0, 0, 52, 203, 300, 73, False),
        "Wetnosaur": EarthBoundEnemy("Wetnosaur", 0x15a263, 1030, 0, 33098, 745, 17, 126, 172, 59, False),
        "Chomposaur": EarthBoundEnemy("Chomposaur", 0x15a2c1, 1288, 320, 44378, 896, 17, 139, 183, 62, False, "phys_2"),
        "Titanic Ant": EarthBoundEnemy("Titanic Ant", 0x15a31f, 235, 102, 685, 150, 6, 19, 23, 13, False),
        "Gigantic Ant": EarthBoundEnemy("Gigantic Ant", 0x15a37d, 308, 81, 3980, 304, 17, 54, 112, 30, False),
        "Shrooom!": EarthBoundEnemy("Shrooom!", 0x15a3db, 1700, 112, 96323, 4086, 18, 95, 154, 48, False),
        "Plague Rat of Doom": EarthBoundEnemy("Plague Rat of Doom", 0x15a439, 1827, 60, 115272, 4464, 19, 71, 180, 47, False),
        "Mondo Mole": EarthBoundEnemy("Mondo Mole", 0x15a497, 498, 161, 5791, 400, 9, 37, 50, 23, False),
        "Guardian Digger": EarthBoundEnemy("Guardian Digger", 0x15a4f5, 386, 110, 17301, 1467, 17, 59, 129, 32, False, "phys_2"),
        "Scalding Coffee Cup": EarthBoundEnemy("Scalding Coffee Cup", 0x15a553, 190, 0, 2462, 280, 23, 55, 20, 30, False),
        "Loaded Dice": EarthBoundEnemy("Loaded Dice", 0x15a5b1, 307, 0, 10672, 703, 77, 146, 113, 59, False),
        "Slimy Little Pile": EarthBoundEnemy("Slimy Little Pile", 0x15a60f, 224, 0, 1978, 124, 15, 42, 61, 24, False),
        "Even Slimier Little Pile": EarthBoundEnemy("Even Slimier Little Pile", 0x15a66d, 326, 0, 15075, 579, 22, 103, 101, 49, False),
        "Arachnid!": EarthBoundEnemy("Arachnid!", 0x15a6cb, 216, 0, 4933, 296, 23, 61, 30, 32, False),
        "Arachnid!!!": EarthBoundEnemy("Arachnid!!!", 0x15a729, 344, 0, 10449, 412, 20, 87, 86, 45, False),
        "Kraken": EarthBoundEnemy("Kraken", 0x15a787, 1097, 176, 79267, 3049, 21, 105, 166, 54, False),
        "Bionic Kraken": EarthBoundEnemy("Bionic Kraken", 0x15a7e5, 900, 60, 50308, 960, 42, 155, 195, 70, False),
        "Spinning Robo": EarthBoundEnemy("Spinning Robo", 0x15a843, 113, 17, 297, 21, 7, 21, 22, 14, False),
        "Whirling Robo": EarthBoundEnemy("Whirling Robo", 0x15a8a1, 374, 36, 5782, 256, 18, 78, 90, 39, False),
        "Hyper Spinning Robo": EarthBoundEnemy("Hyper Spinning Robo", 0x15a8ff, 553, 83, 28866, 756, 28, 122, 130, 56, False),
        "Cop": EarthBoundEnemy("Cop", 0x15a95d, 75, 0, 86, 18, 5, 15, 18, 7, False),
        "Coil Snake": EarthBoundEnemy("Coil Snake", 0x15a9bb, 18, 0, 1, 4, 2, 3, 4, 1, False),
        "Thirsty Coil Snake": EarthBoundEnemy("Thirsty Coil Snake", 0x15aa19, 270, 0, 2786, 276, 18, 52, 80, 28, False),
        "Mr. Batty": EarthBoundEnemy("Mr. Batty", 0x15aa77, 86, 0, 304, 30, 29, 25, 5, 15, False),
        "Elder Batty": EarthBoundEnemy("Elder Batty", 0x15aad5, 294, 0, 4177, 371, 33, 66, 72, 35, False),
        "Violent Roach": EarthBoundEnemy("Violent Roach", 0x15ab33, 209, 0, 1757, 80, 35, 30, 26, 18, False),
        "Filthy Attack Roach": EarthBoundEnemy("Filthy Attack Roach", 0x15ab91, 399, 0, 10543, 432, 77, 84, 33, 42, False),
        "Crazed Sign": EarthBoundEnemy("Crazed Sign", 0x15abef, 295, 98, 3618, 244, 17, 64, 96, 34, False),
        "Wooly Shambler": EarthBoundEnemy("Wooly Shambler", 0x15ac4d, 391, 140, 5397, 458, 18, 81, 91, 40, False),
        "Wild 'n Wooly Shambler": EarthBoundEnemy("Wild 'n Wooly Shambler", 0x15acab, 722, 212, 33818, 906, 38, 144, 171, 65, False),
        "Skate Punk": EarthBoundEnemy("Skate Punk", 0x15ad09, 31, 0, 12, 17, 5, 7, 8, 3, False),
        "Skelpion": EarthBoundEnemy("Skelpion", 0x15ad67, 137, 21, 1823, 140, 37, 41, 23, 24, False),
        "Dread Skelpion": EarthBoundEnemy("Dread Skelpion", 0x15adc5, 214, 125, 9908, 609, 40, 82, 57, 41, False),
        "Starman": EarthBoundEnemy("Starman", 0x15ae23, 545, 155, 23396, 720, 24, 103, 126, 55, False),
        "Starman Super": EarthBoundEnemy("Starman Super", 0x15ae81, 568, 310, 30145, 735, 24, 112, 129, 56, False, "psi_2"),
        "Ghost of Starman": EarthBoundEnemy("Ghost of Starman", 0x15aedf, 750, 462, 48695, 807, 46, 152, 170, 68, False),
        "Smilin' Sphere": EarthBoundEnemy("Smilin' Sphere", 0x15af3d, 233, 60, 2218, 191, 17, 50, 65, 27, False),
        "Uncontrollable Sphere": EarthBoundEnemy("Uncontrollable Sphere", 0x15af9b, 577, 180, 20389, 796, 27, 116, 134, 56, False, "psi_1"),
        "Petrified Royal Guard": EarthBoundEnemy("Petrified Royal Guard", 0x15aff9, 573, 0, 19163, 628, 12, 106, 173, 53, False),
        "Guardian General": EarthBoundEnemy("Guardian General", 0x15b057, 831, 6, 95390, 3235, 21, 109, 214, 55, False),
        "Starman Deluxe": EarthBoundEnemy("Starman Deluxe", 0x15b0b5, 1400, 418, 160524, 3827, 27, 143, 186, 65, False, "psi_2"),
        "Final Starman": EarthBoundEnemy("Final Starman", 0x15b113, 840, 860, 61929, 915, 47, 178, 187, 71, False, "psi_2"),
        "Urban Zombie": EarthBoundEnemy("Urban Zombie", 0x15b171, 171, 0, 700, 58, 10, 31, 24, 19, False),
        "Zombie Possessor": EarthBoundEnemy("Zombie Possessor", 0x15b1cf, 176, 0, 950, 81, 30, 28, 19, 17, False),
        "Zombie Dog": EarthBoundEnemy("Zombie Dog", 0x15b22d, 210, 0, 1354, 54, 30, 39, 51, 22, False),
        "Crooked Cop": EarthBoundEnemy("Crooked Cop", 0x15b28b, 140, 0, 492, 159, 15, 20, 24, 13, False),
        "Over Zealous Cop": EarthBoundEnemy("Over Zealous Cop", 0x15b2e9, 325, 0, 7448, 420, 18, 69, 75, 36, False),
        "Territorial Oak": EarthBoundEnemy("Territorial Oak", 0x15b347, 145, 41, 356, 29, 5, 26, 30, 15, False),
        "Hostile Elder Oak": EarthBoundEnemy("Hostile Elder Oak", 0x15b3a5, 609, 76, 17567, 690, 14, 134, 146, 59, False),
        "Diamond Dog": EarthBoundEnemy("Diamond Dog", 0x15b403, 3344, 154, 337738, 6968, 31, 167, 230, 70, False, "phys_2"),
        "Marauder Octobot": EarthBoundEnemy("Marauder Octobot", 0x15b461, 482, 0, 14475, 499, 23, 99, 121, 49, False),
        "Military Octobot": EarthBoundEnemy("Military Octobot", 0x15b4bf, 604, 0, 25607, 637, 26, 138, 147, 61, False),
        "Mechanical Octobot": EarthBoundEnemy("Mechanical Octobot", 0x15b51d, 768, 0, 41738, 744, 43, 147, 176, 66, False),
        "Ultimate Octobot": EarthBoundEnemy("Ultimate Octobot", 0x15b57b, 792, 0, 47876, 815, 44, 163, 181, 70, False),
        "Mad Duck": EarthBoundEnemy("Mad Duck", 0x15b5d9, 51, 0, 41, 12, 30, 12, 24, 8, False),
        "Dali's Clock": EarthBoundEnemy("Dali's Clock", 0x15b637, 296, 0, 2503, 314, 4, 65, 66, 34, False),
        "Trillionage Sprout": EarthBoundEnemy("Trillionage Sprout", 0x15b695, 1048, 240, 30303, 1358, 16, 54, 88, 29, False),
        "Musica": EarthBoundEnemy("Musica", 0x15b6f3, 292, 0, 3748, 341, 21, 69, 85, 35, False),
        "Desert Wolf": EarthBoundEnemy("Desert Wolf", 0x15b751, 247, 0, 3740, 114, 33, 57, 67, 30, False),
        "Master Belch": EarthBoundEnemy("Master Belch", 0x15b7af, 650, 0, 12509, 664, 16, 50, 88, 27, False), #Real one
        "Big Pile of Puke": EarthBoundEnemy("Big Pile of Puke", 0x15b80d, 631, 0, 19659, 728, 16, 120, 158, 57, False),
        "Master Barf": EarthBoundEnemy("Master Barf", 0x15b86b, 1319, 0, 125056, 3536, 24, 136, 177, 60, False),
        "Kiss of Death": EarthBoundEnemy("Kiss of Death", 0x15b8c9, 333, 0, 10354, 528, 19, 91, 100, 46, False),
        "French Kiss of Death": EarthBoundEnemy("French Kiss of Death", 0x15b927, 588, 0, 19210, 879, 30, 160, 160, 70, False),
        "Foppy": EarthBoundEnemy("Foppy", 0x15b985, 120, 10, 1311, 93, 1, 29, 9, 16, False),
        "Fobby": EarthBoundEnemy("Fobby", 0x15b9e3, 240, 19, 18348, 620, 5, 98, 84, 48, False),
        "Zap Eel": EarthBoundEnemy("Zap Eel", 0x15ba41, 370, 0, 12170, 611, 29, 97, 93, 48, False),
        "Tangoo": EarthBoundEnemy("Tangoo", 0x15ba9f, 371, 5, 14718, 572, 19, 96, 99, 48, False),
        "Boogey Tent": EarthBoundEnemy("Boogey Tent", 0x15bafd, 579, 56, 5500, 407, 10, 43, 69, 25, False),
        "Squatter Demon": EarthBoundEnemy("Squatter Demon", 0x15bb5b, 774, 60, 48311, 897, 45, 158, 192, 69, False),
        "Crested Booka": EarthBoundEnemy("Crested Booka", 0x15bbb9, 265, 0, 3011, 130, 17, 53, 73, 28, False),
        "Great Crested Booka": EarthBoundEnemy("Great Crested Booka", 0x15bc17, 452, 0, 16365, 604, 20, 100, 110, 49, False),
        "Lesser Mook": EarthBoundEnemy("Lesser Mook", 0x15bc75, 401, 190, 7640, 467, 17, 76, 102, 39, False),
        "Mook Senior": EarthBoundEnemy("Mook Senior", 0x15bcd3, 501, 700, 21056, 715, 25, 108, 122, 54, False),
        "Smelly Ghost": EarthBoundEnemy("Smelly Ghost", 0x15bd31, 194, 50, 606, 71, 10, 35, 89, 21, False),
        "Stinky Ghost": EarthBoundEnemy("Stinky Ghost", 0x15bd8f, 444, 0, 13179, 541, 18, 90, 179, 46, False),
        "Everdred": EarthBoundEnemy("Everdred", 0x15bded, 182, 0, 986, 171, 6, 25, 35, 15, False),
        "Attack Slug": EarthBoundEnemy("Attack Slug", 0x15be4b, 30, 6, 27, 6, 1, 9, 2, 5, False),
        "Pit Bull Slug": EarthBoundEnemy("Pit Bull Slug", 0x15bea9, 217, 11, 9994, 543, 2, 79, 77, 39, False),
        "Rowdy Mouse": EarthBoundEnemy("Rowdy Mouse", 0x15bf07, 36, 0, 34, 9, 5, 7, 20, 6, False),
        "Deadly Mouse": EarthBoundEnemy("Deadly Mouse", 0x15bf65, 416, 0, 9225, 406, 18, 63, 98, 38, False),
        "Care Free Bomb": EarthBoundEnemy("Care Free Bomb", 0x15bfc3, 504, 0, 14941, 641, 31, 135, 215, 60, False),
        "Electro Specter": EarthBoundEnemy("Electro Specter", 0x15c021, 3092, 80, 261637, 6564, 29, 148, 203, 67, False, "psi_2"),
        "Handsome Tom": EarthBoundEnemy("Handsome Tom", 0x15c07f, 133, 16, 520, 45, 11, 27, 25, 16, False),
        "Smilin' Sam": EarthBoundEnemy("Smilin' Sam", 0x15c0dd, 161, 55, 712, 48, 17, 34, 44, 20, False),
        "Manly Fish": EarthBoundEnemy("Manly Fish", 0x15c13b, 500, 0, 15826, 624, 22, 83, 114, 42, False),
        "Manly Fish's Brother": EarthBoundEnemy("Manly Fish's Brother", 0x15c199, 526, 210, 15970, 686, 24, 114, 123, 56, False),
        "Runaway Dog": EarthBoundEnemy("Runaway Dog", 0x15c1f7, 21, 0, 4, 3, 26, 4, 5, 2, False),
        "Trick or Trick Kid": EarthBoundEnemy("Trick or Trick Kid", 0x15c255, 142, 0, 570, 47, 7, 30, 37, 18, False),
        "Cave Boy": EarthBoundEnemy("Cave Boy", 0x15c2b3, 314, 0, 618, 17, 79, 21, 33, 14, False),
        "Abstract Art": EarthBoundEnemy("Abstract Art", 0x15c311, 301, 60, 4361, 255, 19, 67, 79, 35, False),
        "Shattered Man": EarthBoundEnemy("Shattered Man", 0x15c36f, 694, 0, 44690, 2630, 18, 104, 138, 51, False),
        "Fierce Shattered Man": EarthBoundEnemy("Fierce Shattered Man", 0x15c3cd, 516, 0, 17423, 577, 12, 101, 116, 50, False),
        "Ego Orb": EarthBoundEnemy("Ego Orb", 0x15c42b, 592, 0, 24180, 836, 17, 125, 140, 58, False),
        "Thunder and Storm": EarthBoundEnemy("Thunder and Storm", 0x15c489, 2065, 70, 129026, 4736, 21, 111, 178, 56, False),
        "Yes Man Junior": EarthBoundEnemy("Yes Man Junior", 0x15c4e7, 33, 0, 13, 18, 4, 8, 9, 4, False),
        "Frankystein Mark II": EarthBoundEnemy("Frankystein Mark II", 0x15c545, 91, 0, 76, 31, 4, 15, 18, 7, False),
        "Frank": EarthBoundEnemy("Frank", 0x15c5a3, 63, 0, 50, 48, 7, 12, 17, 6, False),
        "Cute Li'l UFO": EarthBoundEnemy("Cute Li'l UFO", 0x15c601, 162, 25, 1519, 110, 58, 49, 32, 27, False),
        "Beautiful UFO": EarthBoundEnemy("Beautiful UFO", 0x15c65f, 339, 15, 8257, 426, 59, 86, 87, 44, False),
        "Pogo Punk": EarthBoundEnemy("Pogo Punk", 0x15c6bd, 35, 0, 15, 18, 3, 8, 10, 4, False),
        "Tough Guy": EarthBoundEnemy("Tough Guy", 0x15c71b, 342, 0, 9310, 525, 18, 72, 92, 37, False),
        "Mad Taxi": EarthBoundEnemy("Mad Taxi", 0x15c779, 253, 0, 2336, 216, 38, 53, 68, 28, False),
        "Evil Mani-Mani": EarthBoundEnemy("Evil Mani-Mani", 0x15c7d7, 860, 88, 28139, 1852, 15, 86, 145, 45, False),
        "Mr. Molecule": EarthBoundEnemy("Mr. Molecule", 0x15c835, 280, 21, 8708, 659, 18, 118, 97, 56, False),
        "Worthless Protoplasm": EarthBoundEnemy("Worthless Protoplasm", 0x15c893, 38, 0, 17, 11, 27, 11, 21, 7, False),
        "Sentry Robot": EarthBoundEnemy("Sentry Robot", 0x15c8f1, 372, 0, 5034, 392, 17, 77, 105, 39, False),
        #"Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15c94f, 1746, 999, 0, 0, 51, 150, 274, 72, False),
        "Psychic Psycho": EarthBoundEnemy("Psychic Psycho", 0x15c9ad, 591, 252, 30094, 682, 30, 124, 144, 58, False),
        "Major Psychic Psycho": EarthBoundEnemy("Major Psychic Psycho", 0x15ca0b, 618, 574, 39247, 862, 31, 145, 152, 65, False),
        "Mole Playing Rough": EarthBoundEnemy("Mole Playing Rough", 0x15ca69, 103, 0, 456, 36, 9, 22, 28, 14, False),
        "Gruff Goat": EarthBoundEnemy("Gruff Goat", 0x15cac7, 45, 0, 20, 9, 12, 8, 23, 7, False),
        "Clumsy Robot": EarthBoundEnemy("Clumsy Robot", 0x15cb25, 962, 0, 32378, 2081, 83, 88, 137, 46, False, "psi_1"),
        "Soul Consuming Flame": EarthBoundEnemy("Soul Consuming Flame", 0x15cb83, 602, 0, 37618, 768, 30, 131, 262, 59, False),
        "Demonic Petunia": EarthBoundEnemy("Demonic Petunia", 0x15cbe1, 478, 0, 15171, 724, 26, 102, 111, 50, False),
        "Ranboob": EarthBoundEnemy("Ranboob", 0x15cc3f, 232, 42, 2486, 158, 20, 41, 63, 24, False),
        "Li'l UFO": EarthBoundEnemy("Li'l UFO", 0x15cc9d, 82, 0, 223, 14, 53, 18, 17, 12, False),
        "High-class UFO": EarthBoundEnemy("High-class UFO", 0x15ccfb, 433, 72, 12385, 456, 60, 93, 103, 47, False, "phys_1"),
        "Noose Man": EarthBoundEnemy("Noose Man", 0x15cd59, 231, 0, 1990, 220, 18, 47, 52, 26, False),
        "Robo-pump": EarthBoundEnemy("Robo-pump", 0x15cdb7, 431, 0, 4797, 349, 19, 70, 113, 36, False),
        "Plain Crocodile": EarthBoundEnemy("Plain Crocodile", 0x15ce15, 234, 0, 1928, 62, 10, 40, 55, 24, False),
        "Strong Crocodile": EarthBoundEnemy("Strong Crocodile", 0x15ce73, 417, 0, 10122, 495, 17, 85, 131, 43, False),
        "Hard Crocodile": EarthBoundEnemy("Hard Crocodile", 0x15ced1, 522, 0, 19484, 692, 23, 110, 128, 55, False),
        "No Good Fly": EarthBoundEnemy("No Good Fly", 0x15cf2f, 100, 0, 415, 26, 10, 23, 13, 15, False),
        "Mostly Bad Fly": EarthBoundEnemy("Mostly Bad Fly", 0x15cf8d, 141, 0, 1116, 84, 15, 32, 16, 19, False),
        "Spiteful Crow": EarthBoundEnemy("Spiteful Crow", 0x15cfeb, 24, 0, 3, 5, 77, 5, 3, 3, False),
        #"Master Belch": EarthBoundEnemy("Master Belch", 0x15d397, 650, 0, 12509, 664, 16, 50, 88, 27, False), Unused
        #"Insane Cultist (2)": EarthBoundEnemy("Insane Cultist", 0x15d3f5, 94, 0, 353, 33, 8, 19, 25, 13, False),
        "Dept. Store Spook (2)": EarthBoundEnemy("Dept. Store Spook (2)", 0x15d453, 610, 290, 24291, 1648, 19, 82, 135, 42, False),
        "Ness's Nightmare (2)": EarthBoundEnemy("Ness's Nightmare (2)", 0x15d4b1, 1654, 882, 89004, 4442, 31, 172, 253, 71, False),
        "Mr. Carpainter (2)": EarthBoundEnemy("Mr. Carpainter (2)", 0x15d50f, 262, 70, 1412, 195, 8, 33, 45, 21, False),
        "Carbon Dog (2)": EarthBoundEnemy("Carbon Dog (2)", 0x15d56d, 1672, 0, 0, 0, 31, 159, 174, 70, False),
        "Chomposaur (2)": EarthBoundEnemy("Chomposaur (2)", 0x15d5cb, 1288, 320, 44378, 896, 17, 139, 183, 62, False),
        "Titanic Ant (2)": EarthBoundEnemy("Titanic Ant (2)", 0x15d629, 235, 102, 685, 150, 6, 19, 23, 13, False),
        "Gigantic Ant (2)": EarthBoundEnemy("Gigantic Ant (2)", 0x15d687, 308, 81, 3980, 304, 17, 54, 112, 30, False),
        "Shrooom! (2)": EarthBoundEnemy("Shrooom! (2)", 0x15d6e5, 1700, 112, 96323, 4086, 18, 95, 154, 48, False),
        "Plague Rat of Doom (2)": EarthBoundEnemy("Plague Rat of Doom (2)", 0x15d743, 1827, 60, 115272, 4464, 19, 71, 180, 47, False),
        "Mondo Mole (2)": EarthBoundEnemy("Mondo Mole (2)", 0x15d7a1, 498, 161, 5791, 400, 9, 37, 50, 23, False),
        "Guardian Digger (2)": EarthBoundEnemy("Guardian Digger (2)", 0x15d7ff, 386, 110, 17301, 1467, 17, 59, 129, 32, False),
        "Kraken (2)": EarthBoundEnemy("Kraken (2)", 0x15d85d, 1097, 176, 79267, 3049, 21, 105, 166, 54, False),
        #"Bionic Kraken (2)": EarthBoundEnemy("Bionic Kraken", 0x15d8bb, 900, 60, 50308, 960, 42, 155, 195, 70, False),
        "Starman (2)": EarthBoundEnemy("Starman (2)", 0x15d919, 545, 155, 23396, 720, 24, 103, 126, 55, False),
        "Starman Super (2)": EarthBoundEnemy("Starman Super (2)", 0x15d977, 568, 310, 30145, 735, 24, 112, 129, 56, False),
        "Ghost of Starman (2)": EarthBoundEnemy("Ghost of Starman (2)", 0x15d9d5, 750, 462, 48695, 807, 46, 152, 170, 68, False),
        "Starman Deluxe (2)": EarthBoundEnemy("Starman Deluxe (2)", 0x15da33, 1400, 418, 160524, 3827, 27, 143, 186, 65, False),
        "Final Starman (2)": EarthBoundEnemy("Final Starman (2)", 0x15da91, 840, 860, 61929, 915, 47, 178, 187, 71, False),
        #"Urban Zombie": EarthBoundEnemy("Urban Zombie", 0x15daef, 171, 0, 700, 58, 10, 31, 24, 19, False),
        "Diamond Dog (2)": EarthBoundEnemy("Diamond Dog (2)", 0x15db4d, 3344, 154, 337738, 6968, 31, 167, 230, 70, False),
        "Trillionage Sprout (2)": EarthBoundEnemy("Trillionage Sprout (2)", 0x15dbab, 1048, 240, 30303, 1358, 16, 54, 88, 29, False),
        "Master Belch (2)": EarthBoundEnemy("Master Belch (2)", 0x15dc09, 650, 0, 12509, 664, 16, 50, 88, 27, False),
        #"Big Pile of Puke": EarthBoundEnemy("Big Pile of Puke", 0x15dc67, 609, 76, 17567, 690, 14, 134, 146, 59, False),
        "Master Barf (2)": EarthBoundEnemy("Master Barf (2)", 0x15dcc5, 1319, 0, 125056, 3536, 24, 136, 177, 60, False),
        "Loaded Dice (2)": EarthBoundEnemy("Loaded Dice (2)", 0x15dd23, 307, 0, 10672, 703, 77, 146, 113, 59, False),
        #"Tangoo": EarthBoundEnemy("Tangoo", 0x15dd81, 371, 5, 14718, 572, 19, 96, 99, 48, False),
        "Boogey Tent (2)": EarthBoundEnemy("Boogey Tent (2)", 0x15dddf, 579, 56, 5500, 407, 10, 43, 69, 25, False),
        #"Squatter Demon": EarthBoundEnemy("Squatter Demon", 0x15de3d, 774, 60, 48311, 897, 45, 158, 192, 69, False),
        "Everdred (2)": EarthBoundEnemy("Everdred (2)", 0x15de9b, 182, 0, 986, 171, 6, 25, 35, 15, False),
        "Electro Specter (2)": EarthBoundEnemy("Electro Specter (2)", 0x15def9, 3092, 80, 261637, 6564, 29, 148, 203, 67, False),
        "Thunder and Storm (2)": EarthBoundEnemy("Thunder and Storm (2)", 0x15df57, 2065, 70, 129026, 4736, 21, 111, 178, 56, False),
        "Frankystein Mark II (2)": EarthBoundEnemy("Frankystein Mark II (2)", 0x15dfb5, 91, 0, 76, 31, 4, 15, 18, 7, False),
        "Evil Mani-Mani (2)": EarthBoundEnemy("Evil Mani-Mani (2)", 0x15e013, 860, 88, 28139, 1852, 15, 86, 145, 45, False),
        #"Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15e071, 1746, 999, 0, 0, 51, 150, 274, 72, False),
        "Clumsy Robot (2)": EarthBoundEnemy("Clumsy Robot (2)", 0x15e0cf, 962, 0, 32378, 2081, 83, 88, 137, 46, False),
        "Robo-pump (2)": EarthBoundEnemy("Robo-pump (2)", 0x15e12d, 431, 0, 4797, 349, 19, 70, 113, 36, False),
        #"Foppy": EarthBoundEnemy("Foppy", 0x15e18b, 120, 10, 1311, 93, 1, 29, 9, 16, False),
        "Guardian General (2)": EarthBoundEnemy("Guardian General (2)", 0x15e1e9, 831, 6, 95390, 3235, 21, 109, 214, 55, False),
        "Black Antoid (2)": EarthBoundEnemy("Black Antoid (2)", 0x15e247, 34, 25, 37, 7, 4, 14, 13, 7, False), #Separate enemy used in the titanic ant fight
        "Struttin' Evil Mushroom (2)": EarthBoundEnemy("Struttin' Evil Mushroom (2)", 0x15e2a5, 60, 0, 95, 15, 5, 15, 10, 7, False),
        #"Runaway Dog (2)": EarthBoundEnemy("Runaway Dog", 0x15e303, 21, 0, 4, 3, 26, 4, 5, 73, False),
        "Cave Boy (2)": EarthBoundEnemy("Cave Boy (2)", 0x15e361, 314, 0, 618, 17, 5, 21, 33, 11, False),
        "Tiny Li'l Ghost": EarthBoundEnemy("Tiny Li'l Ghost", 0x15e3bf, 90, 0, 1, 162, 100, 19, 7, 18, False),
        "Starman Junior": EarthBoundEnemy("Starman Junior", 0x15e41d, 200, 999, 16, 20, 1, 11, 10, 6, False),
        "Buzz Buzz": EarthBoundEnemy("Buzz Buzz", 0x15e47b, 2000, 999, 0, 0, 100, 40, 92, 20, False),
        "Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15e4d9, 2000, 999, 0, 0, 60, 145, 255, 80, False),
        #"Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15e537, 1746, 999, 0, 0, 51, 150, 274, 72, False), Cutscene?
        "Giygas (2)": EarthBoundEnemy("Giygas (2)", 0x15e595, 9999, 999, 0, 0, 80, 255, 255, 80, False),
        "Giygas (3)": EarthBoundEnemy("Giygas (3)", 0x15e5f3, 9999, 0, 0, 0, 80, 255, 255, 80, False),
        "Giygas (4)": EarthBoundEnemy("Giygas (4)", 0x15e651, 2000, 0, 0, 0, 80, 255, 255, 80, False),
        "Giygas (5)": EarthBoundEnemy("Giygas (5)", 0x15e6af, 9999, 0, 0, 0, 80, 255, 255, 80, False),
        "Farm Zombie": EarthBoundEnemy("Farm Zombie", 0x15e70d, 171, 0, 700, 58, 10, 31, 24, 19, False),
        "Criminal Caterpillar": EarthBoundEnemy("Criminal Caterpillar", 0x15e76b, 250, 168, 30384, 0, 134, 37, 16, 23, False),
        "Evil Eye": EarthBoundEnemy("Evil Eye", 0x15e7c9, 720, 400, 46376, 896, 38, 141, 162, 63, False),
        #"Magic Butterfly": EarthBoundEnemy("Magic Butterfly", 0x15e827, 16, 0, 1, 0, 25, 2, 2, 0, False),
        "Mini Barf": EarthBoundEnemy("Mini Barf", 0x15e885, 616, 0, 7521, 460, 10, 45, 71, 26, False),
        "Master Criminal Worm": EarthBoundEnemy("Master Criminal Worm", 0x15e8e3, 377, 300, 82570, 0, 136, 73, 40, 37, False),
        "Captain Strong": EarthBoundEnemy("Captain Strong", 0x15e941, 140, 0, 492, 159, 15, 20, 24, 13, False),
        "Giygas (6)": EarthBoundEnemy("Giygas (6)", 0x15e99f, 9999, 0, 0, 0, 80, 255, 127, 80, False),
        "Clumsy Robot (3)": EarthBoundEnemy("Clumsy Robot (3)", 0x15e9fd, 962, 0, 32378, 2081, 83, 88, 137, 46, False),
    }
    
    boss_data = {
        "Frank": [0xC0, 0x01, 0x2EC684],
        "Frankystein Mark II": [0xC1, 0x01, 0x2EC68A],
        "Titanic Ant": [0xC2, 0x01, 0x2EC69E],
        "Captain Strong": [0xC4, 0x01],
        "Everdred": [0xC5, 0x01],
        "Mr. Carpainter": [0xC6, 0x01],
        "Mondo Mole": [0xC7, 0x01],
        "Master Belch": [0xC8, 0x01],
        "Trillionage Sprout": [0xC9, 0x01],
        "Boogey Tent": [0xCA, 0x01],
        "Guardian Digger": [0xCB, 0x01],
        "Dept. Store Spook": [0xCC, 0x01],
        "Evil Mani-Mani": [0xCD, 0x01],
        "Clumsy Robot": [0xCE, 0x01],
        "Plague Rat of Doom": [0xCF, 0x01],
        "Thunder and Storm": [0xD0, 0x01],
        "Shrooom!": [0xD1, 0x01],
        "Starman Deluxe": [0xD2, 0x01],
        "Kraken": [0xD3, 0x01],
        "Guardian General": [0xD4, 0x01],
        "Master Barf": [0xD5, 0x01],
        "Electro Specter": [0xD6, 0x01],
        "Carbon Dog": [0xD7, 0x01],
        "Ness's Nightmare": [0xD8, 0x01],
        "Starman Junior": [0xDA, 0x01],
        "Mini Barf": [0xE2, 0x01],
        "Heavily Armed Pokey": [0x07, 0x00],
    }

    boss_sprites = {
        "Frank": [0x99, 0x00],
        "Frankystein Mark II": [0x91, 0x01],
        "Titanic Ant": [0x39, 0x01],
        "Captain Strong": [0x4B, 0x00],
        "Everdred": [0x9D, 0x00],
        "Mr. Carpainter": [0x9F, 0x00],
        "Mondo Mole": [0x9F, 0x01],
        "Master Belch": [0x48, 0x01],
        "Trillionage Sprout": [0x3D, 0x01],
        "Boogey Tent": [0x10, 0x01],
        "Guardian Digger": [0xA3, 0x01],
        "Dept. Store Spook": [0xC7, 0x01],
        "Evil Mani-Mani": [0x25, 0x01],
        "Clumsy Robot": [0xA2, 0x01],
        "Plague Rat of Doom": [0xA0, 0x01],
        "Thunder and Storm": [0x44, 0x01],
        "Shrooom!": [0x23, 0x01],
        "Starman Deluxe": [0x2F, 0x01],
        "Kraken": [0x27, 0x01],
        "Guardian General": [0x42, 0x01],
        "Master Barf": [0x2B, 0x01],
        "Electro Specter": [0xA5, 0x01],
        "Carbon Dog": [0x4A, 0x01],
        "Ness's Nightmare": [0x25, 0x01],
        "Starman Junior": [0x2F, 0x01],
        "Mini Barf": [0x3B, 0x01],
        "Heavily Armed Pokey": [0xCA, 0x01],
    }

    boss_sprite_addrs = {
        "Frank": [0x0F9338],
        "Frankystein Mark II": [0x0F96F0],
        "Captain Strong": [0x0302CE, 0x05F870, 0x0F8E3D, 0x05F886, 0x05F8A1, 0x05F8E3, 0x05FB0E, 0x05FBFC, 0x05FD08, 0x05FD5C],
        "Everdred": [0x0F9A64, 0x0F9FB4],
        "Mr. Carpainter": [0x0FA27E],
        "Master Belch": [0x0FB7CF],
        "Boogey Tent": [0x0FACEB],
        "Guardian Digger": [0x0FC11B, 0x0FC0B5, 0x0FC12C, 0x0FC0D7, 0x0FC0C6],
        "Dept. Store Spook": [0x0FC803],
        "Evil Mani-Mani": [0x0FE6E4],
        "Clumsy Robot": [0x0FC429],
        "Starman Deluxe": [0x0FB626],
        "Kraken": [],
        "Guardian General": [],
        "Master Barf": [],
        "Ness's Nightmare": [],
        #"Starman Junior": [0x2F, 0x01],
        "Mini Barf": [],
        "Heavily Armed Pokey": [],
    }

    coupled_bosses = {
        "Titanic Ant": ["Black Antoid (2)"],
        "Master Belch": ["Slimy Little Pile"],
        "Trillionage Sprout": ["Tough Mobile Sprout"],
        "Master Barf": ["Even Slimier Little Pile"],
        "Starman Deluxe": ["Starman Super", "Starman"],
        "Carbon Dog": ["Diamond Dog"]
    }


    world.regional_enemies = {"Northern Onett": {world.enemies["Spiteful Crow"], world.enemies["Runaway Dog"], world.enemies["Coil Snake"]},
                              "Onett": {world.enemies["Pogo Punk"], world.enemies["Skate Punk"], world.enemies["Yes Man Junior"], world.enemies["Frank"], world.enemies["Frankystein Mark II"]},
                              "Giant Step": {world.enemies["Attack Slug"], world.enemies["Black Antoid"], world.enemies["Black Antoid (2)"], world.enemies["Rowdy Mouse"], world.enemies["Titanic Ant"]},
                              "Twoson": {world.enemies["Black Antoid"], world.enemies["Cop"], world.enemies["Captain Strong"], world.enemies["Ramblin' Evil Mushroom"],
                                         world.enemies["Annoying Old Party Man"], world.enemies["Cranky Lady"], world.enemies["Mobile Sprout"], world.enemies["New Age Retro Hippie"], world.enemies["Unassuming Local Guy"],
                                         world.enemies["Runaway Dog"]},
                              "Everdred's House": {world.enemies["Everdred"]},
                              "Peaceful Rest Valley": {world.enemies["Li'l UFO"], world.enemies["Mobile Sprout"], world.enemies["Spinning Robo"], world.enemies["Territorial Oak"]},
                              "Happy-Happy Village": {world.enemies["Coil Snake"], world.enemies["Insane Cultist"], world.enemies["Spiteful Crow"], world.enemies["Unassuming Local Guy"], world.enemies["Mr. Carpainter"], world.enemies["Mr. Carpainter (2)"]},
                              "Lilliput Steps": {world.enemies["Mighty Bear"], world.enemies["Mole Playing Rough"], world.enemies["Mr. Batty"], world.enemies["Mondo Mole"]},
                              "Threed": {world.enemies["Coil Snake"], world.enemies["Handsome Tom"], world.enemies["Smilin' Sam"], world.enemies["Trick or Trick Kid"],
                                         world.enemies["Zombie Dog"], world.enemies["Putrid Moldyman"], world.enemies["Smelly Ghost"]},
                              "Threed Underground": {world.enemies["No Good Fly"], world.enemies["Urban Zombie"], world.enemies["Zombie Possessor"], world.enemies["Mini Barf"], world.enemies["Zombie Dog"]},
                              "Grapefruit Falls": {world.enemies["Armored Frog"], world.enemies["Black Antoid"], world.enemies["Coil Snake"], world.enemies["Farm Zombie"],
                                                   world.enemies["Plain Crocodile"], world.enemies["Red Antoid"], world.enemies["Violent Roach"], world.enemies["Mad Duck"], world.enemies["Black Antoid (2)"]},
                              "Belch's Factory": {world.enemies["Farm Zombie"], world.enemies["Foppy"], world.enemies["Mostly Bad Fly"], world.enemies["Slimy Little Pile"], world.enemies["Master Belch"], world.enemies["Master Belch (2)"]},
                              "Milky Well": {world.enemies["Mad Duck"], world.enemies["Ranboob"], world.enemies["Struttin' Evil Mushroom"], world.enemies["Tough Mobile Sprout"], world.enemies["Trillionage Sprout"]},
                              "Dusty Dunes Desert": {world.enemies["Bad Buffalo"], world.enemies["Crested Booka"], world.enemies["Criminal Caterpillar"], world.enemies["Cute Li'l UFO"], world.enemies["Desert Wolf"], world.enemies["Mole Playing Rough"],
                                                     world.enemies["Skelpion"], world.enemies["Smilin' Sphere"]},
                              "Fourside": {world.enemies["Annoying Reveler"], world.enemies["Crazed Sign"], world.enemies["Extra Cranky Lady"], world.enemies["Mad Taxi"],
                                           world.enemies["Abstract Art"], world.enemies["Dali's Clock"], world.enemies["Enraged Fire Plug"], world.enemies["Robo-pump"], world.enemies["Evil Mani-Mani"]},
                              "Gold Mine": {world.enemies["Gigantic Ant"], world.enemies["Mad Duck"], world.enemies["Noose Man"], world.enemies["Thirsty Coil Snake"], world.enemies["Guardian Digger"], world.enemies["Guardian Digger (2)"]},
                              "Fourside Dept. Store": {world.enemies["Musica"], world.enemies["Mystical Record"], world.enemies["Scalding Coffee Cup"], world.enemies["Dept. Store Spook"], world.enemies["Dept. Store Spook (2)"]},
                              "Monkey Caves": {world.enemies["Struttin' Evil Mushroom (2)"], world.enemies["Tough Mobile Sprout"], world.enemies["Struttin' Evil Mushroom"]},
                              "Monotoli Building": {world.enemies["Sentry Robot"], world.enemies["Clumsy Robot"], world.enemies["Clumsy Robot (2)"], world.enemies["Clumsy Robot (3)"]},
                              "Rainy Circle": {world.enemies["Arachnid!"], world.enemies["Cave Boy"], world.enemies["Elder Batty"], world.enemies["Mighty Bear Seven"], world.enemies["Strong Crocodile"], world.enemies["Shrooom!"]},
                              "Summers": {world.enemies["Crazed Sign"], world.enemies["Mad Taxi"], world.enemies["Mole Playing Rough"], world.enemies["Over Zealous Cop"], world.enemies["Tough Guy"], world.enemies["Kraken"], world.enemies["Kraken (2)"]},
                              "Summers Museum": {world.enemies["Shattered Man"]},
                              "Magnet Hill": {world.enemies["Deadly Mouse"], world.enemies["Filthy Attack Roach"], world.enemies["Stinky Ghost"], world.enemies["Plague Rat of Doom"]},
                              "Pink Cloud": {world.enemies["Conducting Menace"], world.enemies["Kiss of Death"], world.enemies["Tangoo"], world.enemies["Thunder Mite"], world.enemies["Thunder and Storm"]},
                              "Scaraba": {world.enemies["Beautiful UFO"], world.enemies["Dread Skelpion"], world.enemies["Great Crested Booka"], world.enemies["High-class UFO"], world.enemies["Master Criminal Worm"]},
                              "Pyramid": {world.enemies["Arachnid!!!"], world.enemies["Fierce Shattered Man"], world.enemies["Guardian Hieroglyph"], world.enemies["Lethal Asp Hieroglyph"], world.enemies["Petrified Royal Guard"],
                                          world.enemies["Guardian General"], world.enemies["Guardian General (2)"]},
                              "Southern Scaraba": {world.enemies["Beautiful UFO"], world.enemies["High-class UFO"], world.enemies["Marauder Octobot"]},
                              "Dungeon Man": {world.enemies["Dali's Clock"], world.enemies["Mystical Record"], world.enemies["Lesser Mook"], world.enemies["Mystical Record"], world.enemies["Scalding Coffee Cup"], world.enemies["Worthless Protoplasm"]},
                              "Deep Darkness": {world.enemies["Mole Playing Rough"]},
                              "Deep Darkness Darkness": {world.enemies["Big Pile of Puke"], world.enemies["Demonic Petunia"], world.enemies["Even Slimier Little Pile"], world.enemies["Hard Crocodile"], world.enemies["Hostile Elder Oak"],
                                                         world.enemies["Manly Fish"], world.enemies["Manly Fish's Brother"], world.enemies["Pit Bull Slug"], world.enemies["Zap Eel"], world.enemies["Master Barf"]},
                              "Boogey Tent": {world.enemies["Boogey Tent"], world.enemies["Boogey Tent (2)"]},
                              "Southern Winters": {world.enemies["Rowdy Mouse"], world.enemies["Worthless Protoplasm"], world.enemies["Mad Duck"],
                                                   world.enemies["Lesser Mook"], world.enemies["Whirling Robo"], world.enemies["Wooly Shambler"]},
                              "Stonehenge Base": {world.enemies["Atomic Power Robot"], world.enemies["Military Octobot"], world.enemies["Mook Senior"], world.enemies["Starman"], world.enemies["Starman Super"], world.enemies["Starman Deluxe"], world.enemies["Starman Super (2)"]},
                              "Lumine Hall": {world.enemies["Conducting Spirit"], world.enemies["Fobby"], world.enemies["Hyper Spinning Robo"], world.enemies["Uncontrollable Sphere"], world.enemies["Electro Specter"]},
                              "Lost Underworld": {world.enemies["Chomposaur"], world.enemies["Chomposaur (2)"], world.enemies["Ego Orb"], world.enemies["Wetnosaur"]},
                              "Fire Spring": {world.enemies["Evil Elemental"], world.enemies["Major Psychic Psycho"], world.enemies["Psychic Psycho"], world.enemies["Soul Consuming Flame"], world.enemies["Carbon Dog"], world.enemies["Diamond Dog"]},
                              "Magicant": {world.enemies["Care Free Bomb"], world.enemies["Electro Swoosh"], world.enemies["French Kiss of Death"], world.enemies["Loaded Dice"], world.enemies["Mr. Molecule"], world.enemies["Uncontrollable Sphere"],
                                           world.enemies["Fobby"], world.enemies["Beautiful UFO"], world.enemies["High-class UFO"], world.enemies["Kraken"], world.enemies["Ness's Nightmare"], world.enemies["Ness's Nightmare (2)"], world.enemies["Kraken (2)"],
                                           world.enemies["Loaded Dice (2)"]},
                              "Cave of the Past": {world.enemies["Bionic Kraken"], world.enemies["Final Starman"], world.enemies["Ghost of Starman"], world.enemies["Nuclear Reactor Robot"], world.enemies["Squatter Demon"],
                                                   world.enemies["Ultimate Octobot"], world.enemies["Wild 'n Wooly Shambler"], world.enemies["Final Starman (2)"], world.enemies["Ghost of Starman (2)"]},
                              "Endgame": {world.enemies["Heavily Armed Pokey"], world.enemies["Giygas (1)"], world.enemies["Giygas (2)"], world.enemies["Giygas (3)"], world.enemies["Giygas (4)"], world.enemies["Giygas (5)"], world.enemies["Giygas (6)"]},
                        
    }


combat_regions = [
    "Northern Onett",
    "Onett",
    "Giant Step",
    "Twoson",
    "Happy-Happy Village",
    "Lilliput Steps",
    "Threed",
    "Milky Well",
    "Dusty Dunes Desert",
    "Fourside",
    "Gold Mine",
    "Monkey Caves",
    "Monotoli Building",
    "Rainy Circle",
    "Summers",
    "Magnet Hill",
    "Pink Cloud",
    "Scaraba",
    "Pyramid",
    "Southern Scaraba",
    "Dungeon Man",
    "Deep Darkness",
    "Deep Darkness Darkness",
    "Stonehenge Base",
    "Lumine Hall",
    "Lost Underworld",
    "Fire Spring",
    "Magicant",
    "Cave of the Past",
    "Endgame",
    "Grapefruit Falls",
    "Peaceful Rest Valley",
    "Everdred's House",
    "Belch's Factory",
    "Southern Winters",
    "Summers Museum",
    "Fourside Dept. Store",
    "Threed Underground",
    "Boogey Tent"
]

levels = [
    1,  #north onett
    2, #south onett
    3, #giant step
    5, #twoson
    7, #everdred
    9, #peaceful rest
    10, #happy happy
    12, #lilliput steps
    13, #threed
    14, #threed caverns
    15, #grapefruit falls
    17, #belch base
    18, #milky well
    19, #duty dunes
    21, #fourside
    23, #gold mine
    24, #dept store
    25, #monkey cabves
    26, #monotoli building
    28, #winters
    29, #southern winters
    31, #rainy circle
    32, #summers
    33, #museum
    36, #magnet hill
    38, #pink cloud
    39, #scaraba
    42, #pyramid
    43, #scaraba south
    45, #dungeon man
    47, #deep darkness
    49, #deep darkness swamp
    52, #stonehenge
    56, #lumine hall
    59, #lost underworld
    65, #fire spring
    69, #magicant
    70, #cave of the past
    73] #gigyas

spell_breaks: Dict[str, Dict[int, str]] = {
    "freeze": {30: "alpha", 50: "beta", 70: "gamma", 100: "omega"},
    "fire": {20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "lifeup": {20: "alpha", 50: "beta", 70: "gamma", 100: "omega"},
    "thunder": {20: "alpha", 30: "beta", 50: "gamma", 100: "omega"},
    "flash": {25: "alpha", 45: "beta", 60: "gamma", 100: "omega"},
    "special": {25: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "healing": {20: "alpha", 40: "beta", 60: "gamma", 100: "omega"},
    "starstorm": {50: "alpha", 100: "beta"},
    "diamond_eyes": {35: "alpha", 40: "beta", 100: "gamma"},
    "nauseous_breath": {25: "alpha", 100: "beta"},
    "poison_stinger": {25: "alpha", 100: "beta"},
    "kiss_of_death": {25: "alpha", 100: "beta"},
    "summon_storm": {25: "alpha", 45: "beta", 60: "gamma", 100: "omega"},
    "scalding_espresso": {20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "extinguishing_blast": {20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "spray_fire": {20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "breathe_fire": {20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "poisonous_fangs": {25: "alpha", 100: "beta"},
    "flaming_fireball": {20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "glorious_light": {25: "alpha", 45: "beta", 60: "gamma", 100: "omega"},
    "poison_flute": {25: "alpha", 100: "beta"},
    "diamond_bite": {35: "alpha", 40: "beta", 100: "gamma"},
    "scatter_spores": {25: "alpha", 100: "beta"},
    "hacking_cough": {25: "alpha", 100: "beta"},
    "stuffiness_beam": {25: "alpha", 100: "beta"},
    "crashing_boom_bang": {20: "alpha", 30: "beta", 50: "gamma", 100: "omega"},
    "paralysis": {35: "alpha", 60: "beta", 100: "gamma"},
    "electrical_shock": {20: "alpha", 30: "beta", 50: "gamma", 100: "omega"},
    #bombs and bottle rockets too? Also missile maybe? hmmm
}

def get_psi_levels(level: int, breaks: Dict[int, str]) -> str:
    for top_val, psi_level in breaks.items():
        if level <= top_val:
            return psi_level


enemy_psi = {
    "Dept. Store Spook": ["freeze", "fire", "lifeup", "null"],
    "Dept. Store Spook (2)": ["null", "null", "freeze", "null"],
    "Black Antoid": ["null", "null", "null", "lifeup"],
    "Struttin' Evil Mushroom": ["null", "null", "null", "scatter_spores"],
    "Mobile Sprout": ["null", "null", "null", "lifeup"],
    "Tough Mobile Sprout": ["null", "null", "null", "lifeup"],
    "Mystical Record": ["null", "null", "lifeup", "null"],
    "Guardian Hieroglyph": ["hacking_cough", "thunder", "flash", "thunder"],
    "Conducting Menace": ["flash", "flash", "thunder", "thunder"],
    "Conducting Spirit": ["flash", "flash", "thunder", "thunder"],
    "Ness's Nightmare": ["null", "special", "glorious_light", "null"],
    "Mr. Carpainter": ["crashing_boom_bang", "lifeup", "null", "null"],
    "Carbon Dog": ["flaming_fireball", "null", "null", "null"],
    "Thunder Mite": ["thunder", "thunder", "thunder", "thunder"],
    "Chomposaur": ["fire", "fire", "null", "null"],
    "Gigantic Ant": ["null", "poison_stinger", "null", "null"],
    "Shrooom!": ["null", "lifeup", "scatter_spores", "null"],
    "Plague Rat of Doom": ["poisonous_fangs", "null", "null", "null"],
    "Mondo Mole": ["lifeup", "null", "null", "null"],
    "Scalding Coffee Cup": ["scalding_espresso", "scalding_espresso", "scalding_espresso", "scalding_espresso"],
    "Arachnid!": ["null", "null", "null", "poison_stinger"],
    "Arachnid!!!": ["poison_stinger", "null", "null", "null"],
    "Slimy Little Pile": ["hacking_cough", "null", "null", "null"],
    "Even Slimier Little Pile": ["null", "null", "null", "hacking_cough"],
    "Kraken": ["breathe_fire", "null", "crashing_boom_bang", "null"],
    "Bionic Kraken": ["null", "crashing_boom_bang", "breathe_fire", "null"], #Generate tornado?
    "Spinning Robo": ["null", "null", "stuffiness_beam", "null"],
    "Whirling Robo": ["null", "stuffiness_beam", "null", "null"],
    "Thirsty Coil Snake": ["poisonous_fangs", "null", "null", "null"],
    "Crazed Sign": ["null", "null", "paralysis", "null"],
    "Wooly Shambler": ["null", "null", "null", "flash"],
    "Wild 'n Wooly Shambler": ["null", "null", "null", "flash"],
    "Skelpion": ["null", "poison_stinger", "null", "thunder"],
    "Dread Skelpion": ["poison_stinger", "null", "thunder", "thunder"],
    "Ghost of Starman": ["starstorm", "null", "null", "null"],
    "Smilin' Sphere": ["null", "fire", "null", "null"],
    "Uncontrollable Sphere": ["null", "fire", "fire", "null"],
    "Starman Deluxe": ["null", "null", "starstorm", "null"],
    "Final Starman": ["null", "null", "starstorm", "null"],
    "Urban Zombie": ["null", "null", "nauseous_breath", "null"],
    "Zombie Dog": ["null", "null", "null", "poisonous_fangs"],
    "Diamond Dog": ["null", "null", "null", "glorious_light"],
    "Trillionage Sprout": ["null", "null", "flash", "paralysis"],
    "Musica": ["electrical_shock", "null", "null", "electrical_shock"],
    "Desert Wolf": ["null", "null", "null", "poisonous_fangs"],
    "Master Belch": ["nauseous_breath", "nauseous_breath", "null", "null"],
    "Big Pile of Puke": ["null", "hacking_cough", "null", "nauseous_breath"],
    "Master Barf": ["nauseous_breath", "null", "null", "null"],
    "Kiss of Death": ["null", "null", "kiss_of_death", "null"],
    "French Kiss of Death": ["kiss_of_death", "kiss_of_death", "kiss_of_death", "kiss_of_death"],
    "Zap Eel": ["electrical_shock", "electrical_shock", "electrical_shock", "electrical_shock"],
    "Tangoo": ["null", "null", "poison_flute", "null"],
    "Squatter Demon": ["poisonous_fangs", "diamond_bite", "null", "null"],
    "Lesser Mook": ["freeze", "freeze", "null", "diamond_eyes"],
    "Mook Senior": ["freeze", "fire", "lifeup", "diamond_eyes"],
    "Smelly Ghost": ["null", "null", "lifeup", "null"],
    "Deadly Mouse": ["poisonous_fangs", "null", "null", "null"],
    "Electro Specter": ["electrical_shock", "null", "electrical_shock", "null"],
    "Smilin' Sam": ["null", "null", "null", "lifeup"],
    "Manly Fish's Brother": ["null", "null", "freeze", "healing"],
    "Thunder and Storm": ["crashing_boom_bang", "null", "null", "null"],
    "Cute Li'l UFO": ["null", "null", "null", "lifeup"],
    "Beautiful UFO": ["null", "null", "null", "lifeup"],
    "Evil Mani-Mani": ["null", "paralysis", "null", "null"],
    "Mr. Molecule": ["thunder", "flash", "fire", "freeze"],
    "Heavily Armed Pokey": ["null", "fire", "null", "null"],
    "Psychic Psycho": ["fire", "fire", "fire", "fire"],
    "Major Psychic Psycho": ["fire", "null", "paralysis", "fire"],
    "Soul Consuming Flame": ["null", "breathe_fire", "flaming_fireball", "spray_fire"],
    "Demonic Petunia": ["null", "extinguishing_blast", "null", "null"],
    "Li'l UFO": ["null", "null", "stuffiness_beam", "null"],
    "Ness's Nightmare (2)": ["special", "lifeup", "special", "null"],
    "Mr. Carpainter (2)": ["crashing_boom_bang", "null", "null", "null"],
    "Carbon Dog (2)": ["fire_spray", "null", "null", "null"],
    "Gigantic Ant (2)": ["paralysis", "null", "null", "null"],
    "Chomposaur (2)": ["null", "null", "fire", "fire"],
    "Guardian Digger (2)": ["null", "null", "null", "lifeup"],
    "Kraken (2)": ["flash", "breathe_fire", "null", "null"], #tornado?
    "Starman Super (2)": ["null", "healing", "null", "null"],
    "Ghost of Starman (2)": ["null", "null", "starstorm", "null"],
    "Final Starman (2)": ["starstorm", "null", "healing", "null"],
    "Diamond Dog (2)": ["null", "null", "null", "diamond_bite"],
    "Trillionage Sprout (2)": ["null", "null", "diamond_eyes", "null"],
    "Master Belch (2)": ["nauseous_breath", "null", "null", "null"],
    "Master Barf (2)": ["null", "null", "nauseous_breath", "null"],
    "Boogey Tent (2)": ["null", "null", "flash", "null"],
    "Electro Specter (2)": ["null", "null", "electrical_shock", "null"],
    "Thunder and Storm (2)": ["summon_storm", "null", "crashing_boom_bang", "null"],
    "Evil Mani-Mani (2)": ["null", "null", "glorious_light", "null"],
    "Black Antoid (2)": ["lifeup", "lifeup", "lifeup", "lifeup"],
    "Giygas (1)": ["special", "special", "special", "special"],
    "Farm Zombie": ["null", "null", "nauseous_breath", "null"],
    "Criminal Caterpillar": ["fire", "fire", "fire", "fire"],
    "Evil Eye": ["null", "diamond_eyes", "paralysis", "null"],
    "Master Criminal Worm": ["fire", "fire", "fire", "fire"]
}

spell_data = {
    "freeze": {
        "alpha": [0x12, 0x00, 0x09],
        "beta": [0x13, 0x00, 0x0A],
        "gamma": [0x14, 0x00, 0x0B],
        "omega": [0x15, 0x00, 0x0C]
    },
    "fire": {
        "alpha": [0x0E, 0x00, 0x05],
        "beta": [0x0F, 0x00, 0x06],
        "gamma": [0x10, 0x00, 0x07],
        "omega": [0x11, 0x00, 0x08]
    },
    "lifeup": {
        "alpha": [0x20, 0x00, 0x17],
        "beta": [0x21, 0x00, 0x18],
        "gamma": [0x22, 0x00, 0x19],
        "omega": [0x23, 0x00, 0x1A]
    },
    "flash": {
        "alpha": [0x1A, 0x00, 0x11],
        "beta": [0x1B, 0x00, 0x12],
        "gamma": [0x1C, 0x00, 0x13],
        "omega": [0x1D, 0x00, 0x14]
    },
    "thunder": {
        "alpha": [0x16, 0x00, 0x0D],
        "beta": [0x17, 0x00, 0x0E],
        "gamma": [0x18, 0x00, 0x0F],
        "omega": [0x19, 0x00, 0x10]
    },
    "special": {
        "alpha": [0x0A, 0x00, 0x01],
        "beta": [0x0B, 0x00, 0x02],
        "gamma": [0x0C, 0x00, 0x03],
        "omega": [0x0D, 0x00, 0x04]
    },
    "healing": {
        "alpha": [0x24, 0x00, 0x1B],
        "beta": [0x25, 0x00, 0x1C],
        "gamma": [0x26, 0x00, 0x1D],
        "omega": [0x27, 0x00, 0x1E]
    },
    "starstorm": {
        "alpha": [0x1E, 0x00, 0x15],
        "beta": [0x1F, 0x00, 0x16]
    },
    "scatter_spores": {
        "alpha": [0xED, 0x00, 0x00],
        "beta": [0x3F, 0x01, 0x00]
    },
    "nauseous_breath": {
        "alpha": [0x4A, 0x00, 0x00],
        "beta": [0x47, 0x00, 0x00]
    },
    "diamond_eyes": {
        "alpha": [0x40, 0x01, 0x00],
        "beta": [0x41, 0x01, 0x00],
        "gamma": [0x44, 0x00, 0x00]
    },
    "glorious_light": {
        "alpha": [0x42, 0x01, 0x00],
        "beta": [0x43, 0x01, 0x00],
        "gamma": [0xC9, 0x00, 0x00],
        "omega": [0x44, 0x01, 0x00],
    },
    "flaming_fireball": {
        "alpha": [0x45, 0x01, 0x00],
        "beta": [0x46, 0x01, 0x00],
        "gamma": [0x47, 0x01, 0x00],
        "omega": [0x68, 0x00, 0x00],
    },
    "breathe_fire": {
        "alpha": [0x48, 0x01, 0x00],
        "beta": [0x49, 0x01, 0x00],
        "gamma": [0x5E, 0x00, 0x00],
        "omega": [0x4A, 0x00, 0x00],
    },
    "spray_fire": {
        "alpha": [0x4B, 0x01, 0x00],
        "beta": [0x4C, 0x01, 0x00],
        "gamma": [0x4D, 0x01, 0x00],
        "omega": [0x5D, 0x00, 0x00],
    },
    "paralysis": {
        "alpha": [0xFF, 0xFF, 0xFF],#CHANGE LATER
        "beta": [0x38, 0x00, 0x2F],
        "gamma": [0x39, 0x00, 0x30]
    },
    "poisonous_fangs": {
        "alpha": [0x4E, 0x01, 0x00],
        "beta": [0x64, 0x00, 0x00]
    },
    "poison_stinger": {
        "alpha": [0x4F, 0x01, 0x00],
        "beta": [0x48, 0x00, 0x00]
    },
    "crashing_boom_bang": {
        "alpha": [0x50, 0x01, 0x00],
        "beta": [0x5C, 0x00, 0x00],
        "gamma": [0x51, 0x01, 0x00],
        "omega": [0x52, 0x01, 0x00]
    },

    "electrical_shock": {
        "alpha": [0x53, 0x01, 0x00],
        "beta": [0xCA, 0x00, 0x00],
        "gamma": [0x54, 0x01, 0x00],
        "omega": [0x55, 0x01, 0x00]
    },
    "scalding_espresso": {
        "alpha": [0x59, 0x00, 0x00],
        "beta": [0x56, 0x01, 0x00],
        "gamma": [0x57, 0x01, 0x00],
        "omega": [0x58, 0x01, 0x00]
    },
    "extinguishing_blast": {
        "alpha": [0x59, 0x01, 0x00],
        "beta": [0x5A, 0x01, 0x00],
        "gamma": [0x5B, 0x00, 0x00],
        "omega": [0x5B, 0x01, 0x00]
    },
    "diamond_bite": {
        "alpha": [0x5C, 0x01, 0x00],
        "beta": [0x5D, 0x01, 0x00],
        "gamma": [0xE4, 0x00, 0x00]
    },
    "poison_flute": {
        "alpha": [0x5E, 0x01, 0x00],
        "beta": [0xCD, 0x00, 0x00]
    },
    "kiss_of_death": {
        "alpha": [0x5F, 0x01, 0x00],
        "beta": [0x49, 0x00, 0x00]
    },
    "stuffiness_beam": {
        "alpha": [0xF1, 0x00, 0x00],
        "beta": [0x45, 0x00, 0x00]
    },
        "hacking_cough": {
        "alpha": [0xD5, 0x00, 0x00],
        "beta": [0x57, 0x00, 0x00]
    }

}

shield_table = {
    "disabled": 0x00,
    "phys_1": 0x03,
    "phys_2": 0x04,
    "psi_1": 0x01,
    "psi_2": 0x02
}

def assumed_player_speed_for_level(level):
    return 2 + 58 * (level - 1) / 80

def scale_enemy_speed(enemy, new_level):
    normal_dodge_chance = (2 * enemy.speed - assumed_player_speed_for_level(enemy.level)) / 500

    enemy_scaled_speed  = (normal_dodge_chance * 500 + assumed_player_speed_for_level(new_level)) / 2
    return enemy_scaled_speed

def scale_exp(base_exp, base_level, new_level, k):
    new_exp = base_exp * (new_level / base_level) ** k
    return new_exp

def scale_shield(level, shield):
    if shield != None:
        if level < 10:
            enemy_shield = "disabled"
        elif shield in ["phys_1", "phys_2"]:
            if level < 25:
                enemy_shield = "phys_1"
            else:
                enemy_shield = "phys_2"
        elif shield in ["psi_1", "psi_2"]:
            if level < 25:
                enemy_shield = "psi_1"
            else:
                enemy_shield = "psi_2"
        return enemy_shield


def scale_enemies(world, rom):
    world.Paula_scaled = False
    world.Jeff_scaled = False
    world.Poo_scaled = False
    world.last_combat_region = None
    state = world.multiworld.get_all_state(True)
    distances: Dict[str, int] = {}
    for region in world.multiworld.get_regions(world.player):
        if region.name != "Menu":
            if region in state.path:
                connected, connection = state.path[region]
                distance = 0
                while connection is not None:
                    if not any(connected == entrance.name for entrance in world.multiworld.get_entrances(world.player)):
                        distance += 1
                    connected, connection = connection
                distances[region.name] = distance

    paths = state.path
    world.location_order = []
    location_test = []
    world.scale_warning = False
    for i, sphere in enumerate(world.multiworld.get_spheres()):
        all_locs = [loc for loc in sphere]
        for loc in all_locs:
            if loc.parent_region.name in combat_regions:
                world.last_combat_region = loc.parent_region.name
            if (loc.parent_region.name in [world.Paula_region, world.Jeff_region, world.Poo_region] and loc.parent_region.name not in combat_regions) and world.options.auto_scale_party_members:
                if loc.parent_region.name == world.Paula_region and world.Paula_scaled == False:
                    world.Paula_region = world.last_combat_region
                    world.Paula_scaled = True
                elif loc.parent_region.name == world.Jeff_region and world.Jeff_scaled == False:
                    world.Jeff_region = world.last_combat_region
                    world.Jeff_scaled = True
                if loc.parent_region.name == world.Poo_region and world.Poo_scaled == False:
                    world.Poo_region = world.last_combat_region
                    world.Poo_scaled = True
        locs = [loc for loc in sphere if loc.player == world.player and loc.parent_region.name in combat_regions and loc.parent_region.name not in world.location_order]
        regions = {loc.parent_region.name for loc in locs}
        for region in sorted(regions, key=lambda x: distances.get(x, float('inf'))):
            #if region not in distances:
                #warning(f"Warning: {region} is not in distances. for player {world.player}")
                #if world.scale_warning == False:
                    #warning(f"{distances}")
                    #world.scale_warning = True
            world.location_order.append(region)
    if world.options.magicant_mode == 2 and world.options.giygas_required:
        world.location_order.remove("Magicant")
        world.location_order.insert(world.location_order.index("Endgame") + 1, "Magicant")
    elif world.options.magicant_mode == 3:
        world.location_order.remove("Magicant")
        world.location_order.insert(world.location_order.index("Endgame") - 1, "Magicant")

    #if world.scale_warning == True:
        #warning(f"{world.location_order}")
    if world.options.auto_scale_party_members:
        if "Paula" in world.start_items or world.Paula_region == None:
            world.Paula_region = world.location_order[0]
        if "Jeff" in world.start_items or world.Jeff_region == None:
            world.Jeff_region = world.location_order[0]
        if "Poo" in world.start_items or world.Poo_region == None:
            world.Poo_region = world.location_order[0]
        rom.write_bytes(0x15F60F, bytearray([max(levels[world.location_order.index(world.Paula_region)] + world.random.randint(-3, 3), 1)])) #Paula starting level
        rom.write_bytes(0x15F623, bytearray([max(levels[world.location_order.index(world.Jeff_region)] + world.random.randint(-3, 3), 1)])) #Jeff starting level
        rom.write_bytes(0x15F637, bytearray([max(levels[world.location_order.index(world.Poo_region)] + world.random.randint(-3, 3), 1)])) #Poo starting level

    for region, level in zip(world.location_order, levels):
        for enemy in world.regional_enemies[region]:
            if enemy.is_scaled is False:
                enemy_hp = int(enemy.hp * level / enemy.level)
                enemy_pp = int(enemy.pp * level / enemy.level)
                k = 2.258
                #enemy_exp = int(scale_exp(enemy.exp, enemy.level, level, k))
                enemy_exp = int(enemy.exp * level / enemy.level)
                enemy_exp = int(enemy_exp * world.options.experience_modifier.value / 100)
                enemy_money = int(enemy.money * level / enemy.level)
                enemy_speed = max(2, int(scale_enemy_speed(enemy, level)))
                enemy_offense = int(enemy.offense * level / enemy.level)
                enemy_defense = int(enemy.defense * level / enemy.level)
                enemy_level = int(enemy.level * level / enemy.level)
                enemy_shield = scale_shield(level, enemy.shield)

                #print(f"\nEnemy: {enemy.name}\nLevel: {enemy_level}\nHP: {enemy_hp}\nPP: {enemy_pp}\nEXP: {enemy_exp}\n${enemy_money}\nSpeed: {enemy_speed}\nOffense: {enemy_offense}\nDefense: {enemy_defense}\nSpeed: {enemy_speed} {enemy.shield}")
                enemy_hp = struct.pack('<H', enemy_hp)
                enemy_pp = struct.pack('<H', enemy_pp)
                enemy_exp = struct.pack('<I', enemy_exp)
                enemy_money = struct.pack('<H', enemy_money)
                enemy_offense = struct.pack('<H', enemy_offense)
                enemy_defense = struct.pack('<H', enemy_defense)
                rom.write_bytes(enemy.address + 33, bytearray(enemy_hp))
                rom.write_bytes(enemy.address + 35, bytearray(enemy_pp))
                rom.write_bytes(enemy.address + 37, bytearray(enemy_exp))
                rom.write_bytes(enemy.address + 41, bytearray(enemy_money))
                rom.write_bytes(enemy.address + 60, bytearray([enemy_speed]))
                rom.write_bytes(enemy.address + 56, bytearray(enemy_offense))
                rom.write_bytes(enemy.address + 58, bytearray(enemy_defense))
                rom.write_bytes(enemy.address + 54, bytearray([enemy_level]))
                if enemy.shield is not None:
                    rom.write_bytes(enemy.address + 89, bytearray([shield_table[enemy_shield]]))
                
                if enemy.name in enemy_psi:
                    for index, spell in [(i, s) for i, s in enumerate(enemy_psi[enemy.name]) if s != "null"]:
                        #print(enemy.name)
                        #print(index, spell)
                        psi_level = get_psi_levels(level, spell_breaks[spell])
                        rom.write_bytes(enemy.address + 70 + (index * 2), bytearray(spell_data[spell][psi_level][0:2]))
                        rom.write_bytes(enemy.address + 80 + index, bytearray([spell_data[spell][psi_level][2]]))
                        #print(f"{spell} {psi_level} at {hex(enemy.address + 70 + (index * 2))}")
                if world.options.shuffle_enemy_drops:
                    rom.write_bytes(enemy.address + 88, bytearray([world.random.choice(world.filler_drops)]))
                enemy.is_scaled = True
