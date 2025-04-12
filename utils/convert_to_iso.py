from datetime import datetime
import pytz

uzbekistan_tz = pytz.timezone('Asia/Tashkent')

def convert_to_iso(date_str):
    try:
        if ':' in date_str and '.' in date_str:
            dt = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        elif ':' in date_str:
            today = datetime.now(uzbekistan_tz)
            dt = datetime.strptime(date_str, "%H:%M")
            dt = dt.replace(year=today.year, month=today.month, day=today.day)
        else:
            raise ValueError("Unknown date format")
        
        dt = uzbekistan_tz.localize(dt)
        dt_utc = dt.astimezone(pytz.utc)
        return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    except Exception as e:
        return f"Error: {e}"
    
if __name__ == "__main__":
    print(convert_to_iso("20.04.2025 20:30"))
    print(convert_to_iso("20:15"))
