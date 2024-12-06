# Importing necessary libraries
import mysql.connector
from googleapiclient.discovery import build
import googleapiclient.discovery
import pandas as pd
import streamlit as st
from datetime import datetime
from datetime import timedelta
import re
import streamlit as st
import json

# Function to establish a connection to the YouTube Data API
def api_connection():
    api_key = "AIzaSyAz4NXgN_D9fOkmcy1LAS5aQ1LP7zMQLgU"
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    return youtube

youtube = api_connection()    # The 'youtube' variable now holds the authenticated YouTube Data API client object

# Function to fetch details for the YouTube channels
def get_channel_details(channel_ids=None):

    # If no channel IDs are provided, then this default list of channel IDs is used
    if channel_ids is None:
        channel_ids = ["UCqsRYAAtXopb8eK6SrK6duA","UCQqmjKQBKQkRbWbSntYJX0Q","UC-s0bfmR0JCVC2xRxYq_I5w","UCxsQHU5SwYtO6uc1jiLdvrg",
            "UC-1kzHtwBY8n0TY5NhYxNaw", "UCTwVVVVfsOkNfaxbCEkspOg", "UCgVq7NWVuHkf-nLujTS6jFA", "UCSZzkikEEdPJ6SIwTv-Jwdw",
            "UCGKIAihHaivngERJKO7Le0A", "UCEkyvszqWQRsQLYPQdQ-wGw"]
    
    # If a single channel ID is provided as a string, convert it into a list
    if isinstance(channel_ids, str):
        channel_ids = [channel_ids]
    if not channel_ids:  
        return []

    channel_data_list = []
    for chn_id in channel_ids:
        try:
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=chn_id)
            response = request.execute()

            for i in response['items']:

                # Extracting relevant data from the API response and store it in a dictionary
                data = dict(Channel_Id = i['id'],
                        Channel_Name = i['snippet']['title'],
                        Channel_Views = i['statistics']['viewCount'],                        
                        Channel_Description = i['snippet']['description'],                                 
                        Playlist_Id = i['contentDetails']['relatedPlaylists']['uploads'])
                
                channel_data_list.append(data)

        # Handle any exceptions that occur during API requests        
        except Exception as e:
            print(f"Error fetching data for channel {chn_id}: {e}")
    return channel_data_list

# Function to fetch video details for the Channel IDs
def get_video_details(channel_ids=None):
    if channel_ids is None:
        channel_ids = ["UCqsRYAAtXopb8eK6SrK6duA","UCQqmjKQBKQkRbWbSntYJX0Q","UC-s0bfmR0JCVC2xRxYq_I5w","UCxsQHU5SwYtO6uc1jiLdvrg",
            "UC-1kzHtwBY8n0TY5NhYxNaw", "UCTwVVVVfsOkNfaxbCEkspOg", "UCgVq7NWVuHkf-nLujTS6jFA", "UCSZzkikEEdPJ6SIwTv-Jwdw",
            "UCGKIAihHaivngERJKO7Le0A", "UCEkyvszqWQRsQLYPQdQ-wGw"]  
        
    
    if isinstance(channel_ids, str):
        channel_ids = [channel_ids]
    if not channel_ids:  
        return []

    all_video_ids = []
    for channel_id in channel_ids:
        video_ids = []
        request1 = youtube.channels().list(id=channel_id, part="contentDetails")
        response1 = request1.execute()
        playlist_id = response1['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token = None
        while True:

            # Request to fetch videos in the playlist (50 videos per page)
            request2 = youtube.playlistItems().list(playlistId=playlist_id, part="snippet", maxResults=50, pageToken=next_page_token)
            response2 = request2.execute()

            # Extracting video IDs from the response and adding to the list
            for i in range(len(response2['items'])):
                video_ids.append(response2['items'][i]['snippet']['resourceId']['videoId'])
            next_page_token = response2.get('nextPageToken')

            # Check if there is a next page; if not, break the loop
            if next_page_token is None:
                break
        all_video_ids.extend(video_ids)

    video_data = []
    for video_id in all_video_ids:
        request3 = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response3 = request3.execute()

        for item in response3['items']:
            data = {
                "Video_Id": item['id'],
                "Channel_Id": item['snippet']['channelId'],
                "Video_Name": item['snippet']['title'],
                "Video_Description": item['snippet'].get('description'),
                "PublishedAt": item['snippet']['publishedAt'],
                "Views_Count": item['statistics'].get('viewCount'),
                "Like_Count": item['statistics'].get('likeCount'),
                "Favourite_Count": item['statistics']['favoriteCount'],
                "Comment_Count": item['statistics'].get('commentCount'),
                "Duration": item['contentDetails']['duration'],
                "Caption_Status": item['contentDetails']['caption'],
            }
            video_data.append(data)

    return video_data

# Function to fetch comment details for either a specific video or all videos in the provided channels
def get_comment_details(channel_ids=None, video_id=None):
    comments_data = []

    # If a specific video ID is provided, fetch comments for that video only
    if video_id:  
        try:

            # API request to fetch comments for the given video ID
            request5 = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=50)
            response5 = request5.execute()

            for item in response5.get('items', []):  
                data = {
                    "Comment_Id": item['snippet']['topLevelComment']['id'],
                    "Video_Id": item['snippet']['topLevelComment']['snippet']['videoId'],
                    "Comment_Text": item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    "Comment_Author": item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    "Comment_PublishedAt": item['snippet']['topLevelComment']['snippet']['publishedAt'],
                }
                comments_data.append(data)
        except googleapiclient.errors.HttpError as e:

            # Handle API errors (e.g., if comments are disabled)
            error_content = json.loads(e.content.decode('utf-8'))
            error_reason = error_content.get('error', {}).get('errors', [{}])[0].get('reason', '')
            if error_reason == "commentsDisabled":
                print(f"Comments are disabled for video ID {video_id}. Skipping...")
            else:
                print(f"Error fetching comments for video ID {video_id}: {e}")
        return comments_data

    # If no video ID is provided, proceed to fetch comments for videos in given channels
    if channel_ids is None:       
        channel_ids = [
            "UCqsRYAAtXopb8eK6SrK6duA", "UCQqmjKQBKQkRbWbSntYJX0Q", "UC-s0bfmR0JCVC2xRxYq_I5w", "UCxsQHU5SwYtO6uc1jiLdvrg",
            "UC-1kzHtwBY8n0TY5NhYxNaw", "UCTwVVVVfsOkNfaxbCEkspOg", "UCgVq7NWVuHkf-nLujTS6jFA", "UCSZzkikEEdPJ6SIwTv-Jwdw",
            "UCGKIAihHaivngERJKO7Le0A", "UCEkyvszqWQRsQLYPQdQ-wGw"
        ]
    elif isinstance(channel_ids, str):  
        channel_ids = [channel_ids]

    all_video_ids = []
    for channel_id in channel_ids:
        video_ids = []
        try:
           
            request1 = youtube.channels().list(id=channel_id, part="contentDetails")
            response1 = request1.execute()
            playlist_id = response1['items'][0]['contentDetails']['relatedPlaylists']['uploads']

       
            next_page_token = None
            while True:
                request2 = youtube.playlistItems().list(
                    playlistId=playlist_id, part="snippet", maxResults=50, pageToken=next_page_token
                )
                response2 = request2.execute()

                for i in range(len(response2['items'])):
                    video_ids.append(response2['items'][i]['snippet']['resourceId']['videoId'])
                next_page_token = response2.get('nextPageToken')

                if next_page_token is None:
                    break
        except Exception as e:
            print(f"Error fetching videos for channel ID {channel_id}: {e}")
        all_video_ids.extend(video_ids)

    
    try:
        for vdid in all_video_ids:
            try:
                request5 = youtube.commentThreads().list(part="snippet", videoId=vdid, maxResults=50)
                response5 = request5.execute()

                for item in response5.get('items', []):  
                    data = {
                        "Comment_Id": item['snippet']['topLevelComment']['id'],
                        "Video_Id": item['snippet']['topLevelComment']['snippet']['videoId'],
                        "Comment_Text": item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        "Comment_Author": item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        "Comment_PublishedAt": item['snippet']['topLevelComment']['snippet']['publishedAt'],
                    }
                    comments_data.append(data)
            except googleapiclient.errors.HttpError as e:
                error_content = json.loads(e.content.decode('utf-8'))
                error_reason = error_content.get('error', {}).get('errors', [{}])[0].get('reason', '')
                if error_reason == "commentsDisabled":
                    print(f"Comments are disabled for video ID {vdid}. Skipping...")
                else:
                    print(f"Error fetching comments for video ID {vdid}: {e}")
    except Exception as e:
        print(f"Error fetching comments: {e}")

    return comments_data

# Function to create a database if it does not already exist
def create_database_if_not_exists(database_name):
    try:

        # Connecting to the MySQL server using root credentials
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Suraaj121097"
        )
        mycursor = mydb.cursor()  # Create a cursor object to execute SQL queries

        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        mydb.commit()     # Committing the transaction to ensure the database is created
        print(f"Database '{database_name}' created successfully.")

    except mysql.connector.Error as err:
        if err.errno == 1007:                    # Error code 1007 indicates the database already exists
            print(f"Database '{database_name}' already exists.")
        else:
            print(f"Error creating database: {err}")
    
mycursor = create_database_if_not_exists("youtube_data")

# Function to create the 'Channel' table and populate it with data from a list of channel IDs
def channel_table(a=None, b=None, c=None):
    try:

        # Connect to the MySQL database 'youtube_data'
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Suraaj121097",
            database="youtube_data"  
        )
        mycursor = mydb.cursor()

        # Checking if the 'Channel' table already exists
        mycursor.execute("SHOW TABLES LIKE 'Channel'")
        result = mycursor.fetchone()

        if result:
            print("Table 'Channel' already exists.")     # Notify if the table already exists
        else:
            
            # SQL query to create the 'Channel' table
            mycursor.execute('''CREATE TABLE Channel (
                Channel_Id VARCHAR(255) PRIMARY KEY, 
                Channel_Name VARCHAR(255), 
                Channel_Views INT, 
                Channel_Description TEXT, 
                Playlist_Id VARCHAR(255)
            )''')
            mydb.commit()

            print("Table 'Channel' created successfully.")

        # Defining a list of YouTube channel IDs to process
        channel_ids = [
            "UCqsRYAAtXopb8eK6SrK6duA", "UCQqmjKQBKQkRbWbSntYJX0Q", "UC-s0bfmR0JCVC2xRxYq_I5w", "UCxsQHU5SwYtO6uc1jiLdvrg",
            "UC-1kzHtwBY8n0TY5NhYxNaw", "UCTwVVVVfsOkNfaxbCEkspOg", "UCgVq7NWVuHkf-nLujTS6jFA", "UCSZzkikEEdPJ6SIwTv-Jwdw",
            "UCGKIAihHaivngERJKO7Le0A", "UCEkyvszqWQRsQLYPQdQ-wGw"
        ]

        # Fetching channel details using the `get_channel_details` function
        channel_details = get_channel_details(channel_ids)

        sqlFormula = '''INSERT INTO Channel (Channel_Id, Channel_Name, Channel_Views, Channel_Description, Playlist_Id) 
                         VALUES (%s, %s, %s, %s, %s)
                         ON DUPLICATE KEY UPDATE 
                         Channel_Name=VALUES(Channel_Name), 
                         Channel_Views=VALUES(Channel_Views), 
                         Channel_Description=VALUES(Channel_Description), 
                         Playlist_Id=VALUES(Playlist_Id)'''

        val = []
        for channel in channel_details:
            val.append((
                channel.get('Channel_Id'), 
                channel.get('Channel_Name'), 
                channel.get('Channel_Views'),
                channel.get('Channel_Description'), 
                channel.get('Playlist_Id')
            ))

        if val:             # Only proceed if there is data to insert
            mycursor.executemany(sqlFormula, val)        # Insert or update multiple rows
            mydb.commit()

        mycursor.execute("SELECT * FROM Channel")
        rows = mycursor.fetchall()           # Fetch all rows from the table

        for row in rows:
            print(row)

    except mysql.connector.Error as err:
        print("An error occurred:", err)

    finally:

        # Ensuring the database connection is closed properly
        if mydb.is_connected():
            mycursor.close()
            mydb.close()  

# Calling the function to create the 'Channel' table and populate it with data
channel_table()

# Function to create the 'Video' table and populate it with video details
def video_table(a=None, b=None, c=None):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Suraaj121097",
            database="youtube_data" 
        )
        mycursor = mydb.cursor()

        # Check if the 'Video' table already exists
        mycursor.execute("SHOW TABLES LIKE 'video'")
        result = mycursor.fetchone()

        # If the 'Video' table does not exist, create it and populate it
        if not result:
            channel_ids = ["UCqsRYAAtXopb8eK6SrK6duA", "UCQqmjKQBKQkRbWbSntYJX0Q", "UC-s0bfmR0JCVC2xRxYq_I5w", "UCxsQHU5SwYtO6uc1jiLdvrg",
                        "UC-1kzHtwBY8n0TY5NhYxNaw", "UCTwVVVVfsOkNfaxbCEkspOg", "UCgVq7NWVuHkf-nLujTS6jFA", "UCSZzkikEEdPJ6SIwTv-Jwdw",
                        "UCGKIAihHaivngERJKO7Le0A", "UCEkyvszqWQRsQLYPQdQ-wGw"]

            video_details = get_video_details(channel_ids)

            # SQL query to create the 'Video' table
            mycursor.execute('''CREATE TABLE Video (Video_Id VARCHAR(255) primary key, 
                                Channel_Id VARCHAR(255), 
                                Video_Name VARCHAR(255),
                                Video_Description TEXT,
                                PublishedAt DATETIME,                                       
                                Views_Count INT,
                                Like_Count INT,
                                Favourite_Count INT,
                                Comment_Count INT, 
                                Duration INT,                    
                                Caption_Status VARCHAR(255))''')
            mydb.commit()       # Commit the transaction to save the table creation

            sqlFormula = '''INSERT INTO Video(Video_Id, Channel_Id, Video_Name, Video_Description, PublishedAt, Views_Count, Like_Count, Favourite_Count,
                            Comment_Count, Duration, Caption_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            # Preparing data for insertion into the 'Video' table
            val = []
            for video_data in video_details:

                # Parsing the published date string into a datetime object
                published_at_str = video_data.get('PublishedAt')
                published_at_datetime = datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%SZ') 

                # Parsing the duration string and convert it to seconds
                duration_str = video_data.get('Duration')
                duration_unit = duration_str[-1]  
                duration_value = int(re.findall(r'\d+', duration_str)[0])

                # Converting duration to seconds based on the unit (M=minutes, S=seconds)
                if duration_unit == 'M':
                    duration_in_seconds = duration_value * 60
                elif duration_unit == 'S':
                    duration_in_seconds = duration_value

                val.append((
                    video_data.get('Video_Id'), video_data.get('Channel_Id'), video_data.get('Video_Name'),
                    video_data.get('Video_Description'), published_at_datetime, video_data.get('Views_Count'),
                    video_data.get('Like_Count'), video_data.get('Favourite_Count'), video_data.get('Comment_Count'),
                    duration_in_seconds, video_data.get('Caption_Status')
                ))

            mycursor.executemany(sqlFormula, val)
            mydb.commit()
        else:
            print("Video table already exists.")

    except mysql.connector.Error as err:
        print("An error occurred:", err)
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# Calling the function to create the 'Video' table and populate it with data    
video_table()

# Function to create the 'Comment' table and populate it with data
def comment_table(a=None, b=None, c=None):
    try:   
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Suraaj121097",
            database="youtube_data"  
        )
        mycursor = mydb.cursor()

        # Check if the 'Comment' table already exists
        mycursor.execute("SHOW TABLES LIKE 'comment'")
        result = mycursor.fetchone()

        if not result:           
            channel_ids = ["UCqsRYAAtXopb8eK6SrK6duA", "UCQqmjKQBKQkRbWbSntYJX0Q", "UC-s0bfmR0JCVC2xRxYq_I5w", "UCxsQHU5SwYtO6uc1jiLdvrg",
                        "UC-1kzHtwBY8n0TY5NhYxNaw", "UCTwVVVVfsOkNfaxbCEkspOg", "UCgVq7NWVuHkf-nLujTS6jFA", "UCSZzkikEEdPJ6SIwTv-Jwdw",
                        "UCGKIAihHaivngERJKO7Le0A", "UCEkyvszqWQRsQLYPQdQ-wGw"]

            comment_details = get_comment_details(channel_ids)

            # SQL query to create the 'Comment' table
            mycursor.execute('''CREATE TABLE Comment (Comment_Id VARCHAR(255) primary key, 
                                Video_Id VARCHAR(255), 
                                Comment_Text TEXT,
                                Comment_Author VARCHAR(255),
                                Comment_PublishedAt DATETIME)''')
            mydb.commit()

            sqlFormula = '''INSERT INTO Comment (Comment_Id, Video_Id, Comment_Text, Comment_Author, Comment_PublishedAt) 
            VALUES (%s, %s, %s, %s, %s)'''

            val = []
            for video_data in comment_details:
                published_at_str = video_data.get('Comment_PublishedAt')
                published_at_datetime = datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%SZ')  # Assuming 'Z' for UTC
                
                val.append((
                    video_data['Comment_Id'],video_data['Video_Id'],video_data['Comment_Text'],video_data['Comment_Author'],
                    published_at_datetime
                ))

            mycursor.executemany(sqlFormula, val)
            mydb.commit()

            print("Comment table created successfully.")
        else:
            print("Comment table already exists.")

    except mysql.connector.Error as err:
        print("An error occurred:", err)
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# Calling the function to create the 'Comment' table and populate it with data
comment_table()

# Function to fetch and display channel details from the 'channel' table in the MySQL database.
def show_channel():
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Suraaj121097",
            database="youtube_data"
        )
    mycursor = mydb.cursor()
    
    # Executing a SQL query to select all data from the 'channel' table
    mycursor.execute("SELECT * FROM channel")
    myresult = mycursor.fetchall()

    data_list = []
    for x in myresult:
        data_list.append(x)

    # Defining column names to be used for the DataFrame
    desired_columns = ['Channel_Id', 'Channel_Name', 'Channel_Views', 'Channel_Description', 'Playlist_Id']

    # Creating a pandas DataFrame with the fetched data and the column names
    df_channeldetail = pd.DataFrame(myresult, columns = desired_columns)

    # Displaying the DataFrame in a Streamlit app
    return st.dataframe(df_channeldetail)

# Function to fetch and display video details from the 'video' table in the MySQL database.
def show_video():
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Suraaj121097",
            database="youtube_data"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM video")
    myresult2 = mycursor.fetchall()

    data_list2 = []
    for x in myresult2:
        data_list2.append(x)

    desired_columns2 = ['Video_Id','Channel_Id', 'Video_Name', 'Video_Description', 'PublishedAt', 'Views_Count', 'Like_Count', 'Favourite_Count',
                        'Comment_Count', 'Duration', 'Caption_Status']
    
    df_videodetail = pd.DataFrame(myresult2, columns = desired_columns2)
    return st.dataframe(df_videodetail)

# Function to fetch and display comment details from the 'comment' table in the MySQL database.
def show_comment():
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Suraaj121097",
            database="youtube_data"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM comment")
    myresult3 = mycursor.fetchall()

    data_list3 = []
    for x in myresult3:
        data_list3.append(x)

    desired_columns3 = ['Comment_Id','Video_Id', 'Comment_Text', 'Comment_Author', 'Comment_PublishedAt']

    df_commentdetail = pd.DataFrame(myresult3, columns = desired_columns3)
    return st.dataframe(df_commentdetail)

# Function to display all details (Channel, Video, Comment) using Streamlit
def tables():
    st.title("YouTube Channel Details")
    show_channel()
    
    st.title("YouTube Video Details")
    show_video()
    
    st.title("YouTube Comment Details")
    show_comment()
    return "Uploaded Successfully"

# Setting the title of the Streamlit app with styled text
st.title(":blue[YouTube Data Harvesting and Warehousing using SQL and Streamlit]")

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Suraaj121097",
    database = "youtube_data"
)
mycursor = mydb.cursor()

# Input field for the user to provide a channel ID
channel_id_user = st.text_input("Enter the Channel_ID")

# Determine the list of channel IDs to process
if channel_id_user:          # If the user provides a Channel ID
    channel_ids = [channel_id_user]
else:                        # Use default IDs if no input is provided
    channel_ids = ["default", "channel", "ids"]

# Button to trigger data collection and storage
if st.button("Collect and Store Data"):

    # Fetching existing Channel IDs from the database to avoid duplicates
    mycursor.execute("SELECT Channel_Id FROM channel")
    existing_channels = [x[0] for x in mycursor.fetchall()]

    # Processing only if the input Channel ID is not already in the database
    if channel_id_user not in existing_channels:
        try:

            # Fetching channel details using the provided Channel ID
            channel_data = get_channel_details(channel_id_user)
            if channel_data:           # Proceed if data is successfully fetched
                for channel_info in channel_data:

                    # Extracting channel details
                    channel_id = channel_info['Channel_Id']
                    channel_name = channel_info['Channel_Name']
                    channel_views = channel_info['Channel_Views']
                    channel_description = channel_info['Channel_Description']
                    playlist_id = channel_info['Playlist_Id']

                    # Inserting channel details into the database
                    sql = "INSERT INTO Channel (Channel_Id, Channel_Name, Channel_Views, Channel_Description, Playlist_Id) VALUES (%s, %s, %s, %s, %s)"
                    val = (channel_id, channel_name, channel_views, channel_description, playlist_id)
                    mycursor.execute(sql, val)
                    mydb.commit()   

                    # Fetching video details for the channel
                    video_data = get_video_details(channel_id_user)
                    if video_data:
                        for video_info in video_data:

                            # Convert publication time and duration to appropriate formats
                            published_at_str = video_info['PublishedAt']
                            published_at_datetime = datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%SZ')  

                            duration_str = video_info['Duration']
                            duration_unit = duration_str[-1]               # Last character indicates the unit (e.g., 'M', 'S')
                            duration_value = int(re.findall(r'\d+', duration_str)[0])

                            # Converting duration to seconds
                            if duration_unit == 'M':
                                duration_in_seconds = duration_value * 60
                            elif duration_unit == 'S':
                                duration_in_seconds = duration_value

                            # Extracting video details
                            video_id = video_info['Video_Id']
                            video_name = video_info['Video_Name']
                            video_description = video_info['Video_Description']
                            published = published_at_datetime
                            views_count = video_info['Views_Count']
                            like_count = video_info['Like_Count']
                            favourite_count = video_info['Favourite_Count']
                            comment_count = video_info['Comment_Count']
                            duration1 = duration_in_seconds
                            caption_status = video_info['Caption_Status']

                            # Inserting video details into the database
                            sql_video = """
                            INSERT INTO Video (Video_Id, Channel_Id, Video_Name, Video_Description, PublishedAt, 
                                            Views_Count, Like_Count, Favourite_Count, Comment_Count, Duration, Caption_Status)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            val_video = (video_id, channel_id, video_name, video_description, published, 
                                        views_count, like_count, favourite_count, comment_count, 
                                        duration1, caption_status)
                            mycursor.execute(sql_video, val_video)
                            mydb.commit()

                            # Fetching comment details for the video
                            comment_data = get_comment_details(video_id=video_id)
                            if comment_data:
                                for comment_info in comment_data:
                                    published_at_str = comment_info['Comment_PublishedAt']
                                    published_at_datetime = datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%SZ')  # Assuming 'Z' for UTC

                                    # Extracting comment details
                                    comment_id = comment_info['Comment_Id']
                                    video_id = comment_info['Video_Id']
                                    comment_text = comment_info['Comment_Text']
                                    comment_author = comment_info['Comment_Author']
                                    published = published_at_datetime

                                    # Inserting comment details into the database
                                    sql_comment = '''INSERT IGNORE INTO Comment (Comment_Id, Video_Id, Comment_Text, Comment_Author, Comment_PublishedAt) 
                                                    VALUES (%s, %s, %s, %s, %s)'''
                                    val_comment = (comment_id, video_id, comment_text, comment_author, published)
                                    mycursor.execute(sql_comment, val_comment)
                                    mydb.commit() 

                st.success(f"Data for Channel ID {channel_id_user} collected and stored successfully!")
            else:
                st.error("Failed to fetch data for the given Channel ID. Please check the ID and try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            print(e)

    mycursor.close()
    mydb.close()

    # Displaying tables in Streamlit
    Table = tables()
    st.success(Table)

# Radio button to allow the user to select which table to display
show_python_table = st.radio("Select the Table to Display",("Channels_Data","Video_Information","Comment_Information"))

# Check which table the user selected and call the respective function
if show_python_table == "Channels_Data":
    show_channel()
elif show_python_table == "Video_Information":
    show_video()
elif show_python_table == "Comment_Information":
    show_comment()

# Dropdown (selectbox) for users to choose a question to query
questions = st.selectbox("Choose the question",("1. What are the names of all the videos and their corresponding channels?",
                                                "2. Which channels have the most number of videos, and how many videos do they have?",
                                                "3. What are the top 10 most viewed videos and their respective channels?",
                                                "4. How many comments were made on each video, and what are their corresponding video names?",
                                                "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
                                                "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                                                "7. What is the total number of views for each channel, and what are their corresponding channel names?",
                                                "8. What are the names of all the channels that have published videos in the year 2022?",
                                                "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                                "10. Which videos have the highest number of comments, and what are their corresponding channel names?"))


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Suraaj121097",
    database = "youtube_data"
)
mycursor = mydb.cursor()

if questions == "1. What are the names of all the videos and their corresponding channels?":
    query1 = '''SELECT a.channel_name, b.video_name 
                FROM channel a 
                JOIN video b ON a.channel_id = b.channel_id'''
    mycursor.execute(query1)
    t1 = mycursor.fetchall()
    mydb.commit()
    df = pd.DataFrame(t1, columns=['Channel Name', 'Video Name'])
    st.write(df)

elif questions == "2. Which channels have the most number of videos, and how many videos do they have?":
    query2 = '''SELECT channel_name, COUNT(video_id) AS video_count 
                FROM channel a 
                JOIN video b ON a.channel_id = b.channel_id 
                GROUP BY channel_name 
                ORDER BY video_count DESC;'''
    mycursor.execute(query2)
    t2 = mycursor.fetchall()
    mydb.commit()
    df2 = pd.DataFrame(t2, columns=['Channel Name', 'Videos Count'])
    st.write(df2)

elif questions == "3. What are the top 10 most viewed videos and their respective channels?":
    query3 = '''SELECT channel_name, video_name, views_count
                FROM channel a
                JOIN video b ON a.channel_id = b.channel_id
                ORDER BY b.views_count DESC
                LIMIT 10;'''
    mycursor.execute(query3)
    t3 = mycursor.fetchall()
    mydb.commit()
    df3 = pd.DataFrame(t3, columns=['Channel Name', 'Videos Name', 'Views Count'])
    st.write(df3)

elif questions == "4. How many comments were made on each video, and what are their corresponding video names?":
    query4 = '''SELECT video_name, comment_count
                FROM video
                WHERE comment_count is not null;'''
    mycursor.execute(query4)
    t4 = mycursor.fetchall()
    mydb.commit()
    df4 = pd.DataFrame(t4, columns=['Videos Name', 'Comment Count'])
    st.write(df4)

elif questions == "5. Which videos have the highest number of likes, and what are their corresponding channel names?":
    query5 = '''SELECT channel_name, video_name, like_count
                FROM channel a
                JOIN video b ON a.channel_id = b.channel_id
                WHERE like_count is not null
                ORDER BY like_count DESC;'''
    mycursor.execute(query5)
    t5 = mycursor.fetchall()
    mydb.commit()
    df5 = pd.DataFrame(t5, columns=['Channel Name','Videos Name', 'Like Count'])
    st.write(df5)

elif questions == "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
    query6 = '''SELECT video_name, like_count
                FROM video;'''
    mycursor.execute(query6)
    t6 = mycursor.fetchall()
    mydb.commit()
    df6 = pd.DataFrame(t6, columns=['Videos Name', 'Like Count'])
    st.write(df6)

elif questions == "7. What is the total number of views for each channel, and what are their corresponding channel names?":
    query7 = '''SELECT channel_name, SUM(views_count) 
                FROM channel a
                JOIN video b ON a.channel_id = b.channel_id
                GROUP BY channel_name;'''
    mycursor.execute(query7)
    t7 = mycursor.fetchall()
    mydb.commit()
    df7 = pd.DataFrame(t7, columns=['Channel Name', 'Total View Count'])
    st.write(df7)

elif questions == "8. What are the names of all the channels that have published videos in the year 2022?":
    query8 = '''SELECT DISTINCT channel_name
                FROM channel a
                JOIN video b ON a.channel_id = b.channel_id
                WHERE YEAR(b.publishedat) = 2022;'''
    mycursor.execute(query8)
    t8 = mycursor.fetchall()
    mydb.commit()
    df8 = pd.DataFrame(t8, columns=['Channel Name'])
    st.write(df8)

elif questions == "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
    query9 = '''SELECT channel_name, AVG(duration)
                FROM channel a
                JOIN video b ON a.channel_id = b.channel_id
                GROUP BY channel_name;'''
    mycursor.execute(query9)
    t9 = mycursor.fetchall()
    mydb.commit()
    df9 = pd.DataFrame(t9, columns=['Channel Name', 'Average Duration'])
    st.write(df9)

elif questions == "10. Which videos have the highest number of comments, and what are their corresponding channel names?":
    query10 = '''SELECT channel_name, video_name, comment_count
                FROM channel a
                JOIN video b ON a.channel_id = b.channel_id
                ORDER BY comment_count DESC;'''
    mycursor.execute(query10)
    t10 = mycursor.fetchall()
    mydb.commit()
    df10 = pd.DataFrame(t10, columns=['Channel Name', 'Video Name', 'Comments Count'])
    st.write(df10)
