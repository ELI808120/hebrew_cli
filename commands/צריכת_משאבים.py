import subprocess
import platform
import re
import time

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        lines.append({"text": "למערכות אחרות, יש לחפש פקודות כמו 'top' או 'htop'.", "type": "sys-out"})
        return {"lines": lines}

    lines.append({"text": "📈 אוסף נתונים על צריכת משאבי מערכת (מעבד וזיכרון)...", "type": "sys-out"})

    try:
        # Get CPU Usage
        # Wmic doesn't give a direct % for current usage. It's often "LoadPercentage" or needs calculation over time.
        # Let's use "wmic cpu get LoadPercentage /value" - this gives a snapshot.
        cpu_command = ["wmic", "cpu", "get", "LoadPercentage", "/value"]
        cpu_process = subprocess.run(cpu_command, capture_output=True, text=True, check=True, encoding='utf-8')
        cpu_output = cpu_process.stdout.strip()
        cpu_load_match = re.search(r"LoadPercentage=(\d+)", cpu_output)
        cpu_usage = cpu_load_match.group(1) if cpu_load_match else "N/A"
        
        lines.append({"text": "--- צריכת משאבים ---", "type": "success"})
        lines.append({"text": f"  שימוש במעבד: {cpu_usage}%", "type": ""})

        # Get Memory Usage
        # Re-using logic from זיכרון_פנוי.py
        total_mem_command = ["wmic", "ComputerSystem", "get", "TotalPhysicalMemory", "/value"]
        total_mem_process = subprocess.run(total_mem_command, capture_output=True, text=True, check=True, encoding='utf-8')
        total_mem_output = total_mem_process.stdout.strip()

        free_mem_command = ["wmic", "OS", "get", "FreePhysicalMemory", "/value"]
        free_mem_process = subprocess.run(free_mem_command, capture_output=True, text=True, check=True, encoding='utf-8')
        free_mem_output = free_mem_process.stdout.strip()

        total_mem_gb = 0
        match = re.search(r"TotalPhysicalMemory=(\d+)", total_mem_output)
        if match:
            total_mem_bytes = int(match.group(1))
            total_mem_gb = total_mem_bytes / (1024**3)

        free_mem_gb = 0
        match = re.search(r"FreePhysicalMemory=(\d+)", free_mem_output)
        if match:
            free_mem_kb = int(match.group(1))
            free_mem_gb = free_mem_kb / (1024**2)
        
        if total_mem_gb > 0:
            used_mem_gb = total_mem_gb - free_mem_gb
            used_mem_percent = (used_mem_gb / total_mem_gb) * 100 if total_mem_gb > 0 else 0
            lines.append({"text": f"  זיכרון בשימוש: {used_mem_gb:.2f} GB מתוך {total_mem_gb:.2f} GB ({used_mem_percent:.2f}%)", "type": ""})
        else:
            lines.append({"text": "  זיכרון: לא זמין", "type": ""})

        lines.append({"text": "✅ אחזור צריכת משאבים הושלם.", "type": "success"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'wmic' לא נמצאה. ודא שהיא קיימת בנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת WMIC: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
