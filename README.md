# YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit
This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a SQL database, and enables users to search for channel details and join tables to view data in the Streamlit app.

1. Data Volume
'''
1. Channels:
Size: 10 rows in the Channel table.

2. Videos:
Size: ~200 rows in the Video table.

3. Comments:
Size: ~10,000 rows in the Comment table.

2. Technologies Used
1. Programming Language:
Python: Main language for development.
'''
2. Database:
MySQL: Used for storing data in structured tables (Channel, Video, Comment).

3. Frontend Framework:
Streamlit: Interactive user interface for:
* Collecting Channel IDs.
* Displaying data.
* Answering specific analytical queries.

4. API Integration:
YouTube Data API v3: To fetch channel, video, and comment data.

5. Libraries:
* pandas: Data manipulation and analysis.
* mysql-connector-python: Connecting and interacting with the MySQL database.
* Streamlit: Building an interactive web application.
* datetime: Handling date and time formats.

6. Other Tools:
Regular Expressions (re): Parsing duration and time formats from API responses.

3. Methodologies Used
1. Data Harvesting:
Method: Fetching data directly from the YouTube Data API v3 for the channels, videos, and comments.

2. Data Warehousing:
* Database Design:
   * Three normalized tables: Channel, Video, Comment.
   * Proper indexing with primary and foreign keys.
   * Ensures efficient querying and data integrity.
* ETL Process:
   * Extract: Fetch data from the API.
   * Transform: Parse, clean, and format the data (e.g., duration to seconds).
   * Load: Insert data into MySQL tables.
     
3. Data Integration:
SQL joins are used to link tables (e.g., Channel ↔ Video, Video ↔ Comment).

4. Data Analysis:
* Dynamic SQL queries:
   * Aggregations (e.g., total views, comments).
   * Filters (e.g., videos published in a specific year).

5. Visualization:
* Method:
   * Display data tables directly using Streamlit (st.dataframe).
   * Provide user-friendly interfaces to explore and analyze data interactively.

4. Workflow for Completing the Project
1.Requirement Analysis:
* Define the scope: Collect data from YouTube, store it in a database, and perform specific analyses.
* Identify tools and APIs required (YouTube API, MySQL, Streamlit).

2. Setup and Configuration:
* Create the MySQL database and tables.
* Set up a Python environment with required libraries.
* Obtain YouTube API credentials.

3. Development:
* Backend:
    * Write Python functions to fetch data from the API.
    * Process and clean the data.
    * Store data into MySQL.
      
* Frontend:
Build a Streamlit UI for user input and data visualization.

* SQL Queries:
Write queries to answer analytical questions.

4. Testing:
* Validate API responses and data insertion.
* Test SQL queries for accuracy.
* Ensure the Streamlit app works as expected.
  
5. Deployment:
Host the Streamlit app


