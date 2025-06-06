from __future__ import annotations

import base64
from datetime import datetime, timezone

from seadex import EntryRecord, File, TorrentRecord, Tracker


def test_torrent_record_movie() -> None:
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
    record = TorrentRecord.from_dict(sample_data)

    assert TorrentRecord.from_json(record.to_json()) == TorrentRecord.from_dict(record.to_dict())
    assert record.collection_id == "oiwizhmushn5qqh"
    assert record.collection_name == "torrents"
    assert isinstance(record.created_at, datetime)
    assert record.is_dual_audio
    assert len(record.files) == 1
    assert record.files[0].name == "Tamako.Love.Story.2014.1080p.BluRay.Opus2.0.H.265-LYS1TH3A.mkv"
    assert record.files[0].size == 4636316199
    assert File.from_json(record.files[0].to_json()) == File.from_dict(record.files[0].to_dict())
    assert record.size == 4636316199
    assert record.id == "pcpina3ekbqk7a5"
    assert record.infohash == "23f77120cfdf9df8b42a10216aa33e281c58b456"
    assert record.is_best
    assert record.release_group == "LYS1TH3A"
    assert record.tracker is Tracker.NYAA
    assert isinstance(record.updated_at, datetime)
    assert record.url == "https://nyaa.si/view/1693872"


def test_torrent_record_tv() -> None:
    """
    Tests that `_from_dict` correctly parses a dictionary into a TorrentRecord object.
    """
    # ruff: noqa: E501
    sample_data = {
        "collectionId": "oiwizhmushn5qqh",
        "collectionName": "torrents",
        "created": "2025-04-24 12:45:04.500Z",
        "dualAudio": True,
        "files": [
            {
                "length": 7104731698,
                "name": "DAN.DA.DAN.S01E01.That's.How.Love.Starts.Ya.Know.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 6806413318,
                "name": "DAN.DA.DAN.S01E02.That's.a.Space.Alien.Ain't.It.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 6870896112,
                "name": "DAN.DA.DAN.S01E03.It's.a.Granny.vs.Granny.Clash.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 7083129160,
                "name": "DAN.DA.DAN.S01E04.Kicking.Turbo.Granny's.Ass.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 6836508162,
                "name": "DAN.DA.DAN.S01E05.Like.Where.Are.Your.Balls.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 6813577317,
                "name": "DAN.DA.DAN.S01E06.A.Dangerous.Woman.Arrives.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 6808794549,
                "name": "DAN.DA.DAN.S01E07.To.a.Kinder.World.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 7070929817,
                "name": "DAN.DA.DAN.S01E08.I've.Got.This.Funny.Feeling.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 6857504844,
                "name": "DAN.DA.DAN.S01E09.Merge.Serpo.Dover.Demon.Nessie.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 7001167363,
                "name": "DAN.DA.DAN.S01E10.Have.You.Ever.Seen.a.Cattle.Mutilation.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 6803425880,
                "name": "DAN.DA.DAN.S01E11.First.Love.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
            {
                "length": 6722527363,
                "name": "DAN.DA.DAN.S01E12.Let's.Go.to.the.Cursed.House.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            },
        ],
        "groupedUrl": "",
        "id": "qppmbbhxkwe6xkx",
        "infoHash": "<redacted>",
        "isBest": True,
        "releaseGroup": "CRUCiBLE",
        "tracker": "AB",
        "updated": "2025-04-30 22:57:07.177Z",
        "url": "/torrents.php?id=94649&torrentid=1168369",
    }
    record = TorrentRecord.from_dict(sample_data)

    assert TorrentRecord.from_json(record.to_json()) == TorrentRecord.from_dict(record.to_dict())
    assert record.collection_id == "oiwizhmushn5qqh"
    assert record.collection_name == "torrents"
    assert record.created_at == datetime(2025, 4, 24, 12, 45, 4, 500000, tzinfo=timezone.utc)
    assert record.is_dual_audio
    assert record.files == (
        File(
            name="DAN.DA.DAN.S01E01.That's.How.Love.Starts.Ya.Know.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=7104731698,
        ),
        File(
            name="DAN.DA.DAN.S01E02.That's.a.Space.Alien.Ain't.It.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=6806413318,
        ),
        File(
            name="DAN.DA.DAN.S01E03.It's.a.Granny.vs.Granny.Clash.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=6870896112,
        ),
        File(
            name="DAN.DA.DAN.S01E04.Kicking.Turbo.Granny's.Ass.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=7083129160,
        ),
        File(
            name="DAN.DA.DAN.S01E05.Like.Where.Are.Your.Balls.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=6836508162,
        ),
        File(
            name="DAN.DA.DAN.S01E06.A.Dangerous.Woman.Arrives.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=6813577317,
        ),
        File(
            name="DAN.DA.DAN.S01E07.To.a.Kinder.World.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=6808794549,
        ),
        File(
            name="DAN.DA.DAN.S01E08.I've.Got.This.Funny.Feeling.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=7070929817,
        ),
        File(
            name="DAN.DA.DAN.S01E09.Merge.Serpo.Dover.Demon.Nessie.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=6857504844,
        ),
        File(
            name="DAN.DA.DAN.S01E10.Have.You.Ever.Seen.a.Cattle.Mutilation.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=7001167363,
        ),
        File(
            name="DAN.DA.DAN.S01E11.First.Love.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=6803425880,
        ),
        File(
            name="DAN.DA.DAN.S01E12.Let's.Go.to.the.Cursed.House.1080p.BluRay.Remux.Dual-Audio.FLAC2.0.H.264-CRUCiBLE.mkv",
            size=6722527363,
        ),
    )
    assert record.size == 82779605583
    assert record.id == "qppmbbhxkwe6xkx"
    assert record.infohash is None
    assert record.is_best
    assert record.release_group == "CRUCiBLE"
    assert record.tracker is Tracker.ANIMEBYTES
    assert record.updated_at == datetime(2025, 4, 30, 22, 57, 7, 177000, tzinfo=timezone.utc)


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

    record = EntryRecord.from_dict(sample_data)

    assert EntryRecord.from_json(record.to_json()) == EntryRecord.from_dict(record.to_dict())
    assert record.anilist_id == 20519
    assert record.collection_id == "3l2x9nxip35gqb5"
    assert record.collection_name == "entries"
    assert record.comparisons == ("https://slow.pics/c/rc6qrB1F",)  # Tuple with one element
    assert isinstance(record.created_at, datetime)
    assert record.id == "c344w8ld7q1yppz"
    assert not record.is_incomplete
    assert record.notes == (
        "Okay-Subs is JPN BD Encode+Commie with additional honorifics track\nLYS1TH3A is Okay-Subs+Dub"
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
    assert record.size == sum(tr.size for tr in record.torrents)
