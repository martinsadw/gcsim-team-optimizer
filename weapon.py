def upgrade_weapons(weapons_data):
    for weapons_type in weapons_data.values():
        for weapon in weapons_type:
            weapon['level'] = 90
            weapon['max_level'] = 90
            weapon['ascension'] = 6
