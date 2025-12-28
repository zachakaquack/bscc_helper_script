from enum import Enum
from typing import Optional
from urllib.parse import urlparse
import requests


# there will often be acronyms for these:
# BL = beatleader
# SS = scoresaber
# RL = scoresaber reloaded
# BS = beat saver (not saber)
class LeaderboardType(Enum):
    # https://api.beatleader.com/swagger/index.html
    # example: https://beatleader.com/leaderboard/global/262f071/1
    BEATLEADER = 1

    # https://docs.scoresaber.com/
    # example: https://scoresaber.com/leaderboard/644634
    SCORESABER = 0

    # https://ssr-api.fascinated.cc/swagger
    # example: https://ssr.fascinated.cc/leaderboard/200648
    SCORESABER_RELOADED = 2
    UNKNOWN = 3

    # also, beatsaver.
    # https://api.beatsaver.com/docs/index.html


def get_leaderboard_type(link: str) -> LeaderboardType:
    domain = urlparse(link)
    hostname = domain.netloc.split(".")[0].lower()

    match hostname:
        case "scoresaber":
            return LeaderboardType.SCORESABER
        case "beatleader":
            return LeaderboardType.BEATLEADER
        case "ssr":
            return LeaderboardType.SCORESABER_RELOADED
    return LeaderboardType.UNKNOWN


# BL's api call is much better and more informant, and avoids a call to BS.
# the goal of this function is to try to convert any link into a map_id
def get_map_id(link: str, type: LeaderboardType) -> Optional[str]:

    if type == LeaderboardType.UNKNOWN:
        return ""

    if type == LeaderboardType.BEATLEADER:
        # sometimes the linkj has a /1 at the end of it so we have to worry
        # about that too
        map_id = link.split("/")[5]
        return map_id

    # for some fucking reason, SS does NOT provide the map code (like 1b6fc)
    # in ANY of their endpoints. so i have to get the hash, and ask BS.
    if type == LeaderboardType.SCORESABER:
        ss_id = link.split("/")[-1]

        r = requests.get(f"https://scoresaber.com/api/leaderboard/by-id/{ss_id}/info")
        if not r.ok:
            return None

        js = r.json()
        song_hash = js["songHash"]

        # now we have to call beatsaver for the actual map ID. yes, we could
        # just use this request and fill out the information, but to keep the
        # same workflow with beatleader, we just use that.
        r = requests.get(f"https://api.beatsaver.com/maps/hash/{song_hash}")
        if not r.ok:
            return ""

        js = r.json()
        map_id = js["id"]

        return map_id

    # the id's at the end of the link are (thankfully) synced with SS
    if type == LeaderboardType.SCORESABER_RELOADED:
        ss_id = link.split("/")[-1]
        r = requests.get(f"https://ssr-api.fascinated.cc/leaderboard/by-id/{ss_id}")
        if not r.ok:
            return ""
        js = r.json()
        return js["beatsaver"]["bsr"]


# gets all the relevant information from beatleader
def get_map_info(map_id) -> Optional[dict]:
    r = requests.get(f"https://api.beatleader.com/leaderboard/{map_id}")
    if not r.ok:
        return None

    js = r.json()
    return js
