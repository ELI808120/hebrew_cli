import urllib.request
import urllib.error
import json

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק שם מטבע קריפטו (לדוגמה: bitcoin, ethereum).", "type": "error"})
        lines.append({"text": "דוגמה: קריפטו bitcoin", "type": "sys-out"})
        lines.append({"text": "דוגמה: קריפטו ethereum", "type": "sys-out"})
        return {"lines": lines}

    crypto_id = args[0].lower()
    
    lines.append({"text": f"📈 מאחזר מחיר נוכחי עבור '{crypto_id}'...", "type": "sys-out"})

    try:
        # Using CoinGecko API for cryptocurrency prices
        # Docs: https://www.coingecko.com/api/documentation
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd,ils"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if crypto_id in data:
                price_info = data[crypto_id]
                usd_price = price_info.get("usd")
                ils_price = price_info.get("ils")

                lines.append({"text": f"--- מחיר נוכחי של {crypto_id.capitalize()} ---", "type": "success"})
                if usd_price:
                    lines.append({"text": f'  דולר ארה"ב (USD): {usd_price:,.2f}$', "type": ""})
                if ils_price:
                    lines.append({"text": f"  שקל ישראלי (ILS): {ils_price:,.2f}₪", "type": ""})
                
                if not usd_price and not ils_price:
                     lines.append({"text": "⚠️ לא ניתן היה לאחזר מחירים עבור מטבע זה.", "type": "sys-out"})

                lines.append({"text": "✅ אחזור מחיר קריפטו הושלם.", "type": "success"})
            else:
                lines.append({"text": f"⚠️ מטבע קריפטו '{crypto_id}' לא נמצא או לא נתמך.", "type": "sys-out"})

    except urllib.error.HTTPError as he:
        lines.append({"text": f"❌ שגיאת HTTP בעת אחזור מחיר קריפטו: {he.code} - {he.reason}", "type": "error"})
    except urllib.error.URLError as ue:
        lines.append({"text": f"❌ שגיאת רשת בעת אחזור מחיר קריפטו: {ue.reason}", "type": "error"})
    except json.JSONDecodeError:
        lines.append({"text": "❌ שגיאה בניתוח תגובת ה-API של קריפטו.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
