from ..game_data.local_data import psi_item_table, character_item_table, special_name_table, item_id_table
import struct

shop_locations = {
"Onett Drugstore - Right Counter Slot 1",
"Onett Drugstore - Right Counter Slot 2",
"Onett Drugstore - Right Counter Slot 3",
"Onett Drugstore - Right Counter Slot 4",
"Onett Drugstore - Right Counter Slot 5",
"Onett Drugstore - Left Counter",
"Summers - Beach Cart",
"Onett Burger Shop - Slot 1",
"Onett Burger Shop - Slot 2",
"Onett Burger Shop - Slot 3",
"Onett Burger Shop - Slot 4",
"Onett Bakery - Slot 1",
"Onett Bakery - Slot 2",
"Onett Bakery - Slot 3",
"Onett Bakery - Slot 4",
"Twoson Department Store Burger Shop - Slot 1",
"Twoson Department Store Burger Shop - Slot 2",
"Twoson Department Store Burger Shop - Slot 3",
"Twoson Department Store Burger Shop - Slot 4",
"Twoson Department Store Bakery - Slot 1",
"Twoson Department Store Bakery - Slot 2",
"Twoson Department Store Bakery - Slot 3",
"Twoson Department Store Bakery - Slot 4",
"Twoson Department Store Top Floor - Right Counter Slot 1",
"Twoson Department Store Top Floor - Right Counter Slot 2",
"Twoson Department Store Top Floor - Right Counter Slot 3",
"Twoson Department Store Top Floor - Right Counter Slot 4",
"Twoson Department Store Top Floor - Right Counter Slot 5",
"Twoson Department Store Top Floor - Right Counter Slot 6",
"Twoson Department Store Top Floor - Left Counter Slot 1",
"Summers - Magic Cake Cart Shop Slot",
"Burglin Park Junk Shop - Slot 1",
"Burglin Park Junk Shop - Slot 2",
"Burglin Park Junk Shop - Slot 3",
"Burglin Park Junk Shop - Slot 4",
"Burglin Park Junk Shop - Slot 5",
"Burglin Park Junk Shop - Slot 6",
"Burglin Park Bread Stand - Slot 1",
"Burglin Park Bread Stand - Slot 2",
"Burglin Park Bread Stand - Slot 3",
"Burglin Park Bread Stand - Slot 4",
"Burglin Park Bread Stand - Slot 5",
"Burglin Park Bread Stand - Slot 6",
"Burglin Park - Banana Stand",
"Happy-Happy Village Drugstore - Right Counter Slot 1",
"Happy-Happy Village Drugstore - Right Counter Slot 2",
"Happy-Happy Village Drugstore - Right Counter Slot 3",
"Happy-Happy Village Drugstore - Right Counter Slot 4",
"Happy-Happy Village Drugstore - Right Counter Slot 5",
"Threed Drugstore - Right Counter Slot 1",
"Threed Drugstore - Right Counter Slot 2",
"Threed Drugstore - Right Counter Slot 3",
"Threed Drugstore - Right Counter Slot 4",
"Threed Drugstore - Right Counter Slot 5",
"Threed Drugstore - Left Counter Slot 1",
"Threed Drugstore - Left Counter Slot 2",
"Threed Drugstore - Left Counter Slot 3",
"Threed Drugstore - Left Counter Slot 4",
"Threed Drugstore - Left Counter Slot 5",
"Threed - Arms Dealer Slot 1",
"Threed - Arms Dealer Slot 2",
"Threed - Arms Dealer Slot 3",
"Threed - Arms Dealer Slot 4",
"Threed Bakery - Slot 1",
"Threed Bakery - Slot 2",
"Threed Bakery - Slot 3",
"Threed Bakery - Slot 4",
"Threed Bakery - Slot 5",
"Threed Bakery - Slot 6",
"Threed Bakery - Slot 7",
"Scaraba - Expensive Water Guy",
"Winters Drugstore - Slot 1",
"Winters Drugstore - Slot 2",
"Winters Drugstore - Slot 3",
"Winters Drugstore - Slot 4",
"Winters Drugstore - Slot 5",
"Winters Drugstore - Slot 6",
"Winters Drugstore - Slot 7",
"Saturn Valley Shop - Center Saturn Slot 1",
"Saturn Valley Shop - Center Saturn Slot 2",
"Saturn Valley Shop - Center Saturn Slot 3",
"Saturn Valley Shop - Center Saturn Slot 4",
"Saturn Valley Shop - Center Saturn Slot 5",
"Dusty Dunes Drugstore - Counter Slot 1",
"Dusty Dunes Drugstore - Counter Slot 2",
"Dusty Dunes Drugstore - Counter Slot 3",
"Dusty Dunes Drugstore - Counter Slot 4",
"Dusty Dunes Drugstore - Counter Slot 5",
"Dusty Dunes - Arms Dealer Slot 1",
"Dusty Dunes - Arms Dealer Slot 2",
"Dusty Dunes - Arms Dealer Slot 3",
"Dusty Dunes - Arms Dealer Slot 4",
"Fourside Bakery - Slot 1",
"Fourside Bakery - Slot 2",
"Fourside Bakery - Slot 3",
"Fourside Bakery - Slot 4",
"Fourside Bakery - Slot 5",
"Fourside Bakery - Slot 6",
"Fourside Department Store - Tool Shop Slot 1",
"Fourside Department Store - Tool Shop Slot 2",
"Fourside Department Store - Tool Shop Slot 3",
"Fourside Department Store - Tool Shop Slot 4",
"Fourside Department Store - Tool Shop Slot 5",
"Fourside Department Store - Tool Shop Slot 6",
"Fourside Department Store - Tool Shop Slot 7",
"Fourside Department Store - Shop Shop Slot 1",
"Fourside Department Store - Shop Shop Slot 2",
"Fourside Department Store - Shop Shop Slot 3",
"Fourside Department Store - Shop Shop Slot 4",
"Fourside Department Store - Food Shop Slot 1",
"Fourside Department Store - Food Shop Slot 2",
"Fourside Department Store - Food Shop Slot 3",
"Fourside Department Store - Food Shop Slot 4",
"Fourside Department Store - Food Shop Slot 5",
"Fourside Department Store - 2F Cart Slot 1",
"Fourside Department Store - 2F Cart Slot 2",
"Fourside Department Store - 2F Cart Slot 3",
"Fourside Department Store - 2F Cart Slot 4",
"Fourside Department Store - 2F Cart Slot 5",
"Fourside Department Store - 2F Cart Slot 6",
"Fourside Department Store - 2F Cart Slot 7",
"Fourside Department Store - Toys Shop Slot 1",
"Fourside Department Store - Toys Shop Slot 2",
"Fourside Department Store - Toys Shop Slot 3",
"Fourside Department Store - Toys Shop Slot 4",
"Fourside Department Store - Toys Shop Slot 5",
"Fourside Department Store - Toys Shop Slot 6",
"Fourside Department Store - Sports Shop Slot 1",
"Fourside Department Store - Sports Shop Slot 2",
"Fourside Department Store - Sports Shop Slot 3",
"Fourside Department Store - Sports Shop Slot 4",
"Fourside Department Store - Burger Shop Slot 1",
"Fourside Department Store - Burger Shop Slot 2",
"Fourside Department Store - Burger Shop Slot 3",
"Fourside Department Store - Burger Shop Slot 4",
"Fourside Department Store - Burger Shop Slot 5",
"Fourside Department Store - Arms Dealer Slot 1",
"Fourside Department Store - Arms Dealer Slot 2",
"Fourside Department Store - Arms Dealer Slot 3",
"Fourside Department Store - Arms Dealer Slot 4",
"Fourside Department Store - Arms Dealer Slot 5",
"Fourside - Northeast Alley Junk Shop Slot 1",
"Fourside - Northeast Alley Junk Shop Slot 2",
"Fourside - Northeast Alley Junk Shop Slot 3",
"Fourside - Northeast Alley Junk Shop Slot 4",
"Magicant - Shop Slot 1",
"Magicant - Shop Slot 2",
"Summers - Scam Shop Slot 1",
"Summers - Scam Shop Slot 2",
"Summers - Scam Shop Slot 3",
"Summers - Scam Shop Slot 4",
"Summers - Scam Shop Slot 5",
"Summers - Scam Shop Slot 6",
"Summers - Scam Shop Slot 7",
"Summers Harbor - Shop Slot 1",
"Summers Harbor - Shop Slot 2",
"Summers Harbor - Shop Slot 3",
"Summers Harbor - Shop Slot 4",
"Summers Harbor - Shop Slot 5",
"Summers Harbor - Shop Slot 6",
"Summers Harbor - Shop Slot 7",
"Summers Restaurant - Slot 1",
"Summers Restaurant - Slot 2",
"Summers Restaurant - Slot 3",
"Summers Restaurant - Slot 4",
"Summers Restaurant - Slot 5",
"Summers Restaurant - Slot 6",
"Scaraba - Indoors Shop Slot 1",
"Scaraba - Indoors Shop Slot 2",
"Scaraba - Indoors Shop Slot 3",
"Scaraba - Indoors Shop Slot 4",
"Scaraba - Indoors Shop Slot 5",
"Scaraba - Indoors Shop Slot 6",
"Scaraba Bazaar - Red Snake Carpet Slot 1",
"Scaraba Bazaar - Red Snake Carpet Slot 2",
"Scaraba Bazaar - Red Snake Carpet Slot 3",
"Scaraba Bazaar - Bottom Left Carpet Slot 1",
"Scaraba Bazaar - Bottom Left Carpet Slot 2",
"Scaraba Bazaar - Bottom Left Carpet Slot 3",
"Scaraba Bazaar - Bottom Left Carpet Slot 4",
"Scaraba Bazaar - Bottom Left Carpet Slot 5",
"Scaraba Bazaar - Bottom Left Carpet Slot 6",
"Scaraba Hotel - Arms Dealer Slot 1",
"Scaraba Hotel - Arms Dealer Slot 2",
"Scaraba Hotel - Arms Dealer Slot 3",
"Scaraba Hotel - Arms Dealer Slot 4",
"Deep Darkness - Businessman Slot 1",
"Deep Darkness - Businessman Slot 2",
"Deep Darkness - Businessman Slot 3",
"Deep Darkness - Businessman Slot 4",
"Deep Darkness - Businessman Slot 5",
"Deep Darkness - Businessman Slot 6",
"Deep Darkness - Businessman Slot 7",
"Happy-Happy Village - Trust Shop Slot 1",
"Happy-Happy Village - Trust Shop Slot 2",
"Saturn Valley Shop - Post-Belch Saturn Slot 1",
"Saturn Valley Shop - Post-Belch Saturn Slot 2",
"Saturn Valley Shop - Post-Belch Saturn Slot 3",
"Saturn Valley Shop - Post-Belch Saturn Slot 4",
"Scaraba - Southern Camel Shop Slot 1",
"Scaraba - Southern Camel Shop Slot 2",
"Scaraba - Southern Camel Shop Slot 3",
"Scaraba - Southern Camel Shop Slot 4",
"Scaraba - Southern Camel Shop Slot 5",
"Scaraba - Southern Camel Shop Slot 6",
"Scaraba - Southern Camel Shop Slot 7",
"Deep Darkness - Arms Dealer Slot 1",
"Deep Darkness - Arms Dealer Slot 2",
"Deep Darkness - Arms Dealer Slot 3",
"Deep Darkness - Arms Dealer Slot 4",
"Lost Underworld - Tenda Camp Shop Slot 1",
"Lost Underworld - Tenda Camp Shop Slot 2",
"Lost Underworld - Tenda Camp Shop Slot 3",
"Lost Underworld - Tenda Camp Shop Slot 4",
"Lost Underworld - Tenda Camp Shop Slot 5",
"Lost Underworld - Tenda Camp Shop Slot 6",
"Lost Underworld - Tenda Camp Shop Slot 7",
"Happy-Happy Village Drugstore - Left Counter Slot 1",
"Happy-Happy Village Drugstore - Left Counter Slot 2",
"Happy-Happy Village Drugstore - Left Counter Slot 3",
"Happy-Happy Village Drugstore - Left Counter Slot 4",
"Happy-Happy Village Drugstore - Left Counter Slot 5",
"Happy-Happy Village Drugstore - Left Counter Slot 6",
"Happy-Happy Village Drugstore - Left Counter Slot 7",
"Grapefruit Falls - Hiker Shop Slot 1",
"Grapefruit Falls - Hiker Shop Slot 2",
"Grapefruit Falls - Hiker Shop Slot 3",
"Saturn Valley Shop - Top Saturn Slot 1",
"Saturn Valley Shop - Top Saturn Slot 2",
"Saturn Valley Shop - Top Saturn Slot 3",
"Saturn Valley Shop - Top Saturn Slot 4",
"Saturn Valley Shop - Top Saturn Slot 5",
"Saturn Valley Shop - Top Saturn Slot 6",
"Saturn Valley Shop - Top Saturn Slot 7",
"Dusty Dunes Drugstore - Left Shop Slot 1",
"Dusty Dunes Drugstore - Left Shop Slot 2",
"Dusty Dunes Drugstore - Left Shop Slot 3",
"Dusty Dunes Drugstore - Left Shop Slot 4",
"Dusty Dunes Drugstore - Left Shop Slot 5",
"Dusty Dunes Drugstore - Left Shop Slot 6",
"Dusty Dunes Drugstore - Left Shop Slot 7",
"Dusty Dunes - Mine Food Cart Slot 1",
"Dusty Dunes - Mine Food Cart Slot 2",
"Dusty Dunes - Mine Food Cart Slot 3",
"Dusty Dunes - Mine Food Cart Slot 4",
"Dusty Dunes - Mine Food Cart Slot 5",
"Dusty Dunes - Mine Food Cart Slot 6",
"Dusty Dunes - Mine Food Cart Slot 7",
"Moonside Hotel - Shop Slot 1",
"Moonside Hotel - Shop Slot 2",
"Moonside Hotel - Shop Slot 3",
"Moonside Hotel - Shop Slot 4",
"Moonside Hotel - Shop Slot 5",
"Dalaam Restaurant - Slot 1",
"Dalaam Restaurant - Slot 2",
"Dalaam Restaurant - Slot 3",
"Dalaam Restaurant - Slot 4",
"Scaraba Bazaar - Delicacy Shop Slot 1",
"Scaraba Bazaar - Delicacy Shop Slot 2",
"Scaraba Bazaar - Delicacy Shop Slot 3",
"Scaraba Bazaar - Delicacy Shop Slot 4",
"Scaraba Bazaar - Delicacy Shop Slot 5",
"Scaraba Bazaar - Delicacy Shop Slot 6",
"Scaraba Bazaar - Delicacy Shop Slot 7",
"Twoson/Scaraba - Shared Condiment Shop Slot 1",
"Twoson/Scaraba - Shared Condiment Shop Slot 2",
"Twoson/Scaraba - Shared Condiment Shop Slot 3",
"Twoson/Scaraba - Shared Condiment Shop Slot 4",
"Twoson/Scaraba - Shared Condiment Shop Slot 5",
"Twoson/Scaraba - Shared Condiment Shop Slot 6",
"Twoson/Scaraba - Shared Condiment Shop Slot 7",
"Andonuts Lab - Caveman Shop Slot 1",
"Andonuts Lab - Caveman Shop Slot 2",
"Andonuts Lab - Caveman Shop Slot 3",
"Andonuts Lab - Caveman Shop Slot 4",
"Andonuts Lab - Caveman Shop Slot 5"
}

def write_shop_checks(world, rom, shop_checks):
    for location in shop_checks:
        flag = location.address - 0xEB1000
        if location.item.player == world.player:
            if world.options.remote_items:
                if location.item.name in special_name_table:
                    item_type = 0x04
                    item_id = 0xAD
                else:
                    item_type = 0x05
                    item_id = item_id_table[location.item.name]
            else:
                if location.item.name in psi_item_table:
                    item_type = 0x01
                    item_id = psi_item_table[location.item.name]
                elif location.item.name in character_item_table:
                    item_type = 0x02
                    item_id = character_item_table[location.item.name][0]
                else:
                    item_type = 0x00
                    item_id = item_id_table[location.item.name] 

        else:
            item_type = 0x04
            item_id = 0xAD
        
        price = int((world.random.randint(1, 100) * (world.accessible_regions.index(location.parent_region.name) + 1)))
        item_struct = struct.pack('BHBH', item_id, price, item_type, flag)
        rom.write_bytes(0x34002A + (0x06 * flag), item_struct)
        rom.write_bytes(0x019DE5, struct.pack("Q", 0xF0077C5C))  # Build the shop menus
        rom.write_bytes(0x019E23, struct.pack("Q", 0xF008355C))  # Display the item name
        rom.write_bytes(0x019E8F, struct.pack("Q", 0xF0090B5C))  # Display the item price
        rom.write_bytes(0x011AC6, struct.pack("Q", 0xF009555C))  # Pop up a textbox displaying the player the item goes to
        rom.write_bytes(0x019EDD, struct.pack("Q", 0xF00A4B5C))  # Transfer the used data and player selection into a script for processing
        rom.write_bytes(0x019ED3, struct.pack("Q", 0xF00A7E5C))  # Display SOLD OUT for items which have been flagged as bought
        rom.write_bytes(0x019B66, struct.pack("Q", 0xF00AAC5C))  # Prevent items for other players flashing the "you can equip this"

        rom.write_bytes(0x05E0A9, struct.pack("Q", 0xF4900008))  # Compare the price of the item with money on hand
        rom.write_bytes(0x05E0B6, struct.pack("Q", 0xF4905308))  # Display the item we bought and ask to confirm
        rom.write_bytes(0x05E0CE, struct.pack("Q", 0xF492B20A))  # The player bought the item; set a flag and give it to them
        rom.write_bytes(0x05E0C8, struct.pack("Q", 0xF492B20A))  # The player bought the item; set a flag and give it to them
        rom.write_bytes(0x05DF1E, struct.pack("I", 0xF494620A))  # Prevent the game from checking inventory space if not needed
        rom.write_bytes(0x05E029, struct.pack("I", 0xF494820A))
        rom.write_bytes(0x05E1AE, struct.pack("I", 0xF4947B))  # Post-shop cleanup

#Grapefruit falls