import random
import string

def execute(args):
    lines = []
    
    length = 12 # Default password length
    if args:
        try:
            length = int(args[0])
            if length <= 0:
                lines.append({"text": "❌ שגיאה: אורך הסיסמה חייב להיות מספר חיובי.", "type": "error"})
                return {"lines": lines}
        except ValueError:
            lines.append({"text": "❌ שגיאה: אורך הסיסמה חייב להיות מספר שלם.", "type": "error"})
            lines.append({"text": "דוגמה: צור_סיסמה 16", "type": "sys-out"})
            return {"lines": lines}

    lines.append({"text": f"🔑 יוצר סיסמה באורך {length} תווים...", "type": "sys-out"})

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))

    lines.append({"text": f"✅ הסיסמה שנוצרה: '{password}'", "type": "success"})
    lines.append({"text": "⚠️ אנא שמור את הסיסמה במקום בטוח ואל תשתף אותה.", "type": "sys-out"})
    
    return {"lines": lines}
