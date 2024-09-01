import time
from datetime import datetime, timedelta

log_file_path = 'systems.log'
keywords = ["ERROR", "FAIL"]

def parse_timestamp(line):
    try:
        timestamp_str = ' '.join(line.split(' ')[0:3])
        log_time = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')
        log_time = log_time.replace(year=datetime.now().year)
        return log_time
    except ValueError:
        return None

def is_within_time_window(log_time, time_window):
    return log_time >= datetime.now() - time_window

def contains_keywords(line, keywords):
    return any(keyword in line for keyword in keywords)

def monitor_log_file(log_file):
    time_window = timedelta(minutes=10)
    recent_logs = []

    with open(log_file, 'r') as file:
        file.seek(0, 2)
        
        while True:
            line = file.readline()
            if not line:
                time.sleep(1)
                continue

            line = line.strip()
            if not line:
                continue

            log_time = parse_timestamp(line)
            if not log_time:
                continue

            recent_logs = clean_old_logs(recent_logs, time_window)
            recent_logs.append({'time': log_time, 'line': line})

            if contains_keywords(line, keywords) and is_within_time_window(log_time, time_window):
                print("ALERT: Error detected in the logs!")

def clean_old_logs(recent_logs, time_window):
    return [log for log in recent_logs if log['time'] >= datetime.now() - time_window]

if __name__ == "__main__":
    monitor_log_file(log_file_path)
