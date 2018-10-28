# Log analysis challenge

## Streaming logs
- Logs are read continuously by the file 'streaming_script.py'.
- Continously, logs are being parsed and written into a database table 'logs'
 ```
 CREATE TABLE logs
    (
        LogType VARCHAR(255),
        Date VARCHAR(255),
        Time VARCHAR(255),
        DateTime VARCHAR(255),
        PID VARCHAR(255),
        ResponseTime INT,
        UID VARCHAR(255),
        URL VARCHAR(255)
    );
 ```
- Cursor position is regularly updated and used so that any time the script resumes, it resumes from the right location in the log.
 ```
 CREATE TABlE cursor_position
    (
        position INT
    );
 ```
- Real-time analysis can be done by running the script 'analysis.py' or viewing on Jupyter Notebook the file 'Data Analysis.ipynb'


## Notes
- I used pandas in Python 3 as I felt this was the fastest, cheapest and easiest way for the particular problem statement. 
- The problem with pandas is that the dataframes are stored in memory, and upon reaching a certain size, it can affect the performance of the system and prove to be the bottleneck. 
    - I have avoided this by loading data into dataframes into batches and sending them into MySQL in batches as well. 
- The only assumption I would make is everything in the log file would always be appended, as it usually does. 
- If I had more time-
    - I would have written the code for writing a log everytime a set of rules is broken. 
    - I would have benchmarked the batch size of my parsed log data