#!/usr/bin/env python3
"""
HK Smart Factory Monitor
Minimal production line tracking system
"""

import time
from datetime import datetime


class LineStation:
    """Represents a single workstation on production line"""
    
    def __init__(self, station_num, cycle_time_sec):
        self.num = station_num
        self.cycle = cycle_time_sec
        self.units_made = 0
        self.running = True
        self.last_check = datetime.now()
    
    def work_cycle(self):
        """Simulate one work cycle"""
        if self.running:
            self.units_made += 1
            self.last_check = datetime.now()
            return True
        return False
    
    def report(self):
        """Generate station status report"""
        status_mark = "✓" if self.running else "✗"
        return f"Station {self.num} [{status_mark}]: {self.units_made} units | Cycle: {self.cycle}s"


class ProductionLine:
    """Manages multiple stations"""
    
    def __init__(self, name):
        self.name = name
        self.stations = []
        self.shift_start = datetime.now()
    
    def add_station(self, cycle_time):
        """Add new workstation"""
        station = LineStation(len(self.stations) + 1, cycle_time)
        self.stations.append(station)
        return station
    
    def run_shift(self, duration_min):
        """Run production for specified duration"""
        print(f"\n{'='*60}")
        print(f"HK SMART FACTORY - {self.name}")
        print(f"Shift started: {self.shift_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        end_time = time.time() + (duration_min * 60)
        
        while time.time() < end_time:
            for st in self.stations:
                st.work_cycle()
            
            # Show status every 5 seconds
            print(f"\r[{datetime.now().strftime('%H:%M:%S')}] Running...", end='', flush=True)
            time.sleep(1)
        
        print("\n")
        self.print_summary()
    
    def print_summary(self):
        """Print production summary"""
        print(f"\n{'='*60}")
        print("SHIFT SUMMARY")
        print(f"{'='*60}")
        
        total_output = 0
        for st in self.stations:
            print(st.report())
            total_output += st.units_made
        
        print(f"\nTotal Line Output: {total_output} units")
        
        runtime = (datetime.now() - self.shift_start).total_seconds()
        rate = (total_output / runtime) * 3600 if runtime > 0 else 0
        print(f"Production Rate: {rate:.1f} units/hour")
        print(f"{'='*60}\n")


def main():
    """Entry point"""
    line = ProductionLine("Assembly Line A")
    
    # Configure stations with different cycle times
    line.add_station(2)  # Fast station
    line.add_station(3)  # Medium station  
    line.add_station(2)  # Fast station
    
    print("\nStarting HK Smart Factory Monitor...")
    print("Press Ctrl+C to stop early\n")
    
    try:
        line.run_shift(0.1)  # Run for 6 seconds (0.1 min) for demo
    except KeyboardInterrupt:
        print("\n\nShift ended by operator")
        line.print_summary()


if __name__ == "__main__":
    main()
