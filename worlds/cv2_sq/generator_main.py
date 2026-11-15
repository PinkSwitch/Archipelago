from BaseClasses import Item, ItemClassification


class CV2Item(Item):
    game: str = "Castlevania II: Simon's Quest"


def generate_early(world) -> None:
    if hasattr(world.multiworld, "re_gen_passthrough"):  # If UT
        if "Castlevania II: Simon's Quest" not in world.multiworld.re_gen_passthrough:
            return

        passthrough = world.multiworld.re_gen_passthrough["Castlevania II: Simon's Quest"]
        world.options.dracula_parts_required.value = passthrough["drac_parts"]
        world.options.orbs_required.value = passthrough["orbs_required"]
        world.options.poison_proof_ring.value = passthrough["poison_ring"]
        world.options.inclusive_white_crystal.value = passthrough["white_crystal"]

    world.auth_id = world.random.getrandbits(32)