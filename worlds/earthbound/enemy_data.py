from BaseClasses import CollectionState
from typing import Dict, List
import struct

class EarthBoundEnemy:
    def __init__(self, name, address, hp, pp, exp, money, speed, offense, defense, level, is_scaled):
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

enemies = {
"Insane Cultist": EarthBoundEnemy("Insane Cultist", 0x1595e7, 94, 0, 353, 33, 8, 19, 25, 13, False),
"Dept. Store Spook": EarthBoundEnemy("Dept. Store Spook", 0x159645, 610, 290, 24291, 1648, 19, 82, 135, 42, False),
"Armored Frog": EarthBoundEnemy("Armored Frog", 0x1596a3, 202, 0, 1566, 77, 7, 37, 108, 22, False),
"Bad Buffalo": EarthBoundEnemy("Bad Buffalo", 0x159701, 341, 0, 4108, 172, 11, 64, 104, 34, False),
"Black Antoid": EarthBoundEnemy("Black Antoid", 0x15975f, 34, 25, 37, 7, 4, 14, 13, 7, False),
"Red Antoid": EarthBoundEnemy("Red Antoid", 0x1597bd, 112, 30, 1175, 35, 10, 29, 27, 20, False),
"Ramblin' Evil Mushroom": EarthBoundEnemy("Ramblin' Evil Mushroom", 0x15981b, 60, 0, 95, 15, 5, 15, 10, 7, False),
"Struttin' Evil Mushroom (2)": EarthBoundEnemy("Struttin' Evil Mushroom", 0x159879, 157, 0, 1492, 95, 28, 29, 22, 17, False),
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
"Ness's Nightmare": EarthBoundEnemy("Ness's Nightmare", 0x159d3f, 1654, 882, 89004, 4442, 31, 172, 253, 71, False),
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
"Giygas (1)": EarthBoundEnemy("Giygas", 0x15a205, 3600, 0, 0, 0, 52, 203, 300, 73, False),
"Wetnosaur": EarthBoundEnemy("Wetnosaur", 0x15a263, 1030, 0, 33098, 745, 17, 126, 172, 59, False),
"Chomposaur": EarthBoundEnemy("Chomposaur", 0x15a2c1, 1288, 320, 44378, 896, 17, 139, 183, 62, False),
"Titanic Ant": EarthBoundEnemy("Titanic Ant", 0x15a31f, 235, 102, 685, 150, 6, 19, 23, 13, False),
"Gigantic Ant": EarthBoundEnemy("Gigantic Ant", 0x15a37d, 308, 81, 3980, 304, 17, 54, 112, 30, False),
"Shrooom!": EarthBoundEnemy("Shrooom!", 0x15a3db, 1700, 112, 96323, 4086, 18, 95, 154, 48, False),
"Plague Rat of Doom": EarthBoundEnemy("Plague Rat of Doom", 0x15a439, 1827, 60, 115272, 4464, 19, 71, 180, 47, False),
"Mondo Mole": EarthBoundEnemy("Mondo Mole", 0x15a497, 498, 161, 5791, 400, 9, 37, 50, 23, False),
"Guardian Digger": EarthBoundEnemy("Guardian Digger", 0x15a4f5, 386, 110, 17301, 1467, 17, 59, 129, 32, False),
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
"Starman Super": EarthBoundEnemy("Starman Super", 0x15ae81, 568, 310, 30145, 735, 24, 112, 129, 56, False),
"Ghost of Starman": EarthBoundEnemy("Ghost of Starman", 0x15aedf, 750, 462, 48695, 807, 46, 152, 170, 68, False),
"Smilin' Sphere": EarthBoundEnemy("Smilin' Sphere", 0x15af3d, 233, 60, 2218, 191, 17, 50, 65, 27, False),
"Uncontrollable Sphere": EarthBoundEnemy("Uncontrollable Sphere", 0x15af9b, 577, 180, 20389, 796, 27, 116, 134, 56, False),
"Petrified Royal Guard": EarthBoundEnemy("Petrified Royal Guard", 0x15aff9, 573, 0, 19163, 628, 12, 106, 173, 53, False),
"Guardian General": EarthBoundEnemy("Guardian General", 0x15b057, 831, 6, 95390, 3235, 21, 109, 214, 55, False),
"Starman Deluxe": EarthBoundEnemy("Starman Deluxe", 0x15b0b5, 1400, 418, 160524, 3827, 27, 143, 186, 65, False),
"Final Starman": EarthBoundEnemy("Final Starman", 0x15b113, 840, 860, 61929, 915, 47, 178, 187, 71, False),
"Urban Zombie": EarthBoundEnemy("Urban Zombie", 0x15b171, 171, 0, 700, 58, 10, 31, 24, 19, False),
"Zombie Possessor": EarthBoundEnemy("Zombie Possessor", 0x15b1cf, 176, 0, 950, 81, 30, 28, 19, 17, False),
"Zombie Dog": EarthBoundEnemy("Zombie Dog", 0x15b22d, 210, 0, 1354, 54, 30, 39, 51, 22, False),
"Crooked Cop": EarthBoundEnemy("Crooked Cop", 0x15b28b, 140, 0, 492, 159, 15, 20, 24, 13, False),
"Over Zealous Cop": EarthBoundEnemy("Over Zealous Cop", 0x15b2e9, 325, 0, 7448, 420, 18, 69, 75, 36, False),
"Territorial Oak": EarthBoundEnemy("Territorial Oak", 0x15b347, 145, 41, 356, 29, 5, 26, 30, 15, False),
"Hostile Elder Oak": EarthBoundEnemy("Hostile Elder Oak", 0x15b3a5, 609, 76, 17567, 690, 14, 134, 146, 59, False),
"Diamond Dog": EarthBoundEnemy("Diamond Dog", 0x15b403, 3344, 154, 337738, 6968, 31, 167, 230, 70, False),
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
"Electro Specter": EarthBoundEnemy("Electro Specter", 0x15c021, 3092, 80, 261637, 6564, 29, 148, 203, 67, False),
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
"Clumsy Robot": EarthBoundEnemy("Clumsy Robot", 0x15cb25, 962, 0, 32378, 2081, 83, 88, 137, 46, False),
"Soul Consuming Flame": EarthBoundEnemy("Soul Consuming Flame", 0x15cb83, 602, 0, 37618, 768, 30, 131, 262, 59, False),
"Demonic Petunia": EarthBoundEnemy("Demonic Petunia", 0x15cbe1, 478, 0, 15171, 724, 26, 102, 111, 50, False),
"Ranboob": EarthBoundEnemy("Ranboob", 0x15cc3f, 232, 42, 2486, 158, 20, 41, 63, 24, False),
"Li'l UFO": EarthBoundEnemy("Li'l UFO", 0x15cc9d, 82, 0, 223, 14, 53, 18, 17, 12, False),
"High-class UFO": EarthBoundEnemy("High-class UFO", 0x15ccfb, 433, 72, 12385, 456, 60, 93, 103, 47, False),
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
"Mr. Carpainter (2)": EarthBoundEnemy("Mr. Carpainter", 0x15d50f, 262, 70, 1412, 195, 8, 33, 45, 21, False),
"Carbon Dog (2)": EarthBoundEnemy("Carbon Dog", 0x15d56d, 1672, 0, 0, 0, 31, 159, 174, 70, False),
"Chomposaur (2)": EarthBoundEnemy("Chomposaur (2)", 0x15d5cb, 1288, 320, 44378, 896, 17, 139, 183, 62, False),
"Titanic Ant (2)": EarthBoundEnemy("Titanic Ant", 0x15d629, 235, 102, 685, 150, 6, 19, 23, 13, False),
"Gigantic Ant (2)": EarthBoundEnemy("Gigantic Ant", 0x15d687, 308, 81, 3980, 304, 17, 54, 112, 30, False),
"Shrooom! (2)": EarthBoundEnemy("Shrooom!", 0x15d6e5, 1700, 112, 96323, 4086, 18, 95, 154, 48, False),
"Plague Rat of Doom (2)": EarthBoundEnemy("Plague Rat of Doom", 0x15d743, 1827, 60, 115272, 4464, 19, 71, 180, 47, False),
"Mondo Mole (2)": EarthBoundEnemy("Mondo Mole", 0x15d7a1, 498, 161, 5791, 400, 9, 37, 50, 23, False),
"Guardian Digger (2)": EarthBoundEnemy("Guardian Digger", 0x15d7ff, 386, 110, 17301, 1467, 17, 59, 129, 32, False),
"Kraken (2)": EarthBoundEnemy("Kraken", 0x15d85d, 1097, 176, 79267, 3049, 21, 105, 166, 54, False),
#"Bionic Kraken (2)": EarthBoundEnemy("Bionic Kraken", 0x15d8bb, 900, 60, 50308, 960, 42, 155, 195, 70, False),
"Starman (2)": EarthBoundEnemy("Starman", 0x15d919, 545, 155, 23396, 720, 24, 103, 126, 55, False),
"Starman Super (2)": EarthBoundEnemy("Starman Super", 0x15d977, 568, 310, 30145, 735, 24, 112, 129, 56, False),
"Ghost of Starman (2)": EarthBoundEnemy("Ghost of Starman", 0x15d9d5, 750, 462, 48695, 807, 46, 152, 170, 68, False),
"Starman Deluxe (2)": EarthBoundEnemy("Starman Deluxe", 0x15da33, 1400, 418, 160524, 3827, 27, 143, 186, 65, False),
"Final Starman (2)": EarthBoundEnemy("Final Starman", 0x15da91, 840, 860, 61929, 915, 47, 178, 187, 71, False),
#"Urban Zombie": EarthBoundEnemy("Urban Zombie", 0x15daef, 171, 0, 700, 58, 10, 31, 24, 19, False),
"Diamond Dog (2)": EarthBoundEnemy("Diamond Dog", 0x15db4d, 3344, 154, 337738, 6968, 31, 167, 230, 70, False),
"Trillionage Sprout (2)": EarthBoundEnemy("Trillionage Sprout", 0x15dbab, 1048, 240, 30303, 1358, 16, 54, 88, 29, False),
"Master Belch (2)": EarthBoundEnemy("Master Belch", 0x15dc09, 650, 0, 12509, 664, 16, 50, 88, 27, False), 
#"Big Pile of Puke": EarthBoundEnemy("Big Pile of Puke", 0x15dc67, 609, 76, 17567, 690, 14, 134, 146, 59, False),
"Master Barf (2)": EarthBoundEnemy("Master Barf", 0x15dcc5, 1319, 0, 125056, 3536, 24, 136, 177, 60, False),
"Loaded Dice (2)": EarthBoundEnemy("Loaded Dice", 0x15dd23, 307, 0, 10672, 703, 77, 146, 113, 59, False),
#"Tangoo": EarthBoundEnemy("Tangoo", 0x15dd81, 371, 5, 14718, 572, 19, 96, 99, 48, False),
"Boogey Tent (2)": EarthBoundEnemy("Boogey Tent", 0x15dddf, 579, 56, 5500, 407, 10, 43, 69, 25, False),
#"Squatter Demon": EarthBoundEnemy("Squatter Demon", 0x15de3d, 774, 60, 48311, 897, 45, 158, 192, 69, False),
"Everdred (2)": EarthBoundEnemy("Everdred", 0x15de9b, 182, 0, 986, 171, 6, 25, 35, 15, False),
"Electro Specter (2)": EarthBoundEnemy("Electro Specter", 0x15def9, 3092, 80, 261637, 6564, 29, 148, 203, 67, False),
"Thunder and Storm (2)": EarthBoundEnemy("Thunder and Storm", 0x15df57, 2065, 70, 129026, 4736, 21, 111, 178, 56, False),
"Frankystein Mark II (2)": EarthBoundEnemy("Frankystein Mark II", 0x15dfb5, 91, 0, 76, 31, 4, 15, 18, 7, False),
"Evil Mani-Mani (2)": EarthBoundEnemy("Evil Mani-Mani", 0x15e013, 860, 88, 28139, 1852, 15, 86, 145, 45, False),
#"Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15e071, 1746, 999, 0, 0, 51, 150, 274, 72, False),
"Clumsy Robot (2)": EarthBoundEnemy("Clumsy Robot", 0x15e0cf, 962, 0, 32378, 2081, 83, 88, 137, 46, False),
"Robo-pump (2)": EarthBoundEnemy("Robo-pump", 0x15e12d, 431, 0, 4797, 349, 19, 70, 113, 36, False),
#"Foppy": EarthBoundEnemy("Foppy", 0x15e18b, 120, 10, 1311, 93, 1, 29, 9, 16, False),
"Guardian General (2)": EarthBoundEnemy("Guardian General", 0x15e1e9, 831, 6, 95390, 3235, 21, 109, 214, 55, False),
"Black Antoid (2)": EarthBoundEnemy("Black Antoid", 0x15e247, 34, 25, 37, 7, 4, 14, 13, 7, False), #Separate enemy used in the titanic ant fight
"Struttin' Evil Mushroom": EarthBoundEnemy("Struttin' Evil Mushroom", 0x15e2a5, 60, 0, 95, 15, 5, 15, 10, 7, False),
#"Runaway Dog (2)": EarthBoundEnemy("Runaway Dog", 0x15e303, 21, 0, 4, 3, 26, 4, 5, 73, False),
"Cave Boy": EarthBoundEnemy("Cave Boy", 0x15e361, 314, 0, 618, 17, 5, 21, 33, 11, False),
"Tiny Li'l Ghost": EarthBoundEnemy("Tiny Li'l Ghost", 0x15e3bf, 90, 0, 1, 162, 100, 19, 7, 18, False),
"Starman Junior": EarthBoundEnemy("Starman Junior", 0x15e41d, 200, 999, 16, 20, 1, 11, 10, 6, False),
"Buzz Buzz": EarthBoundEnemy("Buzz Buzz", 0x15e47b, 2000, 999, 0, 0, 100, 40, 92, 20, False),
"Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15e4d9, 2000, 999, 0, 0, 60, 145, 255, 80, False),
#"Heavily Armed Pokey": EarthBoundEnemy("Heavily Armed Pokey", 0x15e537, 1746, 999, 0, 0, 51, 150, 274, 72, False), Cutscene?
"Giygas (2)": EarthBoundEnemy("Giygas", 0x15e595, 9999, 999, 0, 0, 80, 255, 255, 80, False),
"Giygas (3)": EarthBoundEnemy("Giygas", 0x15e5f3, 9999, 0, 0, 0, 80, 255, 255, 80, False),
"Giygas (4)": EarthBoundEnemy("Giygas", 0x15e651, 2000, 0, 0, 0, 80, 255, 255, 80, False),
"Giygas (5)": EarthBoundEnemy("Giygas", 0x15e6af, 9999, 0, 0, 0, 80, 255, 255, 80, False),
"Farm Zombie": EarthBoundEnemy("Farm Zombie", 0x15e70d, 171, 0, 700, 58, 10, 31, 24, 19, False),
"Criminal Caterpillar": EarthBoundEnemy("Criminal Caterpillar", 0x15e76b, 250, 168, 30384, 0, 134, 37, 16, 23, False),
"Evil Eye": EarthBoundEnemy("Evil Eye", 0x15e7c9, 720, 400, 46376, 896, 38, 141, 162, 63, False),
#"Magic Butterfly": EarthBoundEnemy("Magic Butterfly", 0x15e827, 16, 0, 1, 0, 25, 2, 2, 0, False),
"Mini Barf": EarthBoundEnemy("Mini Barf", 0x15e885, 616, 0, 7521, 460, 10, 45, 71, 26, False),
"Master Criminal Worm": EarthBoundEnemy("Master Criminal Worm", 0x15e8e3, 377, 300, 82570, 0, 136, 73, 40, 37, False),
"Captain Strong": EarthBoundEnemy("Captain Strong", 0x15e941, 140, 0, 492, 159, 15, 20, 24, 13, False),
"Giygas (6)": EarthBoundEnemy("Giygas", 0x15e99f, 9999, 0, 0, 0, 80, 255, 127, 80, False),
"Clumsy Robot (3)": EarthBoundEnemy("Clumsy Robot", 0x15e9fd, 962, 0, 32378, 2081, 83, 88, 137, 46, False),
}


regional_enemies = {"Northern Onett": {enemies["Spiteful Crow"], enemies["Runaway Dog"], enemies["Coil Snake"]},
                    "Onett": {enemies["Pogo Punk"], enemies["Skate Punk"], enemies["Yes Man Junior"], enemies["Frank"], enemies["Frankystein Mark II"]},
                    "Giant Step": {enemies["Attack Slug"], enemies["Black Antoid"], enemies["Black Antoid (2)"], enemies["Rowdy Mouse"], enemies["Titanic Ant"]},
                    "Twoson": {enemies["Black Antoid"], enemies["Cop"], enemies["Captain Strong"], enemies["Ramblin' Evil Mushroom"], 
                               enemies["Annoying Old Party Man"], enemies["Cranky Lady"], enemies["Mobile Sprout"], enemies["New Age Retro Hippie"], enemies["Unassuming Local Guy"]},
                    "Everdred's House": {enemies["Everdred"]},
                    "Peaceful Rest Valley": {enemies["Li'l UFO"], enemies["Mobile Sprout"], enemies["Spinning Robo"], enemies["Territorial Oak"]},
                    "Happy-Happy Village": {enemies["Coil Snake"], enemies["Insane Cultist"], enemies["Spiteful Crow"], enemies["Unassuming Local Guy"], enemies["Mr. Carpainter"]},
                    "Lilliput Steps": {enemies["Mighty Bear"], enemies["Mole Playing Rough"], enemies["Mr. Batty"], enemies["Mondo Mole"]},
                    "Threed": {enemies["Coil Snake"], enemies["Handsome Tom"], enemies["Smilin' Sam"], enemies["Trick or Trick Kid"],
                               enemies["Boogey Tent"], enemies["Zombie Dog"], enemies["Putrid Moldyman"], enemies["Smelly Ghost"], enemies["Boogey Tent (2)"]},
                    "Threed Underground": {enemies["No Good Fly"], enemies["Urban Zombie"], enemies["Zombie Possessor"], enemies["Mini Barf"]},
                    "Grapefruit Falls": {enemies["Armored Frog"], enemies["Black Antoid"], enemies["Coil Snake"], enemies["Farm Zombie"],
                                         enemies["Plain Crocodile"], enemies["Red Antoid"], enemies["Violent Roach"], enemies["Mad Duck"]},
                    "Belch's Factory": {enemies["Farm Zombie"], enemies["Foppy"], enemies["Mostly Bad Fly"], enemies["Slimy Little Pile"], enemies["Master Belch"], enemies["Master Belch (2)"]},
                    "Milky Well": {enemies["Mad Duck"], enemies["Ranboob"], enemies["Struttin' Evil Mushroom (2)"], enemies["Tough Mobile Sprout"], enemies["Trillionage Sprout"]},
                    "Dusty Dunes Desert": {enemies["Bad Buffalo"], enemies["Crested Booka"], enemies["Criminal Caterpillar"], enemies["Cute Li'l UFO"], enemies["Desert Wolf"], enemies["Mole Playing Rough"],
                                           enemies["Skelpion"], enemies["Smilin' Sphere"]},
                    "Fourside": {enemies["Annoying Reveler"], enemies["Crazed Sign"], enemies["Extra Cranky Lady"], enemies["Mad Taxi"],
                                 enemies["Abstract Art"], enemies["Dali's Clock"], enemies["Enraged Fire Plug"], enemies["Robo-pump"], enemies["Evil Mani-Mani"]},
                    "Gold Mine": {enemies["Gigantic Ant"], enemies["Mad Duck"], enemies["Noose Man"], enemies["Thirsty Coil Snake"], enemies["Guardian Digger"], enemies["Guardian Digger (2)"]},
                    "Fourside Dept. Store": {enemies["Musica"], enemies["Mystical Record"], enemies["Scalding Coffee Cup"], enemies["Dept. Store Spook"], enemies["Dept. Store Spook (2)"]},
                    "Monkey Caves": {enemies["Struttin' Evil Mushroom (2)"], enemies["Tough Mobile Sprout"]},
                    "Monotoli Building": {enemies["Sentry Robot"], enemies["Clumsy Robot"], enemies["Clumsy Robot (2)"], enemies["Clumsy Robot (3)"]},
                    "Rainy Circle": {enemies["Arachnid!"], enemies["Cave Boy"], enemies["Elder Batty"], enemies["Mighty Bear Seven"], enemies["Strong Crocodile"], enemies["Shrooom!"]},
                    "Summers": {enemies["Crazed Sign"], enemies["Mad Taxi"], enemies["Mole Playing Rough"], enemies["Over Zealous Cop"], enemies["Tough Guy"], enemies["Kraken"], enemies["Kraken (2)"]},
                    "Summers Museum": {enemies["Shattered Man"]},
                    "Magnet Hill": {enemies["Deadly Mouse"], enemies["Filthy Attack Roach"], enemies["Stinky Ghost"], enemies["Plague Rat of Doom"]},
                    "Pink Cloud": {enemies["Conducting Menace"], enemies["Kiss of Death"], enemies["Tangoo"], enemies["Thunder Mite"], enemies["Thunder and Storm"]},
                    "Scaraba": {enemies["Beautiful UFO"], enemies["Dread Skelpion"], enemies["Great Crested Booka"], enemies["High-class UFO"], enemies["Master Criminal Worm"]},
                    "Pyramid": {enemies["Arachnid!!!"], enemies["Fierce Shattered Man"], enemies["Guardian Hieroglyph"], enemies["Lethal Asp Hieroglyph"], enemies["Petrified Royal Guard"],
                                enemies["Guardian General"], enemies["Guardian General (2)"]},
                    "Southern Scaraba": {enemies["Beautiful UFO"], enemies["High-class UFO"], enemies["Marauder Octobot"]},
                    "Dungeon Man": {enemies["Dali's Clock"], enemies["Mystical Record"], enemies["Lesser Mook"], enemies["Mystical Record"], enemies["Scalding Coffee Cup"], enemies["Worthless Protoplasm"]},
                    "Deep Darkness": {enemies["Mole Playing Rough"]},
                    "Deep Darkness Darkness": {enemies["Big Pile of Puke"], enemies["Demonic Petunia"], enemies["Even Slimier Little Pile"], enemies["Hard Crocodile"], enemies["Hostile Elder Oak"],
                                               enemies["Manly Fish"], enemies["Manly Fish's Brother"], enemies["Pit Bull Slug"], enemies["Zap Eel"], enemies["Master Barf"]},
                    "Winters": {enemies["Lesser Mook"], enemies["Whirling Robo"], enemies["Wooly Shambler"]},
                    "Southern Winters": {enemies["Rowdy Mouse"], enemies["Worthless Protoplasm"], enemies["Mad Duck"]},
                    "Stonehenge Base": {enemies["Atomic Power Robot"], enemies["Military Octobot"], enemies["Mook Senior"], enemies["Starman"], enemies["Starman Super"], enemies["Starman Deluxe"], enemies["Starman Super (2)"]},
                    "Lumine Hall": {enemies["Conducting Spirit"], enemies["Fobby"], enemies["Hyper Spinning Robo"], enemies["Uncontrollable Sphere"], enemies["Electro Specter"]},
                    "Lost Underworld": {enemies["Chomposaur"], enemies["Chomposaur (2)"], enemies["Ego Orb"], enemies["Wetnosaur"]},
                    "Fire Spring": {enemies["Evil Elemental"], enemies["Major Psychic Psycho"], enemies["Psychic Psycho"], enemies["Soul Consuming Flame"], enemies["Carbon Dog"], enemies["Diamond Dog"]},
                    "Magicant": {enemies["Care Free Bomb"], enemies["Electro Swoosh"], enemies["French Kiss of Death"], enemies["Loaded Dice"], enemies["Mr. Molecule"], enemies["Uncontrollable Sphere"],
                                 enemies["Fobby"], enemies["Beautiful UFO"], enemies["High-class UFO"], enemies["Kraken"], enemies["Ness's Nightmare"], enemies["Ness's Nightmare (2)"], enemies["Kraken (2)"]},
                    "Cave of the Past": {enemies["Bionic Kraken"], enemies["Final Starman"], enemies["Ghost of Starman"], enemies["Nuclear Reactor Robot"], enemies["Squatter Demon"],
                                         enemies["Ultimate Octobot"], enemies["Wild 'n Wooly Shambler"], enemies["Final Starman (2)"], enemies["Ghost of Starman (2)"]},
                    "Endgame": {enemies["Heavily Armed Pokey"], enemies["Giygas (1)"], enemies["Giygas (2)"], enemies["Giygas (3)"], enemies["Giygas (4)"], enemies["Giygas (5)"], enemies["Giygas (6)"]},
                    
}

combat_regions = [
    "Northern Onett",
    "Onett",
    "Giant Step",
    "Twoson",
    "Happy-Happy Village",
    "Lilliput Steps",
    "Threed",
    "Winters",
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
    "Threed Underground"
]

levels = [
1,
2,
3,
5,
7,
9,
10,
12,
13,
14,
15,
17,
18,
19,
21,
23,
24,
25,
26,
28,
29,
31,
32,
33,
36,
38,
39,
42,
43,
45,
47,
49,
52,
56,
59,
65,
69,
70,
73]

spell_breaks: Dict[str, Dict[int, str]] = {
    "freeze": {30: "alpha", 50: "beta", 70: "gamma", 100: "omega"},
    "fire": {20: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "lifeup": {20: "alpha", 40: "beta", 60: "gamma", 100: "omega"},
    "thunder": {20: "alpha", 30: "beta", 50: "gamma", 100: "omega"},
    "flash": {25: "alpha", 45: "beta", 60: "gamma", 100: "omega"},
    "special": {25: "alpha", 30: "beta", 40: "gamma", 100: "omega"},
    "healing": {20: "alpha", 40: "beta", 60: "gamma", 100: "omega"},
    "starstorm": {50: "alpha", 100: "beta"},
}

def get_psi_levels(level: int, breaks: Dict[int, str]) -> str:
    for top_val, psi_level in breaks.items():
        if level <= top_val:
            return psi_level


enemy_psi = {
    "Dept. Store Spook": ["freeze", "fire", "lifeup", "null"],
    "Dept. Store Spook (2)": ["null", "null", "freeze", "null"],
    "Black Antoid": ["null", "null", "null", "lifeup"],
    "Mobile Sprout": ["null", "null", "null", "lifeup"],
    "Tough Mobile Sprout": ["null", "null", "null", "lifeup"],
    "Mystical Record": ["null", "null", "lifeup", "null"],
    "Guardian Hieroglyph": ["null", "thunder", "flash", "thunder"],
    "Conducting Menace": ["flash", "flash", "thunder", "thunder"],
    "Conducting Spirit": ["flash", "flash", "thunder", "thunder"],
    "Ness's Nightmare": ["null", "special", "null", "null"],
    "Mr. Carpainter": ["null", "lifeup", "null", "null"],
    "Thunder Mite": ["thunder", "thunder", "thunder", "thunder"],
    "Chomposaur": ["fire", "fire", "null", "null"],
    "Shrooom!": ["null", "lifeup", "null", "null"],
    "Mondo Mole": ["lifeup", "null", "null", "null"],
    "Wooly Shambler": ["null", "null", "null", "flash"],
    "Wild 'n Wooly Shambler": ["null", "null", "null", "flash"],
    "Skelpion": ["null", "null", "null", "thunder"],
    "Dread Skelpion": ["null", "null", "thunder", "thunder"],
    "Ghost of Starman": ["starstorm", "null", "null", "null"],
    "Smilin' Sphere": ["null", "fire", "null", "null"],
    "Uncontrollable Sphere": ["null", "fire", "fire", "null"],
    "Starman Deluxe": ["null", "null", "starstorm", "null"],
    "Final Starman": ["null", "null", "starstorm", "null"],
    "Trillionage Sprout": ["null", "null", "flash", "null"],
    "Lesser Mook": ["freeze", "freeze", "null", "null"],
    "Mook Senior": ["freeze", "fire", "lifeup", "null"],
    "Smelly Ghost": ["null", "null", "lifeup", "null"],
    "Smilin' Sam": ["null", "null", "null", "lifeup"],
    "Manly Fish's Brother": ["null", "null", "freeze", "healing"],
    "Cute Li'l UFO": ["null", "null", "null", "lifeup"],
    "Beautiful UFO": ["null", "null", "null", "lifeup"],
    "Mr. Molecule": ["thunder", "flash", "fire", "freeze"],
    "Heavily Armed Pokey": ["null", "fire", "null", "null"],
    "Psychic Psycho": ["fire", "fire", "fire", "fire"],
    "Major Psychic Psycho": ["fire", "null", "null", "fire"],
    "Ness's Nightmare (2)": ["special", "lifeup", "special", "null"],
    "Chomposaur (2)": ["null", "null", "fire", "fire"],
    "Guardian Digger (2)": ["null", "null", "null", "lifeup"],
    "Kraken (2)": ["flash", "null", "null", "null"],
    "Starman Super (2)": ["null", "healing", "null", "null"],
    "Ghost of Starman (2)": ["null", "null", "starstorm", "null"],
    "Final Starman (2)": ["starstorm", "null", "healing", "null"],
    "Boogey Tent (2)": ["null", "null", "flash", "null"],
    "Black Antoid (2)": ["lifeup", "lifeup", "lifeup", "lifeup"],
    "Giygas (1)": ["special", "special", "special", "special"],
    "Criminal Caterpillar": ["fire", "fire", "fire", "fire"],
    "Master Criminal Worm": ["fire", "fire", "fire", "fire"]
}

spell_data = {
    "freeze": {
        "alpha": [0x12, 0x09],
        "beta": [0x13, 0x0A],
        "gamma": [0x14, 0x0B],
        "omega": [0x15, 0x0C]
    },
    "fire": {
        "alpha": [0x0E, 0x05],
        "beta": [0x0F, 0x06],
        "gamma": [0x10, 0x07],
        "omega": [0x11, 0x08]
    },
    "lifeup": {
        "alpha": [0x20, 0x17],
        "beta": [0x21, 0x18],
        "gamma": [0x22, 0x19],
        "omega": [0x23, 0x1A]
    },
    "flash": {
        "alpha": [0x1A, 0x11],
        "beta": [0x1B, 0x12],
        "gamma": [0x1C, 0x13],
        "omega": [0x1D, 0x14]
    },
    "thunder": {
        "alpha": [0x16, 0x0D],
        "beta": [0x17, 0x0E],
        "gamma": [0x18, 0x0F],
        "omega": [0x19, 0x10]
    },
    "special": {
        "alpha": [0x0A, 0x01],
        "beta": [0x0B, 0x02],
        "gamma": [0x0C, 0x03],
        "omega": [0x0D, 0x04]
    },
    "healing": {
        "alpha": [0x24, 0x1B],
        "beta": [0x25, 0x1C],
        "gamma": [0x26, 0x1D],
        "omega": [0x27, 0x1E]
    },
    "starstorm": {
        "alpha": [0x1E, 0x15],
        "beta": [0x1F, 0x16]
    }

}



def scale_enemies(world, rom):
    state = world.multiworld.get_all_state(True)
    distances: Dict[str, int] = {}
    for region in world.multiworld.get_regions(world.player):
        if region.name != "Menu":
            connected, connection = state.path[region]
            distance = 0
            while connection is not None:
                if not any(connected == entrance.name for entrance in world.multiworld.get_entrances(world.player)):
                    distance += 1
                connected, connection = connection
            distances[region.name] = distance

    paths = state.path
    location_order = []
    location_test = []
    for i, sphere in enumerate(world.multiworld.get_spheres()):
        locs = [loc for loc in sphere if loc.player == world.player and loc.parent_region.name in combat_regions and loc.parent_region.name not in location_order]
        regions = {loc.parent_region.name for loc in locs}
        location_order.extend(sorted(regions, key=lambda x: distances[x]))
    if world.options.magicant_mode == 2:
        location_order.remove ("Magicant")
        location_order.insert(location_order.index("Endgame") + 1, "Magicant")

    for region, level in zip(location_order, levels):
        for enemy in regional_enemies[region]:
            if enemy.is_scaled == False:
                enemy_hp = int(enemy.hp * level / enemy.level)
                enemy_pp = int(enemy.pp * level / enemy.level)
                enemy_exp = int(enemy.exp * level / enemy.level)
                enemy_exp = int(enemy_exp * world.options.experience_modifier.value / 100)
                enemy_money = int(enemy.money * level / enemy.level)
                enemy_speed = min(int(enemy.speed * level / enemy.level), 255)
                enemy_offense = int(enemy.offense * level / enemy.level)
                enemy_defense = int(enemy.defense * level / enemy.level)
                enemy_level = int(enemy.level * level / enemy.level)

                #print(f"\nEnemy: {enemy.name}\nLevel: {enemy_level}\nHP: {enemy_hp}\nPP: {enemy_pp}\nEXP: {enemy_exp}\n${enemy_money}\nSpeed: {enemy_speed}\nOffense: {enemy_offense}\nDefense: {enemy_defense}\nSpeed: {enemy_speed}")
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
                
                if enemy.name in enemy_psi:
                    for index, spell in enumerate([i for i in enemy_psi[enemy.name] if i != "null"]):
                        psi_level = get_psi_levels(level, spell_breaks[spell])
                        rom.write_bytes(enemy.address + 70 + (index * 2), bytearray([spell_data[spell][psi_level][0]]))
                        rom.write_bytes(enemy.address + 80 + index, bytearray([spell_data[spell][psi_level][1]]))
                        #print(f"{spell} {psi_level} at {hex(enemy.address + 70 + (index * 2))}")
                enemy.is_scaled = True