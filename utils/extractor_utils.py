def pad_season_or_episode(number):
    """
    If the number is not provided, assume it is the first
    (especially for season).
    Otherwise, left-pad the season/episode number with zero. So, season "2"
    will become "02". Also, episode "5" will become "05", while episode
    "15" or "127" will remain as is.

    :param number: the number representing the season or the episode
    :return: padded number
    """
    if not str(number).strip():
        return '01'
    else:
        return str(number).zfill(2)
