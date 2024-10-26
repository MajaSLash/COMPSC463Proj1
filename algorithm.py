import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

@dataclass
class FinancialDataPoint:
    timestamp: datetime
    price: float
    volume: Optional[float] = None
    
@dataclass
class AnomalyReport:
    timestamp: datetime
    value: float
    deviation: float
    anomaly_type: str

class FinancialAnalyzer:
    def __init__(self):
        self.data: List[FinancialDataPoint] = []
        
    def load_data(self, timestamps: List[datetime], prices: List[float], volumes: Optional[List[float]] = None):
        """Load financial data into the analyzer."""
        self.data = [
            FinancialDataPoint(ts, price, vol) 
            for ts, price, vol in zip(timestamps, prices, volumes if volumes else [None] * len(prices))
        ]
    
    def merge_sort(self, arr: List[FinancialDataPoint]) -> List[FinancialDataPoint]:
        """Merge sort implementation for time series data."""
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[FinancialDataPoint], right: List[FinancialDataPoint]) -> List[FinancialDataPoint]:
        """Helper function for merge sort."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i].timestamp <= right[j].timestamp:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def find_max_subarray(self, start: int, end: int) -> Tuple[int, int, float]:
        """Find the maximum subarray using divide-and-conquer (modified Kadane's algorithm)."""
        if start == end:
            return start, end, 0
            
        mid = (start + end) // 2
        
        # Find max crossing subarray
        left_sum = float('-inf')
        curr_sum = 0
        max_left = mid
        
        for i in range(mid, start - 1, -1):
            price_change = self.data[i + 1].price - self.data[i].price
            curr_sum += price_change
            if curr_sum > left_sum:
                left_sum = curr_sum
                max_left = i
                
        right_sum = float('-inf')
        curr_sum = 0
        max_right = mid + 1
        
        for i in range(mid + 1, end + 1):
            price_change = self.data[i].price - self.data[i - 1].price
            curr_sum += price_change
            if curr_sum > right_sum:
                right_sum = curr_sum
                max_right = i
                
        # Recursively find max subarrays in left and right halves
        left_low, left_high, left_sum = self.find_max_subarray(start, mid)
        right_low, right_high, right_sum = self.find_max_subarray(mid + 1, end)
        
        # Return the maximum of the three possible subarrays
        cross_sum = left_sum + right_sum
        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        else:
            return max_left, max_right, cross_sum
    
    def detect_anomalies(self, window_size: int = 20, threshold: float = 2.0) -> List[AnomalyReport]:
        """Detect anomalies using rolling statistics and closest pair principles."""
        if len(self.data) < window_size:
            return []
            
        anomalies = []
        
        # Calculate rolling mean and standard deviation
        prices = [dp.price for dp in self.data]
        rolling_mean = pd.Series(prices).rolling(window=window_size).mean()
        rolling_std = pd.Series(prices).rolling(window=window_size).std()
        
        for i in range(window_size, len(self.data)):
            price = self.data[i].price
            z_score = (price - rolling_mean[i]) / rolling_std[i]
            
            if abs(z_score) > threshold:
                anomalies.append(AnomalyReport(
                    timestamp=self.data[i].timestamp,
                    value=price,
                    deviation=z_score,
                    anomaly_type="Price spike" if z_score > 0 else "Price drop"
                ))
                
        return anomalies
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive analysis report."""
        # Sort data if not already sorted
        self.data = self.merge_sort(self.data)
        
        # Find period of maximum gain
        start_idx, end_idx, max_gain = self.find_max_subarray(0, len(self.data) - 1)
        
        # Detect anomalies
        anomalies = self.detect_anomalies()
        
        # Calculate basic statistics
        prices = [dp.price for dp in self.data]
        volumes = [dp.volume for dp in self.data if dp.volume is not None]
        
        report = {
            "data_points": len(self.data),
            "date_range": {
                "start": self.data[0].timestamp,
                "end": self.data[-1].timestamp
            },
            "price_statistics": {
                "mean": np.mean(prices),
                "std": np.std(prices),
                "min": min(prices),
                "max": max(prices)
            },
            "max_gain_period": {
                "start_date": self.data[start_idx].timestamp,
                "end_date": self.data[end_idx].timestamp,
                "gain": max_gain
            },
            "anomalies": [
                {
                    "timestamp": a.timestamp,
                    "value": a.value,
                    "deviation": a.deviation,
                    "type": a.anomaly_type
                }
                for a in anomalies
            ]
        }
        
        if volumes:
            report["volume_statistics"] = {
                "mean": np.mean(volumes),
                "std": np.std(volumes),
                "min": min(volumes),
                "max": max(volumes)
            }
            
        return report
    
    def plot_analysis(self, save_path: Optional[str] = None):
        """Generate visualization of the analysis results."""
        timestamps = [dp.timestamp for dp in self.data]
        prices = [dp.price for dp in self.data]
        
        plt.figure(figsize=(15, 10))
        
        # Plot price data
        plt.subplot(2, 1, 1)
        plt.plot(timestamps, prices, label='Price')
        
        # Highlight maximum gain period
        start_idx, end_idx, max_gain = self.find_max_subarray(0, len(self.data) - 1)
        plt.fill_between(
            timestamps[start_idx:end_idx+1],
            prices[start_idx:end_idx+1],
            alpha=0.3,
            color='green',
            label='Max Gain Period'
        )
        
        # Mark anomalies
        anomalies = self.detect_anomalies()
        anomaly_times = [a.timestamp for a in anomalies]
        anomaly_prices = [a.value for a in anomalies]
        plt.scatter(anomaly_times, anomaly_prices, color='red', label='Anomalies')
        
        plt.title('Financial Data Analysis')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        
        # Plot volume if available
        volumes = [dp.volume for dp in self.data]
        if any(v is not None for v in volumes):
            plt.subplot(2, 1, 2)
            plt.plot(timestamps, volumes, label='Volume')
            plt.xlabel('Time')
            plt.ylabel('Volume')
            plt.legend()
        
        if save_path:
            plt.savefig(save_path)
        plt.close()