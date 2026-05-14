import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime

root = tk.Tk()

root.geometry("1350x750")
root.resizable(False, False)

BG_COLOR = "slategray1"

PRODUCTS_IMAGES = [
    {"name": "Oreo", "image": "Biscuits/oreo.jpeg", "price": 25.00},
    {"name": "Bingo", "image": "Biscuits/bingo.png", "price": 45.99},
    {"name": "Soy Sauce", "image": "Condiments/soysauce.png", "price": 12.50},
    {"name": "Vinegar", "image": "Condiments/vinegar.jpg", "price": 12.50},
    {"name": "Oil", "image": "Condiments/oil.jpg", "price": 12.50},
    {"name": "Creme", "image": "Dairy/creme.png", "price": 12.50},
    {"name": "Eden", "image": "Dairy/eden.jpg", "price": 12.50},
    {"name": "Nestle", "image": "Dairy/nestle.jpeg", "price": 12.50},
    {"name": "Gatorade", "image": "Energy drink/gatorade.jpeg", "price": 12.50},
    {"name": "Sting", "image": "Energy drink/sting.jpg", "price": 12.50},
    {"name": "Tomato", "image": "Fruits - Vegetables/tomato.png", "price": 12.50},
    {"name": "Melon", "image": "Fruits - Vegetables/melon.jpg", "price": 12.50},
    {"name": "Cabbage", "image": "Fruits - Vegetables/cabbage.png", "price": 12.50},
    {"name": "C2", "image": "Juice/c2.bmp", "price": 12.50},
    {"name": "Del Monte", "image": "Juice/delmonte.jpeg", "price": 12.50},
    {"name": "Zesto", "image": "Juice/zesto.bmp", "price": 12.50},
    {"name": "Marty's", "image": "Junk Foods/martys.jpg", "price": 12.50},
    {"name": "Piattos", "image": "Junk Foods/piattos.png", "price": 12.50},
    {"name": "Coca Cola", "image": "Softdrinks/cocacola.bmp", "price": 12.50},
    {"name": "Sprite", "image": "Softdrinks/sprite.bmp", "price": 12.50},



    # ... add the rest of your 20 items here
]

# Cart dictionary to track items and quantities
cart = {}

top_frame = tk.Frame(root, width=1350, height=550, bg=BG_COLOR)
top_frame.grid(row=0, column=0)
  
# number frame
numbers_frame = tk.Frame(top_frame, bg="gainsboro", width=350, height=490, borderwidth=4, relief="ridge")
numbers_frame.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

  
def press(n):
    entry_cost.config(state="normal")
    
    current_value = entry_cost.get()
    
    # if ang n kay '.' 
    # and ang entry nato is empty
    # then dili nato e add ang period
    
    if n == '.' and len(current_value) == 0:
        entry_cost.config(state="disabled")
        return
    
    entry_cost.delete(0, tk.END)
    entry_cost.insert(0, str(current_value) + str(n))
        
    entry_cost.config(state="disabled")


def clear_cost():
    entry_cost.config(state="normal")
    entry_cost.delete(0, tk.END)
    entry_cost.config(state="disabled")


def save_receipt():
    """Generate and save receipt as a .txt file"""
    try:
        # Get all items from the tree
        items = tree.get_children()
        
        if not items:
            messagebox.showwarning("No Items", "Please add items to the receipt before saving.")
            return
        
        # Generate receipt content
        receipt = "=" * 50 + "\n"
        receipt += "RECEIPT\n"
        receipt += "=" * 50 + "\n"
        receipt += f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += "=" * 50 + "\n\n"
        
        receipt += f"{'Item':<25} {'Qty':>8} {'Amount':>15}\n"
        receipt += "-" * 50 + "\n"
        
        for item in items:
            values = tree.item(item)['values']
            item_name = values[0]
            quantity = values[1]
            amount = values[2]
            receipt += f"{item_name:<25} {quantity:>8} ₱{float(amount):>13.2f}\n"
        
        receipt += "-" * 50 + "\n"
        receipt += f"\nSubtotal: ₱{entry_subtotal.get() if entry_subtotal.get() else '0.00'}\n"
        receipt += f"Tax:      ₱{entry_tax.get() if entry_tax.get() else '0.00'}\n"
        receipt += f"Total:    ₱{entry_total.get() if entry_total.get() else '0.00'}\n"
        
        if entry_modepayment.get():
            receipt += f"\nMode of Payment: {entry_modepayment.get()}\n"
        
        if entry_change.get():
            receipt += f"Change: ₱{entry_change.get()}\n"
        
        receipt += "\n" + "=" * 50 + "\n"
        receipt += "Thank you for your purchase!\n"
        receipt += "=" * 50 + "\n"
        
        # Open file dialog to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"Receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if file_path:
            with open(file_path, 'w') as file:
                file.write(receipt)
            messagebox.showinfo("Success", f"Receipt saved successfully!\n{file_path}")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")
    

def add_to_cart(product_name, price):
    """Add item to cart or increase quantity if already exists"""
    if product_name in cart:
        cart[product_name]['quantity'] += 1
    else:
        cart[product_name] = {'price': price, 'quantity': 1}
    
    update_tree_view()
    update_totals()


def update_tree_view():
    """Update the tree view with current cart items"""
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
    
    # Add items from cart
    for item_name, item_data in cart.items():
        quantity = item_data['quantity']
        price = item_data['price']
        amount = quantity * price
        tree.insert('', tk.END, values=(item_name, quantity, f"₱{amount:.2f}"))


def update_totals():
    """Calculate and update subtotal, tax, and total"""
    subtotal = sum(item_data['price'] * item_data['quantity'] for item_data in cart.values())
    
    # Get tax if entered, otherwise assume 0
    tax_rate = 0.0
    try:
        tax_value = float(entry_tax.get()) if entry_tax.get() else 0.0
        if tax_value > 1:  # If value is greater than 1, assume it's a peso amount
            tax = tax_value
        else:  # Otherwise treat as percentage
            tax = subtotal * tax_value
    except:
        tax = 0.0
    
    total = subtotal + tax
    
    # Update entry fields
    entry_subtotal.delete(0, tk.END)
    entry_subtotal.insert(0, f"{subtotal:.2f}")
    
    entry_total.delete(0, tk.END)
    entry_total.insert(0, f"{total:.2f}")


def reset_cart():
    """Clear the cart and reset all entries"""
    global cart
    cart = {}
    update_tree_view()
    
    entry_subtotal.delete(0, tk.END)
    entry_tax.delete(0, tk.END)
    entry_total.delete(0, tk.END)
    entry_modepayment.delete(0, tk.END)
    entry_change.delete(0, tk.END)


def remove_selected_item():
    """Remove selected item from tree"""
    selected_item = tree.selection()
    if selected_item:
        # Get the item name from the tree
        item_values = tree.item(selected_item[0])['values']
        item_name = item_values[0]
        
        # Remove from cart
        if item_name in cart:
            del cart[item_name]
        
        update_tree_view()
        update_totals()
    
  
# number buttons
btn1 = tk.Button(numbers_frame, text='1', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(1))
btn2 = tk.Button(numbers_frame, text='2', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(2))
btn3 = tk.Button(numbers_frame, text='3', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(3))
btn4 = tk.Button(numbers_frame, text='4', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(4))
btn5 = tk.Button(numbers_frame, text='5', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(5))
btn6 = tk.Button(numbers_frame, text='6', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(6))
btn7 = tk.Button(numbers_frame, text='7', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(7))
btn8 = tk.Button(numbers_frame, text='8', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(8))
btn9 = tk.Button(numbers_frame, text='9', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(9))
btn0 = tk.Button(numbers_frame, text='0', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(0))
btnperiod = tk.Button(numbers_frame, text='.', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press('.'))
btnclear = tk.Button(numbers_frame, text='C', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda:clear_cost())

btn1.grid(row=0, column=0, sticky="nsew")
btn2.grid(row=0, column=1, sticky="nsew")
btn3.grid(row=0, column=2, sticky="nsew")
btn4.grid(row=1, column=0, sticky="nsew")
btn5.grid(row=1, column=1, sticky="nsew")
btn6.grid(row=1, column=2, sticky="nsew")
btn7.grid(row=2, column=0, sticky="nsew")
btn8.grid(row=2, column=1, sticky="nsew")
btn9.grid(row=2, column=2, sticky="nsew")
btn0.grid(row=3, column=0, sticky="nsew")
btnperiod.grid(row=3, column=1, columnspan=2, sticky="nsew")
btnclear.grid(row=4, column=0, columnspan=3, sticky="nsew")

# .grid_rowconfigure 
# -- para mo expand ang mga buttons sa width saiyang parent

for i in range(6):  # rows
    numbers_frame.grid_rowconfigure(i, weight=1)

for j in range(3):  # columns
    numbers_frame.grid_columnconfigure(j, weight=1)
  
# products frame
products_frame = tk.Frame(top_frame, bg="gray")
products_frame.grid(row=0, column=1, sticky="nsew")

# middle_frame
middle_frame = tk.Frame(top_frame, width=390, height=490, borderwidth=4, bg="gainsboro", relief="ridge")
middle_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# item list
columns = ("Item", "Quantity", "Amount")
tree = ttk.Treeview(middle_frame, columns=columns, show="headings", height=16)
tree.heading("Item", text="Item")
tree.heading("Quantity", text="Quantity")
tree.heading("Amount", text="Amount")
tree.column("Item", width=180, anchor="w")
tree.column("Quantity", width=60, anchor="center")
tree.column("Amount", width=120, anchor="center")

scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.grid(row=0, column=0, sticky="nsew", padx=(4, 0), pady=(4, 0))
scrollbar.grid(row=0, column=1, sticky="ns", pady=(4, 0))

# barcode (not yet working)
barcode = tk.Canvas(middle_frame, height=70, highlightthickness=0, bg="gainsboro")
barcode.grid(row=3, columnspan=2, padx=5, pady=5, sticky="ew")

# right frame

products_frame = tk.Frame(top_frame, bg="gainsboro", width=575, height=490,
                          borderwidth=4, relief="ridge")
products_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

products_frame_row = 0
products_frame_col = 0
for image in PRODUCTS_IMAGES:  # The variable name is 'image'
    item_container = tk.Frame(products_frame, bg="white", borderwidth=1, relief="groove")
    item_container.grid(row=products_frame_row, column=products_frame_col, padx=3.5 , pady=4)

    # 1. Process image
    product_image_1 = Image.open(image["image"])
    product_image_1 = product_image_1.resize((100, 80))
    product_image_1_photo = ImageTk.PhotoImage(product_image_1)

    # 2. Use .pack() for both so they stack correctly
    product_image_1_label = tk.Label(item_container, image=product_image_1_photo, bg="white", cursor="hand2")
    product_image_1_label.image = product_image_1_photo
    product_image_1_label.pack(side="top", pady=1)  # Changed .grid to .pack
    
    # Bind click event to add item to cart
    product_image_1_label.bind("<Button-1>", lambda e, name=image["name"], price=image["price"]: add_to_cart(name, price))

    # 3. Use 'image' instead of 'item' here
    price_text = f"₱{image['price']:.2f}"
    price_label = tk.Label(item_container, text=price_text, font=("Tahoma", 9, "bold"), bg="white", fg="darkgreen")
    price_label.pack(side="bottom", fill="x", pady=2)

    # 4. Handle grid for the container
    products_frame_col += 1
    if (products_frame_col == 5):
        products_frame_row += 1
        products_frame_col = 0

# kani para sundon sa frame ang gihatag nato nga width and height nya,
# kay by default automatic iyang width and height
top_frame.grid_propagate(False)
numbers_frame.grid_propagate(False)
middle_frame.grid_propagate(False)
products_frame.grid_propagate(False)

# bottom frame
bottom_frame = tk.Frame(root, width=1350, height=200, borderwidth=4, bg=BG_COLOR)
bottom_frame.grid(row=1 , column=0, sticky="nsew")

# 3 bottom sections
bottomleft_frame = tk.Frame(bottom_frame, bg="gainsboro", width=437, height=180, relief="ridge", bd=3)
bottomleft_frame.grid(row=0 , column=0, padx=5, pady=5)

bottommiddle_frame = tk.Frame(bottom_frame, bg="gainsboro", width=437, height=180, relief="ridge", bd=3)
bottommiddle_frame.grid(row=0 , column=1, padx=5, pady=5)

bottomright_frame = tk.Frame(bottom_frame, bg="gainsboro", width=437, height=180, relief="ridge", bd=3)
bottomright_frame.grid(row=0 , column=2, padx=5, pady=5)

bottomleft_frame.grid_propagate(False)
bottommiddle_frame.grid_propagate(False)
bottomright_frame.grid_propagate(False)

# bottomleft_frame entries
tk.Label(bottomleft_frame, text="Subtotal", font=("Tahoma", 14), bg="gainsboro").grid(row=0, column=0, padx=12, pady=12)
entry_subtotal = tk.Entry(bottomleft_frame, width=20, font=("Tahoma", 12))
entry_subtotal.grid(row=0, column=1, padx=12, pady=12)

tk.Label(bottomleft_frame, text="Tax", font=("Tahoma", 14), bg="gainsboro").grid(row=1, column=0, padx=12, pady=12)
entry_tax = tk.Entry(bottomleft_frame, width=20, font=("Tahoma", 12))
entry_tax.grid(row=1, column=1, padx=12, pady=12)

tk.Label(bottomleft_frame, text="Total", font=("Tahoma", 14), bg="gainsboro").grid(row=2, column=0, padx=12, pady=12)
entry_total = tk.Entry(bottomleft_frame, width=20, font=("Tahoma", 12))
entry_total.grid(row=2, column=1, padx=12, pady=12)

# bottommiddle_frame entries
tk.Label(bottommiddle_frame, text="Mode of Payment", font=("Tahoma", 14), bg="gainsboro").grid(row=0, column=0, padx=12, pady=12)
entry_modepayment = tk.Entry(bottommiddle_frame, width=20, font=("Tahoma", 12))
entry_modepayment.grid(row=0, column=1, padx=12, pady=12)

tk.Label(bottommiddle_frame, text="Cost", font=("Tahoma", 14), bg="gainsboro").grid(row=1, column=0, padx=12, pady=12)
entry_cost = tk.Entry(bottommiddle_frame, width=20, font=("Tahoma", 12), state="disabled")
entry_cost.grid(row=1, column=1, padx=12, pady=12)

tk.Label(bottommiddle_frame, text="Change", font=("Tahoma", 14), bg="gainsboro").grid(row=2, column=0, padx=12, pady=12)
entry_change = tk.Entry(bottommiddle_frame, width=20, font=("Tahoma", 12))
entry_change.grid(row=2, column=1, padx=12, pady=12)

# bottomright_frame entries
pay_btn = tk.Button(bottomright_frame, text="Pay", font=("Tahoma", 16), width=16, height=3)
reset_btn = tk.Button(bottomright_frame, text="Reset", font=("Tahoma", 16), width=16, height=3, command=reset_cart)
save_btn = tk.Button(bottomright_frame, text="Save", font=("Tahoma", 16), width=16, height=3, command=save_receipt)
removeitem_btn = tk.Button(bottomright_frame, text="Remove", font=("Tahoma", 16), width=16, height=3, command=remove_selected_item)

pay_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
reset_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
save_btn.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
removeitem_btn.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

for i in range(2):
    bottomright_frame.grid_rowconfigure(i, weight=1)
    bottomleft_frame.grid_columnconfigure(i, weight=1)

root.mainloop()
