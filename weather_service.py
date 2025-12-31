import requests
from datetime import datetime

class WeatherService:
    def __init__(self, city="Taipei"):
        self.city = city
        self.url = f"https://wttr.in/{city}?format=j1"

    def fetch_weather(self):
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                # 基本資訊
                result = {
                    "temp_C": current['temp_C'],
                    "desc": current['weatherDesc'][0]['value'],
                    "uv": current['uvIndex'],
                    "wind": f"{current['windspeedKmph']} km/h {current['winddir16Point']}",
                    "humidity": current['humidity'],
                    "pressure": current['pressure'],
                    "visibility": current['visibility'],
                    "sunrise": data['weather'][0]['astronomy'][0]['sunrise'],
                    "sunset": data['weather'][0]['astronomy'][0]['sunset'],
                    "forecast": []
                }
                
                # 預報資訊 (前 5 天)
                for day in data['weather'][:5]:
                    d_obj = datetime.strptime(day['date'], '%Y-%m-%d')
                    result["forecast"].append({
                        "day": d_obj.strftime('%a'),
                        "max": day['maxtempC'],
                        "min": day['mintempC'],
                        "desc": day['hourly'][4]['weatherDesc'][0]['value'] # 取中午左右的描述
                    })
                
                return result
            return None
        except Exception as e:
            print(f"Weather error: {e}")
            return None
