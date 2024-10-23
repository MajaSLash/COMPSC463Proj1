import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from collections import namedtuple

@dataclass
class FinancialDataPoint:
    timestamp: datetime
    price: float
    volume: float = 0.0
    
@dataclass
class AnomalyReport:
    timestamp: datetime
    value: float
    expected_value: float
    deviation_percentage: float
    
@dataclass
class MaximumSubarrayResult:
    start_index: int
    end_index: int
    sum_value: float
    
class FinancialAnalyzer:
    def __init__(self):
        self.data: List[FinancialDataPoint] = []
        
    def merge_sort(self, arr: List[FinancialDataPoint]) -> List[FinancialDataPoint]:
        """Merge sort implementation for time series data."""
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        
        # Merge sorted halves
        merged = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i].timestamp <= right[j].timestamp:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
    
    def find_maximum_subarray(self, prices: List[float]) -> MaximumSubarrayResult:
        """
        Implementation of Kadane's algorithm using divide-and-conquer approach
        to find the maximum subarray (period of maximum gain)
        """
        def max_crossing_sum(arr: List[float], low: int, mid: int, high: int) -> Tuple[int, int, float]:
            # Find maximum sum crossing to left
            left_sum = float('-inf')
            sum_temp = 0
            max_left = mid
            
            for i in range(mid - 1, low - 1, -1):
                sum_temp += arr[i]
                if sum_temp > left_sum:
                    left_sum = sum_temp
                    max_left = i
                    
            # Find maximum sum crossing to right
            right_sum = float('-inf')
            sum_temp = 0
            max_right = mid + 1
            
            for i in range(mid + 1, high + 1):
                sum_temp += arr[i]
                if sum_temp > right_sum:
                    right_sum = sum_temp
                    max_right = i
                    
            return max_left, max_right, left_sum + arr[mid] + right_sum
            
        def max_subarray(arr: List[float], low: int, high: int) -> Tuple[int, int, float]:
            if high == low:
                return low, high, arr[low]
                
            mid = (low + high) // 2
            
            # Find maximum subarray in left half
            left_low, left_high, left_sum = max_subarray(arr, low, mid)
            
            # Find maximum subarray in right half
            right_low, right_high, right_sum = max_subarray(arr, mid + 1, high)
            
            # Find maximum subarray crossing the midpoint
            cross_low, cross_high, cross_sum = max_crossing_sum(arr, low, mid, high)
            
            if left_sum >= right_sum and left_sum >= cross_sum:
                return left_low, left_high, left_sum
            elif right_sum >= left_sum and right_sum >= cross_sum:
                return right_low, right_high, right_sum
            else:
                return cross_low, cross_high, cross_sum
                
        if not prices:
            return MaximumSubarrayResult(0, 0, 0.0)
            
        # Calculate price changes
        price_changes = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
        if not price_changes:
            return MaximumSubarrayResult(0, 0, 0.0)
            
        start, end, total_gain = max_subarray(price_changes, 0, len(price_changes)-1)
        return MaximumSubarrayResult(start, end + 1, total_gain)
    
    def find_closest_pairs(self, points: List[Tuple[datetime, float]], 
                         threshold: float) -> List[AnomalyReport]:
        """
        Implementation of closest pair algorithm for anomaly detection
        Returns points that are significantly different from their neighbors
        """
        def distance(p1: Tuple[datetime, float], p2: Tuple[datetime, float]) -> float:
            # Calculate normalized distance between two points
            time_diff = (p2[0] - p1[0]).total_seconds() / 86400  # Convert to days
            price_diff = abs(p2[1] - p1[1]) / p1[1]  # Normalized price difference
            return np.sqrt(time_diff**2 + price_diff**2)
        
        def closest_pair_rec(points: List[Tuple[datetime, float]], 
                           start: int, end: int) -> List[AnomalyReport]:
            if end - start <= 3:
                # Base case: brute force for small arrays
                anomalies = []
                for i in range(start, end):
                    for j in range(i + 1, end):
                        dist = distance(points[i], points[j])
                        if dist > threshold:
                            # Report both points as potential anomalies
                            expected = points[i][1]
                            deviation = abs(points[j][1] - expected) / expected * 100
                            anomalies.append(AnomalyReport(
                                points[j][0], points[j][1], expected, deviation
                            ))
                return anomalies
            
            # Divide array into two halves
            mid = (start + end) // 2
            mid_point = points[mid][0]
            
            # Recursive calls
            left_anomalies = closest_pair_rec(points, start, mid)
            right_anomalies = closest_pair_rec(points, mid, end)
            
            # Combine results and check for anomalies across the divide
            combined_anomalies = left_anomalies + right_anomalies
            
            # Check points near the dividing line
            strip = []
            for i in range(start, end):
                time_diff = abs((points[i][0] - mid_point).total_seconds())
                if time_diff <= threshold * 86400:  # Convert threshold to seconds
                    strip.append(points[i])
            
            # Check strip points for anomalies
            strip.sort(key=lambda x: x[1])  # Sort by price for efficient comparison
            for i in range(len(strip)):
                for j in range(i + 1, min(i + 7, len(strip))):
                    dist = distance(strip[i], strip[j])
                    if dist > threshold:
                        expected = strip[i][1]
                        deviation = abs(strip[j][1] - expected) / expected * 100
                        combined_anomalies.append(AnomalyReport(
                            strip[j][0], strip[j][1], expected, deviation
                        ))
            
            return combined_anomalies
        
        # Sort points by timestamp before processing
        sorted_points = sorted(points, key=lambda x: x[0])
        return closest_pair_rec(sorted_points, 0, len(sorted_points))
    
    def analyze_financial_data(self, data: List[FinancialDataPoint], 
                             anomaly_threshold: float = 0.1) -> Dict:
        """
        Main analysis function that processes financial data and generates reports
        """
        # Sort data by timestamp
        self.data = self.merge_sort(data)
        
        # Extract prices for maximum subarray analysis
        prices = [point.price for point in self.data]
        
        # Find period of maximum gain
        max_gain_period = self.find_maximum_subarray(prices)
        
        # Detect anomalies
        points = [(point.timestamp, point.price) for point in self.data]
        anomalies = self.find_closest_pairs(points, anomaly_threshold)
        
        # Generate report
        report = {
            'data_points': len(self.data),
            'start_date': self.data[0].timestamp,
            'end_date': self.data[-1].timestamp,
            'max_gain_period': {
                'start_date': self.data[max_gain_period.start_index].timestamp,
                'end_date': self.data[max_gain_period.end_index].timestamp,
                'total_gain': max_gain_period.sum_value
            },
            'anomalies': anomalies
        }
        
        return report
    
    def visualize_results(self, report: Dict) -> None:
        """
        Create visualizations of the analysis results
        """
        timestamps = [point.timestamp for point in self.data]
        prices = [point.price for point in self.data]
        
        plt.figure(figsize=(15, 10))
        
        # Plot price data
        plt.plot(timestamps, prices, label='Price')
        
        # Highlight maximum gain period
        max_gain_start = report['max_gain_period']['start_date']
        max_gain_end = report['max_gain_period']['end_date']
        plt.axvspan(max_gain_start, max_gain_end, alpha=0.3, color='green', 
                   label='Maximum Gain Period')
        
        # Mark anomalies
        anomaly_timestamps = [a.timestamp for a in report['anomalies']]
        anomaly_prices = [a.value for a in report['anomalies']]
        plt.scatter(anomaly_timestamps, anomaly_prices, color='red', 
                   label='Anomalies', zorder=5)
        
        plt.title('Financial Data Analysis')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()