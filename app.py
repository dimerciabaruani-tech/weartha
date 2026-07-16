# app.py
import streamlit as st
import requests
from weather_utils import get_current_weather, get_forecast, parse_forecast_data, get_time_of_day_greeting
from clothing_engine import get_recommendation_from_prefs, get_animation_backdrop
from ui_components import (
    load_css,
    display_outfit_recommendation,
    build_weather_backdrop,
    get_icon_svg,
    get_period_icon,
)

# --- CONFIG ---
st.set_page_config(page_title="Wearther", page_icon="🌤", layout="centered")
load_css()

# --- SIDEBAR (User Prefs) ---
with st.sidebar:
    st.markdown(
        f'<div class="section-label" style="margin-top:0;">'
        f'{get_icon_svg("gear", color="#8B93A6", size=15)} Personalize</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### How do you feel about the weather?")
    temp_pref = st.selectbox(
        "Temperature Sensitivity",
        ["I'm pretty neutral", "I get cold easily", "I get hot easily"],
        label_visibility="collapsed",
    )
    st.caption("We'll adjust recommendations based on how you feel.")
    st.markdown("---")
    st.caption("Data powered by OpenWeatherMap")

# --- HEADER ---
greeting = get_time_of_day_greeting()
st.markdown(
    f"""
<div class="brand-row">{get_icon_svg("hanger", color="#8B93A6", size=16)} WEARTHER</div>
<div class="cloak-hero">
    <h1>{get_period_icon(greeting['period'])}{greeting['text']}</h1>
    <p>Tell me where you are,</p>
    <p>And I'll tell you what to put on.</p>
</div>
""",
    unsafe_allow_html=True,
)

# --- INPUTS ---
api_key = st.secrets.get("OWM_API_KEY", "") if hasattr(st, "secrets") else ""
if not api_key:
    api_key = st.text_input("OpenWeatherMap API key", type="password")

st.markdown(
    f'<div class="section-label">{get_icon_svg("location", color="#8B93A6", size=15)} Location</div>',
    unsafe_allow_html=True,
)
city = st.text_input("City", placeholder="e.g. Cape Town", label_visibility="collapsed")

# Forecast options inline
st.markdown('<div class="section-label">Forecast</div>', unsafe_allow_html=True)
view_mode = st.segmented_control(
    "Forecast",
    ["Today", "Tomorrow", "7-Day"],
    default="Today",
    label_visibility="collapsed",
)

go = st.button("Get Suggestion", type="primary", use_container_width=True)

# --- MAIN LOGIC ---
# Auto-detect location and load data on startup
if not city:
    try:
        # Try to get location from IP
        ip_response = requests.get('https://ipapi.co/json/', timeout=5)
        if ip_response.status_code == 200:
            ip_data = ip_response.json()
            auto_city = ip_data.get('city', '')
            if auto_city:
                city = auto_city
                # Force a rerun to load data
                st.rerun()
    except:
        pass  # Silent fail, user will need to enter city

# Check if we should auto-load data
if city and api_key and not go:
    # Auto-load on page load if city and API key are available
    go = True

# Show a friendly message if no data is loaded yet
if not go and not city:
    st.info("👋 Enter a city above to get personalized outfit recommendations based on your local weather!")

if go:
    if not api_key:
        st.error("Please enter your OpenWeatherMap API key.")
    elif not city:
        st.error("Please enter a city name.")
    else:
        unit_param = "metric"
        unit_symbol = "°C"
        wind_unit = "m/s"

        try:
            # 1. Fetch Data
            weather_data = get_current_weather(city, api_key, unit_param)
            forecast_data = get_forecast(city, api_key, unit_param)

            # 2. Parse Current
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            condition = weather_data["weather"][0]["main"]
            description = weather_data["weather"][0]["description"]
            wind_speed = weather_data["wind"]["speed"]
            humidity = weather_data["main"]["humidity"]
            uv_index = 0  # Note: UV index requires a separate API call (OpenWeather UV). Defaulting to 0 for now.
            city_name = weather_data["name"]
            country = weather_data["sys"]["country"]

            # 3. Parse Forecast
            parsed_forecast = parse_forecast_data(forecast_data, unit_symbol)

            # Handle filter logic
            if view_mode == "Today":
                display_data = parsed_forecast[:1]
            elif view_mode == "Tomorrow":
                display_data = parsed_forecast[1:2] if len(parsed_forecast) > 1 else []
            else:  # 7-Day
                display_data = parsed_forecast

            # 4. Ambient backdrop — CSS-only particles
            anim_type = get_animation_backdrop(condition)
            backdrop_html = build_weather_backdrop(anim_type, seed=abs(hash(city_name)) % 1000)

            # Render Weather Card
            st.markdown(
                f"""
            <div class="weather-card">
                {backdrop_html}
                <div class="weather-card-content">
                    <div>
                        <div class="weather-city">{city_name}, {country}</div>
                        <div class="weather-temp">{temp:.0f}{unit_symbol}</div>
                        <div class="weather-sub">
                            <span>Feels like <b>{feels_like:.0f}{unit_symbol}</b></span>
                            <span>Wind <b>{wind_speed:.0f} {wind_unit}</b></span>
                            <span>Humidity <b>{humidity}%</b></span>
                        </div>
                    </div>
                    <div class="weather-condition">{description}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Render Forecast Filter Result
            if display_data:
                st.markdown(
                    f'<div class="section-label">{get_icon_svg("sun_cloud", color="#8B93A6", size=15)} Forecast</div>',
                    unsafe_allow_html=True,
                )
                cols = st.columns(len(display_data))
                for i, day in enumerate(display_data):
                    with cols[i]:
                        st.metric(
                            label=f"{day['day']}",
                            value=f"{day['max']:.0f}{unit_symbol}",
                            delta=f"{day['min']:.0f}{unit_symbol} min",
                            delta_color="off",
                        )

            # 5. Compute Outfit
            temp_c = temp  # Already in Celsius

            items = get_recommendation_from_prefs(
                temp_c=temp_c,
                condition=condition,
                wind_speed=wind_speed,
                humidity=humidity,
                uv_index=uv_index,
                user_prefs=temp_pref,
            )

            st.markdown(
                f'<div class="section-label">{get_icon_svg("hanger", color="#8B93A6", size=15)} Complete Outfit</div>',
                unsafe_allow_html=True,
            )
            st.markdown(display_outfit_recommendation(items), unsafe_allow_html=True)

        except requests.exceptions.HTTPError as e:
            st.error(f"API Error: {e}")
        except Exception as e:
            st.error(f"System Error: {e}")