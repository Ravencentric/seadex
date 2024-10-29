from __future__ import annotations

try:
    from cyclopts import App
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Missing required dependencies for the CLI, run 'pip install seadex[cli]' to install them."
    )

from seadex._cli._backup import backup_app
from seadex._cli._entry import entry_app
from seadex._cli._torrent import torrent_app
from seadex._version import __version__

app = App(
    "seadex",
    version=__version__,
    help="Command line interface to the SeaDex API.",
    help_format="plaintext",
)

app.command(backup_app)
app.command(torrent_app)
app.command(entry_app)

if __name__ == "__main__":
    app()
