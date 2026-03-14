import datetime
def execute(args):
    return {"lines": [{"text": f"התאריך היום: {datetime.date.today().strftime('%d/%m/%Y')}", "type": "success"}]}