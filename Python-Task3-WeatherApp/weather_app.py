import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk
import io
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = "3d3a184f973e3fe276b3e1bf074d7376"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Weather App - Pro")
        self.root.geometry("550x720")
        self.root.resizable(False, False)

        # Theme & Unit States
        self.unit = tk.StringVar(value="C")
        self.is_dark_mode = False
        self.search_history = []

        # Color Palettes
        self.themes = {
            "light": {
                "bg": "#f0f4f8",
                "card_bg": "#ffffff",
                "fg": "#2c3e50",
                "sub_fg": "#7f8c8d",
                "btn_bg": "#3498db",
                "btn_fg": "white"
            },
            "dark": {
                "bg": "#121212",
                "card_bg": "#1e1e1e",
                "fg": "#e0e0e0",
                "sub_fg": "#a0a0a0",
                "btn_bg": "#bb86fc",
                "btn_fg": "#121212"
            }
        }

        # UI Setup
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        # Main Container Frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header & Dark Mode Button
        header_frame = tk.Frame(self.main_frame)
        header_frame.pack(pady=10, fill=tk.X, padx=20)

        self.title_label = tk.Label(header_frame, text="🌦️ Live Weather App", font=("Arial", 18, "bold"))
        self.title_label.pack(side=tk.LEFT)

        self.theme_btn = tk.Button(header_frame, text="🌙 Dark Mode", font=("Arial", 9, "bold"), command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT)

        # --- Search Bar & History (Combobox) ---
        input_frame = tk.Frame(self.main_frame)
        input_frame.pack(pady=5)

        # Using Combobox for Search History
        self.city_entry = ttk.Combobox(input_frame, font=("Arial", 14), width=16)
        self.city_entry.grid(row=0, column=0, padx=5)

        search_btn = tk.Button(
            input_frame, text="Search", font=("Arial", 11, "bold"), 
            bg="#3498db", fg="white", command=self.get_weather_by_city
        )
        search_btn.grid(row=0, column=1, padx=5)

        auto_loc_btn = tk.Button(
            input_frame, text="📍 Auto", font=("Arial", 10), 
            bg="#2ecc71", fg="white", command=self.get_auto_location
        )
        auto_loc_btn.grid(row=0, column=2, padx=5)

        # --- Unit Toggle (Celsius / Fahrenheit) ---
        unit_frame = tk.Frame(self.main_frame)
        unit_frame.pack(pady=5)

        self.unit_lbl = tk.Label(unit_frame, text="Unit:", font=("Arial", 10, "bold"))
        self.unit_lbl.pack(side=tk.LEFT, padx=5)
        
        self.c_radio = tk.Radiobutton(
            unit_frame, text="°C (Celsius)", variable=self.unit, value="C", 
            command=self.refresh_weather
        )
        self.c_radio.pack(side=tk.LEFT)
        
        self.f_radio = tk.Radiobutton(
            unit_frame, text="°F (Fahrenheit)", variable=self.unit, value="F", 
            command=self.refresh_weather
        )
        self.f_radio.pack(side=tk.LEFT)

        # --- Main Weather Card ---
        self.card_frame = tk.Frame(self.main_frame, bd=1, relief=tk.RIDGE)
        self.card_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.city_name_label = tk.Label(self.card_frame, text="Search a city...", font=("Arial", 16, "bold"))
        self.city_name_label.pack(pady=(10, 0))

        self.icon_label = tk.Label(self.card_frame)
        self.icon_label.pack()

        self.temp_label = tk.Label(self.card_frame, text="-- °C", font=("Arial", 28, "bold"), fg="#e74c3c")
        self.temp_label.pack()

        self.desc_label = tk.Label(self.card_frame, text="--", font=("Arial", 12, "italic"))
        self.desc_label.pack(pady=2)

        # Details Grid (Humidity & Wind)
        self.details_frame = tk.Frame(self.card_frame)
        self.details_frame.pack(pady=10)

        self.humidity_label = tk.Label(self.details_frame, text="Humidity: --%", font=("Arial", 10))
        self.humidity_label.grid(row=0, column=0, padx=15)

        self.wind_label = tk.Label(self.details_frame, text="Wind: -- m/s", font=("Arial", 10))
        self.wind_label.grid(row=0, column=1, padx=15)

        # --- Forecast Section Notebook ---
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.tab_6h = tk.Frame(self.notebook)
        self.tab_5d = tk.Frame(self.notebook)

        self.notebook.add(self.tab_6h, text="6-Hour Forecast")
        self.notebook.add(self.tab_5d, text="5-Day Forecast")

        self.last_searched_city = ""

    def apply_theme(self):
        """Dynamic Light/Dark Theme Switcher"""
        theme = self.themes["dark"] if self.is_dark_mode else self.themes["light"]

        self.root.config(bg=theme["bg"])
        self.main_frame.config(bg=theme["bg"])
        
        # Header items
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.card_frame and widget != self.notebook:
                widget.config(bg=theme["bg"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=theme["bg"], fg=theme["fg"])
                    elif isinstance(child, tk.Radiobutton):
                        child.config(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["card_bg"])

        # Card Frame & its elements
        self.card_frame.config(bg=theme["card_bg"])
        for child in self.card_frame.winfo_children():
            if isinstance(child, tk.Label) and child != self.temp_label:
                child.config(bg=theme["card_bg"], fg=theme["fg"])
            elif isinstance(child, tk.Frame):
                child.config(bg=theme["card_bg"])
                for sub_child in child.winfo_children():
                    if isinstance(sub_child, tk.Label):
                        sub_child.config(bg=theme["card_bg"], fg=theme["sub_fg"])

        # Notebook tabs container styling adjustment
        self.tab_6h.config(bg=theme["card_bg"])
        self.tab_5d.config(bg=theme["card_bg"])

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.theme_btn.config(text="☀️ Light Mode")
        else:
            self.theme_btn.config(text="🌙 Dark Mode")
        self.apply_theme()
        if self.last_searched_city:
            self.refresh_forecast_ui_theme()

    def refresh_forecast_ui_theme(self):
        theme = self.themes["dark"] if self.is_dark_mode else self.themes["light"]
        for tab in [self.tab_6h, self.tab_5d]:
            tab.config(bg=theme["card_bg"])
            for widget in tab.winfo_children():
                widget.config(bg=theme["card_bg"])
                for c in widget.winfo_children():
                    if isinstance(c, tk.Label):
                        c.config(bg=theme["card_bg"], fg=theme["fg"])

    def get_auto_location(self):
        try:
            res = requests.get("https://ipapi.co/json/", timeout=5)
            if res.status_code == 200:
                city = res.json().get("city", "")
                if city:
                    self.city_entry.set(city)
                    self.get_weather_by_city()
                else:
                    messagebox.showerror("Error", "Could not detect city automatically.")
        except Exception:
            messagebox.showerror("Error", "Network error during Auto Location detection.")

    def get_weather_by_city(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name!")
            return
        
        # Add to Search History
        if city not in self.search_history:
            self.search_history.insert(0, city)
            if len(self.search_history) > 5:  # Keep last 5 searches
                self.search_history.pop()
            self.city_entry['values'] = self.search_history

        self.last_searched_city = city
        self.fetch_weather_data(city)

    def refresh_weather(self):
        if self.last_searched_city:
            self.fetch_weather_data(self.last_searched_city)

    def fetch_weather_data(self, city):
        units_param = "metric" if self.unit.get() == "C" else "imperial"
        unit_symbol = "°C" if self.unit.get() == "C" else "°F"

        curr_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units_param}"
        
        try:
            res = requests.get(curr_url)
            data = res.json()

            if res.status_code != 200:
                error_msg = data.get("message", "City not found or API error.")
                messagebox.showerror("Error", f"Failed: {error_msg.capitalize()}")
                return

            self.city_name_label.config(text=f"{data['name']}, {data['sys']['country']}")
            self.temp_label.config(text=f"{data['main']['temp']} {unit_symbol}")
            self.desc_label.config(text=data['weather'][0]['description'].capitalize())
            self.humidity_label.config(text=f"💧 Humidity: {data['main']['humidity']}%")
            self.wind_label.config(text=f"🌬️ Wind: {data['wind']['speed']} {'m/s' if units_param == 'metric' else 'mph'}")

            icon_code = data['weather'][0]['icon']
            self.load_weather_icon(icon_code, self.icon_label, size=(80, 80))

            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units_param}"
            f_res = requests.get(forecast_url)
            if f_res.status_code == 200:
                self.update_forecasts(f_res.json(), unit_symbol)

        except requests.exceptions.RequestException:
            messagebox.showerror("Network Error", "Please check your internet connection.")

    def load_weather_icon(self, icon_code, target_label, size=(50, 50)):
        try:
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            img_data = requests.get(icon_url).content
            image = Image.open(io.BytesIO(img_data)).resize(size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            target_label.config(image=photo)
            target_label.image = photo
        except Exception:
            pass

    def update_forecasts(self, data, unit_symbol):
        for widget in self.tab_6h.winfo_children():
            widget.destroy()
        for widget in self.tab_5d.winfo_children():
            widget.destroy()

        list_data = data.get("list", [])
        theme = self.themes["dark"] if self.is_dark_mode else self.themes["light"]

        # --- 6 Hours Forecast ---
        for item in list_data[:2]:
            time_str = datetime.fromtimestamp(item['dt']).strftime('%I:%M %p')
            temp = f"{item['main']['temp']} {unit_symbol}"
            icon = item['weather'][0]['icon']

            frame = tk.Frame(self.tab_6h, bg=theme["card_bg"], bd=1, relief=tk.SOLID)
            frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=10)

            tk.Label(frame, text=time_str, font=("Arial", 9, "bold"), bg=theme["card_bg"], fg=theme["fg"]).pack(pady=2)
            lbl_icon = tk.Label(frame, bg=theme["card_bg"])
            lbl_icon.pack()
            self.load_weather_icon(icon, lbl_icon)
            tk.Label(frame, text=temp, font=("Arial", 9), bg=theme["card_bg"], fg=theme["fg"]).pack(pady=2)

        # --- 5 Days Forecast ---
        daily_items = [item for item in list_data if "12:00:00" in item['dt_txt']]
        
        for item in daily_items[:5]:
            day_str = datetime.fromtimestamp(item['dt']).strftime('%a, %b %d')
            temp = f"{item['main']['temp']} {unit_symbol}"
            icon = item['weather'][0]['icon']

            row_frame = tk.Frame(self.tab_5d, bg=theme["card_bg"])
            row_frame.pack(fill=tk.X, padx=10, pady=4)

            tk.Label(row_frame, text=day_str, font=("Arial", 10, "bold"), width=12, anchor="w", bg=theme["card_bg"], fg=theme["fg"]).pack(side=tk.LEFT)
            lbl_icon = tk.Label(row_frame, bg=theme["card_bg"])
            lbl_icon.pack(side=tk.LEFT, padx=5)
            self.load_weather_icon(icon, lbl_icon, size=(30, 30))
            tk.Label(row_frame, text=temp, font=("Arial", 10), bg=theme["card_bg"], fg=theme["fg"]).pack(side=tk.RIGHT, padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()