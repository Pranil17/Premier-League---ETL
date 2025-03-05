# Premier-League---ETL
Make a sample ETL with Premier League data

This sample ETL is made with the help of python & pandas.

Architecture:
The pipeline follows a **modular plugin-based architecture** where there is a common script for ETL named (/src/etl_job.py) :
1. **Extract**: Reads JSON files from the `data` folder.
2. **Transform**: Dynamically loads transformation logic (e.g., `position_table`, `best_scoring_team`).There is a separate folder with transformations written in pandas.
3. **Load**: Saves results to CSV files in the `output` folder.


Output:
Output is stored in csv format in a separate commond folder.

Thoughts:
Further this can be enhanced by using real time scheduler like Airflow,CA Wade,etc. Moreover if scaled-up, we use handle processing on spark and storage solution capable to store big data(hdfs,etc).
