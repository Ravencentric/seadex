from __future__ import annotations

from datetime import datetime

from seadex import EntryRecord, TorrentRecord, Tracker


def test_torrent_record():
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

    assert record.collection_id == sample_data["collectionId"]
    assert record.collection_name == sample_data["collectionName"]
    assert isinstance(record.created_at, datetime)
    assert record.is_dual_audio == sample_data["dualAudio"]

    assert len(record.files) == 1
    assert record.files[0].name == sample_data["files"][0]["name"]
    assert record.files[0].size == sample_data["files"][0]["length"]

    assert record.id == sample_data["id"]
    assert record.infohash == sample_data["infoHash"]
    assert record.is_best == sample_data["isBest"]
    assert record.release_group == sample_data["releaseGroup"]
    assert record.tracker == Tracker(sample_data["tracker"])
    assert isinstance(record.updated_at, datetime)
    assert record.url == sample_data["url"]


def test_entry_record():
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

    record = EntryRecord._from_dict(sample_data)

    assert record.anilist_id == sample_data["alID"]
    assert record.collection_id == sample_data["collectionId"]
    assert record.collection_name == sample_data["collectionName"]
    assert record.comparisons == (sample_data["comparison"],)  # Tuple with one element
    assert isinstance(record.created_at, datetime)
    assert record.id == sample_data["id"]
    assert not record.is_incomplete
    assert record.notes == sample_data["notes"]
    assert record.theoretical_best is None
    assert record.torrents[0].url == "https://nyaa.si/view/1693872"
    assert record.torrents[1].url == "https://animebytes.tv/torrents.php?id=20684&torrentid=1053072"
    assert record.torrents[0].infohash is not None
    assert record.torrents[1].infohash is None
    assert isinstance(record.updated_at, datetime)
