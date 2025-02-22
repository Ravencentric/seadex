from __future__ import annotations

try:
    from cyclopts import App
except ModuleNotFoundError:
    import sys

    print("Error: Required dependencies for the CLI are missing. Install `seadex[cli]` to fix this.")
    sys.exit(1)


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
