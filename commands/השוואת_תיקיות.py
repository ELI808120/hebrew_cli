import filecmp
import os

def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק נתיבים לשתי תיקיות להשוואה.", "type": "error"})
        lines.append({"text": "דוגמה: השוואת_תיקיות folder1 folder2", "type": "sys-out"})
        return {"lines": lines}

    dir1 = args[0]
    dir2 = args[1]

    if not os.path.exists(dir1) or not os.path.isdir(dir1):
        lines.append({"text": f"❌ שגיאה: התיקייה הראשונה '{dir1}' לא נמצאה או אינה תיקייה.", "type": "error"})
        return {"lines": lines}
    if not os.path.exists(dir2) or not os.path.isdir(dir2):
        lines.append({"text": f"❌ שגיאה: התיקייה השנייה '{dir2}' לא נמצאה או אינה תיקייה.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"🆚 משווה בין התיקיות '{dir1}' ו-'{dir2}'...", "type": "sys-out"})

    try:
        dc = filecmp.dircmp(dir1, dir2)

        if dc.left_only:
            lines.append({"text": "--- קבצים/תיקיות ייחודיים בתיקייה הראשונה ---", "type": "sys-out"})
            for item in dc.left_only:
                lines.append({"text": f"  + {os.path.join(dir1, item)}", "type": ""})
        
        if dc.right_only:
            lines.append({"text": "--- קבצים/תיקיות ייחודיים בתיקייה השנייה ---", "type": "sys-out"})
            for item in dc.right_only:
                lines.append({"text": f"  - {os.path.join(dir2, item)}", "type": ""})

        if dc.diff_files:
            lines.append({"text": "--- קבצים שונים בשתי התיקיות ---", "type": "sys-out"})
            for item in dc.diff_files:
                lines.append({"text": f'  ≠ {os.path.join(dir1, item)} (שונה מ-{os.path.join(dir2, item)})', "type": ""})
        
        if dc.common_funny:
            lines.append({"text": "--- קבצים/תיקיות נפוצים עם שגיאות ---", "type": "sys-out"})
            for item in dc.common_funny:
                lines.append({"text": f"  ? {item}", "type": ""})

        if not dc.left_only and not dc.right_only and not dc.diff_files and not dc.common_funny:
            lines.append({"text": "✅ התיקיות זהות.", "type": "success"})
        else:
            lines.append({"text": "✅ השוואת תיקיות הושלמה. נמצאו הבדלים.", "type": "success"})

    except PermissionError:
        lines.append({"text": "❌ אין הרשאה לגשת לאחת מהתיקיות.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
