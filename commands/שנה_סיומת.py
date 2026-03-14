import os

def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק סיומת קיימת וסיומת חדשה.", "type": "error"})
        lines.append({"text": "דוגמה: שנה_סיומת .txt .md", "type": "sys-out"})
        return {"lines": lines}

    old_extension = args[0]
    new_extension = args[1]

    if not old_extension.startswith('.'):
        old_extension = '.' + old_extension
    if not new_extension.startswith('.'):
        new_extension = '.' + new_extension

    lines.append({"text": f"🔄 משנה סיומות קבצים מ-'*{old_extension}' ל-'*{new_extension}' בתיקייה הנוכחית...", "type": "sys-out"})

    try:
        current_dir = os.getcwd()
        changed_count = 0
        for filename in os.listdir(current_dir):
            if filename.endswith(old_extension):
                old_path = os.path.join(current_dir, filename)
                new_filename = filename[:-len(old_extension)] + new_extension
                new_path = os.path.join(current_dir, new_filename)
                
                os.rename(old_path, new_path)
                lines.append({"text": f"  ✅ שינה '{filename}' ל-'{new_filename}'", "type": ""})
                changed_count += 1
        
        if changed_count > 0:
            lines.append({"text": f"✅ הושלם שינוי סיומות עבור {changed_count} קבצים.", "type": "success"})
        else:
            lines.append({"text": f"ℹ️ לא נמצאו קבצים עם הסיומת '{old_extension}' לשינוי.", "type": "sys-out"})

    except PermissionError:
        lines.append({"text": "❌ אין הרשאה לשנות שמות קבצים בתיקייה הנוכחית.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
