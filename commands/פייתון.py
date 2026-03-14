import subprocess
import os

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק שם קובץ פייתון להרצה, או ביטוי פייתון עם הארגומנט '-c'.", "type": "error"})
        lines.append({"text": "דוגמה: פייתון my_script.py", "type": "sys-out"})
        lines.append({"text": "דוגמה: פייתון -c "print('שלום עולם')"", "type": "sys-out"})
        return {"lines": lines}

    # Prepend 'python' to the arguments
    python_command = ["python"] + args

    lines.append({"text": f"🐍 מריץ פקודת python: {' '.join(python_command)}...", "type": "sys-out"})

    try:
        # Using Popen to stream output
        process = subprocess.Popen(python_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', bufsize=1)
        
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
            lines.append({"text": f"❌ פקודת python נכשלה עם קוד יציאה {process.returncode}.", "type": "error"})
        else:
            lines.append({"text": "✅ פקודת python בוצעה בהצלחה.", "type": "success"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: המפרש 'python' לא נמצא. ודא ש-Python מותקן ובנתיב המערכת.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
