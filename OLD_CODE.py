from rich.traceback import install
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import qdarktheme
import sys
from AsyncioPySide6 import AsyncioPySide6
import aiohttp

install()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setFixedSize(1280, 720)

        self.main_widget = QFrame(self)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.setCentralWidget(self.main_widget)

        self.title_box = QTextEdit()
        self.description_box = QTextEdit()

        for edit in [self.title_box, self.description_box]:
            edit.setReadOnly(True)
            edit.setStyleSheet("background-color: #1e1e1e; color: white;")
            edit.setFont(QFont("Jetbrains Mono", 12))

        self.main_layout.addWidget(self.title_box)
        self.main_layout.addWidget(self.description_box)

        self.main_layout.setStretch(0, 10)
        self.main_layout.setStretch(1, 90)

    def keyPressEvent(self, event: QKeyEvent, /) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()

        if event.key() == Qt.Key.Key_V:
            self.paste()

        return super().keyPressEvent(event)

    def paste(self):

        clipboard = QGuiApplication.clipboard()
        text = clipboard.text()
        columns = text.split("\t")
        print("pasting:", text)

        level_id = columns[2].split("/")[-1]
        AsyncioPySide6.runTask(self.scoresaber_call(level_id, columns))

    async def scoresaber_call(self, level_id, columns):
        print("calling ss")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://scoresaber.com/api/leaderboard/by-id/{level_id}/info"
            ) as r:
                data = await r.json()
                await self.beatsaver_call(data["songHash"], columns)

    async def beatsaver_call(self, song_hash, columns):
        print("calling bs")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.beatsaver.com/maps/hash/{song_hash}"
            ) as r:
                data = await r.json()

                map_download_link = f"https://beatsaver.com/maps/{data['id']}"

                md = data["metadata"]
                map_name, map_author, artist = (
                    md["songName"],
                    md["levelAuthorName"],
                    md["songAuthorName"],
                )

                name = columns[3].title()
                achievement = columns[4].title()
                twitch = columns[5]
                youtube = columns[6]
                special = columns[8]

                self.title_box.setText(
                    f"Beat Saber | {name} | {map_name} | {artist} | {map_author} | {achievement}"
                )

                self.description_box.setText(
                    f"Beat Saber Challenge Community\n"
                    f"Player: {name}\n"
                    f"Special Note: {special}\n\n"
                    f"Their YT: {youtube}\n"
                    f"Their Twitch: {twitch}\n"
                    f"Map Download: {map_download_link}\n"
                    """
 If you would like to get featured here because you think you did some sort of crazy challenge map of some sort, message me on discord, mid1203, or check out the server to submit something or use this link to submit something - https://docs.google.com/forms/d/e/1FAIpQLSfjQ3j9SADfmQZauwUuGu7CSLLMuL9rvoIRtF0tvXksr8Ya0g/viewform

Socials:
BSCC Discord Server: https://discord.gg/NEuqTsGeSv
Twitter: https://twitter.com/MidWdg
Twitch: https://www.twitch.tv/wdg_mid


Title: Player - Map name - Song Author - Mapper - Rank - Some sort of skillful Modification"""
                )


app = QApplication(sys.argv)
with AsyncioPySide6.use_asyncio():
    w = MainWindow()
    qdarktheme.load_stylesheet()
    w.show()
    sys.exit(app.exec())
