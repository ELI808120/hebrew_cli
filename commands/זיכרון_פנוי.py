import subprocess
import platform

def execute(args):
    lines = []

    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        lines.append({"text": "למערכות אחרות יש להשתמש בפקודות כמו 'free -m' או 'top'.", "type": "sys-out"})
        return {"lines": lines}

    lines.append({"text": "🧠 אוסף נתוני זיכרון...", "type": "sys-out"})

    try:
        # Using WMIC to get memory information
        command = ["wmic", "ComputerSystem", "get", "TotalPhysicalMemory", "/value"]
        total_mem_process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        total_mem_output = total_mem_process.stdout.strip()

        total_mem_gb = 0
        match = re.search(r"TotalPhysicalMemory=(\d+)", total_mem_output)
        if match:
            total_mem_bytes = int(match.group(1))
            total_mem_gb = total_mem_bytes / (1024**3) # Bytes to GB
            lines.append({"text": f"סה"כ זיכרון פיזי: {total_mem_gb:.2f} GB", "type": "sys-out"})
        else:
            lines.append({"text": "⚠️ לא ניתן היה לקבל את סך הזיכרון הפיזי.", "type": "sys-out"})

        command = ["wmic", "OS", "get", "FreePhysicalMemory", "/value"]
        free_mem_process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        free_mem_output = free_mem_process.stdout.strip()

        free_mem_gb = 0
        match = re.search(r"FreePhysicalMemory=(\d+)", free_mem_output)
        if match:
            free_mem_kb = int(match.group(1))
            free_mem_gb = free_mem_kb / (1024**2) # KB to GB
            lines.append({"text": f"זיכרון פיזי פנוי: {free_mem_gb:.2f} GB", "type": "sys-out"})
        else:
            lines.append({"text": "⚠️ לא ניתן היה לקבל את הזיכרון הפיזי הפנוי.", "type": "sys-out"})
        
        if total_mem_gb > 0 and free_mem_gb > 0:
            used_mem_gb = total_mem_gb - free_mem_gb
            lines.append({"text": f"זיכרון פיזי בשימוש: {used_mem_gb:.2f} GB", "type": "sys-out"})
            lines.append({"text": f"📊 סקירת זיכרון הושלמה.", "type": "success"})


    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'wmic' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת WMIC: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
