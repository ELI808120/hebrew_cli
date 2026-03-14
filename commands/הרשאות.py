import os
import datetime
import stat # For parsing stat.st_mode on Unix-like systems, though primarily focusing on Windows access checks here

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב לקובץ או לתיקייה.", "type": "error"})
        lines.append({"text": "דוגמה: הרשאות my_file.txt", "type": "sys-out"})
        return {"lines": lines}

    path = args[0]

    if not os.path.exists(path):
        lines.append({"text": f"❌ שגיאה: הנתיב '{path}' לא נמצא.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"🔐 מציג מידע על הרשאות עבור '{path}'...", "type": "sys-out"})

    try:
        file_stat = os.stat(path)
        
        lines.append({"text": "--- מידע כללי ---", "type": "success"})
        lines.append({"text": f"  שם: {os.path.basename(path)}", "type": ""})
        lines.append({"text": f"  סוג: {'תיקייה' if os.path.isdir(path) else 'קובץ'}", "type": ""})
        lines.append({"text": f"  גודל: {file_stat.st_size} בתים", "type": ""})
        lines.append({"text": f"  תאריך שינוי אחרון: {datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}", "type": ""})
        lines.append({"text": f"  תאריך יצירה: {datetime.datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}", "type": ""})

        lines.append({"text": "--- הרשאות משתמש נוכחי ---", "type": "success"})
        
        can_read = os.access(path, os.R_OK)
        can_write = os.access(path, os.W_OK)
        can_execute = os.access(path, os.X_OK)

        lines.append({"text": f"  קריאה: {'✅ כן' if can_read else '❌ לא'}", "type": ""})
        lines.append({"text": f"  כתיבה: {'✅ כן' if can_write else '❌ לא'}", "type": ""})
        lines.append({"text": f"  ביצוע: {'✅ כן' if can_execute else '❌ לא'}", "type": ""})

        if os.name == 'posix': # Unix-like systems, can show numeric/rwx permissions
            mode = file_stat.st_mode
            lines.append({"text": "--- הרשאות POSIX (קבועות) ---", "type": "sys-out"})
            lines.append({"text": f"  מספרים (octal): {oct(mode)[-3:]}", "type": ""})
            lines.append({"text": f"  מחרוזת (rwx): {stat.filemode(mode)}", "type": ""})
        else: # Windows
            lines.append({"text": "--- הערה (Windows) ---", "type": "sys-out"})
            lines.append({"text": "  במערכות Windows, הרשאות מפורטות (ACLs) מורכבות יותר.", "type": "sys-out"})
            lines.append({"text": "  המידע הנ"ל מתייחס ליכולת הגישה של המשתמש הנוכחי בלבד.", "type": "sys-out"})
        
        lines.append({"text": "✅ הצגת מידע הרשאות הושלמה.", "type": "success"})

    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה לגשת למידע על הנתיב '{path}'.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאה בלתי צפויה בעת בדיקת הרשאות: {e}", "type": "error"})
    
    return {"lines": lines}
