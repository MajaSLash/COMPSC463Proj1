import unittest
from datetime import datetime, timedelta
import numpy as np
from algorithm import FinancialAnalyzer, FinancialDataPoint, AnomalyReport

class TestFinancialAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.analyzer = FinancialAnalyzer()
        
        # Create sample data for testing
        base_date = datetime(2024, 1, 1)
        self.sample_timestamps = [base_date + timedelta(days=i) for i in range(10)]
        self.sample_prices = [100.0, 102.0, 101.0, 103.0, 102.5, 104.0, 103.5, 105.0, 106.0, 107.0]
        self.sample_volumes = [1000.0, 1100.0, 950.0, 1200.0, 1150.0, 1300.0, 1250.0, 1400.0, 1450.0, 1500.0]

    def test_load_data(self):
        """Test data loading functionality."""
        # Test normal case
        self.analyzer.load_data(self.sample_timestamps, self.sample_prices, self.sample_volumes)
        self.assertEqual(len(self.analyzer.data), 10)
        self.assertEqual(self.analyzer.data[0].price, 100.0)
        self.assertEqual(self.analyzer.data[0].volume, 1000.0)
        
        # Test loading without volumes
        self.analyzer.load_data(self.sample_timestamps, self.sample_prices)
        self.assertEqual(self.analyzer.data[0].volume, None)
        
        # Test with empty data
        with self.assertRaises(ValueError):
            self.analyzer.load_data([], [], [])
            
        # Test with mismatched lengths
        with self.assertRaises(ValueError):
            self.analyzer.load_data(self.sample_timestamps, self.sample_prices[:-1])

    def test_merge_sort(self):
        """Test merge sort implementation."""
        # Test normal case
        self.analyzer.load_data(self.sample_timestamps[::-1], self.sample_prices[::-1])  # Reverse data
        sorted_data = self.analyzer.merge_sort(self.analyzer.data)
        
        self.assertEqual(len(sorted_data), 10)
        self.assertTrue(all(sorted_data[i].timestamp <= sorted_data[i+1].timestamp 
                          for i in range(len(sorted_data)-1)))
        
        # Test with single element
        single_data = [FinancialDataPoint(self.sample_timestamps[0], self.sample_prices[0])]
        sorted_single = self.analyzer.merge_sort(single_data)
        self.assertEqual(len(sorted_single), 1)
        
        # Test with empty list
        empty_data = []
        sorted_empty = self.analyzer.merge_sort(empty_data)
        self.assertEqual(len(sorted_empty), 0)

    def test_find_max_subarray(self):
        """Test maximum subarray implementation."""
        self.analyzer.load_data(self.sample_timestamps, self.sample_prices)
        
        # Test normal case
        start_idx, end_idx, max_gain = self.analyzer.find_max_subarray(0, len(self.analyzer.data)-1)
        self.assertIsInstance(start_idx, int)
        self.assertIsInstance(end_idx, int)
        self.assertIsInstance(max_gain, float)
        self.assertTrue(start_idx <= end_idx)
        
        # Test with single element
        start_idx, end_idx, max_gain = self.analyzer.find_max_subarray(0, 0)
        self.assertEqual(start_idx, 0)
        self.assertEqual(end_idx, 0)
        self.assertEqual(max_gain, 0)
        
        # Test with known pattern
        known_prices = [10.0, 11.0, 9.0, 15.0, 12.0]  # Max gain should be between indices 2 and 3
        known_timestamps = [self.sample_timestamps[i] for i in range(5)]
        self.analyzer.load_data(known_timestamps, known_prices)
        start_idx, end_idx, max_gain = self.analyzer.find_max_subarray(0, 4)
        self.assertEqual(max_gain, 6.0)  # 15 - 9 = 6

    def test_detect_anomalies(self):
        """Test anomaly detection functionality."""
        # Test normal case
        self.analyzer.load_data(self.sample_timestamps, self.sample_prices, self.sample_volumes)
        anomalies = self.analyzer.detect_anomalies(window_size=3, threshold=1.5)
        self.assertIsInstance(anomalies, list)
        for anomaly in anomalies:
            self.assertIsInstance(anomaly, AnomalyReport)
            
        # Test with known anomalies
        anomaly_prices = [100.0] * 5 + [200.0] + [100.0] * 4  # Clear spike at index 5
        self.analyzer.load_data(self.sample_timestamps, anomaly_prices)
        anomalies = self.analyzer.detect_anomalies(window_size=3, threshold=2.0)
        self.assertTrue(any(a.timestamp == self.sample_timestamps[5] for a in anomalies))
        
        # Test with insufficient data
        self.analyzer.load_data(self.sample_timestamps[:2], self.sample_prices[:2])
        anomalies = self.analyzer.detect_anomalies(window_size=3)
        self.assertEqual(len(anomalies), 0)

    def test_generate_report(self):
        """Test report generation functionality."""
        self.analyzer.load_data(self.sample_timestamps, self.sample_prices, self.sample_volumes)
        report = self.analyzer.generate_report()
        
        # Test report structure
        self.assertIn('data_points', report)
        self.assertIn('date_range', report)
        self.assertIn('price_statistics', report)
        self.assertIn('max_gain_period', report)
        self.assertIn('anomalies', report)
        self.assertIn('volume_statistics', report)
        
        # Test report content
        self.assertEqual(report['data_points'], 10)
        self.assertEqual(report['date_range']['start'], self.sample_timestamps[0])
        self.assertEqual(report['date_range']['end'], self.sample_timestamps[-1])
        
        # Test statistics calculations
        price_stats = report['price_statistics']
        self.assertAlmostEqual(price_stats['mean'], np.mean(self.sample_prices))
        self.assertAlmostEqual(price_stats['std'], np.std(self.sample_prices))
        self.assertEqual(price_stats['min'], min(self.sample_prices))
        self.assertEqual(price_stats['max'], max(self.sample_prices))

    def test_plot_analysis(self):
        """Test visualization functionality."""
        self.analyzer.load_data(self.sample_timestamps, self.sample_prices, self.sample_volumes)
        
        # Test normal case
        try:
            self.analyzer.plot_analysis("test_plot.png")
            self.assertTrue(True)  # If no exception was raised
        except Exception as e:
            self.fail(f"plot_analysis raised {type(e).__name__} unexpectedly!")
            
        # Test without volumes
        self.analyzer.load_data(self.sample_timestamps, self.sample_prices)
        try:
            self.analyzer.plot_analysis("test_plot_no_volume.png")
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"plot_analysis raised {type(e).__name__} unexpectedly!")

def create_edge_case_data():
    """Helper function to create edge case test data."""
    base_date = datetime(2024, 1, 1)
    timestamps = [base_date + timedelta(days=i) for i in range(5)]
    
    # Test cases for different edge scenarios
    test_cases = {
        'constant': {
            'prices': [100.0] * 5,
            'volumes': [1000.0] * 5
        },
        'single_spike': {
            'prices': [100.0, 100.0, 200.0, 100.0, 100.0],
            'volumes': [1000.0] * 5
        },
        'trending_up': {
            'prices': [100.0, 110.0, 120.0, 130.0, 140.0],
            'volumes': [1000.0] * 5
        },
        'trending_down': {
            'prices': [140.0, 130.0, 120.0, 110.0, 100.0],
            'volumes': [1000.0] * 5
        }
    }
    
    return timestamps, test_cases

class TestFinancialAnalyzerEdgeCases(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures for edge cases."""
        self.analyzer = FinancialAnalyzer()
        self.timestamps, self.test_cases = create_edge_case_data()

    def test_constant_prices(self):
        """Test behavior with constant prices."""
        data = self.test_cases['constant']
        self.analyzer.load_data(self.timestamps, data['prices'], data['volumes'])
        report = self.analyzer.generate_report()
        
        self.assertEqual(report['price_statistics']['std'], 0.0)
        self.assertEqual(len(report['anomalies']), 0)

    def test_single_spike(self):
        """Test behavior with a single price spike."""
        data = self.test_cases['single_spike']
        self.analyzer.load_data(self.timestamps, data['prices'], data['volumes'])
        anomalies = self.analyzer.detect_anomalies(window_size=3, threshold=2.0)
        
        self.assertTrue(len(anomalies) > 0)
        self.assertEqual(anomalies[0].timestamp, self.timestamps[2])

    def test_trending_data(self):
        """Test behavior with trending data."""
        # Test upward trend
        data = self.test_cases['trending_up']
        self.analyzer.load_data(self.timestamps, data['prices'], data['volumes'])
        report = self.analyzer.generate_report()
        
        self.assertTrue(report['price_statistics']['mean'] > data['prices'][0])
        
        # Test downward trend
        data = self.test_cases['trending_down']
        self.analyzer.load_data(self.timestamps, data['prices'], data['volumes'])
        report = self.analyzer.generate_report()
        
        self.assertTrue(report['price_statistics']['mean'] < data['prices'][0])

def run_tests():
    """Run all test cases."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes to the suite
    suite.addTests(loader.loadTestsFromTestCase(TestFinancialAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestFinancialAnalyzerEdgeCases))
    
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_tests()