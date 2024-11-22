from __future__ import annotations

from urllib.parse import urljoin

from cyclopts import App
from rich import box, print_json
from rich.console import Console, Group
from rich.table import Table

from seadex._entry import SeaDexEntry
from seadex._exceptions import EntryNotFoundError
from seadex._version import __version__

entry_app = App(
    "entry",
    version=__version__,
    help="Get a SeaDex entry.",
    help_format="plaintext",
    version_flags=None,
)


@entry_app.default
def get_entry(title: str, /, *, json: bool = False, pretty: bool = False) -> None:
    """
    Get the seadex entry for the given title.

    Parameters
    ----------
    title : str
        Title of the anime.
    json : bool, optional
        If True, the output will be in JSON.
    pretty : bool, optional
        If True, the JSON output will be pretty-printed.
    """
    console = Console()

    with SeaDexEntry() as seadex_entry:
        try:
            entry = seadex_entry.from_title(title)
        except EntryNotFoundError as error:
            console.print(f"[red]error:[/] {error.message}")
            return

        if json:
            if pretty:
                print_json(entry.model_dump_json())
                return
            else:
                print(entry.model_dump_json())
                return

        body = f"Title: {entry.__anilist_title}\n"  # type: ignore
        body += f"URL: {urljoin(seadex_entry.base_url, str(entry.anilist_id))}\n"
        body += f"AniList: https://anilist.co/anime/{entry.anilist_id}\n"
        body += f"Incomplete: {entry.is_incomplete}\n"
        body += f"Updated At: {entry.updated_at.strftime('%Y-%m-%d')}"
        if entry.theoretical_best is not None:
            body += f"\nTheoretical Best: {entry.theoretical_best}"

        table = Table(box=box.MARKDOWN)
        table.add_column("Group")
        table.add_column("Best")
        table.add_column("Dual")
        table.add_column("URL")

        for torrent in sorted(
            entry.torrents, key=lambda t: (not (t.is_best and t.is_dual_audio), not t.is_best, not t.is_dual_audio)
        ):
            table.add_row(
                torrent.release_group,
                ":white_check_mark:" if torrent.is_best else ":cross_mark:",
                ":white_check_mark:" if torrent.is_dual_audio else ":cross_mark:",
                torrent.url,
            )

        lower_body = f"Notes:\n{entry.notes}\n"
        lower_body += "\nComparisons:\n"
        for comparison in entry.comparisons:
            lower_body += f"- {comparison}\n"

        console.print(Group(body, table, lower_body))
