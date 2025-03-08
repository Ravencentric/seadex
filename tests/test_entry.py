from __future__ import annotations

import base64
import copy
from datetime import datetime, timezone

from pytest_httpx import HTTPXMock

from seadex import SeaDexEntry, Tracker

SAMPLE_JSON_REPLY = {
    "page": 1,
    "perPage": 500,
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
                        "tracker": "AB",
                        "updated": "2024-01-30 19:28:09.461Z",
                        "url": "/torrents.php?id=20684&torrentid=1053072",
                    },
                    {
                        "collectionId": "oiwizhmushn5qqh",
                        "collectionName": "torrents",
                        "created": "2024-01-30 19:28:09.803Z",
                        "dualAudio": False,
                        "files": [{"length": 4555215904, "name": "[Okay-Subs] Tamako Love Story [45C10FA7].mkv"}],
                        "id": "qhcmujh4dsw55j2",
                        "infoHash": "cfb670c2261701b060b708a16743cf6658c47b62",
                        "isBest": True,
                        "releaseGroup": "Okay-Subs",
                        "tracker": "Nyaa",
                        "updated": "2024-01-30 19:28:09.803Z",
                        "url": "https://nyaa.si/view/1656471",
                    },
                    {
                        "collectionId": "oiwizhmushn5qqh",
                        "collectionName": "torrents",
                        "created": "2024-01-30 19:28:10.159Z",
                        "dualAudio": False,
                        "files": [{"length": 4555215904, "name": "[Okay-Subs] Tamako Love Story [45C10FA7].mkv"}],
                        "id": "enytf1g1cxf0k47",
                        "infoHash": "<redacted>",
                        "isBest": True,
                        "releaseGroup": "Okay-Subs",
                        "tracker": "AB",
                        "updated": "2024-01-30 19:28:10.159Z",
                        "url": "/torrents.php?id=20684&torrentid=1031817",
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


def test_properties(seadex_entry: SeaDexEntry) -> None:
    assert seadex_entry.base_url == "https://releases.moe"


def test_from_anilist_id(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?perPage=500&expand=trs&filter=alID%3D20519&skipTotal=true",
        json=SAMPLE_JSON_REPLY,
    )
    entry = seadex_entry.from_id(20519)
    assert entry.anilist_id == 20519
    assert entry.collection_id == "3l2x9nxip35gqb5"
    assert entry.collection_name == "entries"
    assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
    assert entry.created_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)
    assert entry.id == "c344w8ld7q1yppz"
    assert not entry.is_incomplete
    assert (
        entry.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert entry.theoretical_best is None
    assert entry.torrents[0].url == "https://nyaa.si/view/1693872"
    assert (
        entry.torrents[1].url
        == base64.b64decode(
            b"aHR0cHM6Ly9hbmltZWJ5dGVzLnR2L3RvcnJlbnRzLnBocD9pZD0yMDY4NCZ0b3JyZW50aWQ9MTA1MzA3Mg=="
        ).decode()
    )
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.torrents[0].tracker is Tracker.NYAA
    assert entry.torrents[1].tracker is Tracker.ANIMEBYTES
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert isinstance(entry.updated_at, datetime)


def test_from_seadex_id(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?perPage=500&expand=trs&filter=id%3D%27c344w8ld7q1yppz%27&skipTotal=true",
        json=SAMPLE_JSON_REPLY,
    )
    entry = seadex_entry.from_id("c344w8ld7q1yppz")
    assert entry.anilist_id == 20519
    assert entry.collection_id == "3l2x9nxip35gqb5"
    assert entry.collection_name == "entries"
    assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
    assert entry.created_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)
    assert entry.id == "c344w8ld7q1yppz"
    assert not entry.is_incomplete
    assert (
        entry.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert entry.theoretical_best is None
    assert entry.torrents[0].url == "https://nyaa.si/view/1693872"
    assert (
        entry.torrents[1].url
        == base64.b64decode(
            b"aHR0cHM6Ly9hbmltZWJ5dGVzLnR2L3RvcnJlbnRzLnBocD9pZD0yMDY4NCZ0b3JyZW50aWQ9MTA1MzA3Mg=="
        ).decode()
    )
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.torrents[0].tracker is Tracker.NYAA
    assert entry.torrents[1].tracker is Tracker.ANIMEBYTES
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.updated_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)


def test_from_title(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://graphql.anilist.co",
        json={
            "data": {"Media": {"id": 20519, "title": {"english": "Tamako -love story-", "romaji": "Tamako Love Story"}}}
        },
    )

    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?perPage=500&expand=trs&filter=alID%3D20519&skipTotal=true",
        json=SAMPLE_JSON_REPLY,
    )

    entry = seadex_entry.from_title("tamako love story")
    assert entry.anilist_id == 20519
    assert entry._anilist_title == "Tamako -love story-"  # type: ignore[attr-defined]
    assert entry.collection_id == "3l2x9nxip35gqb5"
    assert entry.collection_name == "entries"
    assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
    assert entry.created_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)
    assert entry.id == "c344w8ld7q1yppz"
    assert not entry.is_incomplete
    assert (
        entry.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert entry.theoretical_best is None
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.torrents[0].tracker is Tracker.NYAA
    assert entry.torrents[1].tracker is Tracker.ANIMEBYTES
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.updated_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)


def test_from_filename(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?filter=trs.files%3F~%27%22name%22%3A%22Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv%22%27&perPage=500&expand=trs&&skipTotal=true",
        json=SAMPLE_JSON_REPLY,
    )

    entries = seadex_entry.from_filename("Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv")
    entry = tuple(entries)[0]  # noqa: RUF015
    assert entry.anilist_id == 20519
    assert entry.collection_id == "3l2x9nxip35gqb5"
    assert entry.collection_name == "entries"
    assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
    assert entry.created_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)
    assert entry.id == "c344w8ld7q1yppz"
    assert not entry.is_incomplete
    assert (
        entry.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert entry.theoretical_best is None
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.torrents[0].tracker is Tracker.NYAA
    assert entry.torrents[1].tracker is Tracker.ANIMEBYTES
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.updated_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)


def test_from_infohash(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?perPage=500&expand=trs&filter=trs.infoHash%3F%3D%2723f77120cfdf9df8b42a10216aa33e281c58b456%27&skipTotal=true",
        json=SAMPLE_JSON_REPLY,
    )

    entries = tuple(seadex_entry.from_infohash("23f77120cfdf9df8b42a10216aa33e281c58b456"))
    assert len(entries) == 1
    entry = tuple(entries)[0]  # noqa: RUF015
    assert entry.anilist_id == 20519
    assert entry.collection_id == "3l2x9nxip35gqb5"
    assert entry.collection_name == "entries"
    assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
    assert entry.created_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)
    assert entry.id == "c344w8ld7q1yppz"
    assert not entry.is_incomplete
    assert (
        entry.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert entry.theoretical_best is None
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.torrents[0].tracker is Tracker.NYAA
    assert entry.torrents[1].tracker is Tracker.ANIMEBYTES
    assert entry.torrents[0].infohash is not None
    assert entry.torrents[1].infohash is None
    assert entry.updated_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)


def test_iterator(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock) -> None:
    # Mimic multi page response
    SAMPLE_JSON_REPLY_PAGE_1 = copy.deepcopy(SAMPLE_JSON_REPLY)  # noqa: N806
    SAMPLE_JSON_REPLY_PAGE_2 = copy.deepcopy(SAMPLE_JSON_REPLY)  # noqa: N806

    # First page should report 2 total pages
    SAMPLE_JSON_REPLY_PAGE_1["totalPages"] = 2

    # Second page should report itself as page 2
    SAMPLE_JSON_REPLY_PAGE_2["page"] = 2
    SAMPLE_JSON_REPLY_PAGE_2["totalPages"] = 2

    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?perPage=500&expand=trs",
        json=SAMPLE_JSON_REPLY_PAGE_1,
    )

    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?perPage=500&expand=trs&page=2",
        json=SAMPLE_JSON_REPLY_PAGE_2,
    )

    for entry in seadex_entry.iterator():
        assert entry.anilist_id == 20519
        assert entry.collection_id == "3l2x9nxip35gqb5"
        assert entry.collection_name == "entries"
        assert entry.comparisons == ("https://slow.pics/c/rc6qrB1F",)
        assert entry.created_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)
        assert entry.id == "c344w8ld7q1yppz"
        assert not entry.is_incomplete
        assert (
            entry.notes
            == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
        )
        assert entry.theoretical_best is None
        assert entry.torrents[0].url == "https://nyaa.si/view/1693872"
        assert (
            entry.torrents[1].url
            == base64.b64decode(
                b"aHR0cHM6Ly9hbmltZWJ5dGVzLnR2L3RvcnJlbnRzLnBocD9pZD0yMDY4NCZ0b3JyZW50aWQ9MTA1MzA3Mg=="
            ).decode()
        )
        assert entry.torrents[0].infohash is not None
        assert entry.torrents[1].infohash is None
        assert entry.torrents[0].tracker is Tracker.NYAA
        assert entry.torrents[1].tracker is Tracker.ANIMEBYTES
        assert entry.torrents[0].infohash is not None
        assert entry.torrents[1].infohash is None
        assert entry.updated_at == datetime(2024, 1, 30, 19, 28, 10, 337000, tzinfo=timezone.utc)


def test_from_filter(seadex_entry: SeaDexEntry, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?perPage=500&expand=trs&filter=alID=20519",
        json=SAMPLE_JSON_REPLY,
    )

    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?perPage=500&expand=trs&filter=alID%3D20519&skipTotal=true",
        json=SAMPLE_JSON_REPLY,
    )

    assert next(seadex_entry.from_filter(f"alID={20519}")) == seadex_entry.from_id(20519)
