import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup

def get_crypto_prices():
    url = "https://coinmarketcap.com/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = soup.find_all("div", class_="sc-a0353bbc-0 gDrtaY")
        names = soup.find_all("p", class_="sc-4984dd93-0 kKpPOn")
        top_prices = []
        top_names = []
        for i in range(selected_table_size):
            top_prices.append(prices[i].find("span").text)
            top_names.append(names[i].text)
        return top_names, top_prices

def search_price_by_name(search_entry):
    search_term = search_entry.get()

    if not search_term:
        messagebox.showinfo("Error", "Please enter a cryptocurrency name.")
        return

    url = f"https://coinmarketcap.com/currencies/{search_term}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        coin_price = soup.find("span", class_="sc-f70bb44c-0 jxpCgO base-text").text
        coin_name = soup.find("span", class_="coin-name-pc").text

        messagebox.showinfo("Last Price", f"The last price of {coin_name} is {coin_price}")
    else:
        messagebox.showinfo("Error", "Cryptocurrency not found or unable to fetch data.")

def show_prices():
    # Clear existing items in the treeview
    for item in treeview.get_children():
        treeview.delete(item)

    url = "https://www.tgju.org/profile/price_dollar_rl"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        dollar = soup.find("span", class_="value").find("span").text

        # Remove comma and convert to integer
        dollar = int(dollar.replace(",", ""))
        # Remove the last character
        dollar = str(dollar)[:-1]

        names, prices = get_crypto_prices()
        for i in range(selected_table_size):
            # Remove dollar sign and commas from the cryptocurrency prices
            clean_price = prices[i].replace("$", "").replace(",", "")
            
            # Calculate Toman values
            toman_value = float(clean_price) * float(dollar)
            # Insert values into the treeview
            treeview.insert("", i, values=(i + 1, names[i], f"{prices[i]}", f"{toman_value:.2f}"))
    else:
        messagebox.showinfo("Error", "Unable to fetch dollar value.")

def update_table_size(event):
    global selected_table_size
    selected_table_size = int(table_size_var.get())
    show_prices()

# Tkinter setup
root = tk.Tk()
root.title("Crypto Prices App")

# Frame for search and fetch section
search_frame = ttk.Frame(root, padding="10")
search_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

# Entry for search term
search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=0, padx=5)

# Button to search for the coin
search_button = tk.Button(search_frame, text="Search", command=lambda: search_price_by_name(search_entry))
search_button.grid(row=0, column=1, padx=5)

# Label for table size
table_size_label = tk.Label(root, text="Table Size:")
table_size_label.grid(row=1, column=0, pady=5, sticky="w")

# Combobox for selecting table size
table_size_var = tk.StringVar()
table_size_combobox = ttk.Combobox(root, textvariable=table_size_var, values=list(range(1, 11)))
table_size_combobox.set(5)  # Default value
table_size_combobox.grid(row=1, column=1, pady=5, sticky="w")
table_size_combobox.bind("<<ComboboxSelected>>", update_table_size)

# Button to fetch and display top prices
fetch_button = tk.Button(root, text="Fetch Prices", command=show_prices)
fetch_button.grid(row=2, column=0, columnspan=2, pady=10)

# Table to display cryptocurrency prices
columns = ("#", "Cryptocurrency", "Price (USD)", "Toman")
treeview = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    treeview.heading(col, text=col)

treeview.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Initial table size
selected_table_size = int(table_size_combobox.get())

# Configure grid weights
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)

root.mainloop()
