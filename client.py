import click
import requests

BASE_URL = "http://localhost:8000"

@click.group()
def cli():
    pass

@cli.command()
@click.argument('account_number')
@click.argument('initial_balance', type=float)
def create_account(account_number, initial_balance):
    response = requests.post(f"{BASE_URL}/account", params={"account_number": account_number, "initial_balance": initial_balance})
    click.echo(response.json()["message"] if response.status_code == 200 else response.json()["detail"])

@cli.command()
@click.argument('account_number')
@click.argument('amount', type=float)
def deposit(account_number, amount):
    response = requests.post(f"{BASE_URL}/deposit", params={"account_number": account_number, "amount": amount})
    click.echo(response.json()["message"] if response.status_code == 200 else response.json()["detail"])

@cli.command()
@click.argument('account_number')
@click.argument('amount', type=float)
def withdraw(account_number, amount):
    response = requests.post(f"{BASE_URL}/withdraw", params={"account_number": account_number, "amount": amount})
    click.echo(response.json()["message"] if response.status_code == 200 else response.json()["detail"])

@cli.command()
@click.argument('from_account_number')
@click.argument('to_account_number')
@click.argument('amount', type=float)
def transfer(from_account_number, to_account_number, amount):
    response = requests.post(f"{BASE_URL}/transfer", params={"from_account_number": from_account_number, "to_account_number": to_account_number, "amount": amount})
    click.echo(response.json()["message"] if response.status_code == 200 else response.json()["detail"])

@cli.command()
@click.argument('account_number')
def balance(account_number):
    response = requests.get(f"{BASE_URL}/balance/{account_number}")
    if response.status_code == 200:
        click.echo(f"Balance for {account_number}: ${response.json()['balance']}")
    else:
        click.echo(response.json()["detail"])

@cli.command()
@click.option('-f', '--file', type=click.Path(), help='File to export data to')
def export(file):
    response = requests.get(f"{BASE_URL}/export")
    if response.status_code == 200:
        if file:
            with open(file, 'w') as f:
                f.write(response.text)
            click.echo(f"Data exported to {file}")
        else:
            click.echo(response.text)
    else:
        click.echo(response.json()["detail"])

@cli.command()
@click.option('-f', '--file', type=click.Path(exists=True), required=True, help='File to import data from')
def import_data(file):
    with open(file, 'rb') as f:
        files = {'file': (file, f)}
        response = requests.post(f"{BASE_URL}/import", files=files)
    click.echo(response.json()["message"] if response.status_code == 200 else response.json()["detail"])
    
if __name__ == "__main__":
    cli()