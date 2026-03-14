import subprocess
import platform
import re

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת רק במערכת הפעלה Windows.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": "🔋 מאחזר מידע על מצב הסוללה...", "type": "sys-out"})

    try:
        command = ["powercfg", "/batteryreport"]
        # This command generates an HTML report.
        # We need to find a way to get direct information without parsing HTML or creating files.
        # Let's try 'powercfg /batteryinfo' or 'WMIC Path Win32_Battery Get EstimatedChargeRemaining,EstimatedRunTime'

        # Attempting WMIC for direct battery info
        wmic_command = ["wmic", "Path", "Win32_Battery", "Get", "EstimatedChargeRemaining,EstimatedRunTime,BatteryStatus", "/value"]
        process = subprocess.run(wmic_command, capture_output=True, text=True, check=True, encoding='utf-8')
        output = process.stdout.strip()

        battery_info = {}
        for line in output.splitlines():
            line = line.strip()
            if "=" in line:
                key, value = line.split("=", 1)
                battery_info[key.strip()] = value.strip()
        
        if battery_info:
            lines.append({"text": "--- מצב סוללה ---", "type": "success"})
            
            charge_percent = battery_info.get("EstimatedChargeRemaining", "לא זמין")
            run_time_minutes = battery_info.get("EstimatedRunTime", "לא זמין") # in minutes
            battery_status_code = battery_info.get("BatteryStatus", "לא זמין")

            status_map = {
                "1": "מתרוקנת",
                "2": "נטענת",
                "3": "טעונה במלואה",
                "4": "לא טעונה",
                "5": "טעינה חריגה",
                "6": "טעינה מוגמרת",
                "7": "טעינה חסרה",
                "8": "מחוברת לזרם AC",
                "9": "לא ידוע",
                "10": "לא נטענת"
            }
            battery_status_text = status_map.get(battery_status_code, "לא ידוע")

            lines.append({"text": f"  אחוז טעינה: {charge_percent}%", "type": ""})
            if run_time_minutes != "לא זמין":
                hours = int(run_time_minutes) // 60
                minutes = int(run_time_minutes) % 60
                lines.append({"text": f"  זמן שימוש משוער שנותר: {hours} שעות ו-{minutes} דקות", "type": ""})
            else:
                lines.append({"text": "  זמן שימוש משוער שנותר: לא זמין", "type": ""})
            lines.append({"text": f"  סטטוס: {battery_status_text}", "type": ""})
            lines.append({"text": "✅ מידע סוללה נשלף בהצלחה.", "type": "success"})
        else:
            lines.append({"text": "⚠️ לא נמצאו נתוני סוללה.", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'wmic' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת WMIC: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
