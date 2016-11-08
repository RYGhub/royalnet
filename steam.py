def convert_sid_1_3(steamid: int, group=False):
    """Convert SteamID1 to SteamID3"""
    accuniverse = steamid % 2
    if group:
        acctype = 0x0170000000000000
    else:
        acctype = 0x0110000100000000
    accid = (steamid - acctype - accuniverse) / 2
    return accid
