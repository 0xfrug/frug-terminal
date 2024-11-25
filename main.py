import requests
import datetime
import time
import os
import pyfiglet
from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def clear_console():
    """Clear the console to reduce clutter."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome_message():
    """Display an ASCII welcome message."""
    ascii_art = pyfiglet.figlet_format("frug")
    console.print(f"[bold cyan]{ascii_art}[/bold cyan]")

def main():
    display_welcome_message()
    while True:
        console.print("[bold]Menu:[/bold]")
        console.print("1. Price")
        console.print("2. Funding Info")
        console.print("3. Position Data")
        console.print("4. Measure Latency")
        console.print("5. Exit")
        choice = Prompt.ask("[bold yellow]Please select an option (1-5)[/bold yellow]")

        clear_console()  # Clear the console before displaying new information

        if choice == '1':
            get_price()
        elif choice == '2':
            get_funding_info()
        elif choice == '3':
            get_position_data()
        elif choice == '4':
            measure_latency()
        elif choice == '5':
            console.print("[bold green]Exiting the program. Goodbye![/bold green]")
            break
        else:
            console.print("[bold red]Invalid option. Please try again.[/bold red]")

def get_price():
    symbol = Prompt.ask("[bold yellow]Enter the symbol (e.g., BTCUSDT)[/bold yellow]").upper()
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    params = {'symbol': symbol}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if 'code' in data:
            console.print(f"[bold red]Error: {data['msg']}[/bold red]")
        else:
            table = Table(title=f"Price Information for [green]{data['symbol']}[/green]")
            table.add_column("Metric", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")

            table.add_row("Price Change", data['priceChange'])
            table.add_row("Price Change Percent", f"{data['priceChangePercent']}%")
            table.add_row("Last Price", data['lastPrice'])
            table.add_row("Open Price", data['openPrice'])
            table.add_row("High Price", data['highPrice'])
            table.add_row("Low Price", data['lowPrice'])
            table.add_row("Volume", data['volume'])

            console.print(table)
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

def get_funding_info():
    symbol = Prompt.ask("[bold yellow]Enter the symbol (e.g., BTCUSDT)[/bold yellow]").upper()
    url = "https://fapi.binance.com/fapi/v1/fundingRate"
    params = {'symbol': symbol, 'limit': 1}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            data = data[0]  # Get the most recent funding rate
            timestamp = int(data['fundingTime']) / 1000
            time_str = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            table = Table(title=f"Funding Information for [green]{data['symbol']}[/green]")
            table.add_column("Metric", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")

            table.add_row("Funding Rate", data['fundingRate'])
            table.add_row("Funding Time", f"{time_str} UTC")

            console.print(table)
        elif 'code' in data:
            console.print(f"[bold red]Error: {data['msg']}[/bold red]")
        else:
            console.print("[bold red]No data available.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

def get_position_data():
    symbol = Prompt.ask("[bold yellow]Enter the symbol (e.g., BTCUSDT)[/bold yellow]").upper()
    valid_periods = ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]
    console.print(f"Available periods: [green]{', '.join(valid_periods)}[/green]")
    period = Prompt.ask("[bold yellow]Enter the period[/bold yellow]")
    if period not in valid_periods:
        console.print("[bold red]Invalid period selected.[/bold red]")
        return
    url = "https://fapi.binance.com/futures/data/topLongShortPositionRatio"
    params = {'symbol': symbol, 'period': period, 'limit': 1}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            item = data[0]  # Get the most recent data point
            timestamp = int(item['timestamp']) / 1000
            time_str = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            table = Table(title=f"Most Recent Position Data for [green]{symbol}[/green] over period '[green]{period}[/green]'")
            table.add_column("Metric", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")

            table.add_row("Timestamp", f"{time_str} UTC")
            table.add_row("Long/Short Ratio", item['longShortRatio'])
            table.add_row("Long Account", item['longAccount'])
            table.add_row("Short Account", item['shortAccount'])

            console.print(table)
        elif 'code' in data:
            console.print(f"[bold red]Error: {data['msg']}[/bold red]")
        else:
            console.print("[bold red]No data available.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

def measure_latency():
    url = "https://fapi.binance.com/fapi/v1/ping"
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        if response.status_code == 200:
            console.print(f"\n[bold]Latency to Binance Futures API:[/bold] [green]{latency:.2f} ms[/green]")
        else:
            console.print(f"[bold red]Error: Received status code {response.status_code}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()
