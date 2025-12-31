import requests
from datetime import datetime

class WeatherService:
    def __init__(self, city="Taipei"):
        self.city = city
        self.url = f"https://wttr.in/{city}?format=j1"

    def get_icon(self, desc):
        desc = desc.lower()
        if "sunny" in desc or "clear" in desc: return "☀️"
        if "partly cloudy" in desc: return "⛅"
        if "cloudy" in desc or "overcast" in desc: return "☁️"
        if "rain" in desc or "drizzle" in desc or "patchy" in desc: return "🌧️"
        if "thunder" in desc or "storm" in desc: return "⛈️"
        if "snow" in desc or "sleet" in desc: return "❄️"
        if "fog" in desc or "mist" in desc: return "🌫️"
        return "✨"

    def fetch_weather(self):
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                desc = current['weatherDesc'][0]['value']
                
                # 基本資訊
                result = {
                    "temp_C": current['temp_C'],
                    "desc": desc,
                    "icon": self.get_icon(desc),
                    "uv": current['uvIndex'],
                    "wind": f"{current['windspeedKmph']} km/h {current['winddir16Point']}",
                    "humidity": current['humidity'],
                    "pressure": current['pressure'],
                    "visibility": current['visibility'],
                    "sunrise": data['weather'][0]['astronomy'][0]['sunrise'],
                    "sunset": data['weather'][0]['astronomy'][0]['sunset'],
                    "rain_chance": data['weather'][0]['hourly'][int(datetime.now().hour/3)]['chanceofrain'],
                    "forecast": []
                }
                
                # 預報資訊 (前 5 天)
                for day in data['weather'][:5]:
                    d_obj = datetime.strptime(day['date'], '%Y-%m-%d')
                    f_desc = day['hourly'][4]['weatherDesc'][0]['value']
                    result["forecast"].append({
                        "day": d_obj.strftime('%a'),
                        "max": day['maxtempC'],
                        "min": day['mintempC'],
                        "desc": f_desc,
                        "icon": self.get_icon(f_desc)
                    })
                
                return result
            return None
        except Exception as e:
            print(f"Weather error: {e}")
            return None
