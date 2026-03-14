import random

def execute(args):
    lines = []
    
    lines.append({"text": "🎨 יוצר קוד צבע הקסדצימלי אקראי...", "type": "sys-out"})

    # Generate 6 random hex characters
    random_color_code = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
    
    lines.append({"text": f"✅ קוד הצבע שנוצר: '{random_color_code}'", "type": "success"})
    
    return {"lines": lines}
