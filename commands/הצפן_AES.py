def execute(args):
    lines = []
    
    lines.append({"text": "❌ שגיאה: פקודת הצפנת AES דורשת את הספרייה החיצונית 'pycryptodome'.", "type": "error"})
    lines.append({"text": "  התקנה: pip install pycryptodome", "type": "sys-out"})
    lines.append({"text": "  לאחר ההתקנה, יהיה ניתן להוסיף את פונקציונליות ההצפנה/פענוח.", "type": "sys-out"})
    lines.append({"text": "  בשל מגבלות ספריות סטנדרטיות, לא ניתן ליישם הצפנה מאובטחת ללא ספרייה זו.", "type": "sys-out"})
    
    return {"lines": lines}
