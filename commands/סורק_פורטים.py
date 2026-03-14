import socket

def execute(args):
    lines = []
    try:
        if len(args) < 2:
            lines.append({"text": "❌ שגיאה: יש לספק כתובת IP/שם מארח ומספר פורט לסריקה.", "type": "error"})
            lines.append({"text": "דוגמה: סורק_פורטים 127.0.0.1 80", "type": "sys-out"})
            return {"lines": lines}

        host = args[0]
        port = int(args[1])

        if not (0 < port < 65536):
            lines.append({"text": "❌ שגיאה: מספר פורט חייב להיות בין 1 ל-65535.", "type": "error"})
            return {"lines": lines}

        lines.append({"text": f"🔍 סורק פורט {port} בשרת {host}...", "type": "sys-out"})

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1) # 1 second timeout
            result = s.connect_ex((host, port))

            if result == 0:
                lines.append({"text": f"✅ פורט {port} פתוח בשרת {host}.", "type": "success"})
            else:
                lines.append({"text": f"❌ פורט {port} סגור או לא נגיש בשרת {host}.", "type": "error"})

    except ValueError:
        lines.append({"text": "❌ שגיאה: מספר פורט אינו תקין.", "type": "error"})
    except socket.gaierror:
        lines.append({"text": f"❌ שגיאה: שם המארח '{host}' לא נפתר לכתובת IP.", "type": "error"})
    except socket.error as se:
        lines.append({"text": f"❌ שגיאת Socket: {se}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
