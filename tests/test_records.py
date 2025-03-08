from __future__ import annotations

import base64
from datetime import datetime

from seadex import EntryRecord, TorrentRecord, Tracker


def test_torrent_record() -> None:
    """
    Tests that `_from_dict` correctly parses a dictionary into a TorrentRecord object.
    """
    sample_data = {
        "collectionId": "oiwizhmushn5qqh",
        "collectionName": "torrents",
        "created": "2024-01-30 19:28:09.110Z",
        "dualAudio": True,
        "files": [
            {"length": 4636316199, "name": "Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv"},
        ],
        "id": "pcpina3ekbqk7a5",
        "infoHash": "23f77120cfdf9df8b42a10216aa33e281c58b456",
        "isBest": True,
        "releaseGroup": "LYS1TH3A",
        "tracker": "Nyaa",
        "updated": "2024-01-30 19:28:09.110Z",
        "url": "https://nyaa.si/view/1693872",
    }
    record = TorrentRecord._from_dict(sample_data)

    assert record.collection_id == "oiwizhmushn5qqh"
    assert record.collection_name == "torrents"
    assert isinstance(record.created_at, datetime)
    assert record.is_dual_audio
    assert len(record.files) == 1
    assert record.files[0].name == "Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv"
    assert record.files[0].size == 4636316199
    assert record.size == 4636316199

    assert record.id == "pcpina3ekbqk7a5"
    assert record.infohash == "23f77120cfdf9df8b42a10216aa33e281c58b456"
    assert record.is_best
    assert record.release_group == "LYS1TH3A"
    assert record.tracker is Tracker.NYAA
    assert isinstance(record.updated_at, datetime)
    assert record.url == "https://nyaa.si/view/1693872"


def test_entry_record() -> None:
    sample_data = {
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
                        {"length": 4636316199, "name": "Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv"}
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
                        {"length": 4636316199, "name": "Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv"}
                    ],
                    "id": "tvh4fn4m2qi19n5",
                    "infoHash": "<redacted>",
                    "isBest": True,
                    "releaseGroup": "LYS1TH3A",
                    "tracker": "AB",
                    "updated": "2024-01-30 19:28:09.461Z",
                    "url": "/torrents.php?id=20684&torrentid=1053072",
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

    record = EntryRecord._from_dict(sample_data)

    assert record.anilist_id == 20519
    assert record.collection_id == "3l2x9nxip35gqb5"
    assert record.collection_name == "entries"
    assert record.comparisons == ("https://slow.pics/c/rc6qrB1F",)  # Tuple with one element
    assert isinstance(record.created_at, datetime)
    assert record.id == "c344w8ld7q1yppz"
    assert not record.is_incomplete
    assert (
        record.notes == "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
    )
    assert record.theoretical_best is None
    assert record.torrents[0].url == "https://nyaa.si/view/1693872"
    assert (
        record.torrents[1].url
        == base64.b64decode(
            b"aHR0cHM6Ly9hbmltZWJ5dGVzLnR2L3RvcnJlbnRzLnBocD9pZD0yMDY4NCZ0b3JyZW50aWQ9MTA1MzA3Mg=="
        ).decode()
    )
    assert record.torrents[0].infohash is not None
    assert record.torrents[1].infohash is None
    assert isinstance(record.updated_at, datetime)
    assert record.url == "https://releases.moe/20519/"
