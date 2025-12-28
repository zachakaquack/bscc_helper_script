from typing import List, Optional, Tuple
from row import Row
import leaderboards


def get_input() -> Optional[List[str]]:
    while True:
        print("Enter row (type [help] for help):")
        items_string = input(">: ")

        if "\t" not in items_string:
            print("Invalid Row!")
            return None

        items = items_string.split("\t")
        return items


def construct(row: Row, info: dict) -> Tuple[str, str]:

    name = row.player_submitted_name.title()
    map_name = info["song"]["name"]
    artist = info["song"]["author"]
    mapper = info["song"]["mapper"]
    submission_note = row.submission_note
    special_note = row.special_note
    youtube = row.youtube_link
    twitch = row.twitch_link
    map_download_link = f"https://beatsaver.com/maps/{info['song']['id']}"

    title = (
        f"Beat Saber | {name} | {map_name} | {artist} | {mapper} | {submission_note}"
    )
    description = f"Beat Saber Challenge Community\n"
    description += f"Player: {name}\n"
    description += f"Special Note: {special_note}\n\n"

    # mid always submits "no.com" and im not supposed to include it
    if not name.lower() == "mid":
        description += f"Their YT: {youtube}\n"
        description += f"Their Twitch: {twitch}\n"

    description += f"Map Download: {map_download_link}\n"

    # ohhhh yeahhhh
    description += """
 If you would like to get featured here because you think you did some sort of crazy challenge map of some sort, message me on discord, mid1203, or check out the server to submit something or use this link to submit something - https://docs.google.com/forms/d/e/1FAIpQLSfjQ3j9SADfmQZauwUuGu7CSLLMuL9rvoIRtF0tvXksr8Ya0g/viewform

Socials:
BSCC Discord Server: https://discord.gg/NEuqTsGeSv
Twitter: https://twitter.com/MidWdg
Twitch: https://www.twitch.tv/wdg_mid


Title: Player - Map name - Song Author - Mapper - Rank - Some sort of skillful Modification"""

    return title, description


def main():

    while True:
        items: Optional[List[str]] = get_input()
        if not items:
            continue

        break

    # awesome python quirk where it remains in scope :trollface:
    row: Row = Row(items)

    leaderboard_type: leaderboards.LeaderboardType = leaderboards.get_leaderboard_type(
        row.leaderboard_link
    )
    map_id: Optional[str] = leaderboards.get_map_id(
        row.leaderboard_link, leaderboard_type
    )
    if not map_id:
        print("Cannot Parse Link:", row.leaderboard_link)
        return

    map_json: Optional[dict] = leaderboards.get_map_info(map_id)
    if not map_json:
        print("Cannot call beatleader for some reason on id:", map_id)
        return

    title, description = construct(row, map_json)

    print("\n\n")
    print(title)
    print("\n")
    print(description)


if __name__ == "__main__":
    main()
