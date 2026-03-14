import subprocess
import os

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק פקודת קומפילציה להרצה (לדוגמה: tsc, gcc main.c).", "type": "error"})
        lines.append({"text": "דוגמה: קומפייל tsc", "type": "sys-out"})
        lines.append({"text": "דוגמה: קומפייל gcc my_program.c -o my_program", "type": "sys-out"})
        return {"lines": lines}

    # The command to execute (e.g., tsc, gcc, etc.)
    compile_command_base = args[0]
    compile_args = args[1:]

    full_command = [compile_command_base] + compile_args

    lines.append({"text": f"🛠️ מריץ קומפילציה עם הפקודה: {' '.join(full_command)}...", "type": "sys-out"})

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
            lines.append({"text": f"❌ הקומפילציה נכשלה עם קוד יציאה {process.returncode}.", "type": "error"})
        else:
            lines.append({"text": "✅ הקומפילציה הושלמה בהצלחה.", "type": "success"})

    except FileNotFoundError:
        lines.append({"text": f"❌ שגיאה: הפקודה '{compile_command_base}' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
