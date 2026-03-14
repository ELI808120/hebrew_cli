import subprocess
import platform
import re

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק שם דומיין לחיפוש DNS מפורט.", "type": "error"})
        lines.append({"text": "דוגמה: מידע_DNS_מפורט google.com", "type": "sys-out"})
        return {"lines": lines}

    domain = args[0]
    
    lines.append({"text": f"🌐 מבצע חיפוש DNS מפורט עבור '{domain}'...", "type": "sys-out"})

    try:
        if platform.system() == "Windows":
            commands = {
                "A (כתובות)": ["nslookup", "-type=A", domain],
                "MX (מייל)": ["nslookup", "-type=MX", domain],
                "NS (שרתי שמות)": ["nslookup", "-type=NS", domain],
            }
        else: # Assuming Unix-like systems for dig
            commands = {
                "A (כתובות)": ["dig", "+short", domain, "A"],
                "MX (מייל)": ["dig", "+short", domain, "MX"],
                "NS (שרתי שמות)": ["dig", "+short", domain, "NS"],
            }
        
        for record_type, command in commands.items():
            lines.append({"text": f"--- רשומות {record_type} ---", "type": "sys-out"})
            process = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8', errors='ignore')
            output = process.stdout.strip()
            
            if process.returncode == 0 and output:
                for line in output.splitlines():
                    # Filter out common nslookup/dig headers and irrelevant lines
                    if "Server:" not in line and "Address:" not in line and "Non-authoritative" not in line and not line.startswith(";;"):
                        lines.append({"text": line.strip(), "type": ""})
            else:
                lines.append({"text": "  לא נמצאו רשומות או שגיאה באחזור.", "type": "sys-out"})
        
        lines.append({"text": "✅ חיפוש DNS מפורט הושלם.", "type": "success"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'nslookup' (Windows) או 'dig' (Unix) לא נמצאה.", "type": "error"})
        lines.append({"text": "  ודא שהכלי המתאים מותקן ובנתיב המערכת.", "type": "sys-out"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
