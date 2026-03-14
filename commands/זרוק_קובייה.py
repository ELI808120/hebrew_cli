import random

def execute(args):
    lines = []
    
    num_dice = 1
    num_sides = 6 # Default to one 6-sided die

    if args:
        try:
            if "d" in args[0].lower(): # e.g., 2d6
                parts = args[0].lower().split("d")
                if parts[0]:
                    num_dice = int(parts[0])
                else: # "d6" implies 1 die
                    num_dice = 1
                num_sides = int(parts[1])
            else: # Just a number, assume number of sides for one die
                num_sides = int(args[0])
        except ValueError:
            lines.append({"text": "❌ שגיאה: פורמט קוביה לא חוקי. השתמש במספר (לדוגמה 6) או XdY (לדוגמה 2d6).", "type": "error"})
            return {"lines": lines}

    if num_dice <= 0 or num_sides <= 0:
        lines.append({"text": "❌ שגיאה: מספר קוביות ופאות חייבים להיות חיוביים.", "type": "error"})
        return {"lines": lines}
    
    lines.append({"text": f"🎲 זורק {num_dice} קוביות בעלות {num_sides} פאות כל אחת...", "type": "sys-out"})

    results = []
    total = 0
    for _ in range(num_dice):
        roll = random.randint(1, num_sides)
        results.append(str(roll))
        total += roll
    
    if num_dice > 1:
        lines.append({"text": f"✅ תוצאות: {', '.join(results)}. סך הכל: {total}", "type": "success"})
    else:
        lines.append({"text": f"✅ התוצאה: {results[0]}", "type": "success"})
    
    return {"lines": lines}
