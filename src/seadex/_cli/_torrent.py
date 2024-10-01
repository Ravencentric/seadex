from __future__ import annotations

from cyclopts import App
from cyclopts.types import ResolvedExistingPath, ResolvedPath
from natsort import natsorted, ns
from rich.console import Console
from rich.progress import track

from seadex._torrent import sanitize_torrent
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
        path = sanitize_torrent(src, destination=dst, overwrite=True)
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
            path = sanitize_torrent(file, destination=dst / file.name, overwrite=True)
            console.print(f":white_check_mark: Saved sanitized torrent to [cyan]{path}[/]", emoji=True)
