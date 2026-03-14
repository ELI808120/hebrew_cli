import urllib.request
import urllib.error
import json

def execute(args):
    lines = []
    
    # Hardcoded coordinates for Tel Aviv, Israel
    # Latitude: 32.0853, Longitude: 34.7818
    latitude = 32.0853
    longitude = 34.7818
    city_name = "תל אביב"

    if args:
        lines.append({"text": "⚠️ פקודת מזג_אוויר כרגע מציגה נתונים עבור תל אביב בלבד.", "type": "sys-out"})
        lines.append({"text": "  ארגומנטים שסופקו יתעלמו.", "type": "sys-out"})

    lines.append({"text": f"☁️ מאחזר נתוני מזג אוויר עבור {city_name}...", "type": "sys-out"})

    try:
        # Open-Meteo API for current weather
        # Docs: https://open-meteo.com/en/docs
        url = (f"https://api.open-meteo.com/v1/forecast?"
               f"latitude={latitude}&longitude={longitude}&"
               f"current_weather=true&hourly=temperature_2m,relativehumidity_2m,precipitation&"
               f"forecast_days=1&timezone=Asia%2FJerusalem") # Added timezone for accuracy

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if "current_weather" in data:
                current_weather = data["current_weather"]
                temperature = current_weather.get("temperature")
                windspeed = current_weather.get("windspeed")
                weathercode = current_weather.get("weathercode")
                
                # Simple mapping for weather codes (Open-Meteo)
                # Full list: https://www.openmeteo.com/en/docs
                weather_description = {
                    0: "שמיים בהירים",
                    1: "בעיקר בהיר",
                    2: "מעונן חלקית",
                    3: "מעונן",
                    45: "ערפל",
                    48: "ערפל מקפיא",
                    51: "אוויר קל",
                    53: "אוויר בינוני",
                    55: "אוויר צפוף",
                    56: "גשם קל מקפיא",
                    57: "גשם כבד מקפיא",
                    61: "גשם קל",
                    63: "גשם בינוני",
                    65: "גשם כבד",
                    66: "גשם קל מקפיא",
                    67: "גשם כבד מקפיא",
                    71: "שלג קל",
                    73: "שלג בינוני",
                    75: "שלג כבד",
                    77: "גרגרי שלג",
                    80: "ממטרים קלים",
                    81: "ממטרים בינוניים",
                    82: "ממטרים אלימים",
                    85: "שלג קל",
                    86: "שלג כבד",
                    95: "סופת רעמים קלה/בינונית",
                    96: "סופת רעמים עם ברד קל",
                    99: "סופת רעמים עם ברד כבד",
                }.get(weathercode, "לא ידוע")

                lines.append({"text": "--- מזג אוויר נוכחי ---", "type": "success"})
                lines.append({"text": f"  מיקום: {city_name}", "type": ""})
                lines.append({"text": f"  טמפרטורה: {temperature}°C", "type": ""})
                lines.append({"text": f"  מהירות רוח: {windspeed} קמ"ש", "type": ""})
                lines.append({"text": f"  מצב: {weather_description}", "type": ""})
                lines.append({"text": "✅ נתוני מזג אוויר נשלפו בהצלחה.", "type": "success"})
            else:
                lines.append({"text": "⚠️ לא ניתן לאחזר נתוני מזג אוויר נוכחיים.", "type": "sys-out"})

    except urllib.error.URLError as ue:
        lines.append({"text": f"❌ שגיאת רשת בעת שליפת מזג אוויר: {ue.reason}", "type": "error"})
    except json.JSONDecodeError:
        lines.append({"text": "❌ שגיאה בניתוח תגובת מזג האוויר.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
