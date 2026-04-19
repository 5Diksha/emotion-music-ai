import subprocess
from recommender import get_recommendations

result = subprocess.check_output(["python", "emotion.py"], text=True)
emotion = result.split("Final Emotion:")[-1].strip()

print("Detected Emotion:", emotion)

songs, playlists = get_recommendations(emotion)

print("\nSongs:")
for s in songs:
    print(s)

print("\nPlaylists:")
for p in playlists:
    print(p)