from __future__ import annotations

from cyclopts import App
from cyclopts.types import ResolvedExistingPath, ResolvedPath

torrent_app = App(
    "torrent",
    help="Perform torrent operations.",
    help_format="plaintext",
)


@torrent_app.command
def sanitize(
    src: ResolvedExistingPath,
    dst: ResolvedPath | None = None,
    /,
    *,
    overwrite: bool = False,
) -> None:
    """
    Sanitize torrent files by removing sensitive data.

    Parameters
    ----------
    src : ResolvedExistingPath
        Path to the source torrent file to sanitize.
    dst : ResolvedPath or None, optional
        Path where the sanitized file will be stored.
    overwrite: bool, optional
        If True, overwrites the destination file if it exists.

    """
    from rich.console import Console

    from seadex._torrent import SeaDexTorrent

    console = Console()

    if src.is_file() and src.suffix.lower() == ".torrent":
        try:
            destination = SeaDexTorrent(src).sanitize(destination=dst, overwrite=overwrite)
        except FileExistsError:
            console.print(
                "[red]error:[/] destination file already exists and overwrite is false. "
                "Use the `--overwrite` flag to replace it."
            )
            return
        console.print(f":white_check_mark: Saved sanitized torrent to [cyan]{destination}[/cyan]", emoji=True)
        return
    console.print("[red]error:[/] src must be an existing torrent file.")


@torrent_app.command
def filelist(src: ResolvedExistingPath, /, *, json: bool = False) -> None:
    """
    Output the list of files in a torrent.

    Parameters
    ----------
    src : ResolvedExistingPath
        Path to the torrent file.
    json : bool, optional
        If True, the output will be a SeaDex compatible JSON string.

    """

    from rich import box, print, print_json

    from seadex._torrent import SeaDexTorrent

    filelist = SeaDexTorrent(src).filelist

    if json:
        import msgspec

        jsonified = msgspec.json.encode(filelist).decode()
        print_json(jsonified)
        return

    import os

    from humanize import naturalsize
    from rich.table import Table

    table = Table("Filename", "Size", box=box.ROUNDED)
    parent = os.path.commonpath(file.name for file in filelist)

    for file in filelist:
        table.add_row(os.path.relpath(file.name, start=parent), naturalsize(file.size))

    print(table)
