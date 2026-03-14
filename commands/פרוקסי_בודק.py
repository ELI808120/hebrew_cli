import urllib.request
import urllib.error
import socket

def execute(args):
    lines = []
    
    if len(args) < 1:
        lines.append({"text": "❌ שגיאה: יש לספק כתובת פרוקסי לבדיקה (לדוגמה: http://myproxy.com:8080).", "type": "error"})
        lines.append({"text": "דוגמה: פרוקסי_בודק http://127.0.0.1:8888", "type": "sys-out"})
        return {"lines": lines}

    proxy_url = args[0]
    target_url = "http://www.google.com" # Known good external URL for testing
    
    lines.append({"text": f"🌐 בודק את שרת הפרוקסי '{proxy_url}'...", "type": "sys-out"})

    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

        # Attempt to open a known external URL through the proxy
        with urllib.request.urlopen(target_url, timeout=5) as response:
            status_code = response.getcode()
            lines.append({"text": f"✅ שרת הפרוקסי פועל! קוד סטטוס מ-{target_url}: {status_code}", "type": "success"})

    except urllib.error.HTTPError as he:
        lines.append({"text": f"❌ שרת הפרוקסי אינו תקין או שהחזיר שגיאת HTTP: {he.code} - {he.reason}", "type": "error"})
    except urllib.error.URLError as ue:
        if isinstance(ue.reason, socket.timeout):
            lines.append({"text": "❌ שגיאה: פסק זמן התקבל מהפרוקסי.", "type": "error"})
        else:
            lines.append({"text": f"❌ שגיאה: שרת הפרוקסי אינו נגיש או אינו תקין. סיבה: {ue.reason}", "type": "error"})
    except socket.timeout:
        lines.append({"text": "❌ שגיאה: פסק זמן התקבל בעת ניסיון התחברות לפרוקסי.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    finally:
        # Reset the global opener to avoid affecting subsequent requests
        urllib.request.install_opener(urllib.request.build_opener())
    
    return {"lines": lines}
