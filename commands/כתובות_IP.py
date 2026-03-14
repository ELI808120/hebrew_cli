import subprocess
import platform
import re

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        lines.append({"text": "למערכות אחרות יש להשתמש בפקודות כמו 'ip addr' או 'ifconfig'.", "type": "sys-out"})
        return {"lines": lines}

    lines.append({"text": "🌐 מאחזר כתובות IP מקומיות...", "type": "sys-out"})

    try:
        command = ["ipconfig"]
        process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        output = process.stdout.strip()

        adapters_found = False
        current_adapter = {}

        for line in output.splitlines():
            line = line.strip()
            if not line:
                if current_adapter:
                    # Process current adapter before clearing
                    if "IPv4 Address" in current_adapter and current_adapter["IPv4 Address"].strip() != "0.0.0.0":
                        adapters_found = True
                        lines.append({"text": f"--- מתאם רשת: {current_adapter.get('Description', 'לא ידוע')} ---", "type": "success"})
                        lines.append({"text": f"  כתובת IPv4: {current_adapter.get('IPv4 Address')}", "type": ""})
                        lines.append({"text": f"  מסכת רשת משנה: {current_adapter.get('Subnet Mask')}", "type": ""})
                        lines.append({"text": f"  שער ברירת מחדל: {current_adapter.get('Default Gateway')}", "type": ""})
                        lines.append({"text": f"  שרתי DNS: {current_adapter.get('DNS Servers')}", "type": ""})
                current_adapter = {} # Reset for next adapter
                continue

            # Check for adapter description (e.g., "Ethernet adapter Local Area Connection:")
            adapter_match = re.match(r"^([^:]+)\s*adapter", line)
            if adapter_match:
                current_adapter["Description"] = adapter_match.group(1).strip()
                continue
            
            # Extract relevant info
            if "IPv4 Address" in line or "כתובת IPv4" in line:
                match = re.search(r":\s*([\d.]+)", line)
                if match: current_adapter["IPv4 Address"] = match.group(1)
            elif "Subnet Mask" in line or "מסכת רשת משנה" in line:
                match = re.search(r":\s*([\d.]+)", line)
                if match: current_adapter["Subnet Mask"] = match.group(1)
            elif "Default Gateway" in line or "שער ברירת מחדל" in line:
                match = re.search(r":\s*([\d.]+)", line)
                if match: current_adapter["Default Gateway"] = match.group(1)
            elif "DNS Servers" in line or "שרתי DNS" in line:
                match = re.findall(r"[\d.]+", line) # Can be multiple DNS servers
                if match: current_adapter["DNS Servers"] = ", ".join(match)

        # Process the last adapter
        if current_adapter and "IPv4 Address" in current_adapter and current_adapter["IPv4 Address"].strip() != "0.0.0.0":
            adapters_found = True
            lines.append({"text": f"--- מתאם רשת: {current_adapter.get('Description', 'לא ידוע')} ---", "type": "success"})
            lines.append({"text": f"  כתובת IPv4: {current_adapter.get('IPv4 Address')}", "type": ""})
            lines.append({"text": f"  מסכת רשת משנה: {current_adapter.get('Subnet Mask')}", "type": ""})
            lines.append({"text": f"  שער ברירת מחדל: {current_adapter.get('Default Gateway')}", "type": ""})
            lines.append({"text": f"  שרתי DNS: {current_adapter.get('DNS Servers')}", "type": ""})

        if not adapters_found:
            lines.append({"text": "⚠️ לא נמצאו כתובות IP פעילות.", "type": "sys-out"})
            lines.append({"text": "  ייתכן שאין חיבורי רשת פעילים.", "type": "sys-out"})
        
        lines.append({"text": "✅ סקירת כתובות IP הושלמה.", "type": "success"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'ipconfig' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת ipconfig: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
