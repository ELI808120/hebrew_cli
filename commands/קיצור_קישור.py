import urllib.request
import urllib.parse
import urllib.error
import json

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק כתובת URL לקיצור.", "type": "error"})
        lines.append({"text": "דוגמה: קיצור_קישור https://www.google.com/very/long/url", "type": "sys-out"})
        return {"lines": lines}

    long_url = args[0]
    
    lines.append({"text": f"🔗 מקצר את הקישור: '{long_url}'...", "type": "sys-out"})

    try:
        # Using TinyURL API
        # Docs: https://tinyurl.com/app/dev
        # The free API is https://tinyurl.com/api-create.php?url=long_url
        
        # Newer API (v2) requires a token for most features, but basic shortening can be done with v1 style.
        # Let's try the simpler v1 style which usually works without a key for basic shortening
        api_url = f"http://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}"

        with urllib.request.urlopen(api_url, timeout=10) as response:
            short_url = response.read().decode('utf-8').strip()
            
            if short_url.startswith("http"): # Check if it's a valid URL
                lines.append({"text": f"✅ הקישור המקוצר: {short_url}", "type": "success"})
            else:
                lines.append({"text": f"⚠️ לא ניתן היה לקצר את הקישור: {short_url}", "type": "sys-out"})

    except urllib.error.URLError as ue:
        lines.append({"text": f"❌ שגיאת רשת בעת קיצור קישור: {ue.reason}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
