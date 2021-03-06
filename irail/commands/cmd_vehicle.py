import click
from irail.cli import pass_context
from irail.commands.utils import *
import requests
from datetime import datetime, timedelta
from time import time

def is_on_the_move(vehicle):
    current_time = time()
    return (int(vehicle[0]["time"]) < int(current_time) and
            int(vehicle[-1]["time"]) > int(current_time))

@click.command()
@click.argument('vehicle_id')
@pass_context
def cli(context, vehicle_id):
    r = vehicle_request(vehicle_id)
    click.secho(parse_time(r["timestamp"]) + " " +
                str.center(r["vehicle"], context.terminal_width - 6),
                reverse = True)
    now = datetime.now()
    for stop in r["stops"]["stop"]:

        stop_time = parse_time(stop["time"])
        stop_time_raw = int(stop["time"])
        stop_delay = int(stop["delay"])
        dim = (datetime.fromtimestamp(stop_time_raw) +
               timedelta(seconds=stop_delay)) < now
        click.secho(stop_time + " " +
                    human_readable_delay_from_delay_string(stop["delay"])[1] + " " +
                    stop["station"],
                    dim=dim)
