import algorithm

# Create sample data
data = [
    algorithm.FinancialDataPoint(algorithm.datetime(2024, 1, i), price) 
    for i, price in enumerate([100, 102, 98, 103, 107, 104, 110], 1)
]

# Initialize analyzer and process data
analyzer = algorithm.FinancialAnalyzer()
report = analyzer.analyze_financial_data(data, anomaly_threshold=0.05)

# Visualize results
analyzer.visualize_results(report)