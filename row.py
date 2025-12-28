from dataclasses import dataclass
from typing import Optional


@dataclass
class Row:
    def __init__(self, items: list[str]):
        # date
        self.date: str = "no"

        # google drive link
        self.video_link: str

        # leaderboard link
        self.leaderboard_link: str

        # player name (usually discord name, sometimes not their preferred name)
        self.player_submitted_name: str

        # submission note for the editors / title
        self.submission_note: str

        # twitch
        self.twitch_link: str

        # youtube
        self.youtube_link: str

        # no longer used field (either "Short" or "Normal Video")
        self._is_short_or_normal: str

        # special note that goes in the description
        self.special_note: str

        # is map showcase (either "Yes" or "No")
        self.is_map_showcase: str

        # map for mid to play: not required in submission
        self.map_for_mid: Optional[str]

        # any extra notes or anything
        # for some reason, the sheet goes all the way to "r"; or 18 columns
        # everything past "m" (13 columns) is unused
        # though, the extra note ("often prefixed with 'zach - '") is
        # normally in column "l", or 12th column
        self.extra: list[str]

        self._parse(items)

    def _parse(self, items: list[str]) -> bool:
        if len(items) < 11:
            return False

        # banger alert
        (
            self.date,
            self.video_link,
            self.leaderboard_link,
            self.player_submitted_name,
            self.submission_note,
            self.twitch_link,
            self.youtube_link,
            self._is_short_or_normal,
            self.special_note,
            self.is_map_showcase,
            self.map_for_mid,
            *self.extra,
        ) = items

        # print(items)

        return True
