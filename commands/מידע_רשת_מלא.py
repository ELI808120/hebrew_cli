import subprocess
import re

def execute(args):
    lines = [{"text": "🌐 שולף נתוני רשת מלאים...", "type": "sys-out"}]
    try:
        res = subprocess.check_output('ipconfig', shell=True).decode('cp862', errors='ignore')
        for line in res.splitlines():
            line = line.strip()
            if "IPv4 Address" in line or "כתובת IPv4" in line:
                ip = re.search(r'(\d+\.\d+\.\d+\.\d+)', line).group(1)
                lines.append({"text": f"📍 כתובת IP פנימית: {ip}", "type": "success"})
            elif "Subnet Mask" in line or "מסכת רשת" in line:
                mask = re.search(r'(\d+\.\d+\.\d+\.\d+)', line).group(1)
                lines.append({"text": f"🖥️ מסכת רשת: {mask}", "type": ""})
            elif "Default Gateway" in line or "שער ברירת מחדל" in line:
                gw = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if gw: lines.append({"text": f"🏠 שער ברירת מחדל (ראוטר): {gw.group(1)}", "type": "sys-out"})
        return {"lines": lines}
    except Exception as e:
        return {"lines": [{"text": f"❌ שגיאה בשליפת נתוני רשת: {e}", "type": "error"}]}