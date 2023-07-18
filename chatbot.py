from lastfmapi import LastFmApi
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Initialize Last.fm API
lastfm = lastfmapi.LastFmApi(api_key='f0a4709f10dbf6ff38b3c0ef3140a78d')

# Initialize IBM Watson NLU
authenticator = IAMAuthenticator('RXseO2bOBlYskqp7j-_pdWXpHZuO8IsFSvoDIKkPQgt9')
nlu = NaturalLanguageUnderstandingV1(version='2021-09-01', authenticator=authenticator)
nlu.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/3adb63f8-7305-48ec-90a2-bc2dd55c8c22')

# Function to get song recommendations based on user input
def get_song_recommendations(user_input):
    # Use IBM Watson NLU to analyze user input emotions
    response = nlu.analyze(
        text=user_input,
        features=Features(emotion=EmotionOptions())).get_result()
    emotions = response['emotion']['document']['emotion']

    # Use Last.fm API to get song recommendations based on user input emotions
    top_tracks = lastfm.chart_getTopTracks(limit=5)
    recommended_songs = []
    for track in top_tracks:
        song_emotions = lastfm.track_getInfo(artist=track.artist['name'], track=track.title)['toptags']
        song_emotions = [emotion['name'] for emotion in song_emotions]
        if any(emotion in song_emotions for emotion in emotions):
            recommended_songs.append(track.title)

    return recommended_songs

# User input
user_input = "I'm feeling happy and energetic"

# Get song recommendations based on user input
recommendations = get_song_recommendations(user_input)

# Print the recommended songs
if recommendations:
    print("Recommended songs:")
    for song in recommendations:
        print(song)
else:
    print("No songs found that match your input")

