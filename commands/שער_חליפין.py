import urllib.request
import urllib.error
import json

def execute(args):
    lines = []
    
    if len(args) < 1:
        lines.append({"text": "❌ שגיאה: יש לספק קוד מטבע בסיס (לדוגמה: USD, EUR).", "type": "error"})
        lines.append({"text": "דוגמה: שער_חליפין USD ILS", "type": "sys-out"})
        lines.append({"text": "דוגמה: שער_חליפין EUR", "type": "sys-out"})
        return {"lines": lines}

    base_currency = args[0].upper()
    target_currency = args[1].upper() if len(args) > 1 else None
    
    lines.append({"text": f"💱 מאחזר שערי חליפין עבור '{base_currency}'...", "type": "sys-out"})

    try:
        # Using ExchangeRate-API (free tier) for exchange rates
        # Docs: https://www.exchangerate-api.com/docs/free
        # Note: Free plan is limited to 1,500 requests/month.
        url = f"https://open.er-api.com/v6/latest/{base_currency}"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data and data.get("result") == "success":
                rates = data.get("rates", {})
                
                lines.append({"text": f"--- שערי חליפין עבור {base_currency} ---", "type": "success"})
                
                if target_currency:
                    if target_currency in rates:
                        lines.append({"text": f"  1 {base_currency} = {rates[target_currency]:.4f} {target_currency}", "type": ""})
                    else:
                        lines.append({"text": f"⚠️ מטבע יעד '{target_currency}' לא נמצא.", "type": "sys-out"})
                else:
                    # Display a few common rates
                    common_targets = ["USD", "EUR", "ILS", "GBP", "JPY", "CAD"]
                    for target in common_targets:
                        if target != base_currency and target in rates:
                            lines.append({"text": f"  1 {base_currency} = {rates[target]:.4f} {target}", "type": ""})
                
                lines.append({"text": "✅ אחזור שערי חליפין הושלם.", "type": "success"})
            else:
                lines.append({"text": f"⚠️ לא ניתן לאחזר שערי חליפין עבור '{base_currency}'.", "type": "sys-out"})

    except urllib.error.HTTPError as he:
        lines.append({"text": f"❌ שגיאת HTTP בעת אחזור שערי חליפין: {he.code} - {he.reason}", "type": "error"})
    except urllib.error.URLError as ue:
        lines.append({"text": f"❌ שגיאת רשת בעת אחזור שערי חליפין: {ue.reason}", "type": "error"})
    except json.JSONDecodeError:
        lines.append({"text": "❌ שגיאה בניתוח תגובת ה-API של שערי חליפין.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
