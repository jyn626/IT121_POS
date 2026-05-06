import tkinter as tk
from tkinter import PhotoImage

root = tk.Tk()

root.geometry("1350x750")
root.resizable(False, False)

top_frame = tk.Frame(root, width=1350, height=550, bg="lightblue")
top_frame.grid(row=0, column=0)
  
# calculator frame
calc_frame = tk.Frame(top_frame, bg="gainsboro", width=350, height=400, borderwidth=4, relief="ridge")
calc_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

  
def press(n):
    pass

  
# calculator buttons
btn1 = tk.Button(calc_frame, text='1', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(1))
btn2 = tk.Button(calc_frame, text='2', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(2))
btn3 = tk.Button(calc_frame, text='3', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(3))
btn4 = tk.Button(calc_frame, text='4', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(4))
btn5 = tk.Button(calc_frame, text='5', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(5))
btn6 = tk.Button(calc_frame, text='6', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(6))
btn7 = tk.Button(calc_frame, text='7', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(7))
btn8 = tk.Button(calc_frame, text='8', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(8))
btn9 = tk.Button(calc_frame, text='9', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(9))
btn0 = tk.Button(calc_frame, text='0', bd=0, fg='black', font=("Tahoma", 16), bg='seashell3', command=lambda: press(0))

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

# .grid_rowconfigure 
# -- para mo expand ang mga buttons sa width saiyang parent

for i in range(6):  # rows
    calc_frame.grid_rowconfigure(i, weight=1)

for j in range(3):  # columns
    calc_frame.grid_columnconfigure(j, weight=1)
  
# products frame
products_frame = tk.Frame(top_frame, bg="gray")
products_frame.grid(row=0, column=1, sticky="nsew")
    
# kani para sundon sa frame ang gihatag nato nga width and height nya,
# kay by default automatic iyang width and height
top_frame.grid_propagate(False)
calc_frame.grid_propagate(False)

root.mainloop()
