import subprocess
import platform
import re
import datetime

def execute(args):
    lines = []
    
    lines.append({"text": "⏱️ מאחזר את זמן פעולת המערכת...", "type": "sys-out"})

    try:
        if platform.system() == "Windows":
            # Using 'systeminfo' for Windows
            command = ["systeminfo"]
            process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
            output = process.stdout.strip()
            
            boot_time_str = None
            for line in output.splitlines():
                if "Boot Time:" in line or "זמן אתחול:" in line:
                    match = re.search(r"(?:Boot Time|זמן אתחול):\s*(.*)", line)
                    if match:
                        boot_time_str = match.group(1).strip()
                        break
            
            if boot_time_str:
                # Example: "2/1/2026, 10:00:00 AM" or "01/02/2026, 10:00:00"
                # Need to handle different date formats based on system locale
                try:
                    # Try common formats
                    boot_time = datetime.datetime.strptime(boot_time_str, "%m/%d/%Y, %I:%M:%S %p")
                except ValueError:
                    try:
                        boot_time = datetime.datetime.strptime(boot_time_str, "%d/%m/%Y, %H:%M:%S")
                    except ValueError:
                        boot_time = datetime.datetime.strptime(boot_time_str, "%d/%m/%Y, %I:%M:%S %p")


                now = datetime.datetime.now()
                uptime_delta = now - boot_time

                days = uptime_delta.days
                hours = uptime_delta.seconds // 3600
                minutes = (uptime_delta.seconds % 3600) // 60
                seconds = uptime_delta.seconds % 60

                lines.append({"text": f"✅ המערכת פעילה מזה: {days} ימים, {hours} שעות, {minutes} דקות, {seconds} שניות.", "type": "success"})
            else:
                lines.append({"text": "⚠️ לא ניתן היה לאתר את זמן האתחול.", "type": "sys-out"})

        elif platform.system() == "Linux" or platform.system() == "Darwin": # For Unix-like systems
            command = ["uptime"]
            process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            output = process.stdout.strip()
            lines.append({"text": f"✅ זמן פעולת המערכת: {output}", "type": "success"})
        else:
            lines.append({"text": "❌ שגיאה: מערכת הפעלה לא נתמכת כרגע עבור פקודה זו.", "type": "error"})
            lines.append({"text": f"  מערכת: {platform.system()}", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה הנדרשת לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת פקודה: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
