# YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit
This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a SQL database, and enables users to search for channel details and join tables to view data in the Streamlit app.

1. Data Volume
```
1. Channels:
Size: 10 rows in the Channel table.

2. Videos:
Size: 443 rows in the Video table.

3. Comments:
Size: 7752 rows in the Comment table.
```
2. Technologies Used
```
1. Programming Language:
Python: Main language for development.

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
```

3. Methodologies Used
```
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
```
4. Workflow for Completing the Project
```
1. Project Setup
1. Environment Setup:
* Install necessary Python packages:
* Set up a MySQL database (e.g., youtube_data) locally or on a server.

2. Define Database Schema:
Tables:
* Channel: Stores channel details.
* Video: Stores video details.
* Comment: Stores comment details.

2. Data Collection
1. Fetch Data from YouTube API:
Use YouTube Data API v3 to collect:
* Channel details
* Video details
* Comment details

2. Functions to Retrieve Data:
* get_channel_details(channel_ids): Fetches channel details.
* get_video_details(channel_ids): Fetches video details for given channel IDs.
* get_comment_details(video_id): Fetches comments for a specific video.

3. Database Operations

1. Database Connection Setup:
* Use mysql.connector to connect to MySQL.
* Functions:
    * create_database_if_not_exists(database_name): Creates the database if it doesn't exist.
    * channel_table(): Creates and populates the Channel table.
    * video_table(): Creates and populates the Video table.
    * comment_table(): Creates and populates the Comment table.

2. Insert Data into Tables:
Insert or update data using:
INSERT INTO ... ON DUPLICATE KEY UPDATE for channel, video, and comment data.

4. Streamlit User Interface

1. App Layout:
* Title: st.title("YouTube Data Harvesting and Warehousing using SQL and Streamlit")
* Textbox: st.text_input("Enter the Channel_ID") for user input.

2. Data Collection Button:
* Button: st.button("Collect and Store Data")
* Actions:
     * Check if channel data already exists in the database.
     * Fetch data for the channel, its videos, and comments.
     * Populate tables in the database.

5. Data Display

1. Interactive Table Selection:
* Radio Button: st.radio("Select the Table to Display", ("Channels_Data", "Video_Information", "Comment_Information"))
* Functions to display data:
      * show_channel(): Displays channel data.
      * show_video(): Displays video data.
      * show_comment(): Displays comment data.

2. Dynamic Queries:
Use SQL queries to answer specific questions, such as:
      * Most viewed videos
      * Channels with the most videos
      * Average video duration per channel

6. Question-Answering Interface
1. Select Questions:
Dropdown: st.selectbox("Choose the question", [list of questions])
2. Dynamic Query Execution:
Display the result in a DataFrame using st.write().

7. Full Streamlit App Workflow
1. Input Data (Channel ID):
User enters a Channel ID to collect data.

2.Fetch and Store Data:
* Fetch channel, video, and comment data.
* Store data in respective MySQL tables.

3. Data Exploration:
Display raw data from tables based on user selection.

4. Answer Specific Questions:
Perform SQL queries based on user-selected questions and display results.

8. Testing and Deployment
Local Testing:
Run the Streamlit app locally:
streamlit run app.py
```

5. User Flow
```
1. User Input:
* Enter a Channel ID.
* Click Collect and Store Data.

2. Data Processing:
Fetch data from YouTube API.
Store channel, video, and comment data in MySQL.

3. Explore Data:
Choose a table to display using radio buttons

4. Answer Questions:
* Select a question from the dropdown.
* View SQL query results in a table.
```

