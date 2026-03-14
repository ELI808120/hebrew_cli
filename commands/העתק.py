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

        lines.append({"text": f"🔄 מנסה להעתיק את '{source}' לתוך '{destination}'...", "type": "sys-out"})

        if os.path.isfile(source):
            shutil.copy2(source, destination)
            lines.append({"text": f"✅ הקובץ '{source}' הועתק בהצלחה ל-'{destination}'.", "type": "success"})
        elif os.path.isdir(source):
            # If destination exists and is a directory, copy into it.
            # If destination does not exist, copytree creates it.
            if os.path.exists(destination) and not os.path.isdir(destination):
                lines.append({"text": f"❌ שגיאה: יעד '{destination}' קיים ואינו תיקייה.", "type": "error"})
                return {"lines": lines}
            
            # If destination is an existing directory, we want to copy the source directory *into* it.
            # E.g., copy 'dirA' to 'dirB' -> 'dirB/dirA'
            final_destination = os.path.join(destination, os.path.basename(source)) if os.path.isdir(destination) else destination
            shutil.copytree(source, final_destination)
            lines.append({"text": f"✅ התיקייה '{source}' הועתקה בהצלחה ל-'{final_destination}'.", "type": "success"})
        else:
            lines.append({"text": f"❌ שגיאה: המקור '{source}' אינו קיים או אינו קובץ/תיקייה חוקיים.", "type": "error"})
            
    except FileNotFoundError:
        lines.append({"text": f"❌ שגיאה: אחד הנתיבים שצוינו לא נמצא.", "type": "error"})
    except PermissionError:
        lines.append({"text": "❌ שגיאה: אין הרשאה לבצע את הפעולה.", "type": "error"})
    except shutil.Error as se:
        lines.append({"text": f"❌ שגיאת העתקה: {se}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
