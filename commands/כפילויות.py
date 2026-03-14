import os
import hashlib

def execute(args):
    lines = []
    
    search_path = "." # Default to current directory
    if args:
        search_path = args[0]
        if not os.path.exists(search_path):
            lines.append({"text": f"❌ שגיאה: נתיב החיפוש '{search_path}' לא נמצא.", "type": "error"})
            return {"lines": lines}
        if not os.path.isdir(search_path):
            lines.append({"text": f"❌ שגיאה: '{search_path}' אינו תיקייה. יש לספק תיקייה לחיפוש.", "type": "error"})
            return {"lines": lines}

    lines.append({"text": f"🔎 סורק את '{search_path}' עבור קבצים כפולים...", "type": "sys-out"})

    duplicates = {}
    try:
        for dirpath, _, filenames in os.walk(search_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    # Calculate SHA256 hash for file content
                    hasher = hashlib.sha256()
                    with open(file_path, 'rb') as f:
                        while chunk := f.read(4096):
                            hasher.update(chunk)
                    file_hash = hasher.hexdigest()

                    if file_hash in duplicates:
                        duplicates[file_hash].append(file_path)
                    else:
                        duplicates[file_hash] = [file_path]
                except PermissionError:
                    lines.append({"text": f"⚠️ אין הרשאה לקרוא את הקובץ '{file_path}'. מדלג.", "type": "sys-out"})
                except Exception as e:
                    lines.append({"text": f"❌ שגיאה בקריאת הקובץ '{file_path}': {e}. מדלג.", "type": "error"})
        
        found_duplicates = False
        lines.append({"text": "--- קבצים כפולים שנמצאו ---", "type": "success"})
        for file_hash, file_list in duplicates.items():
            if len(file_list) > 1:
                found_duplicates = True
                lines.append({"text": f"  Checksum (SHA256): {file_hash}", "type": ""})
                for f_path in file_list:
                    lines.append({"text": f"    - {f_path}", "type": ""})
                lines.append({"text": "", "type": ""}) # Empty line for separation
        
        if not found_duplicates:
            lines.append({"text": "ℹ️ לא נמצאו קבצים כפולים.", "type": "sys-out"})
        else:
            lines.append({"text": "✅ סריקת כפילויות הושלמה.", "type": "success"})

    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה לגשת לנתיב '{search_path}' או לתתי התיקיות שבו.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
