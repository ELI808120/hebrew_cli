import subprocess
import platform

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        lines.append({"text": "למערכות אחרות, יש לחפש פקודות כמו 'systemctl list-units --type=service'.", "type": "sys-out"})
        return {"lines": lines}

    lines.append({"text": "⚙️ מאחזר רשימת שירותי Windows...", "type": "sys-out"})

    try:
        command = ["sc", "query", "type=", "service", "state=", "all"]
        process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        output = process.stdout.strip()

        service_info = []
        current_service = {}
        for line in output.splitlines():
            line = line.strip()
            if not line:
                if current_service:
                    service_info.append(current_service)
                current_service = {}
                continue
            
            if "SERVICE_NAME:" in line:
                if current_service: # If a service was partially parsed, add it
                    service_info.append(current_service)
                    current_service = {}
                current_service["שם שירות"] = line.split(":", 1)[1].strip()
            elif "DISPLAY_NAME:" in line:
                current_service["שם תצוגה"] = line.split(":", 1)[1].strip()
            elif "STATE" in line:
                state_match = line.split(":", 1)[1].strip()
                if "RUNNING" in state_match:
                    current_service["סטטוס"] = "פועל"
                elif "STOPPED" in state_match:
                    current_service["סטטוס"] = "עצור"
                else:
                    current_service["סטטוס"] = state_match.replace("(", "").replace(")", "").strip()

        if current_service: # Add the last service
            service_info.append(current_service)

        if service_info:
            lines.append({"text": "--- שירותי Windows ---", "type": "success"})
            lines.append({"text": "{:<40} {:<30} {:<10}".format("שם תצוגה", "שם שירות", "סטטוס"), "type": "sys-out"})
            lines.append({"text": "--------------------------------------------------------------------------------", "type": "sys-out"})
            for service in service_info:
                display_name = service.get("שם תצוגה", "N/A")[:38] + ".." if len(service.get("שם תצוגה", "N/A")) > 40 else service.get("שם תצוגה", "N/A")
                service_name = service.get("שם שירות", "N/A")[:28] + ".." if len(service.get("שם שירות", "N/A")) > 30 else service.get("שם שירות", "N/A")
                status = service.get("סטטוס", "N/A")
                lines.append({"text": "{:<40} {:<30} {:<10}".format(display_name, service_name, status), "type": ""})
            lines.append({"text": "✅ אחזור שירותי Windows הושלם.", "type": "success"})
        else:
            lines.append({"text": "⚠️ לא נמצאו שירותי Windows.", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'sc' לא נמצאה. ודא שהיא קיימת בנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת sc: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
