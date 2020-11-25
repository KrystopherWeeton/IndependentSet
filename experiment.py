import click


@click.group()
def run():
    pass


@run.command()
@click.option("-n", required=True, type=int, )
def generate_p_graph():
