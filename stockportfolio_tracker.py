import csv
import random
import time

# Base stock prices
base_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "AMZN": 130,
    "META": 320
}

portfolio = {}      # stores stock → quantity
buy_price = {}      # stores stock → average purchase price

def get_live_price(stock):
    """Simulates live stock price fluctuation."""
    base = base_prices[stock]
    fluctuation = random.uniform(-5, 5)   # +/- ₹5 random change
    live_price = round(base + fluctuation, 2)
    return live_price


def add_stock():
    print("\n📌 Add a Stock to Portfolio")
    stock = input("Enter stock symbol: ").upper()

    if stock not in base_prices:
        print("❌ Invalid stock! Try: AAPL, TSLA, GOOGL, AMZN, META.")
        return
    
    try:
        qty = int(input("Enter quantity: "))
    except ValueError:
        print("❌ Invalid quantity!")
        return
    
    price = get_live_price(stock)
    portfolio[stock] = portfolio.get(stock, 0) + qty

    # update average buy price
    if stock in buy_price:
        # weighted avg
        total_prev = buy_price[stock] * (portfolio[stock] - qty)
        total_new = price * qty
        buy_price[stock] = (total_prev + total_new) / portfolio[stock]
    else:
        buy_price[stock] = price

    print(f"✔ Added {qty} of {stock} at ₹{price}")


def view_portfolio():
    print("\n📊 Your Portfolio")
    print("-" * 40)

    if not portfolio:
        print("No stocks yet!")
        return

    total_value = 0
    total_investment = 0

    for stock, qty in portfolio.items():
        live = get_live_price(stock)
        bought = buy_price[stock]

        value = live * qty
        investment = bought * qty
        profit = value - investment

        total_value += value
        total_investment += investment

        print(f"{stock} | Qty: {qty}")
        print(f"   Buy Price: ₹{bought:.2f}")
        print(f"   Current Price: ₹{live}")
        print(f"   Investment: ₹{investment:.2f}")
        print(f"   Current Value: ₹{value:.2f}")
        print(f"   Profit/Loss: ₹{profit:.2f}")
        print("-" * 40)

    print(f"💰 Total Investment: ₹{total_investment:.2f}")
    print(f"📈 Total Current Value: ₹{total_value:.2f}")
    print(f"🏦 Net Profit/Loss: ₹{total_value - total_investment:.2f}")


def export_csv():
    if not portfolio:
        print("❌ No data to export!")
        return

    filename = "advanced_portfolio.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Quantity", "Buy Price", "Live Price", "Investment", "Current Value", "Profit/Loss"])

        for stock, qty in portfolio.items():
            live = get_live_price(stock)
            bought = buy_price[stock]
            investment = bought * qty
            value = live * qty
            profit = value - investment

            writer.writerow([stock, qty, bought, live, investment, value, profit])

    print(f"📁 CSV Exported Successfully → {filename}")


def menu():
    while True:
        print("\n===== STOCK PORTFOLIO TRACKER =====")
        print("1. Add Stock")
        print("2. View Portfolio")
        print("3. Export to CSV")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_stock()
        elif choice == "2":
            view_portfolio()
        elif choice == "3":
            export_csv()
        elif choice == "4":
            print("✔ Exiting... Bye!")
            break
        else:
            print("❌ Invalid option. Try again.")

menu()
