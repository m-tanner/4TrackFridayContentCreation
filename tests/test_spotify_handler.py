from collections import Counter

from src.config_manager import ConfigManager
from src.spotify_handler import SpotifyHandler


def test_spotify_handler():
    config = ConfigManager()

    spotify_handler = SpotifyHandler(config=config)
    spotify_handler.generate_per_feature_metrics()
    genres = []
    for value in spotify_handler.track_dict.values():
        for artist in value.get("artists"):
            genre = spotify_handler.get_artist_genres(artist.get("id"))
            print(f"{artist.get('name')}: {genre}")
            genres.append(genre or ["empty"])
    counter = Counter([genre for sublist in genres for genre in sublist])
    print(counter)


if __name__ == '__main__':
    test_spotify_handler()
