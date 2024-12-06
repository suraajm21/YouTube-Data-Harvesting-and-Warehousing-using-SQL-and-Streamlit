# YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit
This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a SQL database, and enables users to search for channel details and join tables to view data in the Streamlit app.

Workflow
1. Project Setup
Environment Setup:

Install necessary Python packages:
bash
Copy code
pip install mysql-connector-python streamlit pandas
Set up a MySQL database (e.g., youtube_3) locally or on a server.
Define Database Schema:

Tables:
Channel: Stores channel details.
Video: Stores video details.
Comment: Stores comment details.
2. Data Collection
Fetch Data from YouTube API:

Use YouTube Data API v3 to collect:
Channel details
Video details
Comment details
Functions to Retrieve Data:

get_channel_details(channel_ids): Fetches channel details.
get_video_details(channel_ids): Fetches video details for given channel IDs.
get_comment_details(video_id): Fetches comments for a specific video.
3. Database Operations
Database Connection Setup:

Use mysql.connector to connect to MySQL.
Functions:
create_database_if_not_exists(database_name): Creates the database if it doesn't exist.
channel_table(): Creates and populates the Channel table.
video_table(): Creates and populates the Video table.
comment_table(): Creates and populates the Comment table.
Insert Data into Tables:

Insert or update data using:
INSERT INTO ... ON DUPLICATE KEY UPDATE for channel, video, and comment data.
4. Streamlit User Interface
App Layout:

Title: st.title("YouTube Data Harvesting and Warehousing using SQL and Streamlit")
Textbox: st.text_input("Enter the Channel_ID") for user input.
Data Collection Button:

Button: st.button("Collect and Store Data")
Actions:
Check if channel data already exists in the database.
Fetch data for the channel, its videos, and comments.
Populate tables in the database.
5. Data Display
Interactive Table Selection:

Radio Button: st.radio("Select the Table to Display", ("Channels_Data", "Video_Information", "Comment_Information"))
Functions to display data:
show_channel(): Displays channel data.
show_video(): Displays video data.
show_comment(): Displays comment data.
Dynamic Queries:

Use SQL queries to answer specific questions, such as:
Most viewed videos
Channels with the most videos
Average video duration per channel
6. Question-Answering Interface
Select Questions:

Dropdown: st.selectbox("Choose the question", [list of questions])
Dynamic Query Execution:

Example Query for Question 1:

sql
Copy code
SELECT a.channel_name, b.video_name 
FROM channel a 
JOIN video b ON a.channel_id = b.channel_id;
Display the result in a DataFrame using st.write().

7. Full Streamlit App Workflow
Input Data (Channel ID):

User enters a Channel ID to collect data.
Fetch and Store Data:

Fetch channel, video, and comment data.
Store data in respective MySQL tables.
Data Exploration:

Display raw data from tables based on user selection.
Answer Specific Questions:

Perform SQL queries based on user-selected questions and display results.
8. Testing and Deployment
Local Testing:

Run the Streamlit app locally:
bash
Copy code
streamlit run app.py
Deployment:

Host the Streamlit app using platforms like:
Streamlit Community Cloud
Heroku
AWS/GCP
Code Summary
Database Setup:

Functions to create the database and tables.
SQL queries to insert/update data.
Streamlit Interface:

Components for user interaction:
Text inputs, buttons, radio buttons, and dropdowns.
Functions to display data and handle queries.
Data Processing:

Fetching, parsing, and formatting API data.
Populating the database tables.
Sample User Flow
User Input:

Enter a Channel ID.
Click Collect and Store Data.
Data Processing:

Fetch data from YouTube API.
Store channel, video, and comment data in MySQL.
Explore Data:

Choose a table to display using radio buttons.
Answer Questions:

Select a question from the dropdown.
View SQL query results in a table.
This workflow ensures a structured and seamless process for data harvesting, warehousing, and analysis. Let me know if you'd like help with specific sections!
