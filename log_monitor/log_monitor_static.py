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

def process_log_file(log_file):
    time_window = timedelta(minutes=10)
    alert_triggered = False

    with open(log_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            log_time = parse_timestamp(line)
            if not log_time or not is_within_time_window(log_time, time_window):
                continue

            if contains_keywords(line, keywords):
                print("ALERT: Error detected in the logs!")
                alert_triggered = True

    if not alert_triggered:
        print("No errors found in the last 10 minutes.")

if __name__ == "__main__":
    process_log_file(log_file_path)
