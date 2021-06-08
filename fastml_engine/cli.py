import os
import sys
import logging
import click
from fastml_engine.utils.process import exec_cmd

_logger = logging.getLogger(__name__)


def _build_waitress_command(host, port):
    return (
            ["waitress-serve"]
            + ["--host=%s" % host, "--port=%s" % port, "fastml_engine.server:app"]
    )


def _build_gunicorn_command(service_path, host, port, workers, threads, timeout):
    bind_address = "%s:%s" % (host, port)
    return ["gunicorn"] + ["--pid", "%s/logs/gunicorn.pid" % service_path] \
           + ["--error-logfile", "%s/logs/error-access.log" % service_path] \
           + ["--access-logfile", "%s/logs/access.log" % service_path] \
           + ["--worker-class", "gevent"] \
           + ["-e", "SERVICE_PATH=%s" % service_path, "-b", bind_address, "-w", "%s" % workers, "--threads",
              "%s" % threads, "-t", "%s" % timeout, "fastml_engine.server:app"]


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
@click.option(
    "--service-path",
    metavar="PATH",
    type=click.STRING,
    default=None,
    help="input absolute path to the model service,like : /opt/inference-template "
         "or use current directory path as default",
)
@click.option(
    "--model-path",
    metavar="PATH",
    type=click.STRING,
    default=None,
    help="input absolute path to the model dir",
)
@click.option(
    "--host",
    "-h",
    metavar="HOST",
    default="127.0.0.1",
    help="The network address to listen on (default: 127.0.0.1). "
         "Use 0.0.0.0 to bind to all addresses if you want to access the server from other machines.",
)
@click.option(
    "--port",
    "-p",
    metavar="PORT",
    default=5000,
    help="The port to listen on (default: 5000)",
)
@click.option(
    "--workers",
    "-w",
    envvar="INT",
    default=1,
    help="Number of gunicorn worker processes to handle requests (default: 1)",
)
@click.option(
    "--threads",
    envvar="INT",
    default=4,
    help="The number of gunicorn worker threads for handling requests (default:4)",
)
@click.option(
    "--timeout",
    "-t",
    envvar="INT",
    default=30,
    help="Gunicorn Workers silent for more than this many seconds are killed and restarted (default:30)",
)
def server(
        service_path,
        model_path,
        host,
        port,
        workers,
        threads,
        timeout):
    env_map = {}
    if not service_path:
        service_path = os.getcwd()
    env_map['SERVICE_PATH'] = service_path
    if not model_path:
        model_path = service_path+'/model'
    env_map['MODEL_PATH'] = model_path

    if sys.platform == "win32":
        full_command = _build_waitress_command(host, port)
    else:
        full_command = _build_gunicorn_command(service_path, host, port, workers, threads, timeout)
    print(full_command)
    exec_cmd(full_command, env=env_map, stream_output=True)


if __name__ == "__main__":
    cli()
