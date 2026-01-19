from datetime import datetime
import json
import os

LOG_FILE = 'logs/requests.log'

def log_request(endpoint, method, ip_address, user_agent, status_code, response_time=None, error=None):
    """Log API request details"""
    
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'endpoint': endpoint,
        'method': method,
        'ip_address': ip_address,
        'user_agent': user_agent,
        'status_code': status_code,
        'response_time_ms': response_time,
        'error': error
    }
    
    # Create logs directory if doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Write to log file
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def get_request_stats():
    """Get statistics from request logs"""
    
    if not os.path.exists(LOG_FILE):
        return {
            'total_requests': 0,
            'success_rate': 0,
            'avg_response_time': 0
        }
    
    total = 0
    successful = 0
    response_times = []
    
    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                total += 1
                
                if entry['status_code'] == 200:
                    successful += 1
                
                if entry['response_time_ms']:
                    response_times.append(entry['response_time_ms'])
            except:
                continue
    
    avg_time = sum(response_times) / len(response_times) if response_times else 0
    success_rate = (successful / total * 100) if total > 0 else 0
    
    return {
        'total_requests': total,
        'successful_requests': successful,
        'success_rate': round(success_rate, 2),
        'avg_response_time_ms': round(avg_time, 2)
    }