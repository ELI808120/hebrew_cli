import subprocess
import re

def execute(args):
    lines = [{"text": "🌐 סורק מתאמי רשת וכתובות IP פעילות...", "type": "sys-out"}]
    try:
        # הרצת ipconfig באנגלית
        res = subprocess.check_output("ipconfig", shell=True, stderr=subprocess.STDOUT)
        try:
            output = res.decode('cp862', errors='ignore')
        except UnicodeDecodeError:
            output = res.decode('utf-8', errors='ignore')
        
        adapter_name = ""
        found_any = False
        
        for line in output.splitlines():
            line = line.strip()
            if not line: continue
            
            # זיהוי שם מתאם (כרטיס רשת)
            if line.endswith(':'):
                raw_name = line[:-1]
                adapter_name = raw_name.replace("Ethernet adapter", "מתאם קווי").replace("Wireless LAN adapter", "מתאם אלחוטי (Wi-Fi)")
                continue
            
            # זיהוי כתובת IPv4
            ipv4_match = re.search(r'IPv4 Address[\.\s]+: ([\d\.]+)', line, re.IGNORECASE)
            # תמיכה גם בווינדוס שהותקן בעברית
            if not ipv4_match: ipv4_match = re.search(r'IPv4.*: ([\d\.]+)', line)
                
            if ipv4_match:
                ip = ipv4_match.group(1)
                lines.append({"text": f"🔌 {adapter_name}", "type": "success"})
                lines.append({"text": f"    כתובת IP (פנימית): {ip}", "type": ""})
                found_any = True
                continue
                
            # זיהוי Default Gateway (שער ברירת מחדל / ראוטר)
            gateway_match = re.search(r'Default Gateway[\.\s]+: ([\d\.]+)', line, re.IGNORECASE)
            if not gateway_match: gateway_match = re.search(r'ברירת מחדל.*: ([\d\.]+)', line)
                
            if gateway_match:
                lines.append({"text": f"    כתובת הראוטר:      {gateway_match.group(1)}", "type": "sys-out"})
                lines.append({"text": "", "type": ""}) # שורת רווח
                continue

        if not found_any:
            lines.append({"text": "❌ לא נמצאו חיבורי רשת פעילים.", "type": "error"})
            
        return {"lines": lines}
        
    except Exception as e:
        return {"lines": [{"text": f"שגיאה בסריקת הרשת: {e}", "type": "error"}]}