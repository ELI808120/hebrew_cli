import math

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק סיסמה לניתוח.", "type": "error"})
        lines.append({"text": "דוגמה: חוזק_סיסמה MyStrongP@ssw0rd", "type": "sys-out"})
        return {"lines": lines}

    password = " ".join(args)
    
    lines.append({"text": f"🛡️ מנתח את חוזק הסיסמה...", "type": "sys-out"})

    length = len(password)
    
    # Character set analysis
    has_lowercase = any(c.islower() for c in password)
    has_uppercase = any(c.isupper() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_symbols = any(not c.isalnum() for c in password)

    # Estimate character pool size (bit length of character set)
    char_pool_size = 0
    if has_lowercase:
        char_pool_size += 26 # a-z
    if has_uppercase:
        char_pool_size += 26 # A-Z
    if has_digits:
        char_pool_size += 10 # 0-9
    if has_symbols:
        char_pool_size += 32 # Common symbols like !@#$%^&*()_+-=[]{}|;':",./<>?`~

    # Entropy calculation (in bits)
    entropy = 0
    if char_pool_size > 0:
        entropy = length * math.log2(char_pool_size)

    # Strength assessment
    strength = "חלשה מאוד"
    if length >= 8 and entropy >= 60 and (has_lowercase + has_uppercase + has_digits + has_symbols >= 3):
        strength = "טובה"
    if length >= 12 and entropy >= 80 and (has_lowercase + has_uppercase + has_digits + has_symbols >= 4):
        strength = "חזקה"
    if length >= 16 and entropy >= 100 and (has_lowercase + has_uppercase + has_digits + has_symbols >= 4):
        strength = "חזקה מאוד"
    elif length >= 6:
        strength = "בינונית"
    elif length < 6:
        strength = "חלשה מאוד"

    lines.append({"text": "--- ניתוח חוזק סיסמה ---", "type": "success"})
    lines.append({"text": f"  אורך: {length}", "type": ""})
    lines.append({"text": f"  אותיות קטנות: {'✅ כן' if has_lowercase else '❌ לא'}", "type": ""})
    lines.append({"text": f"  אותיות גדולות: {'✅ כן' if has_uppercase else '❌ לא'}", "type": ""})
    lines.append({"text": f"  ספרות: {'✅ כן' if has_digits else '❌ לא'}", "type": ""})
    lines.append({"text": f"  סימנים מיוחדים: {'✅ כן' if has_symbols else '❌ לא'}", "type": ""})
    lines.append({"text": f"  גודל מאגר תווים משוער: {char_pool_size}", "type": ""})
    lines.append({"text": f"  אנטרופיה (ביטים): {entropy:.2f}", "type": ""})
    lines.append({"text": f"  חוזק הסיסמה: {strength}", "type": "success"})
    lines.append({"text": "✅ ניתוח חוזק סיסמה הושלם.", "type": "success"})

    return {"lines": lines}
