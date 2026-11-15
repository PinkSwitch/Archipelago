def place_static_items(world) -> None:
    world.get_location("Dracula Battle").place_locked_item(world.create_item("Dracula Defeated"))