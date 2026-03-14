import subprocess
import platform

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק פקודת npm לביצוע (לדוגמה: install, run dev).", "type": "error"})
        lines.append({"text": "דוגמה: נוד install", "type": "sys-out"})
        lines.append({"text": "דוגמה: נוד run start", "type": "sys-out"})
        return {"lines": lines}

    # Prepend 'npm' to the arguments
    npm_command = ["npm"] + args

    lines.append({"text": f"🚀 מריץ פקודת npm: {' '.join(npm_command)}...", "type": "sys-out"})

    try:
        # Using Popen to stream output
        process = subprocess.Popen(npm_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', bufsize=1)
        
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
            lines.append({"text": f"❌ פקודת npm נכשלה עם קוד יציאה {process.returncode}.", "type": "error"})
        else:
            lines.append({"text": "✅ פקודת npm בוצעה בהצלחה.", "type": "success"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'npm' לא נמצאה. ודא ש-Node.js מותקן ובנתיב המערכת.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
