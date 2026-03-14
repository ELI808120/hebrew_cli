import subprocess
import platform
import re

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        lines.append({"text": "למערכות אחרות, יש לחפש כלים כמו 'cron' או 'systemd-timers'.", "type": "sys-out"})
        return {"lines": lines}

    lines.append({"text": "🗓️ מאחזר רשימת משימות מתוזמנות...", "type": "sys-out"})

    try:
        command = ["schtasks", "/query", "/fo", "list", "/v"] # /v for verbose output
        process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        output = process.stdout.strip()

        tasks = []
        current_task = {}
        for line in output.splitlines():
            line = line.strip()
            if not line:
                if current_task:
                    tasks.append(current_task)
                current_task = {}
                continue
            
            # Key-Value pair parsing
            if ":" in line:
                key, value = line.split(":", 1)
                current_task[key.strip()] = value.strip()
        
        if current_task: # Add the last task
            tasks.append(current_task)

        if tasks:
            lines.append({"text": "--- משימות מתוזמנות ---", "type": "success"})
            for task in tasks:
                lines.append({"text": "--------------------------------------------------------------------------------", "type": "sys-out"})
                lines.append({"text": f"  שם משימה: {task.get('TaskName', 'N/A')}", "type": ""})
                lines.append({"text": f"  מצב: {task.get('Status', 'N/A')}", "type": ""})
                lines.append({"text": f"  הפעלה: {task.get('Last Run Time', 'N/A')}", "type": ""})
                lines.append({"text": f"  תוצאה: {task.get('Last Result', 'N/A')}", "type": ""})
                lines.append({"text": f"  הפעלה הבאה: {task.get('Next Run Time', 'N/A')}", "type": ""})
                lines.append({"text": f"  פקודה: {task.get('Task Command', 'N/A')}", "type": ""}) # 'Task Command' might be 'Task to Run' or similar
            lines.append({"text": "--------------------------------------------------------------------------------", "type": "sys-out"})
            lines.append({"text": f"✅ אחזור משימות מתוזמנות הושלם. נמצאו {len(tasks)} משימות.", "type": "success"})
        else:
            lines.append({"text": "⚠️ לא נמצאו משימות מתוזמנות.", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'schtasks' לא נמצאה. ודא שהיא קיימת בנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת schtasks: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
