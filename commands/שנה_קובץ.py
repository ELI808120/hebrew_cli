import os

def execute(args):
    lines = []
    
    if len(args) < 3:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב לתיקייה, מחרוזת לחיפוש ומחרוזת להחלפה.", "type": "error"})
        lines.append({"text": "דוגמה: שנה_קובץ . 'old_text' 'new_text'", "type": "sys-out"})
        return {"lines": lines}

    target_dir = args[0]
    search_str = args[1]
    replace_str = args[2]

    if not os.path.exists(target_dir):
        lines.append({"text": f"❌ שגיאה: התיקייה '{target_dir}' לא נמצאה.", "type": "error"})
        return {"lines": lines}
    if not os.path.isdir(target_dir):
        lines.append({"text": f"❌ שגיאה: '{target_dir}' אינו תיקייה. יש לספק תיקייה.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"🔄 משנה שמות קבצים בתיקייה '{target_dir}', מחפש '{search_str}' ומחליף ב-'{replace_str}'...", "type": "sys-out"})

    renamed_count = 0
    try:
        for filename in os.listdir(target_dir):
            if search_str in filename:
                old_path = os.path.join(target_dir, filename)
                new_filename = filename.replace(search_str, replace_str)
                new_path = os.path.join(target_dir, new_filename)
                
                if old_path != new_path: # Only rename if there's an actual change
                    os.rename(old_path, new_path)
                    lines.append({"text": f"  ✅ שינה '{filename}' ל-'{new_filename}'", "type": ""})
                    renamed_count += 1
        
        if renamed_count > 0:
            lines.append({"text": f"✅ הושלם שינוי שמות עבור {renamed_count} קבצים.", "type": "success"})
        else:
            lines.append({"text": "ℹ️ לא נמצאו קבצים לשינוי שם התואמים לתבנית.", "type": "sys-out"})

    except PermissionError:
        lines.append({"text": "❌ אין הרשאה לשנות שמות קבצים בתיקייה זו.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
