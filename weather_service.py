import requests

class WeatherService:
    def __init__(self, city="Taipei"):
        self.city = city
        self.url = f"https://wttr.in/{city}?format=j1"

    def fetch_weather(self):
        try:
            response = requests.get(self.url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                temp = current['temp_C']
                desc = current['weatherDesc'][0]['value']
                return f"{temp}°C | {desc}"
            return "無法獲取天氣"
        except Exception as e:
            print(f"Weather error: {e}")
            return "連線失敗"
