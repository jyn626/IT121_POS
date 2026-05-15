import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime

root = tk.Tk()

root.geometry("1350x750")
root.resizable(False, False)

BG_COLOR = "#4e69a2"

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
]

# Cart dictionary to track items and quantities
cart = {}
payment_done = False

top_frame = tk.Frame(root, width=1350, height=550, bg=BG_COLOR)
top_frame.grid(row=0, column=0)
  
# number frame
numbers_frame = ttk.Frame(top_frame, width=300, height=490, style="Styled.TFrame")
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
        if not payment_done:
            messagebox.showwarning("Payment Required", "Please complete payment before saving the receipt.")
            return
        
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
        
        name_width = 28
        qty_width = 6
        amount_width = 12
        sep_line = f"+{'-' * (name_width + 2)}+{'-' * (qty_width + 2)}+{'-' * (amount_width + 2)}+\n"
        receipt += sep_line
        receipt += f"| {'Item':<{name_width}} | {'Qty':^{qty_width}} | {'Amount':^{amount_width}} |\n"
        receipt += sep_line
        
        for item_name, item_data in cart.items():
            quantity = item_data['quantity']
            amount_value = item_data['price'] * quantity
            amount_str = f"₱{amount_value:.2f}"
            receipt += f"| {item_name:<{name_width}} | {quantity:^{qty_width}} | {amount_str:>{amount_width}} |\n"
        
        receipt += sep_line
        receipt += f"\nSubtotal: ₱{entry_subtotal.get() if entry_subtotal.get() else '0.00'}\n"
        receipt += f"Tax:      ₱{entry_tax.get() if entry_tax.get() else '0.00'}\n"
        receipt += f"Total:    ₱{entry_total.get() if entry_total.get() else '0.00'}\n"
        
        selected_payment = entry_modepayment.get().strip()
        if selected_payment and selected_payment != "Select":
            receipt += f"\nMode of Payment: {selected_payment}\n"
        
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
            prefix = "\n\n" if os.path.exists(file_path) and os.path.getsize(file_path) > 0 else ""
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(prefix + receipt)
            messagebox.showinfo("Success", f"Receipt appended successfully!\n{file_path}")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")
    

def process_payment():
    """Validate payment before saving receipt."""
    global payment_done
    
    if not cart:
        messagebox.showwarning("No Items", "Please add items to the cart before payment.")
        return
    
    selected_payment = entry_modepayment.get().strip()
    if not selected_payment or selected_payment == "Select":
        messagebox.showwarning("Payment Required", "Please select a mode of payment before paying.")
        return
    
    try:
        total_value = float(entry_total.get()) if entry_total.get() else 0.0
    except ValueError:
        messagebox.showerror("Invalid Total", "Total is not a valid number. Please check the tax and cart values.")
        return
    
    if total_value <= 0:
        messagebox.showwarning("Invalid Total", "Total amount must be greater than zero.")
        return
    
    try:
        paid_value = float(entry_cost.get()) if entry_cost.get() else 0.0
    except ValueError:
        messagebox.showerror("Invalid Payment", "Cost must be a valid number entered using the keypad.")
        return
    
    if paid_value < total_value:
        messagebox.showwarning("Insufficient Payment", "Payment amount is less than the total. Please enter enough cash.")
        return
    
    change_amount = paid_value - total_value
    entry_change.delete(0, tk.END)
    entry_change.insert(0, f"{change_amount:.2f}")
    payment_done = True
    messagebox.showinfo("Payment Processed", f"Payment accepted. Change: ₱{change_amount:.2f}")


def add_to_cart(product_name, price):
    """Add item to cart or increase quantity if already exists"""
    global payment_done
    payment_done = False
    
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
    # try:
    #     tax_value = float(entry_tax.get()) if entry_tax.get() else 0.0
    #     if tax_value > 1:  # If value is greater than 1, assume it's a peso amount
    #         tax = tax_value
    #     else:  # Otherwise treat as percentage
    #         tax = subtotal * tax_value
    # except:
    #     tax = 0.0
    
    # total = subtotal + tax
    
    # Update entry fields
    entry_subtotal.delete(0, tk.END)
    entry_subtotal.insert(0, f"{subtotal:.2f}")
    
    entry_total.delete(0, tk.END)
    # entry_total.insert(0, f"{total:.2f}")


def reset_cart():
    """Clear the cart and reset all entries"""
    global cart, payment_done
    cart = {}
    payment_done = False
    update_tree_view()
    
    entry_subtotal.delete(0, tk.END)
    entry_tax.delete(0, tk.END)
    entry_total.delete(0, tk.END)
    entry_change.delete(0, tk.END)
    entry_cost.delete(0, tk.END)
    entry_modepayment.set('')
    entry_modepayment.current(-1)


def remove_selected_item():
    """Remove selected item from tree"""
    global payment_done
    payment_done = False
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
    
  
style = ttk.Style(root)
style.theme_use('clam')

style.configure('W.TButton', font=
               ('Tahoma', 12, 'normal'),
                foreground='black',
                background="whitesmoke",
                borderwidth=0,
                padding=((0, 50)))

style.configure('Bottom.TButton', font=
               ('Tahoma', 12, 'normal'),
                foreground='black',
                background="whitesmoke",
                borderwidth=0,
                )

style.configure(
        "Styled.Treeview",
        font=("Tahoma", 12),
        rowheight=26,
        background="white",
        fieldbackground="white",
        borderwidth=2
    )
  
style.configure(
    "Styled.TEntry",
    padding=(5, 5)
)

style.configure(
    "W.TCombobox",
    font=("Tahoma", 12),
)

root.option_add('*TCombobox*Listbox.font', ('Tahoma', 12))
  
style.configure(
    "Styled.TFrame",
    background='whitesmoke',
    borderwidth=0,
)  
  
# number buttons
btn1 = ttk.Button(numbers_frame, text='1', command=lambda: press(1), style="W.TButton")
btn2 = ttk.Button(numbers_frame, text='2', command=lambda: press(2), style="W.TButton")
btn3 = ttk.Button(numbers_frame, text='3', command=lambda: press(3), style="W.TButton")
btn4 = ttk.Button(numbers_frame, text='4', command=lambda: press(4), style="W.TButton")
btn5 = ttk.Button(numbers_frame, text='5', command=lambda: press(5), style="W.TButton")
btn6 = ttk.Button(numbers_frame, text='6', command=lambda: press(6), style="W.TButton")
btn7 = ttk.Button(numbers_frame, text='7', command=lambda: press(7), style="W.TButton")
btn8 = ttk.Button(numbers_frame, text='8', command=lambda: press(8), style="W.TButton")
btn9 = ttk.Button(numbers_frame, text='9', command=lambda: press(9), style="W.TButton")
btn0 = ttk.Button(numbers_frame, text='0', command=lambda: press(0), style="W.TButton")
btnperiod = ttk.Button(numbers_frame, text='.', command=lambda: press('.'), style="W.TButton")
btnclear = ttk.Button(numbers_frame, text='C', command=lambda:clear_cost(), style="W.TButton")

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
btnperiod.grid(row=3, column=1, sticky="nsew")
btnclear.grid(row=3, column=2, sticky="nsew")

# .grid_rowconfigure 
# -- para mo expand ang mga buttons sa width saiyang parent

for i in range(6):  # rows
    numbers_frame.grid_rowconfigure(i, weight=1)

for j in range(3):  # columns
    numbers_frame.grid_columnconfigure(j, weight=1)
  
# middle_frame
middle_frame = ttk.Frame(top_frame, width=380, height=490, style="Styled.TFrame")
middle_frame.grid(row=0, column=1, sticky="nsew")

# style.configure(".", font=('Helvetica', 8), foreground="white")
# style.configure("Treeview", foreground='red')
# style.configure("Treeview.Heading", foreground='green')  # <

# item list
columns = ("Item", "Quantity", "Amount")
tree = ttk.Treeview(middle_frame, columns=columns, show="headings", height=19, style='Styled.Treeview')
tree.heading("Item", text="Item")
tree.heading("Quantity", text="Quantity")
tree.heading("Amount", text="Amount")
tree.column("Item", width=170, anchor="w")  
tree.column("Quantity", width=80, anchor="center")
tree.column("Amount", width=100, anchor="center")

scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.grid(row=0, column=0, sticky="nsew", padx=(4, 0), pady=(4, 0))
scrollbar.grid(row=0, column=1, sticky="ns", pady=(4, 0))

# barcode (not yet working)
# barcode = tk.Canvas(middle_frame, height=70, highlightthickness=0, bg="whitesmoke")
# barcode.grid(row=3, columnspan=2, padx=5, pady=5, sticky="ew")

# right frame

products_frame = ttk.Frame(top_frame, height=490, style="Styled.TFrame")
products_frame.grid(row=0, column=2, padx=2, ipadx=5, pady=2, sticky="nsew")

products_frame_row = 0
products_frame_col = 0
for image in PRODUCTS_IMAGES:  # The variable name is 'image'
    item_container = ttk.Frame(products_frame, width=200)
    item_container.grid(row=products_frame_row, column=products_frame_col, padx=2 , pady=2)

    # 1. Process image
    product_image_1 = Image.open(image["image"])
    product_image_1 = product_image_1.resize((123, 100))
    product_image_1_photo = ImageTk.PhotoImage(product_image_1)

    # 2. Use .pack() for both so they stack correctly
    product_image_1_label = tk.Label(item_container, image=product_image_1_photo, bg="white", cursor="hand2")
    product_image_1_label.image = product_image_1_photo
    product_image_1_label.pack(pady=1)  # Changed .grid to .pack
    
    # Bind click event to add item to cart
    product_image_1_label.bind("<Button-1>", lambda e, name=image["name"], price=image["price"]: add_to_cart(name, price))

    # 3. Use 'image' instead of 'item' here
    price_text = f"₱{image['price']:.2f}"
    price_label = tk.Label(item_container, text=price_text, font=("Tahoma", 9, "bold"), bg="white", fg="darkgreen")
    price_label.pack(fill="x", pady=1)

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
# products_frame.grid_propagate(False)

# bottom frame
bottom_frame = ttk.Frame(root, width=1350, height=200)
bottom_frame.grid(row=1 , column=0, sticky="nsew")

# 3 bottom sections
bottomleft_frame = ttk.Frame(bottom_frame, width=437, height=180, style="Styled.TFrame")
bottomleft_frame.grid(row=0 , column=0, padx=5)

bottommiddle_frame = ttk.Frame(bottom_frame, width=437, height=180, style="Styled.TFrame")
bottommiddle_frame.grid(row=0 , column=1, padx=5)

bottomright_frame = ttk.Frame(bottom_frame, width=437, height=180, style="Styled.TFrame")
bottomright_frame.grid(row=0 , column=2, padx=5)

bottomleft_frame.grid_propagate(False)
bottommiddle_frame.grid_propagate(False)
bottomright_frame.grid_propagate(False)

# bottomleft_frame entries
tk.Label(bottomleft_frame, text="Subtotal", font=("Tahoma", 12)).grid(row=0, column=0, padx=12, pady=12)
entry_subtotal = ttk.Entry(bottomleft_frame, width=20, font=("Tahoma", 12), style="Styled.TEntry")
entry_subtotal.grid(row=0, column=1, padx=12, pady=12)

# tk.Label(bottomleft_frame, text="Tax", font=("Tahoma", 12), bg="whitesmoke").grid(row=1, column=0, padx=12, pady=12)
# entry_tax = ttk.Entry(bottomleft_frame, width=20, font=("Tahoma", 12), style="Styled.TEntry")
# entry_tax.grid(row=1, column=1, padx=12, pady=12)

tk.Label(bottomleft_frame, text="Total", font=("Tahoma", 12), bg="whitesmoke").grid(row=2, column=0, padx=12, pady=12)
entry_total = ttk.Entry(bottomleft_frame, width=20, font=("Tahoma", 12), style="Styled.TEntry")
entry_total.grid(row=2, column=1, padx=12, pady=12)

# bottommiddle_frame entries
tk.Label(bottommiddle_frame, text="Mode", font=("Tahoma", 12), bg="whitesmoke").grid(row=0, column=0, padx=12, pady=12)
entry_modepayment = ttk.Combobox(bottommiddle_frame, values=["Gcash", "Cash"], width=18, font=("Tahoma", 12), style="W.TCombobox", state="readonly")
entry_modepayment.grid(row=0, column=1, padx=12, pady=12)
entry_modepayment.set("Select")

tk.Label(bottommiddle_frame, text="Cost", font=("Tahoma", 12), bg="whitesmoke").grid(row=1, column=0, padx=12, pady=12)
entry_cost = ttk.Entry(bottommiddle_frame, width=20, font=("Tahoma", 12), style="Styled.TEntry")
entry_cost.grid(row=1, column=1, padx=12, pady=12)

tk.Label(bottommiddle_frame, text="Change", font=("Tahoma", 12), bg="whitesmoke").grid(row=2, column=0, padx=12, pady=12)
entry_change = ttk.Entry(bottommiddle_frame, width=20, font=("Tahoma", 12), style="Styled.TEntry")
entry_change.grid(row=2, column=1, padx=12, pady=12)

# bottomright_frame entries
pay_btn = ttk.Button(bottomright_frame, text="Pay", width=20, command=process_payment, style="Bottom.TButton")
reset_btn = ttk.Button(bottomright_frame, text="Reset", width=20, command=reset_cart, style="Bottom.TButton")
save_btn = ttk.Button(bottomright_frame, text="Save", width=20, command=save_receipt, style="Bottom.TButton")
removeitem_btn = ttk.Button(bottomright_frame, text="Remove", width=20, command=remove_selected_item, style="Bottom.TButton")

pay_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
reset_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
save_btn.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
removeitem_btn.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

for i in range(2):
    bottomright_frame.grid_rowconfigure(i, weight=1)
    bottomleft_frame.grid_columnconfigure(i, weight=1)

root.mainloop()
