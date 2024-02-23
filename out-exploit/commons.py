from datetime import datetime

def get_current_datetime():
    current_time = datetime.now()
    formated_time = current_time.strftime("[%d-%m-%Y %H:%M]")
    return formated_time