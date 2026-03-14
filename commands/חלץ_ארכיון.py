import shutil
import os

def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב לקובץ ארכיון (zip) ונתיב לתיקיית יעד.", "type": "error"})
        lines.append({"text": "דוגמה: חלץ_ארכיון my_archive.zip my_extract_folder", "type": "sys-out"})
        return {"lines": lines}

    archive_path = args[0]
    extract_path = args[1]
    
    if not os.path.exists(archive_path):
        lines.append({"text": f"❌ שגיאה: קובץ הארכיון '{archive_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isfile(archive_path):
        lines.append({"text": f"❌ שגיאה: '{archive_path}' אינו קובץ ארכיון.", "type": "error"})
        return {"lines": lines}
    if not archive_path.lower().endswith(".zip"):
        lines.append({"text": f"❌ שגיאה: '{archive_path}' אינו קובץ ZIP. פקודה זו תומכת רק בקבצי ZIP.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"📂 מחלץ את הארכיון '{archive_path}' לתוך '{extract_path}'...", "type": "sys-out"})

    try:
        # Create destination directory if it doesn't exist
        os.makedirs(extract_path, exist_ok=True)
        shutil.unpack_archive(archive_path, extract_path)
        lines.append({"text": f"✅ הארכיון נחלץ בהצלחה ל-'{extract_path}'.", "type": "success"})
    except shutil.ReadError:
        lines.append({"text": f"❌ שגיאה: קובץ הארכיון '{archive_path}' פגום או לא נתמך.", "type": "error"})
    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה לגשת לקובץ הארכיון או לכתוב לתיקיית היעד.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
