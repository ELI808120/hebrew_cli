import os
import shutil
import platform

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": "🗑️ מנקה את התיקייה הזמנית של המשתמש...", "type": "sys-out"})

    temp_dir = os.getenv('TEMP') or os.getenv('TMP')
    if not temp_dir or not os.path.isdir(temp_dir):
        lines.append({"text": "❌ שגיאה: לא ניתן לאתר את התיקייה הזמנית.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"  תיקייה זמנית: {temp_dir}", "type": "sys-out"})
    
    cleaned_count = 0
    cleaned_size_bytes = 0

    try:
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            try:
                if os.path.isfile(item_path):
                    cleaned_size_bytes += os.path.getsize(item_path)
                    os.remove(item_path)
                    cleaned_count += 1
                    # lines.append({"text": f"    ✅ נמחק קובץ: {item}", "type": ""}) # Too verbose
                elif os.path.isdir(item_path):
                    # For directories, get size recursively if possible before deleting
                    dir_size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(item_path) for filename in filenames)
                    cleaned_size_bytes += dir_size
                    shutil.rmtree(item_path)
                    cleaned_count += 1
                    # lines.append({"text": f"    ✅ נמחקה תיקייה: {item}", "type": ""}) # Too verbose
            except PermissionError:
                lines.append({"text": f"  ⚠️ אין הרשאה למחוק את '{item_path}'. מדלג.", "type": "sys-out"})
            except Exception as e:
                lines.append({"text": f"  ❌ שגיאה במחיקת '{item_path}': {e}. מדלג.", "type": "error"})
        
        cleaned_size_mb = cleaned_size_bytes / (1024 * 1024)

        lines.append({"text": "--- ניקוי תיקייה זמנית הושלם ---", "type": "success"})
        lines.append({"text": f"  ✅ נמחקו {cleaned_count} פריטים.", "type": ""})
        lines.append({"text": f"  ✅ שוחרר שטח של {cleaned_size_mb:.2f} MB.", "type": ""})
        lines.append({"text": "⚠️ הערה: סל המיחזור אינו מנוקה על ידי פקודה זו.", "type": "sys-out"})

    except PermissionError:
        lines.append({"text": "❌ אין הרשאה לגשת לתיקייה הזמנית.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
