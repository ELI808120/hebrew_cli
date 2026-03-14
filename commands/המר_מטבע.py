import urllib.request
import urllib.error
import json

def execute(args):
    lines = []
    
    if len(args) < 3:
        lines.append({"text": "❌ שגיאה: יש לספק כמות, מטבע מקור ומטבע יעד.", "type": "error"})
        lines.append({"text": "דוגמה: המר_מטבע 10 USD ILS", "type": "sys-out"})
        return {"lines": lines}

    try:
        amount = float(args[0])
    except ValueError:
        lines.append({"text": "❌ שגיאה: הכמות חייבת להיות מספר חוקי.", "type": "error"})
        return {"lines": lines}

    from_currency = args[1].upper()
    to_currency = args[2].upper()
    
    lines.append({"text": f"💱 ממיר {amount} {from_currency} ל-{to_currency}...", "type": "sys-out"})

    try:
        # Using ExchangeRate-API (free tier) for exchange rates
        url = f"https://open.er-api.com/v6/latest/{from_currency}"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data and data.get("result") == "success":
                rates = data.get("rates", {})
                
                if to_currency in rates:
                    converted_amount = amount * rates[to_currency]
                    lines.append({"text": f"✅ {amount} {from_currency} = {converted_amount:.2f} {to_currency}", "type": "success"})
                else:
                    lines.append({"text": f"⚠️ מטבע יעד '{to_currency}' לא נמצא.", "type": "sys-out"})
                
                lines.append({"text": "✅ המרת מטבע הושלמה.", "type": "success"})
            else:
                lines.append({"text": f"⚠️ לא ניתן לאחזר שערי חליפין עבור '{from_currency}'.", "type": "sys-out"})

    except urllib.error.HTTPError as he:
        lines.append({"text": f"❌ שגיאת HTTP בעת אחזור שערי חליפין: {he.code} - {he.reason}", "type": "error"})
    except urllib.error.URLError as ue:
        lines.append({"text": f"❌ שגיאת רשת בעת אחזור שערי חליפין: {ue.reason}", "type": "error"})
    except json.JSONDecodeError:
        lines.append({"text": "❌ שגיאה בניתוח תגובת ה-API של שערי חליפין.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
