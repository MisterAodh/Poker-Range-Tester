import tkinter as tk

calculation = ""

def add_to_calculation(symbol):
    global calculation
    if symbol != "AC" and symbol != "=":
        calculation += str(symbol)
    if symbol == "AC":
        calculation = ""
    if symbol == "=":
        evaluate_calculation()

    text_result.delete(1.0, "end")
    if calculation is not None:  # Only attempt to insert if calculation is not None
        text_result.insert(1.0, calculation)

def evaluate_calculation():
    global calculation
    try:
        calculation = str(eval(calculation.replace('x', '*')))  # Replacing 'x' with '*' for multiplication
    except:
        clear_field()
        text_result.insert(1.0, "Error")

def clear_field():
    global calculation
    calculation = ""
    text_result.delete(1.0, "end")

root = tk.Tk()

root.geometry("325x225")

text_result = tk.Text(root, height=2, width=16, font=("Arial", 24))
text_result.grid(columnspan=5)
buttons = {}
for i in range(0, 10):
    btn = tk.Button(root, text=str(i), command=lambda i=i: add_to_calculation(str(i)), width=5, font=("Ariel", 14))
    btn.grid(row=((i-1)//3)+2, column=(i-1)%3)
    buttons[str(i)] = btn

btn = tk.Button(root, text='=', command=lambda : add_to_calculation("="), width=5, font=("Ariel", 14))
btn.grid(row=5, column=3)
buttons["="] = btn

btn = tk.Button(root, text='+', command=lambda : add_to_calculation("+"), width=5, font=("Ariel", 14))
btn.grid(row=1, column=3)
buttons["+"] = btn

btn = tk.Button(root, text="-", command=lambda : add_to_calculation("-"), width=5, font=("Ariel", 14))
btn.grid(row=2, column=3)
buttons["-"] = btn

btn = tk.Button(root, text="/", command=lambda : add_to_calculation("/"), width=5, font=("Ariel", 14))
btn.grid(row=3, column=3)
buttons["/"] = btn

btn = tk.Button(root, text="x", command=lambda : add_to_calculation("x"), width=5, font=("Ariel", 14))
btn.grid(row=4, column=3)
buttons["x"] = btn

btn = tk.Button(root, text=".", command=lambda : add_to_calculation("."), width=5, font=("Ariel", 14))
btn.grid(row=1, column=1)
buttons["."] = btn

btn = tk.Button(root, text="AC", command=lambda : add_to_calculation("AC"), width=5, font=("Ariel", 14))
btn.grid(row=1, column=0)
buttons["AC"] = btn
root.mainloop()