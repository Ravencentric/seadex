from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, TypeAlias

from cyclopts import App, Parameter
from cyclopts.types import ResolvedExistingDirectory

if TYPE_CHECKING:
    from seadex._backup import SeaDexBackup

backup_app = App(
    "backup",
    help="Perform backup operations.",
    help_format="plaintext",
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

    from seadex._backup import SeaDexBackup

    with Console().status("Logging in", spinner="earth"):
        return SeaDexBackup(email, password)


@backup_app.command(name="list")
def _list(*, email: EmailType, password: PasswordType, json: bool = False) -> None:
    """
    List all available backups.

    Parameters
    ----------
    email : str
        The administrator email used for authentication.
    password : str
        The administrator password used for authentication.
    json : bool, optional
        If True, the output will be a JSON string.

    """
    from humanize import naturalsize
    from rich import box, print, print_json
    from rich.table import Table

    client = _login(email, password)
    backups = client.get_backups()

    if json:
        import msgspec

        jsonified = msgspec.json.encode(backups).decode()
        print_json(jsonified)
        return

    table = Table("Name", "Size", "Date Modified", box=box.ROUNDED)
    for backup in backups:
        table.add_row(backup.name, naturalsize(backup.size), backup.modified_time.isoformat())
    print(table)


@backup_app.command
def create(name: str | None = None, /, *, email: EmailType, password: PasswordType) -> None:
    """
    Create a new backup.

    Parameters
    ----------
    name : str, optional
        The name of the backup. If not provided, a default name is generated using the
        template `%Y%m%d%H%M%S-seadex-backup.zip`, which supports the full `datetime.strftime`
        formatting.
    email : EmailType
        The administrator email used for authentication.
    password : PasswordType
        The administrator password used for authentication.

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
    name: str | None = None,
    /,
    *,
    email: EmailType,
    password: PasswordType,
    destination: ResolvedExistingDirectory | None = None,
    existing: bool = True,
) -> None:
    """
    Download a backup.

    Parameters
    ----------
    name : str, optional
        The name of the backup to download. If not provided, the latest backup is downloaded.
    email : EmailType
        The administrator email used for authentication.
    password : PasswordType
        The administrator password used for authentication.
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
            backup = client.create(name)
        console.print(f":white_check_mark: Created [cyan]{backup}[/cyan] on remote", emoji=True)

        with console.status(f"Downloading [cyan]{backup}[/cyan]"):
            dest = client.download(backup, destination=destination)
        console.print(f":package: Saved to [cyan]{dest}[/cyan]", emoji=True)

        with console.status(f"Deleting [cyan]{backup}[/cyan] from remote"):
            client.delete(backup)
        console.print(f":litter_in_bin_sign: Deleted [cyan]{backup}[/cyan] from remote", emoji=True)

        return

    backup = name or client.get_latest_backup()  # type: ignore[assignment]
    with console.status(f"Downloading [cyan]{backup}[/cyan]"):
        dest = client.download(backup, destination=destination)
    console.print(f":package: Saved to [cyan]{dest}[/cyan]", emoji=True, highlight=False)


@backup_app.command
def delete(name: str, /, *, email: EmailType, password: PasswordType) -> None:
    """
    Delete a backup by name.

    Parameters
    ----------
    name : str
        The name of the backup to delete.
    email : EmailType
        The administrator email used for authentication.
    password : PasswordType
        The administrator password used for authentication.

    """
    from rich.console import Console

    console = Console()

    client = _login(email, password)

    with console.status(f"Deleting {name}"):
        client.delete(name)

    console.print(f":litter_in_bin_sign: Deleted {name}", emoji=True, highlight=False)
