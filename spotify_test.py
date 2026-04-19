from recommender import get_recommendations

songs, playlists = get_recommendations("happy hindi")

print("Songs:")
for s in songs:
    print(s)

print("\nPlaylists:")
for p in playlists:
    print(p)