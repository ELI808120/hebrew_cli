import os

def execute(args):
    files = [f[:-3] for f in os.listdir('commands') if f.endswith('.py') and not f.startswith('__')]
    files.sort() # סידור אלפביתי
    
    lines = [{"text": "📚 רשימת הפקודות הזמינות במערכת:", "type": "success"}, {"text": "", "type": ""}]
    
    # סידור הפקודות ב"עמודות" כדי לחסוך מקום במסך
    chunked = [files[i:i+4] for i in range(0, len(files), 4)]
    for chunk in chunked:
        row = "  |  ".join(chunk)
        lines.append({"text": row, "type": "sys-out"})
        
    lines.append({"text": "", "type": ""})
    lines.append({"text": f"✅ סך הכל פקודות מותקנות: {len(files)}", "type": "success"})
    lines.append({"text": "💡 טיפ: נסה להריץ אחת מהפקודות כדי לראות מה היא עושה!", "type": "success"})
    
    return {"lines": lines}