import os
import pathlib

import click


@click.group()
@click.option(
    "-c",
    "--config-file",
    "config_file_fp",
    type=str,
    default="~/.config/12factor-app/config.ini",
    help="Configuration file.",
)
@click.option("--debug/--no-debug", default=False, help="Enable debug mode.")
def cli(config_file_fp, debug):
    config_file = pathlib.Path(config_file_fp).expanduser()
    if not config_file.exists():
        raise ValueError(f"Configuration file not found at {str(config_file)}.")
    os.environ.setdefault("12FACTOR_APP_CONFIG", str(config_file))
    os.environ.setdefault("12FACTOR_APP_DEBUG", str(debug).upper())


@click.command(
    add_help_option=False, context_settings=dict(ignore_unknown_options=True)
)
@click.argument("management_args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def django(ctx, management_args):
    "Execute Django subcommands."
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twelve_factor_app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(argv=[ctx.command_path] + list(management_args))


def make_django_command(name, django_command=None, help=None):
    "A wrapper to convert a Django subcommand a Click command"
    if django_command is None:
        django_command = name

    @click.command(
        name=name,
        help=help,
        add_help_option=False,
        context_settings=dict(ignore_unknown_options=True),
    )
    @click.argument("management_args", nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def inner(ctx, management_args):
        ctx.params["management_args"] = (django_command,) + management_args
        ctx.forward(django)

    return inner


cli.add_command(
    make_django_command("shell", help="Run a Python interactive interpreter.")
)


@cli.command(
    add_help_option=False,
    context_settings=dict(ignore_unknown_options=True),
    help="Start gunicorn web server.",
)
@click.argument("gunicorn_args", nargs=-1, type=click.UNPROCESSED)
def start_server(gunicorn_args):
    args = ["gunicorn", "twelve_factor_app.wsgi:application"] + list(gunicorn_args)
    os.execvp(args[0], args)
