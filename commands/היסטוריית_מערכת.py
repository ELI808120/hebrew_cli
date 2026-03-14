import subprocess
import platform
import re
import datetime

def execute(args):
    lines = []
    
    lines.append({"text": "📜 מאחזר היסטוריית מערכת (זמני אתחול)...", "type": "sys-out"})

    try:
        if platform.system() == "Windows":
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
                try:
                    # Attempt common formats
                    boot_time = datetime.datetime.strptime(boot_time_str, "%m/%d/%Y, %I:%M:%S %p")
                except ValueError:
                    try:
                        boot_time = datetime.datetime.strptime(boot_time_str, "%d/%m/%Y, %H:%M:%S")
                    except ValueError:
                        boot_time = datetime.datetime.strptime(boot_time_str, "%d/%m/%Y, %I:%M:%S %p")

                lines.append({"text": "--- היסטוריית אתחול ---", "type": "success"})
                lines.append({"text": f"  זמן אתחול אחרון: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}", "type": ""})
                lines.append({"text": "✅ אחזור היסטוריית מערכת הושלם.", "type": "success"})
            else:
                lines.append({"text": "⚠️ לא ניתן היה לאתר את זמן האתחול.", "type": "sys-out"})

        elif platform.system() == "Linux":
            command = ["last", "reboot"]
            process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            output = process.stdout.strip()
            
            lines.append({"text": "--- היסטוריית אתחול (Linux) ---", "type": "success"})
            for line in output.splitlines():
                if "reboot" in line:
                    lines.append({"text": line, "type": ""})
            lines.append({"text": "✅ אחזור היסטוריית מערכת הושלם.", "type": "success"})

        elif platform.system() == "Darwin": # macOS
            command = ["sysctl", "kern.boottime"]
            process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            output = process.stdout.strip()

            match = re.search(r"sec = (\d+),", output)
            if match:
                boot_timestamp = int(match.group(1))
                boot_time = datetime.datetime.fromtimestamp(boot_timestamp)
                lines.append({"text": "--- היסטוריית אתחול (macOS) ---", "type": "success"})
                lines.append({"text": f"  זמן אתחול: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}", "type": ""})
                lines.append({"text": "✅ אחזור היסטוריית מערכת הושלם.", "type": "success"})
            else:
                lines.append({"text": "⚠️ לא ניתן היה לאתר את זמן האתחול.", "type": "sys-out"})
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
