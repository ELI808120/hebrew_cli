import os
import datetime
import stat # For file mode constants

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב לקובץ כדי להציג את פרטיו.", "type": "error"})
        lines.append({"text": "דוגמה: פרטי_קובץ my_document.txt", "type": "sys-out"})
        return {"lines": lines}

    file_path = args[0]

    if not os.path.exists(file_path):
        lines.append({"text": f"❌ שגיאה: הקובץ '{file_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isfile(file_path):
        lines.append({"text": f"❌ שגיאה: '{file_path}' אינו קובץ. פקודה זו מיועדת לקבצים בלבד.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"📄 מאחזר פרטים עבור הקובץ '{file_path}'...", "type": "sys-out"})

    try:
        file_stat = os.stat(file_path)
        
        file_size_bytes = file_stat.st_size
        file_size_mb = file_size_bytes / (1024 * 1024)

        # Creation time (Windows) / Last metadata change time (Unix)
        creation_time = datetime.datetime.fromtimestamp(file_stat.st_ctime)
        # Last modification time
        modification_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)
        # Last access time
        access_time = datetime.datetime.fromtimestamp(file_stat.st_atime)

        # Read-only status
        # On Windows, os.access(file_path, os.W_OK) is more reliable for writability
        # On Unix, check the write bit in st_mode
        is_read_only = not os.access(file_path, os.W_OK)


        lines.append({"text": "--- פרטי קובץ ---", "type": "success"})
        lines.append({"text": f"  שם הקובץ: {os.path.basename(file_path)}", "type": ""})
        lines.append({"text": f"  גודל: {file_size_bytes} בתים ({file_size_mb:.2f} MB)", "type": ""})
        lines.append({"text": f"  תאריך יצירה/שינוי מטא-דאטה: {creation_time.strftime('%Y-%m-%d %H:%M:%S')}", "type": ""})
        lines.append({"text": f"  תאריך שינוי אחרון: {modification_time.strftime('%Y-%m-%d %H:%M:%S')}", "type": ""})
        lines.append({"text": f"  תאריך גישה אחרון: {access_time.strftime('%Y-%m-%d %H:%M:%S')}", "type": ""})
        lines.append({"text": f"  קריאה בלבד: {'✅ כן' if is_read_only else '❌ לא'}", "type": ""})
        lines.append({"text": "✅ אחזור פרטי קובץ הושלם.", "type": "success"})

    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה לגשת למידע על הקובץ '{file_path}'.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
