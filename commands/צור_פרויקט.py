import subprocess
import os

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק פקודת יצירת פרויקט להרצה (לדוגמה: npm init -y, npx create-react-app my-app).", "type": "error"})
        lines.append({"text": "דוגמה: צור_פרויקט npm init -y", "type": "sys-out"})
        lines.append({"text": "דוגמה: צור_פרויקט npx create-react-app my-app", "type": "sys-out"})
        return {"lines": lines}

    # The command to execute (e.g., npm, npx, etc.)
    scaffold_command_base = args[0]
    scaffold_args = args[1:]

    full_command = [scaffold_command_base] + scaffold_args

    lines.append({"text": f"🏗️ מריץ פקודת יצירת פרויקט: {' '.join(full_command)}...", "type": "sys-out"})

    try:
        # Using Popen to stream output
        process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', bufsize=1)
        
        # Read stdout and stderr in real-time
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()

            if not stdout_line and not stderr_line and process.poll() is not None:
                break
            
            if stdout_line:
                lines.append({"text": stdout_line.strip(), "type": ""})
            if stderr_line:
                lines.append({"text": stderr_line.strip(), "type": "error"})

        process.wait() # Ensure the process has truly finished

        if process.returncode != 0:
            lines.append({"text": f"❌ יצירת הפרויקט נכשלה עם קוד יציאה {process.returncode}.", "type": "error"})
        else:
            lines.append({"text": "✅ יצירת הפרויקט הושלמה בהצלחה.", "type": "success"})

    except FileNotFoundError:
        lines.append({"text": f"❌ שגיאה: הפקודה '{scaffold_command_base}' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
