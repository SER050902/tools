import requests

def get_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    try:
        res = requests.get(url)
        print("🌍 Weather in", city)
        print(res.text)
    except:
        print("❌ Failed to fetch weather data.")

if __name__ == "__main__":
    city = input("Enter your city (e.g., madrid, barcelona): ")
    get_weather(city)
