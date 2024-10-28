from __future__ import annotations

from datetime import datetime

from pytest_httpx import HTTPXMock

from seadex import SeaDexEntry, Tracker

SAMPLE_JSON_REPLY = {
    "page": 1,
    "perPage": 30,
    "totalItems": 1,
    "totalPages": 1,
    "items": [
        {
            "alID": 20519,
            "collectionId": "3l2x9nxip35gqb5",
            "collectionName": "entries",
            "comparison": "https://slow.pics/c/rc6qrB1F",
            "created": "2024-01-30 19:28:10.337Z",
            "expand": {
                "trs": [
                    {
                        "collectionId": "oiwizhmushn5qqh",
                        "collectionName": "torrents",
                        "created": "2024-01-30 19:28:09.110Z",
                        "dualAudio": True,
                        "files": [
                            {
                                "length": 4636316199,
                                "name": "Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv",
                            }
                        ],
                        "id": "pcpina3ekbqk7a5",
                        "infoHash": "23f77120cfdf9df8b42a10216aa33e281c58b456",
                        "isBest": True,
                        "releaseGroup": "LYS1TH3A",
                        "tracker": "Nyaa",
                        "updated": "2024-01-30 19:28:09.110Z",
                        "url": "https://nyaa.si/view/1693872",
                    },
                    {
                        "collectionId": "oiwizhmushn5qqh",
                        "collectionName": "torrents",
                        "created": "2024-01-30 19:28:09.461Z",
                        "dualAudio": True,
                        "files": [
                            {
                                "length": 4636316199,
                                "name": "Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv",
                            }
                        ],
                        "id": "tvh4fn4m2qi19n5",
                        "infoHash": "<redacted>",
                        "isBest": True,
                        "releaseGroup": "LYS1TH3A",
                        "tracker": "AnimeBytes",
                        "updated": "2024-01-30 19:28:09.461Z",
                        "url": "https://animebytes.tv/torrents.php?id=20684&torrentid=1053072",
                    },
                ]
            },
            "id": "c344w8ld7q1yppz",
            "incomplete": False,
            "notes": "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub",
            "theoreticalBest": "",
            "trs": ["pcpina3ekbqk7a5", "tvh4fn4m2qi19n5", "qhcmujh4dsw55j2", "enytf1g1cxf0k47"],
            "updated": "2024-01-30 19:28:10.337Z",
        }
    ],
}


def test_properties(seadex_entry: SeaDexEntry):
    assert seadex_entry.base_url == "https://releases.moe"


def test_from_anilist_id(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?filter=alID%3D20519&expand=trs",
        json=SAMPLE_JSON_REPLY,
    )
    entry = seadex_entry.from_id(20519)
    assert entry.anilist_id == 20519
    assert entry.collection_id == "3l2x9nxip35gqb5"
    assert entry.collection_name == "entries"
    assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
    assert isinstance(entry.created_at, datetime)
    assert entry.id == "c344w8ld7q1yppz"
    assert not entry.is_incomplete
    assert (
        entry.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert entry.theoretical_best is None
    assert entry.torrents[0].url == "https://nyaa.si/view/1693872"
    assert entry.torrents[1].url == "https://animebytes.tv/torrents.php?id=20684&torrentid=1053072"
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.torrents[0].tracker == Tracker.NYAA
    assert entry.torrents[1].tracker == Tracker.ANIMEBYTES
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert isinstance(entry.updated_at, datetime)


def test_from_seadex_id(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?filter=id='c344w8ld7q1yppz'&expand=trs",
        json=SAMPLE_JSON_REPLY,
    )
    entry = seadex_entry.from_id("c344w8ld7q1yppz")
    assert entry.anilist_id == 20519
    assert entry.collection_id == "3l2x9nxip35gqb5"
    assert entry.collection_name == "entries"
    assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
    assert isinstance(entry.created_at, datetime)
    assert entry.id == "c344w8ld7q1yppz"
    assert not entry.is_incomplete
    assert (
        entry.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert entry.theoretical_best is None
    assert entry.torrents[0].url == "https://nyaa.si/view/1693872"
    assert entry.torrents[1].url == "https://animebytes.tv/torrents.php?id=20684&torrentid=1053072"
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.torrents[0].tracker == Tracker.NYAA
    assert entry.torrents[1].tracker == Tracker.ANIMEBYTES
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert isinstance(entry.updated_at, datetime)


def test_from_title(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://graphql.anilist.co",
        json={
            "data": {"Media": {"id": 20519, "title": {"english": "Tamako -love story-", "romaji": "Tamako Love Story"}}}
        },
    )

    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?filter=alID%3D20519&expand=trs",
        json=SAMPLE_JSON_REPLY,
    )

    entry = seadex_entry.from_title("tamako love story")
    assert entry.anilist_id == 20519
    assert entry.collection_id == "3l2x9nxip35gqb5"
    assert entry.collection_name == "entries"
    assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
    assert isinstance(entry.created_at, datetime)
    assert entry.id == "c344w8ld7q1yppz"
    assert not entry.is_incomplete
    assert (
        entry.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert entry.theoretical_best is None
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.torrents[0].tracker == Tracker.NYAA
    assert entry.torrents[1].tracker == Tracker.ANIMEBYTES
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert isinstance(entry.updated_at, datetime)


def test_from_filename(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?filter=trs.files%3F~%27%22name%22%3A%22Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv%22%27&expand=trs",
        json=SAMPLE_JSON_REPLY,
    )

    entries = seadex_entry.from_filename("Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv")
    entry = tuple(entries)[0]
    assert entry.anilist_id == 20519
    assert entry.collection_id == "3l2x9nxip35gqb5"
    assert entry.collection_name == "entries"
    assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
    assert isinstance(entry.created_at, datetime)
    assert entry.id == "c344w8ld7q1yppz"
    assert not entry.is_incomplete
    assert (
        entry.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert entry.theoretical_best is None
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.torrents[0].tracker == Tracker.NYAA
    assert entry.torrents[1].tracker == Tracker.ANIMEBYTES
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert isinstance(entry.updated_at, datetime)
