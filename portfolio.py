import csv
import os


CSV_FILE = "portfolio_summary.csv"


def get_stock_data():
    """Get stock details from the user."""
    portfolio = []

    print("\n=== Stock Portfolio Performance Tracker ===")
    print("Enter stock details. Type 'done' to finish.\n")

    while True:
        symbol = input("Stock ticker (or 'done'): ").strip().upper()

        if symbol == "DONE":
            break

        if not symbol:
            print("Error: Stock ticker cannot be empty.")
            continue

        try:
            buy_price = float(input("Buy price: "))
            quantity = int(input("Number of shares: "))
            current_price = float(input("Current price: "))

            if buy_price <= 0 or quantity <= 0 or current_price < 0:
                print("Error: Prices and quantity must be valid.")
                continue

        except ValueError:
            print("Error: Enter valid numeric values.")
            continue

        portfolio.append({
            "symbol": symbol,
            "buy_price": buy_price,
            "quantity": quantity,
            "current_price": current_price
        })

        print("Stock added successfully!\n")

    return portfolio


def calculate_performance(portfolio):
    """Calculate investment, market value, and profit or loss."""
    results = []

    for stock in portfolio:
        invested = stock["buy_price"] * stock["quantity"]
        market_value = stock["current_price"] * stock["quantity"]
        profit_loss = market_value - invested

        percentage = (profit_loss / invested) * 100

        results.append({
            "symbol": stock["symbol"],
            "buy_price": stock["buy_price"],
            "quantity": stock["quantity"],
            "current_price": stock["current_price"],
            "invested": invested,
            "market_value": market_value,
            "profit_loss": profit_loss,
            "percentage": percentage
        })

    return results


def display_summary(results):
    """Display the portfolio summary in the terminal."""
    print("\n" + "=" * 95)
    print("             STOCK PORTFOLIO PERFORMANCE SUMMARY")
    print("=" * 95)

    if not results:
        print("No stock records available.")
        return

    print(
        f"{'Symbol':<10}{'Buy Price':>12}{'Qty':>8}"
        f"{'Current':>12}{'Invested':>14}{'Market Value':>16}"
        f"{'Profit/Loss':>15}{'Gain/Loss %':>14}"
    )

    print("-" * 101)

    total_invested = 0
    total_market_value = 0

    for stock in results:
        print(
            f"{stock['symbol']:<10}"
            f"{stock['buy_price']:>12.2f}"
            f"{stock['quantity']:>8}"
            f"{stock['current_price']:>12.2f}"
            f"{stock['invested']:>14.2f}"
            f"{stock['market_value']:>16.2f}"
            f"{stock['profit_loss']:>15.2f}"
            f"{stock['percentage']:>13.2f}%"
        )

        total_invested += stock["invested"]
        total_market_value += stock["market_value"]

    total_profit_loss = total_market_value - total_invested

    total_percentage = (
        (total_profit_loss / total_invested) * 100
        if total_invested else 0
    )

    print("-" * 101)
    print(f"Total Investment   : {total_invested:.2f}")
    print(f"Current Value      : {total_market_value:.2f}")
    print(f"Total Profit/Loss  : {total_profit_loss:.2f}")
    print(f"Overall Return     : {total_percentage:.2f}%")


def save_to_csv(results):
    """Save portfolio performance to a CSV file."""
    fieldnames = [
        "symbol",
        "buy_price",
        "quantity",
        "current_price",
        "invested",
        "market_value",
        "profit_loss",
        "percentage"
    ]

    try:
        with open(
            CSV_FILE,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\nPortfolio summary saved to: {os.path.abspath(CSV_FILE)}")

    except OSError as error:
        print(f"Error saving CSV file: {error}")


def main():
    """Run the stock portfolio tracker."""
    portfolio = get_stock_data()
    results = calculate_performance(portfolio)
    display_summary(results)
    save_to_csv(results)


if __name__ == "__main__":
    main()
