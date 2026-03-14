import shutil
import os

def execute(args):
    lines = []
    try:
        if len(args) < 2:
            lines.append({"text": "❌ שגיאה: יש לספק נתיב מקור ונתיב יעד.", "type": "error"})
            return {"lines": lines}

        source = args[0]
        destination = args[1]

        lines.append({"text": f"🔄 מנסה להעביר את '{source}' לתוך '{destination}'...", "type": "sys-out"})

        shutil.move(source, destination)
        lines.append({"text": f"✅ המקור '{source}' הועבר בהצלחה ליעד '{destination}'.", "type": "success"})
            
    except FileNotFoundError:
        lines.append({"text": f"❌ שגיאה: אחד הנתיבים שצוינו לא נמצא.", "type": "error"})
    except PermissionError:
        lines.append({"text": "❌ שגיאה: אין הרשאה לבצע את הפעולה.", "type": "error"})
    except shutil.Error as se:
        lines.append({"text": f"❌ שגיאת העברה: {se}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
