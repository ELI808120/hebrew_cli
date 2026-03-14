import subprocess
import platform
import re

def execute(args):
    lines = []
    
    lines.append({"text": "💻 מאחזר כתובות MAC של מתאמי רשת...", "type": "sys-out"})

    try:
        if platform.system() == "Windows":
            command = ["getmac", "/fo", "csv", "/nh"] # /nh for No Header
            process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            output = process.stdout.strip()

            if output:
                lines.append({"text": "--- כתובות MAC ---", "type": "success"})
                # CSV format is like: "MAC Address","Connection Name"
                for line in output.splitlines():
                    parts = line.strip().split(',')
                    if len(parts) >= 1:
                        mac_address = parts[0].strip('"')
                        connection_name = parts[1].strip('"') if len(parts) > 1 else "לא ידוע"
                        lines.append({"text": f"  {connection_name}: {mac_address}", "type": ""})
                lines.append({"text": "✅ אחזור כתובות MAC הושלם.", "type": "success"})
            else:
                lines.append({"text": "⚠️ לא נמצאו מתאמי רשת פעילים עם כתובות MAC.", "type": "sys-out"})
        else:
            lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
            lines.append({"text": "למערכות אחרות, יש לחפש פקודות כמו 'ip link' או 'ifconfig'.", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'getmac' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת getmac: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
