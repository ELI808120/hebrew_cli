import subprocess
import platform

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        return {"lines": lines}

    username = None
    if args:
        username = args[0]

    lines.append({"text": f"👤 מאחזר מידע על פרופיל המשתמש {username if username else '(נוכחי)'}...", "type": "sys-out"})

    try:
        command_args = ["wmic", "useraccount", "get", "Name,SID,Disabled,Status,FullName,Description,LocalAccount,Lockout,PasswordExpires,PasswordChangeable", "/value"]
        if username:
            command_args.insert(2, "where")
            command_args.insert(3, f"Name='{username}'")

        process = subprocess.run(command_args, capture_output=True, text=True, check=True, encoding='utf-8')
        output = process.stdout.strip()

        user_info = {}
        for line in output.splitlines():
            line = line.strip()
            if "=" in line:
                key, value = line.split("=", 1)
                user_info[key.strip()] = value.strip()
        
        if user_info and user_info.get("Name"):
            lines.append({"text": "--- פרטי פרופיל משתמש ---", "type": "success"})
            lines.append({"text": f"  שם משתמש: {user_info.get('Name', 'N/A')}", "type": ""})
            lines.append({"text": f"  שם מלא: {user_info.get('FullName', 'N/A')}", "type": ""})
            lines.append({"text": f"  תיאור: {user_info.get('Description', 'N/A')}", "type": ""})
            lines.append({"text": f"  SID: {user_info.get('SID', 'N/A')}", "type": ""})
            lines.append({"text": f"  חשבון מקומי: {'כן' if user_info.get('LocalAccount') == 'TRUE' else 'לא'}", "type": ""})
            lines.append({"text": f"  מושבת: {'כן' if user_info.get('Disabled') == 'TRUE' else 'לא'}", "type": ""})
            lines.append({"text": f"  נעול: {'כן' if user_info.get('Lockout') == 'TRUE' else 'לא'}", "type": ""})
            lines.append({"text": f"  הסיסמה תפוג: {'כן' if user_info.get('PasswordExpires') == 'TRUE' else 'לא'}", "type": ""})
            lines.append({"text": f"  הסיסמה ניתנת לשינוי: {'כן' if user_info.get('PasswordChangeable') == 'TRUE' else 'לא'}", "type": ""})
            lines.append({"text": f"  סטטוס: {user_info.get('Status', 'N/A')}", "type": ""})
            lines.append({"text": "✅ אחזור פרטי פרופיל משתמש הושלם.", "type": "success"})
        else:
            lines.append({"text": f"⚠️ לא נמצא מידע עבור פרופיל המשתמש '{username}'.", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'wmic' לא נמצאה. ודא שהיא קיימת בנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        if "No Instance(s) Available." in cpe.stderr:
            lines.append({"text": f"⚠️ לא נמצא משתמש בשם '{username}'.", "type": "sys-out"})
        else:
            lines.append({"text": f"❌ שגיאה בהפעלת WMIC: {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
