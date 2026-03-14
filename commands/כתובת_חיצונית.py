import urllib.request
import urllib.error
import json

def execute(args):
    lines = []
    
    lines.append({"text": "🌐 מאחזר את כתובת ה-IP החיצונית שלך...", "type": "sys-out"})

    try:
        # Using ipify API
        url = "https://api.ipify.org?format=json"

        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            public_ip = data.get("ip")
            
            if public_ip:
                lines.append({"text": f"✅ כתובת ה-IP החיצונית שלך היא: {public_ip}", "type": "success"})
            else:
                lines.append({"text": "⚠️ לא ניתן היה לאחזר את כתובת ה-IP החיצונית.", "type": "sys-out"})

    except urllib.error.URLError as ue:
        lines.append({"text": f"❌ שגיאת רשת בעת אחזור כתובת IP: {ue.reason}", "type": "error"})
    except json.JSONDecodeError:
        lines.append({"text": "❌ שגיאה בניתוח תגובת ה-API של IP.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
