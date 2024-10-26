# COMPSC463Proj1
Project Repository for COMPSC463 Project 1.


# Description of the project

## Problem Description

Develop a system that analyzes large financial datasets (e.g., stock prices, transaction logs, or cryptocurrency data) to detect patterns, trends, and anomalies. The system will use divide-and-conquer techniques to efficiently process, analyze, and report on financial data for decision-making purposes.

## Key components and algorithms

Merge sort for time-series data processing
Using merge sort, you can efficiently sort massive datasets
Sorting financial transactions based on timestamps, or arranging stock prices to detect trends and compute moving averages.
Divide-and-conquer algorithm for maximum subarray (Kadane’s Algorithm for 1D & 2D)
To identify the period of maximum gain or loss, the maximum subarray problem can be solved using a divide-and-conquer approach. It breaks down the stock price changes over time to find the subarray (period) where the profit is maximized.
This can be used to analyze stock performance over time, detect when stocks or assets have shown the best growth, or even identify periods of financial crisis.
Fast closest pair of points for anomaly detection
When analyzing large transaction logs or high-frequency trades, the closest pair of points algorithm can help detect anomalies by identifying trades or prices that deviate significantly from the norm.
Detecting unusual spikes or dips in trade prices, volumes, or transaction times, which could signal fraud or other financial irregularities.
 

## Outline of the Project (These steps provide the overall expected works. You do not need to follow steps in the same way)

Input: A large dataset of stock prices, cryptocurrency prices, or transaction logs.
This data can be sourced from public financial data APIs or historical datasets (e.g., daily stock prices over a year or millions of cryptocurrency transactions).
Step 1: Sort the data using Merge Sort.
Sort stock prices or transaction logs by time to prepare the dataset for further analysis.
This will ensure that subsequent operations (e.g., trend detection, anomaly detection) can be done efficiently on a sorted dataset.
Step 2: Find periods of maximum gain or loss using divide-and-conquer maximum subarray.
Apply the divide-and-conquer version of Kadane’s algorithm to find the sub-period where stock price or transaction volumes exhibited maximum gains (or losses).
Extend this algorithm to handle 2D arrays (e.g., analyzing two different stocks or comparing stock data across two different regions).
Step 3: Detect anomalies using closest pair of points.
Use a divide-and-conquer closest pair of points algorithm to find anomalies in transaction logs or price fluctuations. For instance, it can detect unusual deviations in transaction prices or times compared to historical data.
This can help in fraud detection or identifying unusual market behavior.
Step 4: Generate Reports.
Create reports showing the periods of maximum profit or loss, trends in stock or transaction prices, and detected anomalies.
You can visualize the results using line graphs or tables that highlight the key findings (e.g., the period with the largest gain or anomaly).
Output: The system generates detailed reports or graphs summarizing stock market trends, periods of high performance, or suspicious financial transactions.

# Code Structure

main.py
|_ algorithm.py

main.py: Driver code for the application.
algorithm.py: Contains teh various algorithms used to produce the analysis results based on the data.

# Tutorial

## Required Installs
pip install numpy pandas matplotlib

## Guide

# Test Cases

## Main Program Test Cases

## Test Cases for Individual Parts

# Conclusion
