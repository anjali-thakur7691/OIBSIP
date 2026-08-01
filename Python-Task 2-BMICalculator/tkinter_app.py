"""Desktop Tkinter version of the BMI Wellness Tracker.

Run with: python tkinter_app.py
"""
import tkinter as tk
from tkinter import messagebox, ttk

from bmi import CATEGORY_DETAILS, calculate_bmi, get_category, healthy_weight_range, validate_input
from csv_handler import CSVHandler
from database import BMIDatabase


class BMIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Wellness Tracker")
        self.geometry("900x620")
        self.minsize(800, 560)
        self.db, self.csv = BMIDatabase(), CSVHandler()
        self.result = None
        self._make_style()
        self._make_calculator()

    def _make_style(self):
        ttk.Style(self).theme_use("clam")
        ttk.Style().configure("Title.TLabel", font=("Segoe UI", 21, "bold"))
        ttk.Style().configure("Result.TLabel", font=("Segoe UI", 16, "bold"))

    def _make_calculator(self):
        container = ttk.Frame(self, padding=24)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="BMI Wellness Tracker", style="Title.TLabel").pack(anchor="w")
        ttk.Label(container, text="Calculate your BMI and save a private local history.").pack(anchor="w", pady=(0, 18))
        form = ttk.LabelFrame(container, text="Your details", padding=16)
        form.pack(fill="x")
        self.vars = {key: tk.StringVar() for key in ("name", "age", "weight", "height")}
        self.vars["age"].set("18"); self.vars["weight"].set("60"); self.vars["height"].set("1.65")
        self.gender = tk.StringVar(value="Female")
        fields = [("Full name", "name"), ("Age", "age"), ("Weight (kg)", "weight"), ("Height (m)", "height")]
        for index, (label, key) in enumerate(fields):
            row, column = divmod(index, 2)
            ttk.Label(form, text=label).grid(row=row * 2, column=column, sticky="w", padx=8)
            ttk.Entry(form, textvariable=self.vars[key], width=32).grid(row=row * 2 + 1, column=column, sticky="ew", padx=8, pady=(0, 10))
        ttk.Label(form, text="Gender").grid(row=4, column=0, sticky="w", padx=8)
        ttk.Combobox(form, textvariable=self.gender, values=["Female", "Male", "Other", "Prefer not to say"], state="readonly", width=29).grid(row=5, column=0, sticky="w", padx=8)
        ttk.Button(form, text="Calculate BMI", command=self.calculate).grid(row=5, column=1, sticky="ew", padx=8)
        self.result_label = ttk.Label(container, text="Enter your details to calculate BMI.", style="Result.TLabel", wraplength=760)
        self.result_label.pack(anchor="w", pady=22)
        actions = ttk.Frame(container); actions.pack(fill="x")
        ttk.Button(actions, text="Save result", command=self.save).pack(side="left")
        ttk.Button(actions, text="View BMI history", command=self.show_history).pack(side="left", padx=10)
        ttk.Button(actions, text="Clear form", command=self.clear).pack(side="left")
        ttk.Label(container, text="BMI is a screening tool and not a medical diagnosis.").pack(anchor="w", pady=18)

    def calculate(self):
        try:
            name, age = self.vars["name"].get().strip(), int(self.vars["age"].get())
            weight, height = float(self.vars["weight"].get()), float(self.vars["height"].get())
        except ValueError:
            messagebox.showerror("Invalid input", "Age, weight and height must be numbers."); return
        valid, message = validate_input(weight, height, age)
        if not name or not valid:
            messagebox.showerror("Invalid input", message if not valid else "Please enter a name."); return
        bmi, category = calculate_bmi(weight, height), get_category(calculate_bmi(weight, height))
        low, high = healthy_weight_range(height)
        self.result = (name, age, self.gender.get(), weight, height, bmi, category)
        colour, guidance = CATEGORY_DETAILS[category]
        self.result_label.configure(text=f"BMI: {bmi:.2f}  |  {category}\nHealthy weight range: {low}–{high} kg\n{guidance}", foreground=colour)

    def save(self):
        if not self.result:
            messagebox.showwarning("Calculate first", "Calculate BMI before saving."); return
        if self.db.save_record(*self.result):
            self.csv.sync_records(self.db.get_all_records())
            messagebox.showinfo("Saved", "Result saved to the SQLite database and CSV backup.")
        else:
            messagebox.showerror("Database error", "The result could not be saved.")

    def clear(self):
        for key in self.vars: self.vars[key].set("")
        self.vars["age"].set("18"); self.vars["weight"].set("60"); self.vars["height"].set("1.65")
        self.result = None; self.result_label.configure(text="Enter your details to calculate BMI.", foreground="black")

    def show_history(self):
        window = tk.Toplevel(self); window.title("BMI History"); window.geometry("900x380")
        columns = ("ID", "Name", "Age", "Gender", "Weight", "Height", "BMI", "Category", "Date")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        for column in columns:
            tree.heading(column, text=column); tree.column(column, width=92, anchor="center")
        for record in self.db.get_all_records(): tree.insert("", "end", values=record)
        tree.pack(fill="both", expand=True, padx=12, pady=12)
        def delete_selected():
            selected = tree.selection()
            if selected and messagebox.askyesno("Delete", "Delete the selected record?"):
                self.db.delete_record(tree.item(selected[0])["values"][0]); self.csv.sync_records(self.db.get_all_records()); tree.delete(selected[0])
        ttk.Button(window, text="Delete selected record", command=delete_selected).pack(pady=(0, 12))


if __name__ == "__main__":
    BMIApp().mainloop()
