import re
import requests
import pandas as pd

from io import StringIO
from html import unescape

def clean_comment_text(text):
    text = unescape(text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_video_comments(video_id, video_title, api_key):
    url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=20'

    response = requests.get(url)

    if response.status_code == 200:
        comments_data = response.json()
        comments = []

        for item in comments_data.get('items', []):
          comment = item['snippet']['topLevelComment']['snippet']
          comments.append({
                'video_id': video_id,
                'video_title': video_title,
                'author': comment['authorDisplayName'],
                'text': clean_comment_text(comment['textDisplay']),
                'published_at': comment['publishedAt'],
                'like_count': comment['likeCount']
                })
          
        return comments

    else:
        print(f"Failed to retrieve comments. HTTP Status Code: {response.status_code}")
        return []

def get_video_ids_and_titles_from_playlist(playlist_id, api_key):

    url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key={api_key}&maxResults=50'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        video_details = [(item['snippet']['resourceId']['videoId'], item['snippet']['title']) for item in data['items']]
        return video_details
    else:
        print(f"Failed to retrieve video IDs and titles. HTTP Status Code: {response.status_code}")
        return []
    
def extract_transform_data(playlist_id, api_key):
    vid_infs = get_video_ids_and_titles_from_playlist(playlist_id, api_key)

    all_comments = []
    for video_id, video_title in vid_infs:
        all_comments.extend(get_video_comments(video_id, video_title, api_key))
    
    return all_comments
