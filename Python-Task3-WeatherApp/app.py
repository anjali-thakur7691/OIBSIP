import streamlit as st
import requests

# ===========================
# CONFIGURATION
# ===========================

API_KEY = "3d3a184f973e3fe276b3e1bf074d7376"


st.set_page_config(
    page_title="Weather App Pro",
    page_icon="🌤️",
    layout="wide"
)
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#e0f7fa,#f1f8ff);
    color:#111827;
}

.main .block-container{
    max-width:900px;
    margin:auto;
    padding-top:2rem;
}

div[data-testid="stMetric"]{
    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0 5px 15px rgba(0,0,0,.2);
}

.stButton>button{
    width:100%;
    background:#0077ff;
    color:white;
    border-radius:10px;
    height:45px;
    border:none;
    font-size:16px;
}

.stButton>button:hover{
    background:#0055cc;
}

</style>
""", unsafe_allow_html=True)

# ===========================
# TITLE
# ===========================

st.title("🌤️ Live Weather App")
st.write("Search any city and get live weather information.")

# ===========================
# SIDEBAR
# ===========================

unit = st.sidebar.radio(
    "Select Temperature Unit",
    ["Celsius", "Fahrenheit"]
)

city = st.text_input(
    "Enter City Name",
    placeholder="Example: Balaghat"
)

search = st.button("🔍 Search")

# ===========================
# WEATHER FUNCTION
# ===========================

def get_weather(city):

    units = "metric"
    symbol = "°C"

    if unit == "Fahrenheit":
        units = "imperial"
        symbol = "°F"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "pressure": data["main"]["pressure"],
        "feels": data["main"]["feels_like"],
        "description": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
        "symbol": symbol
    }
def get_forecast(city):

    units = "metric"

    if unit == "Fahrenheit":
        units = "imperial"

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    forecast = []

    for item in data["list"]:

        if "12:00:00" in item["dt_txt"]:

            forecast.append({

                "date": item["dt_txt"].split()[0],

                "temp": item["main"]["temp"],

                "icon": item["weather"][0]["icon"],

                "desc": item["weather"][0]["description"].title()

            })

    return forecast[:5]

# ===========================
# DISPLAY
# ===========================

if search:

    if city == "":
        st.warning("Please enter a city name.")
    else:

        weather = get_weather(city)

        if weather:

            st.success(f"{weather['city']}, {weather['country']}")

            icon_url = f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png"

            st.image(icon_url, width=150)

            st.markdown(f"""
            ## 🌍 {weather['city']}, {weather['country']}

            ### 🌡️ {weather['temp']} {weather['symbol']}

            **☁️ {weather['description']}**
            """)

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"💧 Humidity : {weather['humidity']} %")
                st.info(f"🌬 Wind : {weather['wind']} m/s")

            with col2:
                st.info(f"🌡 Feels Like : {weather['feels']} {weather['symbol']}")
                st.info(f"📈 Pressure : {weather['pressure']} hPa")
            st.write("### Weather")
            st.write(weather["description"])
            st.markdown("---")

            st.subheader("📅 5-Day Weather Forecast")

            forecast = get_forecast(city)

            if forecast:

                    cols = st.columns(len(forecast))

                    for i, day in enumerate(forecast):

                        with cols[i]:

                            icon_url = f"https://openweathermap.org/img/wn/{day['icon']}@2x.png"

                            st.image(icon_url, width=60)

                            st.caption(day["date"])

                            st.write(f"🌡️ {day['temp']} {weather['symbol']}")

                            st.write(day["desc"])

            else:

                st.error("City not found.")

           