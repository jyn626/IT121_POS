import tkinter as tk
from tkinter import ttk, PhotoImage

root = tk.Tk()

root.geometry("1350x750")
root.resizable(False, False)

BG_COLOR = "slategray1"

top_frame = tk.Frame(root, width=1350, height=550, bg=BG_COLOR)
top_frame.grid(row=0, column=0)
  
# number frame
numbers_frame = tk.Frame(top_frame, bg="gainsboro", width=350, height=490, borderwidth=4, relief="ridge")
numbers_frame.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

  
def press(n):
    entry_cost.config(state="normal")
    current_value = entry_cost.get()
    entry_cost.delete(0, tk.END)
    entry_cost.insert(0, str(current_value) + str(n))
    entry_cost.config(state="disabled")


def clear_cost():
    entry_cost.config(state="normal")
    entry_cost.delete(0, tk.END)
    entry_cost.config(state="disabled")
    
  
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
btnclear.grid(row=3, column=1, columnspan=2, sticky="nsew")

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
products_frame.grid_propagate(False)

# kani para sundon sa frame ang gihatag nato nga width and height nya,
# kay by default automatic iyang width and height
top_frame.grid_propagate(False)
numbers_frame.grid_propagate(False)
middle_frame.grid_propagate(False)

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
reset_btn = tk.Button(bottomright_frame, text="Reset", font=("Tahoma", 16), width=16, height=3)
print_btn = tk.Button(bottomright_frame, text="Print", font=("Tahoma", 16), width=16, height=3)
removeitem_btn = tk.Button(bottomright_frame, text="Remove", font=("Tahoma", 16), width=16, height=3)

pay_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
reset_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
print_btn.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
removeitem_btn.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

for i in range(2):
    bottomright_frame.grid_rowconfigure(i, weight=1)
    bottomleft_frame.grid_columnconfigure(i, weight=1)

root.mainloop()
