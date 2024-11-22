from __future__ import annotations

from cyclopts import App
from cyclopts.types import ResolvedExistingPath, ResolvedPath
from natsort import natsorted, ns
from rich import print_json
from rich.console import Console
from rich.progress import track

from seadex._torrent import SeaDexTorrent
from seadex._version import __version__

torrent_app = App(
    "torrent",
    version=__version__,
    help="Perform torrent operations.",
    help_format="plaintext",
    version_flags=None,
)


@torrent_app.command
def sanitize(src: ResolvedExistingPath, dst: ResolvedPath | None = None, /) -> None:
    """
    Sanitize torrent files by removing sensitive data.

    Parameters
    ----------
    src : ResolvedExistingPath
        Path to the source torrent file or directory containing torrent files to sanitize.
    dst : ResolvedPath or None, optional
        Path to the destination where sanitized files will be stored.

    """
    console = Console()

    if src.is_file():
        path = SeaDexTorrent(src).sanitize(destination=dst, overwrite=True)
        console.print(f":white_check_mark: Saved sanitized torrent to [cyan]{path}[/cyan]", emoji=True)
    else:
        if dst is None:
            console.print("[red]error:[/] destination must be an existing directory.")
            return

        if not dst.is_dir():
            console.print(f"[red]error:[/] {dst} must be an existing directory.")
            return

        files = natsorted(src.rglob("*.torrent"), alg=ns.PATH)
        for file in track(files, description="Sanitizing...", total=len(files), transient=True, console=console):
            path = SeaDexTorrent(file).sanitize(destination=dst / file.name, overwrite=True)
            console.print(f":white_check_mark: Saved sanitized torrent to [cyan]{path}[/]", emoji=True)


@torrent_app.command
def json(src: ResolvedExistingPath, /, *, pretty: bool = False, copy: bool = True) -> None:
    """
    Output the list of files in a torrent as a SeaDex compatible JSON string.

    Parameters
    ----------
    src : ResolvedExistingPath
        Path to the torrent file.
    pretty : bool, optional
        If True, the JSON output will be pretty-printed.
    copy : bool, optional
        Copy the JSON output to clipboard.

    """
    filelist = SeaDexTorrent(src).filelist

    if copy:  # pragma: no cover
        try:
            import pyperclip

            pyperclip.copy(filelist.to_json())
        except Exception:
            pass

    if pretty:
        print_json(filelist.to_json())
    else:
        print(filelist.to_json())
