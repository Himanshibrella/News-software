import tkinter as tk
import requests as r
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser



# ----------------- Setup Window --------------------
root = tk.Tk()
root.geometry("800x600")
root.title("UK NEWS")
root.configure(bg="white")



# ----------------- Fetch News --------------------
data = r.get("https://newsapi.org/v2/everything?q=tesla&from=2025-03-17&sortBy=publishedAt&apiKey=08ac9b5d220d4b69bdab35e25dc7fc63")
jsondata = data.json()

# ----------------- Scrollable Frame Setup --------------------
container = tk.Frame(root)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container, bg="white")
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ----------------- Card Creator --------------------
def create_card(parent, item, row=0):
    # Configure parent column to center content
    parent.grid_columnconfigure(0, weight=1)

    # Create the card frame
    card = tk.Frame(parent, bg="#f8bbd0", bd=2, relief="raised")

    # Place the card centered using grid
    card.grid(row=row, column=0, pady=10, padx=10, sticky="n")

    title_text = item.get("title", "No Title")
    desc_text = item.get("description", "No Description")
    image_url = item.get("urlToImage")
    article_url = item.get("url")

    title = tk.Label(card, text=title_text, bg="white", font=("Helvetica", 16, "bold"), fg="#880e4f", wraplength=300, justify="left", anchor="w")
    desc = tk.Label(card, text=desc_text, bg="white", font=("Helvetica", 10), fg="#4a4a4a", wraplength=300, justify="left", anchor="w")
    

    if article_url:
        def open_link():
            webbrowser.open_new(article_url)

        button = tk.Button(card, text="Read More", command=open_link, bg="#d81b60", fg="white", relief="flat", font=("Helvetica", 10, "bold"))
        button.pack(pady=(0, 10))

    title = tk.Label(card, text=title_text, bg="white", font=("Helvetica", 14, "bold"), wraplength=300, justify="left", anchor="w")
    desc = tk.Label(card, text=desc_text, bg="white", font=("Helvetica", 10), wraplength=300, justify="left", anchor="w")

    title.pack(fill="x", padx=10, pady=(10, 0))
    desc.pack(fill="both", expand=True, padx=10, pady=(5, 10))
    # IMAGE LOADER

    return card

# ----------------- Layout Cards in Grid --------------------
columns = 3  # 2 columns per row

for index, item in enumerate(jsondata.get('articles', [])):
    row = index // columns
    col = index % columns
    card = create_card(scrollable_frame, item)
    card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    # Optional: Make cards stretch evenly
    scrollable_frame.grid_columnconfigure(col, weight=2)

# ----------------- Start App --------------------
root.mainloop()
