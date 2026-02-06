#!/usr/bin/env python3
"""
Test suite for HK Smart Factory modules
"""

import unittest
import json
import os
from pathlib import Path
import sys

# Import modules to test
from factory_monitor import LineStation, ProductionLine
from production_logger import ProductionLogger, load_config


class TestLineStation(unittest.TestCase):
    """Tests for LineStation class"""
    
    def test_station_creation(self):
        """Test creating a station"""
        station = LineStation(1, 5)
        self.assertEqual(station.num, 1)
        self.assertEqual(station.cycle, 5)
        self.assertEqual(station.units_made, 0)
        self.assertTrue(station.running)
    
    def test_work_cycle(self):
        """Test work cycle increments units"""
        station = LineStation(1, 5)
        result = station.work_cycle()
        self.assertTrue(result)
        self.assertEqual(station.units_made, 1)
    
    def test_work_cycle_stopped(self):
        """Test work cycle when stopped"""
        station = LineStation(1, 5)
        station.running = False
        result = station.work_cycle()
        self.assertFalse(result)
        self.assertEqual(station.units_made, 0)
    
    def test_report_generation(self):
        """Test report string generation"""
        station = LineStation(1, 5)
        station.work_cycle()
        report = station.report()
        self.assertIn("Station 1", report)
        self.assertIn("1 units", report)


class TestProductionLine(unittest.TestCase):
    """Tests for ProductionLine class"""
    
    def test_line_creation(self):
        """Test creating a production line"""
        line = ProductionLine("Test Line")
        self.assertEqual(line.name, "Test Line")
        self.assertEqual(len(line.stations), 0)
    
    def test_add_station(self):
        """Test adding stations to line"""
        line = ProductionLine("Test Line")
        station = line.add_station(3)
        self.assertEqual(len(line.stations), 1)
        self.assertEqual(station.num, 1)
        self.assertEqual(station.cycle, 3)
    
    def test_multiple_stations(self):
        """Test adding multiple stations"""
        line = ProductionLine("Test Line")
        line.add_station(2)
        line.add_station(4)
        line.add_station(3)
        self.assertEqual(len(line.stations), 3)
        self.assertEqual(line.stations[0].num, 1)
        self.assertEqual(line.stations[2].num, 3)


class TestProductionLogger(unittest.TestCase):
    """Tests for ProductionLogger class"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path("test_production_data")
        self.logger = ProductionLogger(str(self.test_dir))
    
    def tearDown(self):
        """Clean up test files"""
        if self.test_dir.exists():
            for file in self.test_dir.glob("*.json"):
                file.unlink()
            self.test_dir.rmdir()
    
    def test_logger_creation(self):
        """Test logger directory creation"""
        self.assertTrue(self.test_dir.exists())
    
    def test_log_event(self):
        """Test logging an event"""
        self.logger.log_event("test_event", {"value": 123})
        self.assertEqual(len(self.logger.current_log), 1)
        self.assertEqual(self.logger.current_log[0]["event"], "test_event")
    
    def test_save_report(self):
        """Test saving shift report"""
        self.logger.log_event("start", {"line": "A"})
        summary = {"units": 100}
        filename = self.logger.save_shift_report("test", summary)
        
        self.assertTrue(filename.exists())
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(data["line"], "test")
        self.assertEqual(data["summary"]["units"], 100)
        self.assertEqual(len(data["events"]), 1)


class TestConfigLoader(unittest.TestCase):
    """Tests for configuration loading"""
    
    def test_load_existing_config(self):
        """Test loading hk_factory.conf"""
        config = load_config("hk_factory.conf")
        self.assertIn("factory", config)
        self.assertIn("line_a", config)
    
    def test_load_missing_config(self):
        """Test loading non-existent config"""
        config = load_config("nonexistent.conf")
        self.assertEqual(config, {})


def run_tests():
    """Run all tests"""
    print("="*60)
    print("HK Smart Factory - Test Suite")
    print("="*60)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestLineStation))
    suite.addTests(loader.loadTestsFromTestCase(TestProductionLine))
    suite.addTests(loader.loadTestsFromTestCase(TestProductionLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigLoader))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("="*60)
    if result.wasSuccessful():
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("="*60)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
