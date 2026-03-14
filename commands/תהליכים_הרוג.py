import subprocess
import platform

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק PID או שם תהליך להריגה.", "type": "error"})
        lines.append({"text": "דוגמה (לפי PID): תהליכים_הרוג 1234", "type": "sys-out"})
        lines.append({"text": "דוגמה (לפי שם): תהליכים_הרוג explorer.exe", "type": "sys-out"})
        return {"lines": lines}

    target = args[0]
    
    lines.append({"text": f"💀 מנסה להרוג תהליך '{target}'...", "type": "sys-out"})

    try:
        if platform.system() == "Windows":
            if target.isdigit(): # Assume PID if it's a number
                command = ["taskkill", "/PID", target, "/F"] # /F to force kill
            else: # Assume image name
                command = ["taskkill", "/IM", target, "/F"]
            
            process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            output = process.stdout.strip()
            
            lines.append({"text": f"✅ {output}", "type": "success"})

        elif platform.system() == "Linux" or platform.system() == "Darwin":
            if target.isdigit(): # Assume PID
                command = ["kill", "-9", target] # Force kill with -9
            else: # Assume process name
                # Find PID by name first
                pgrep_command = ["pgrep", "-f", target]
                pgrep_process = subprocess.run(pgrep_command, capture_output=True, text=True, check=True, encoding='utf-8')
                pids = pgrep_process.stdout.strip().splitlines()
                
                if not pids:
                    lines.append({"text": f"❌ שגיאה: לא נמצא תהליך בשם '{target}'.", "type": "error"})
                    return {"lines": lines}
                
                for pid in pids:
                    lines.append({"text": f"💀 הורג תהליך {target} עם PID {pid}...", "type": "sys-out"})
                    kill_command = ["kill", "-9", pid]
                    subprocess.run(kill_command, capture_output=True, text=True, check=True, encoding='utf-8')
                    lines.append({"text": f"✅ תהליך PID {pid} נהרג.", "type": "success"})
        else:
            lines.append({"text": "❌ שגיאה: מערכת הפעלה לא נתמכת כרגע עבור פקודה זו.", "type": "error"})
            lines.append({"text": f"  מערכת: {platform.system()}", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'taskkill' (Windows) או 'kill/pgrep' (Unix) לא נמצאה.", "type": "error"})
        lines.append({"text": "ודא שהיא מותקנת ובנתיב המערכת.", "type": "sys-out"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהריגת תהליך: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
