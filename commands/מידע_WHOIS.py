import subprocess
import platform

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק שם דומיין או כתובת IP לחיפוש WHOIS.", "type": "error"})
        lines.append({"text": "דוגמה: מידע_WHOIS google.com", "type": "sys-out"})
        return {"lines": lines}

    target = args[0]
    
    lines.append({"text": f"🌐 מבצע חיפוש WHOIS עבור '{target}'...", "type": "sys-out"})

    try:
        command = ["whois", target]
        process = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8', errors='ignore')
        output = process.stdout.strip()
        stderr_output = process.stderr.strip()

        if process.returncode == 0 and output:
            lines.append({"text": "--- תוצאות WHOIS ---", "type": "success"})
            for line in output.splitlines():
                lines.append({"text": line, "type": ""})
            lines.append({"text": "✅ חיפוש WHOIS הושלם.", "type": "success"})
        else:
            lines.append({"text": f"⚠️ לא ניתן לאחזר מידע WHOIS עבור '{target}'.", "type": "sys-out"})
            if stderr_output:
                lines.append({"text": stderr_output, "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'whois' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
        if platform.system() == "Windows":
            lines.append({"text": "  במערכת Windows, ייתכן שיהיה עליך להתקין לקוח WHOIS.", "type": "sys-out"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
