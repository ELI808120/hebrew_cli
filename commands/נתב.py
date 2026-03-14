import subprocess
import platform
import re

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        lines.append({"text": "למערכות אחרות יש להשתמש ב-route -n או netstat -rn.", "type": "sys-out"})
        return {"lines": lines}

    lines.append({"text": "🔎 מחפש את כתובת הנתב (Default Gateway)...", "type": "sys-out"})

    try:
        command = ["ipconfig"]
        process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        output = process.stdout.strip()

        gateway_found = False
        for line in output.splitlines():
            if "Default Gateway" in line or "שער ברירת מחדל" in line: # Try to catch both English and Hebrew output
                match = re.search(r":\s*([\d.]+)", line)
                if match:
                    gateway_ip = match.group(1)
                    if gateway_ip.strip() and gateway_ip.strip() != "0.0.0.0": # Filter out empty or 0.0.0.0 gateways
                        lines.append({"text": f"✅ כתובת הנתב (Default Gateway): {gateway_ip}", "type": "success"})
                        gateway_found = True
                        break # Found the first valid gateway, exit

        if not gateway_found:
            lines.append({"text": "⚠️ לא נמצאה כתובת נתב פעילה (Default Gateway).", "type": "sys-out"})
            lines.append({"text": "ייתכן שאין חיבור רשת פעיל או שיש בעיה בתצורה.", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'ipconfig' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת ipconfig: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
