import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os


def calculate_bmi(weight, height):
    return weight / (height ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 24.9:
        return 'Normal'
    elif 25 <= bmi < 29.9:
        return 'Overweight'
    else:
        return 'Obese'


def validate_input(value, type_):
    try:
        if type_ == 'float':
            return float(value)
        elif type_ == 'int':
            return int(value)
    except ValueError:
        return None


def save_data(data, filename='bmi_data.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(data)

    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)


def show_graph(frame, filename='bmi_data.json'):
    if not os.path.exists(filename):
        messagebox.showerror("Error", "No data available to show graph.")
        return

    with open(filename, 'r') as file:
        data = json.load(file)

    categories = {'Underweight': 0, 'Normal': 0, 'Overweight': 0, 'Obese': 0}
    for entry in data:
        categories[entry['category']] += 1

    labels = categories.keys()
    sizes = categories.values()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    ax.set_title('BMI Categories Distribution')

    # Clear the frame before adding new plot
    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def show_custom_message(name, bmi, category):
    custom_message = tk.Toplevel(root)
    custom_message.title("BMI Result")

    msg_frame = tk.LabelFrame(custom_message, text="BMI Information", padx=10, pady=10)
    msg_frame.pack(padx=10, pady=10)

    tk.Label(msg_frame, text=f"Hello {name},").grid(row=0, column=0, sticky='w')
    tk.Label(msg_frame, text=f"Your BMI is {bmi:.2f},").grid(row=1, column=0, sticky='w')
    tk.Label(msg_frame, text=f"which is considered {category}.").grid(row=2, column=0, sticky='w')

    close_button = ttk.Button(msg_frame, text="Close", command=custom_message.destroy)
    close_button.grid(row=3, column=0, pady=10)


def calculate_and_save():
    name = entry_name.get()
    age = validate_input(entry_age.get(), 'int')
    height_ft = validate_input(entry_height_ft.get(), 'int')
    height_in = validate_input(entry_height_in.get(), 'int')
    height_cm = validate_input(entry_height_cm.get(), 'float')
    weight = validate_input(entry_weight.get(), 'float')

    if None in [age, weight] or (height_ft is None and height_cm is None):
        messagebox.showerror("Error", "Invalid input. Please enter correct values.")
        return

    if height_cm is not None:
        height = height_cm * 0.01
    else:
        height = height_ft * 0.3048 + height_in * 0.0254

    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)

    show_custom_message(name, bmi, category)

    data = {
        'name': name,
        'age': age,
        'height': height,
        'weight': weight,
        'bmi': bmi,
        'category': category
    }

    save_data(data)


# Setting up the Tkinter GUI
root = tk.Tk()
root.title("BMI Calculator")

# Creating input fields
userinfoframe = tk.LabelFrame(root, text="User Information")
userinfoframe.grid(row=0, column=0, padx=10, pady=5, sticky='w')

tk.Label(userinfoframe, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(userinfoframe)
entry_name.grid(row=0, column=1)

tk.Label(userinfoframe, text="Age").grid(row=1, column=0)
entry_age = tk.Entry(userinfoframe)
entry_age.grid(row=1, column=1)

tk.Label(userinfoframe, text="Height").grid(row=2, column=0)

height_frame = tk.Frame(userinfoframe)
height_frame.grid(row=2, column=1, sticky='w')

tk.Label(height_frame, text="Feet").grid(row=0, column=0)
entry_height_ft = tk.Entry(height_frame, width=5)
entry_height_ft.grid(row=0, column=1)

tk.Label(height_frame, text="Inches").grid(row=0, column=2)
entry_height_in = tk.Entry(height_frame, width=5)
entry_height_in.grid(row=0, column=3)

tk.Label(userinfoframe, text="or Centimeters").grid(row=2, column=2)
entry_height_cm = tk.Entry(userinfoframe, width=10)
entry_height_cm.grid(row=2, column=3)

tk.Label(userinfoframe, text="Weight (in kilograms)").grid(row=3, column=0)
entry_weight = tk.Entry(userinfoframe)
entry_weight.grid(row=3, column=1)

# Creating buttons
ttk.Button(userinfoframe, text="Calculate and Save", command=calculate_and_save).grid(row=4, column=0, pady=10)
ttk.Button(userinfoframe, text="Show Graph", command=lambda: show_graph(chart_frame)).grid(row=4, column=1, pady=10)

# Frame for the chart
chart_frame = tk.Frame(root)
chart_frame.grid(row=1, column=0, padx=10, pady=5)

# Running the main loop
root.mainloop()
