from __future__ import annotations

from cyclopts import App

entry_app = App(
    "entry",
    help="Get a SeaDex entry.",
    help_format="plaintext",
)


@entry_app.default
def get_entry(title: str, /, *, json: bool = False) -> None:
    """
    Get the seadex entry for the given title.

    Parameters
    ----------
    title : str
        Title of the anime.
    json : bool, optional
        If True, the output will be a JSON string.

    """
    from rich import box, print_json
    from rich.console import Console, Group
    from rich.table import Table
    from rich.theme import Theme

    from seadex._entry import SeaDexEntry
    from seadex._exceptions import EntryNotFoundError

    console = Console(theme=Theme({"repr.number": ""}))

    with SeaDexEntry() as seadex_entry:
        try:
            entry = seadex_entry.from_title(title)
            # Grab the anilist title from internal cache
            # This saves us from hitting AniList again
            anilist_title = (
                seadex_entry._al_cache[title]["title"]["english"] or seadex_entry._al_cache[title]["title"]["romaji"]
            )
        except EntryNotFoundError:
            console.print(f"[red]error:[/] no seadex entry found for {title!r}")
            return

        if json:
            print_json(entry.to_json())
            return

        body = f"Title: {anilist_title}\n"
        body += f"URL: {entry.url}\n"
        body += f"AniList: https://anilist.co/anime/{entry.anilist_id}\n"
        body += f"Incomplete: {'Yes' if entry.is_incomplete else 'No'}\n"
        body += f"Updated At: {entry.updated_at.strftime('%b %d, %Y')}"
        if entry.theoretical_best is not None:
            body += f"\nTheoretical Best: {entry.theoretical_best}"

        table = Table(box=box.ROUNDED)
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
