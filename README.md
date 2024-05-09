# Disk Failure Prediction

- Last Modified: 2024-05-09
- Author: Ruitao Lv

## Background and instructions:  

Various disk failures are not rare in large-scale IDCs and cloud computing environments, fortunately, we have S.M.A.R.T. (Self-Monitoring, Analysis, and Reporting Technology; often written as SMART) logs collected from computer hard disk drives (HDDs), solid-state drives (SSDs) and eMMC drives that detects and reports on various indicators of drive reliability, with the intent of enabling the anticipation of hardware failures.

Since 2013, Backblaze has published statistics and insights based on the hard drives in their data center, as well as the data underlying these reports. In this case study, you can download SMART logs from [Backblaze hard drive test data website](https://www.backblaze.com/b2/hard-drive-test-data.html), then design and implement a machine learning-based solution to predict the disk failures daily(output prediction results in each testing day) granularity. The output document should include a detailed illustration of the following parts:
- The methods or flow of data preprocessing and feature engineering.
- How to choose machine learning models and tune the parameters?
- How to evaluate the results?
- What insights or lessons were learned from this task?
 
## Inspirations:    
- You may learn more background information from:
  - https://en.wikipedia.org/wiki/Self-Monitoring,_Analysis_and_Reporting_Technology
  - https://www.backblaze.com/blog/hard-drive-smart-stats/  
- You can consider evaluating the results in weekly or monthly periods.  
- Codes, charts and tables are essential for results interpretation.  
 
## Datasets and meta description:  
- You can download SMART logs from:https://www.backblaze.com/b2/hard-drive-test-data.html 

## Reference:  
Proactive Prediction of Hard Disk Drive Failure

## Structure:
Now the folder structure under the data folder is sth. like:  
   ```
   ├─data  
   │  ├─data_Q1_2018  
   │  ├─data_Q2_2018  
   │  ├─data_Q3_2018  
   │  └─data_Q4_2018  
   ├─data_preprocess  
   ├─dataset.csv  
   └─KNN.py  
   ```