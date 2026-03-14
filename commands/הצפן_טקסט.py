import base64

def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק פעולה (encode/decode) וטקסט/מחרוזת.", "type": "error"})
        lines.append({"text": "דוגמה: הצפן_טקסט encode 'שלום עולם'", "type": "sys-out"})
        lines.append({"text": "דוגמה: הצפן_טקסט decode '1504150C151D149B1501'", "type": "sys-out"})
        return {"lines": lines}

    action = args[0].lower()
    data = " ".join(args[1:])

    try:
        if action == "encode":
            encoded_bytes = base64.b64encode(data.encode('utf-8'))
            encoded_string = encoded_bytes.decode('utf-8')
            lines.append({"text": f"🔐 מקודד (Base64) את: '{data}'", "type": "sys-out"})
            lines.append({"text": f"✅ תוצאה: '{encoded_string}'", "type": "success"})
        elif action == "decode":
            decoded_bytes = base64.b64decode(data.encode('utf-8'))
            decoded_string = decoded_bytes.decode('utf-8')
            lines.append({"text": f"🔓 מפענח (Base64) את: '{data}'", "type": "sys-out"})
            lines.append({"text": f"✅ תוצאה: '{decoded_string}'", "type": "success"})
        else:
            lines.append({"text": "❌ שגיאה: פעולה לא חוקית. השתמש ב-'encode' או 'decode'.", "type": "error"})
    except base64.binascii.Error as be:
        lines.append({"text": f"❌ שגיאה בפענוח Base64: הקלט אינו Base64 תקין. {be}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
