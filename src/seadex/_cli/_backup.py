from __future__ import annotations

from typing import Annotated, TypeAlias

from cyclopts import App, Parameter
from cyclopts.types import ResolvedExistingDirectory

from seadex._backup import SeaDexBackup
from seadex._version import __version__

backup_app = App(
    "backup",
    version=__version__,
    help="Perform backup operations.",
    help_format="plaintext",
    version_flags=None,
)

EmailType: TypeAlias = Annotated[str, Parameter(env_var="SEADEX_EMAIL")]
PasswordType: TypeAlias = Annotated[str, Parameter(env_var="SEADEX_PASSWORD")]


def _login(email: str, password: str) -> SeaDexBackup:
    """
    Log in to SeaDex using email and password.

    Parameters
    ----------
    email : str
        The administrator email used for authentication.
    password : str
        The administrator password used for authentication.

    """
    from rich.console import Console

    with Console().status("Logging in", spinner="earth"):
        return SeaDexBackup(email, password)


@backup_app.command(name="list")
def _list(*, email: EmailType, password: PasswordType) -> None:
    """
    List all available backups.

    Parameters
    ----------
    email : str
        The administrator email used for authentication.
    password : str
        The administrator password used for authentication.

    """
    from rich import print
    from rich.box import MARKDOWN
    from rich.table import Table

    client = _login(email, password)

    table = Table("Name", "Size", "Date Modified", box=MARKDOWN)
    for _backup in client.backups:
        table.add_row(_backup.name, _backup.size.human_readable(), _backup.modified_time.isoformat())
    print(table)


@backup_app.command
def create(*, email: EmailType, password: PasswordType, name: str | None = None) -> None:
    """
    Create a new backup.

    Parameters
    ----------
    email : EmailType
        The administrator email used for authentication.
    password : PasswordType
        The administrator password used for authentication.
    name : str, optional
        The name of the backup. If not provided, a default name is generated using the
        template `%Y%m%d%H%M%S-seadex-backup.zip`, which supports the full `datetime.strftime`
        formatting.

    """
    from rich.console import Console

    console = Console()
    client = _login(email, password)
    filename = "%Y%m%d%H%M%S-seadex-backup.zip" if name is None else name

    with console.status("Creating a backup"):
        backup = client.create(filename)
    console.print(f":package: Created {backup}", emoji=True, highlight=False)


@backup_app.command
def download(
    *,
    email: EmailType,
    password: PasswordType,
    name: str | None = None,
    destination: ResolvedExistingDirectory | None = None,
    existing: bool = True,
) -> None:
    """
    Download a backup.

    Parameters
    ----------
    email : EmailType
        The administrator email used for authentication.
    password : PasswordType
        The administrator password used for authentication.
    name : str, optional
        The name of the backup to download. If not provided, the latest backup is downloaded.
    destination : ResolvedExistingDirectory | None, optional
        The destination directory for the backup. Defaults to the current working directory.
    existing : bool, optional
        If `True`, download an existing backup. If `False`, create a temporary backup on the remote system,
        download it, and then delete it from the remote.

    """
    from rich.console import Console

    console = Console()
    client = _login(email, password)

    if not existing:
        if name is None:
            console.print("[red]error:[/] The `--name` option is required when using `--no-existing`.")
            return
        with console.status("Creating a temporary backup on remote"):
            _backup = client.create(name)
        console.print(f":white_check_mark: Created [cyan]{_backup}[/cyan] on remote", emoji=True)

        with console.status(f"Downloading [cyan]{_backup}[/cyan]"):
            path = client.download(_backup, destination=destination)
        console.print(f":package: Saved to [cyan]{path}[/cyan]", emoji=True)

        with console.status(f"Deleting [cyan]{_backup}[/cyan] from remote"):
            client.delete(_backup)
        console.print(f":litter_in_bin_sign: Deleted [cyan]{_backup}[/cyan] from remote", emoji=True)
    else:
        __backup = name or client.latest_backup
        with console.status(f"Downloading [cyan]{__backup}[/cyan]"):
            path = client.download(__backup, destination=destination)
        console.print(f":package: Saved to [cyan]{path}[/cyan]", emoji=True, highlight=False)


@backup_app.command
def delete(*, email: EmailType, password: PasswordType, name: str) -> None:
    """
    Delete a backup by name.

    Parameters
    ----------
    email : EmailType
        The administrator email used for authentication.
    password : PasswordType
        The administrator password used for authentication.
    name : str
        The name of the backup to delete.

    """
    from rich.console import Console

    console = Console()

    client = _login(email, password)

    with console.status(f"Deleting {name}"):
        client.delete(name)

    console.print(f":litter_in_bin_sign: Deleted {name}", emoji=True, highlight=False)
