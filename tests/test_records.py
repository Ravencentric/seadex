from __future__ import annotations

import datetime
from typing import Any

from seadex import EntryRecord, File, Tag, TorrentRecord, Tracker


def test_entry_record(sample_response: dict[str, Any]) -> None:
    record = EntryRecord.from_dict(sample_response["items"][0])

    assert EntryRecord.from_json(record.to_json()) == record
    assert record.anilist_id == 165790
    assert record.collection_id == "3l2x9nxip35gqb5"
    assert record.collection_name == "entries"
    assert record.comparisons == ("https://slow.pics/c/ntpJn04T",)
    assert record.created_at == datetime.datetime(2025, 3, 5, 22, 27, 18, 283000, tzinfo=datetime.timezone.utc)
    assert record.id == "ydydj1p7bn3o7ro"
    assert record.is_incomplete is False
    assert record.notes == (
        "-ZR- is JPN BD Remux+CR\nSubsPlease is a CR WEB-DL\nMPV deband helps everything, "
        "CR is very starved so a ReinForce or similar mux would be a better alt"
    )
    assert record.theoretical_best is None
    assert record.updated_at == datetime.datetime(2025, 8, 1, 22, 48, 15, 341000, tzinfo=datetime.timezone.utc)
    assert record.url == "https://releases.moe/165790/"
    assert record.size == 119397238820
    assert record.torrents == (
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 16, 546000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(
                    name="365 Days to the Wedding S01E01 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=6998581145,
                ),
                File(
                    name="365 Days to the Wedding S01E02 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=7000491203,
                ),
                File(
                    name="365 Days to the Wedding S01E03 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=6979226594,
                ),
                File(
                    name="365 Days to the Wedding S01E04 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=6996854606,
                ),
                File(
                    name="365 Days to the Wedding S01E05 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=6991295602,
                ),
                File(
                    name="365 Days to the Wedding S01E06 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=6994531903,
                ),
                File(
                    name="365 Days to the Wedding S01E07 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=6993457026,
                ),
                File(
                    name="365 Days to the Wedding S01E08 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=6980374159,
                ),
                File(
                    name="365 Days to the Wedding S01E09 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=7005228304,
                ),
                File(
                    name="365 Days to the Wedding S01E10 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=7010749826,
                ),
                File(
                    name="365 Days to the Wedding S01E11 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=6976051358,
                ),
                File(
                    name="365 Days to the Wedding S01E12 2024 1080p Bluray REMUX AVC LPCM 2.0 English Subbed -ZR-.mkv",
                    size=6972408748,
                ),
                File(name="NCED #01.mkv", size=443750178),
                File(name="NCOP #01.mkv", size=435716138),
            ),
            id="z2hmkedvvo6z9la",
            infohash=None,
            is_best=True,
            release_group="-ZR-",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.ANIMEBYTES,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 280000, tzinfo=datetime.timezone.utc),
            url="https://animebytes.tv/torrents.php?id=94644&torrentid=1160250",
            grouped_url=None,
            size=84778716790,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 16, 667000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 01 (1080p) [29AE676E].mkv", size=1444517064),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 02 (1080p) [0DAD4C4C].mkv", size=1447575015),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 03 (1080p) [DDDB9B82].mkv", size=1440842737),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 04 (1080p) [ADC71869].mkv", size=1443906241),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 05 (1080p) [7D6C78F3].mkv", size=1440349613),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 06 (1080p) [25C5BC0D].mkv", size=1440658774),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 07 (1080p) [E4FF4B15].mkv", size=1445615971),
                File(
                    name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 08v2 (1080p) [7431FDFD].mkv", size=1440150751
                ),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 09 (1080p) [9C080E81].mkv", size=1442618684),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 10 (1080p) [F0B66676].mkv", size=1438335408),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 11 (1080p) [9E20DDC5].mkv", size=1438344410),
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 12 (1080p) [A663077D].mkv", size=1446346347),
            ),
            id="oc96ttoirde3m7i",
            infohash=None,
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.ANIMEBYTES,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 360000, tzinfo=datetime.timezone.utc),
            url="https://animebytes.tv/torrents.php?id=94644&torrentid=1148022",
            grouped_url=None,
            size=17309261015,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 16, 826000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 01 (1080p) [29AE676E].mkv", size=1444517064),
            ),
            id="8hdn2imlud4c2ox",
            infohash="c4c1031570089d70bff40e1a89253025ad1cead7",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 433000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1880265",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1444517064,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 16, 936000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 02 (1080p) [0DAD4C4C].mkv", size=1447575015),
            ),
            id="oxdcaovz9xrfmsb",
            infohash="698546217b6bac38cd2632659baec87919c45c4f",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 509000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1883348",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1447575015,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 17, 56000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 03 (1080p) [DDDB9B82].mkv", size=1440842737),
            ),
            id="m9eatsndt5x7uzj",
            infohash="ce933d9bb5ac5eda640a2e881f5cfa7285263c3a",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 581000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1887035",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1440842737,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 17, 215000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 04 (1080p) [ADC71869].mkv", size=1443906241),
            ),
            id="y04aabmzb3rbfgu",
            infohash="e354c59c629f3ef9b54a5caf37c71f935b85d137",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 661000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1890363",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1443906241,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 17, 332000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 05 (1080p) [7D6C78F3].mkv", size=1440349613),
            ),
            id="h3jrs6pb7968ihl",
            infohash="52b3ca71903a192d58ab6a48b8e7ce343701c34c",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 723000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1893308",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1440349613,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 17, 449000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 06 (1080p) [25C5BC0D].mkv", size=1440658774),
            ),
            id="b8w0rtsysq2lnmc",
            infohash="2cdd212a2b9373334ca7a15db244949cbf407adb",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 794000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1896408",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1440658774,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 17, 566000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 07 (1080p) [E4FF4B15].mkv", size=1445615971),
            ),
            id="cl8lfwio6gcnrgh",
            infohash="1cb4ea3255a31977d3758f32fb405b8bf908dd40",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 871000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1899464",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1445615971,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 17, 699000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(
                    name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 08v2 (1080p) [7431FDFD].mkv", size=1440150751
                ),
            ),
            id="ghs3wco8xkq946s",
            infohash="c7725c95781c1ba2ae0e316e592ae4de5f2513ef",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 14, 949000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1902423",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1440150751,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 17, 809000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 09 (1080p) [9C080E81].mkv", size=1442618684),
            ),
            id="8xwrvd5v8q0trvv",
            infohash="70e89b0966ab8817454b2f58aec39a6b513bfa51",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 15, 18000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1905261",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1442618684,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 17, 949000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 10 (1080p) [F0B66676].mkv", size=1438335408),
            ),
            id="psdoxyu9qnw02ns",
            infohash="d75daf84491e72f028ad4a59dfbdab32405b033f",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 15, 108000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1908001",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1438335408,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 18, 73000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 11 (1080p) [9E20DDC5].mkv", size=1438344410),
            ),
            id="u6t01vc42aafr6n",
            infohash="5191a3e7f51682e57d22550e4e17d31964b55dbf",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 15, 182000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1910785",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1438344410,
        ),
        TorrentRecord(
            collection_id="oiwizhmushn5qqh",
            collection_name="torrents",
            created_at=datetime.datetime(2025, 3, 5, 22, 27, 18, 186000, tzinfo=datetime.timezone.utc),
            is_dual_audio=False,
            files=(
                File(name="[SubsPlease] Kekkon suru tte, Hontou desu ka - 12 (1080p) [A663077D].mkv", size=1446346347),
            ),
            id="6zoa0ti5uuv6ibs",
            infohash="e2b872e65150ba4c0a811d39ad885c15ad6f6249",
            is_best=False,
            release_group="SubsPlease",
            tags=frozenset([Tag.DEBAND_RECOMMENDED]),
            tracker=Tracker.NYAA,
            updated_at=datetime.datetime(2025, 8, 1, 22, 48, 15, 249000, tzinfo=datetime.timezone.utc),
            url="https://nyaa.si/view/1913294",
            grouped_url="https://nyaa.si/?f=0&c=0_0&q=%5BSubsPlease%5D+Kekkon+suru+tte%2C+Hontou+desu+ka+1080p",
            size=1446346347,
        ),
    )
