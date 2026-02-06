#!/usr/bin/env python3
"""
Production data logger for HK Smart Factory
Saves production metrics to files
"""

import json
from datetime import datetime
from pathlib import Path


class ProductionLogger:
    """Handles saving production data"""
    
    def __init__(self, output_dir="production_data"):
        self.dir = Path(output_dir)
        self.dir.mkdir(exist_ok=True)
        self.current_log = []
    
    def log_event(self, event_type, data):
        """Record a production event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "data": data
        }
        self.current_log.append(entry)
    
    def save_shift_report(self, line_name, summary_data):
        """Save end-of-shift report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.dir / f"shift_report_{line_name}_{timestamp}.json"
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "line": line_name,
            "summary": summary_data,
            "events": self.current_log
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved: {filename}")
        self.current_log = []
        return filename


def load_config(config_file="hk_factory.conf"):
    """Parse factory configuration file"""
    config = {}
    current_section = None
    
    try:
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                
                if not line or line.startswith('#'):
                    continue
                
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    config[current_section] = {}
                elif '=' in line and current_section:
                    key, value = line.split('=', 1)
                    config[current_section][key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Config file {config_file} not found, using defaults")
    
    return config


if __name__ == "__main__":
    # Test logger
    logger = ProductionLogger()
    logger.log_event("shift_start", {"line": "A", "operator": "test"})
    logger.log_event("production", {"units": 100})
    
    summary = {
        "total_units": 100,
        "shift_hours": 8,
        "efficiency": 0.95
    }
    
    logger.save_shift_report("test_line", summary)
    print("Logger test completed")
