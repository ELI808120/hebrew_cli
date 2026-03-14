import platform
import os
import socket
import datetime

def execute(args):
    lines = []
    
    lines.append({"text": "📊 אוסף מידע כללי על המערכת...", "type": "sys-out"})

    lines.append({"text": "--- מידע כללי ---", "type": "success"})
    lines.append({"text": f"  מערכת הפעלה: {platform.system()} {platform.release()} ({platform.version()})", "type": ""})
    lines.append({"text": f"  ארכיטקטורה: {platform.machine()}", "type": ""})
    lines.append({"text": f"  שם מחשב: {socket.gethostname()}", "type": ""})
    lines.append({"text": f"  שם משתמש נוכחי: {os.getlogin()}", "type": ""})
    lines.append({"text": f"  זמן נוכחי: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "type": ""})
    
    # Try to get uptime if available (simplified check)
    try:
        import subprocess
        if platform.system() == "Windows":
            cmd = ["systeminfo"]
            p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            boot_time_match = re.search(r"(?:Boot Time|זמן אתחול):\s*(.*)", p.stdout)
            if boot_time_match:
                boot_time_str = boot_time_match.group(1).strip()
                try:
                    boot_time = datetime.datetime.strptime(boot_time_str, "%m/%d/%Y, %I:%M:%S %p")
                except ValueError:
                    try:
                        boot_time = datetime.datetime.strptime(boot_time_str, "%d/%m/%Y, %H:%M:%S")
                    except ValueError:
                        boot_time = datetime.datetime.strptime(boot_time_str, "%d/%m/%Y, %I:%M:%S %p")
                uptime_delta = datetime.datetime.now() - boot_time
                lines.append({"text": f"  זמן פעולה: {uptime_delta.days} ימים, {uptime_delta.seconds // 3600} שעות, {(uptime_delta.seconds % 3600) // 60} דקות", "type": ""})
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            cmd = ["uptime", "-p"] # Portable uptime format
            p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)
            lines.append({"text": f"  זמן פעולה: {p.stdout.strip()}", "type": ""})
    except Exception:
        lines.append({"text": "  זמן פעולה: לא זמין", "type": "sys-out"})


    lines.append({"text": "✅ איסוף מידע מערכת הושלם.", "type": "success"})
    
    return {"lines": lines}
