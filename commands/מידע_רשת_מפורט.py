import subprocess
import platform

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        lines.append({"text": "למערכות אחרות, יש לחפש פקודות כמו 'ip link show' או 'ifconfig'.", "type": "sys-out"})
        return {"lines": lines}

    lines.append({"text": "🌐 מאחזר מידע רשת מפורט...", "type": "sys-out"})

    try:
        command = ["wmic", "nicconfig", "get", "Description,MACAddress,IPAddress,DNSHostName,DefaultIPGateway", "/value"]
        process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        output = process.stdout.strip()

        adapters_info = []
        current_adapter = {}
        for line in output.splitlines():
            line = line.strip()
            if not line:
                if current_adapter:
                    adapters_info.append(current_adapter)
                current_adapter = {}
                continue
            
            if "=" in line:
                key, value = line.split("=", 1)
                current_adapter[key.strip()] = value.strip()
        
        if current_adapter: # Add the last adapter
            adapters_info.append(current_adapter)

        if adapters_info:
            lines.append({"text": "--- מידע מתאמי רשת ---", "type": "success"})
            for adapter in adapters_info:
                if adapter.get("Description"): # Only display if Description is available
                    lines.append({"text": "--------------------------------------------------------------------------------", "type": "sys-out"})
                    lines.append({"text": f"  תיאור: {adapter.get('Description', 'N/A')}", "type": ""})
                    lines.append({"text": f"  כתובת MAC: {adapter.get('MACAddress', 'N/A')}", "type": ""})
                    
                    ip_addresses = adapter.get('IPAddress')
                    if ip_addresses:
                        # IPAddress might be an array or single value
                        if ip_addresses.startswith('{') and ip_addresses.endswith('}'):
                            ip_list = ip_addresses[1:-1].split('","')
                            lines.append({"text": f"  כתובות IP: {', '.join(ip_list)}", "type": ""})
                        else:
                            lines.append({"text": f"  כתובת IP: {ip_addresses}", "type": ""})
                    else:
                         lines.append({"text": "  כתובת IP: N/A", "type": ""})


                    lines.append({"text": f"  שם מארח DNS: {adapter.get('DNSHostName', 'N/A')}", "type": ""})
                    
                    default_gateways = adapter.get('DefaultIPGateway')
                    if default_gateways:
                        if default_gateways.startswith('{') and default_gateways.endswith('}'):
                            gateway_list = default_gateways[1:-1].split('","')
                            lines.append({"text": f"  שערי ברירת מחדל: {', '.join(gateway_list)}", "type": ""})
                        else:
                            lines.append({"text": f"  שער ברירת מחדל: {default_gateways}", "type": ""})
                    else:
                        lines.append({"text": "  שער ברירת מחדל: N/A", "type": ""})

            lines.append({"text": "✅ אחזור מידע רשת הושלם.", "type": "success"})
        else:
            lines.append({"text": "⚠️ לא נמצאו מתאמי רשת עם תצורה.", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'wmic' לא נמצאה. ודא שהיא קיימת בנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת wmic: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
