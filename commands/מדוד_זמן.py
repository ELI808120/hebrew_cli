import subprocess
import time

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק פקודה לביצוע ומדידה.", "type": "error"})
        lines.append({"text": "דוגמה: מדוד_זמן פינג google.com", "type": "sys-out"})
        return {"lines": lines}

    command_to_measure = args
    
    lines.append({"text": f"⏱️ מודד זמן ביצוע של: {' '.join(command_to_measure)}...", "type": "sys-out"})

    start_time = time.perf_counter()

    try:
        # Execute the command, capture output
        process = subprocess.run(command_to_measure, capture_output=True, text=True, check=True, encoding='utf-8')
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        lines.append({"text": "--- פלט הפקודה המקורית ---", "type": "sys-out"})
        if process.stdout:
            for line in process.stdout.splitlines():
                lines.append({"text": line, "type": ""})
        if process.stderr:
            for line in process.stderr.splitlines():
                lines.append({"text": line, "type": "error"})
        
        lines.append({"text": f"✅ זמן ביצוע כולל: {elapsed_time:.4f} שניות.", "type": "success"})

    except FileNotFoundError:
        lines.append({"text": f"❌ שגיאה: הפקודה '{command_to_measure[0]}' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        lines.append({"text": f"❌ הפקודה '{' '.join(command_to_measure)}' נכשלה עם קוד יציאה {cpe.returncode}.", "type": "error"})
        lines.append({"text": f"  פלט שגיאה: {cpe.stderr.strip()}", "type": "error"})
        lines.append({"text": f"  זמן ביצוע עד השגיאה: {elapsed_time:.4f} שניות.", "type": "sys-out"})
    except Exception as e:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
        lines.append({"text": f"  זמן ביצוע עד השגיאה: {elapsed_time:.4f} שניות.", "type": "sys-out"})
    
    return {"lines": lines}
