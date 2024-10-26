import algorithm
from datetime import datetime
import random

# Create analyzer instance
analyzer = algorithm.FinancialAnalyzer()

# Load data
timestamps = [datetime(2024, 1, i) for i in range(1, 31)]
prices = [100 + i + random.random() * 10 for i in range(30)]
volumes = [1000 + random.random() * 100 for _ in range(30)]

analyzer.load_data(timestamps, prices, volumes)

# Generate and print report
report = analyzer.generate_report()
print(report)

# Generate visualization
analyzer.plot_analysis("analysis_results.png")