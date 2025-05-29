from flask import Flask, render_template, request, jsonify
import requests
import datetime
import socket
import os

AUTHOR_NAME = "Jan Kowalski" 

app = Flask(__name__)

COUNTRIES_CITIES = {
    "Poland": ["Warsaw", "Krakow", "Gdansk", "Wroclaw", "Poznan"],
    "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
    "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
    "UK": ["London", "Manchester", "Birmingham", "Liverpool", "Glasgow"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"]
}

WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', "c9292e0bd2cee546ca54c8a0249337c7")

@app.route('/')
def index():
    return render_template('index.html', countries=COUNTRIES_CITIES)

@app.route('/get_cities')
def get_cities():
    country = request.args.get('country')
    if country in COUNTRIES_CITIES:
        return jsonify({"cities": COUNTRIES_CITIES[country]})
    return jsonify({"cities": []})

@app.route('/weather', methods=['POST'])
def get_weather():
    country = request.form.get('country')
    city = request.form.get('city')
    
    weather_data = fetch_weather_data(city)
    
    return render_template('weather.html', 
                           country=country, 
                           city=city, 
                           weather=weather_data)

def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather_info = {
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
            return weather_info
        return {"error": f"Błąd pobierania danych: {data.get('message', 'Nieznany błąd')}"}
    
    except Exception as e:
        return {"error": f"Wystąpił wyjątek: {str(e)}"}

def log_startup_info():
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    port = int(os.environ.get('PORT', 5000))
    print(f"[{start_time}] Aplikacja uruchomiona przez: {AUTHOR_NAME}")
    print(f"[{start_time}] Nasłuchiwanie na porcie TCP: {port}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    log_startup_info()
    app.run(host='0.0.0.0', port=port, debug=False)