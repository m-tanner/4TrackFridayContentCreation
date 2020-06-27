import base64
import json

import requests

from config_manager import ConfigManager


class SpotifyHandler:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.playlist_id = "720360kMd4LiSAVzyA8Ft4"
        self.base_request_uri = "https://api.spotify.com/v1/"
        self.base_authz_uri = "https://accounts.spotify.com/api/token"
        self.cached_token = None
        self.feature_set = {
            "acousticness",
            "danceability",
            "duration_ms",
            "energy",
            "instrumentalness",
            "liveness",
            "loudness",
            "tempo",
            "popularity",
            "valence",
        }
        self.overview_data = self._get_playlist_overview()
        self.playlist_tracks_data = self._get_playlist_tracks()
        self.track_dict = self._build_track_dict(self.playlist_tracks_data)
        self.track_features = self._get_track_features(list(self.track_dict.keys()))
        self.playlist_info = self._get_playlist_info()

    @property
    def token(self):
        if not self.cached_token:
            response = requests.post(
                self.base_authz_uri,
                headers={"Authorization": f"Basic {self._encoded_spotify_auth()}"},
                data={"grant_type": "client_credentials"},
            )
            if response.status_code != 200:
                return None

            self.cached_token = response.json()["access_token"]
        return self.cached_token

    def _encoded_spotify_auth(self):
        return base64.b64encode(
            (
                self.config.spotify_client_id + ":" + self.config.spotify_client_secret
            ).encode("utf-8")
        ).decode("utf-8")

    def _get_playlist_info(self):
        """
        Fetch data from Spotify API and build the playlist json data structure
        """
        for each in self.track_features:
            track_id = each["id"]
            self.track_dict[track_id]["features"] = each
        overview_dict = {k: v for k, v in self.overview_data.items()}
        overview_dict["playlist_count"] = len(self.track_dict.keys())
        overview_dict["track_breakdown"] = self.track_dict

        return overview_dict

    def _get_playlist_overview(self):
        overview_params = (
            "name,description,followers,owner(display_name),external_urls(spotify)"
        )

        response = requests.get(
            self.base_request_uri + f"playlists/{self.playlist_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            params={"fields": overview_params},
        )
        if response.status_code != 200:
            return "error fetching playlist overview"

        return response.json()

    def _get_playlist_tracks(self):
        """
        Get paginated data for all tracks
        """
        album_params = "album(name,release_date,images,album_type)"
        artist_params = "artists(name)"
        track_params = (
            "limit,next,offset,total,href,items(added_at,"
            f"track({album_params},{artist_params},name,release_date,duration_ms,explicit,external_urls,popularity,id))"
        )

        track_list = []
        response = requests.get(
            self.base_request_uri + f"playlists/{self.playlist_id}/tracks",
            headers={"Authorization": f"Bearer {self.token}"},
            params={"fields": track_params},
        )

        if response.status_code == 200:
            track_dict = response.json()
            track_list.extend(track_dict["items"])
            while track_dict["next"]:
                response = requests.get(
                    track_dict["next"],
                    headers={"Authorization": f"Bearer {self.token}"},
                    params={"fields": track_params},
                )
                if response.status_code == 200:
                    track_dict = response.json()
                    track_list.extend(track_dict["items"])

        return track_list

    def _get_track_features(self, song_ids):
        """
        Example response
            {
            "audio_features": [
              {
                "acousticness": 0.135,
                "analysis_url": "https://api.spotify.com/v1/audio-analysis/1PR1JQmuOmI3eD4isHeLlI",
                "danceability": 0.722,
                "duration_ms": 158276,
                "energy": 0.574,
                "id": "1PR1JQmuOmI3eD4isHeLlI",
                "instrumentalness": 0.000865,
                "key": 10,
                "liveness": 0.163,
                "loudness": -5.72,
                "mode": 0,
                "speechiness": 0.179,
                "tempo": 104.983,
                "time_signature": 4,
                "track_href": "https://api.spotify.com/v1/tracks/1PR1JQmuOmI3eD4isHeLlI",
                "type": "audio_features",
                "uri": "spotify:track:1PR1JQmuOmI3eD4isHeLlI",
                "valence": 0.337
              },
            }
        """
        pagination_list = [song_ids[i : i + 100] for i in range(0, len(song_ids), 100)]
        feature_list = []
        for songs in pagination_list:
            song_string = ",".join(songs)

            resp = requests.get(
                self.base_request_uri + "audio-features",
                headers={"Authorization": f"Bearer {self.token}"},
                params={"ids": song_string},
            )
            feature_list.extend(resp.json()["audio_features"])

        return feature_list

    @staticmethod
    def _build_track_dict(playlist_arr):
        track_dict = {}
        for track in playlist_arr:
            track_id = track["track"]["id"]
            track_dict[track_id] = track["track"]
        return track_dict

    def generate_per_feature_metrics(self):
        start_key = next(iter(self.playlist_info["track_breakdown"]))
        default_track = self.playlist_info["track_breakdown"].get(start_key)

        feature_map = dict.fromkeys(self.feature_set)
        for k, v in feature_map.items():
            feature_map[k] = {
                "min": default_track,
                "max": default_track,
                "sum": 0,
                "avg": 0,
            }

        # find the min, max, and avg for each feature
        for k, v in self.playlist_info["track_breakdown"].items():
            for feature_key, feature_val in feature_map.items():
                if feature_key == "popularity":
                    curr_feature = v[feature_key]
                    if curr_feature < feature_map[feature_key]["min"][feature_key]:
                        feature_map[feature_key]["min"] = v
                    if curr_feature > feature_map[feature_key]["max"][feature_key]:
                        feature_map[feature_key]["max"] = v
                    feature_map[feature_key]["sum"] += curr_feature
                else:
                    curr_feature = v["features"][feature_key]
                    if (
                        curr_feature
                        < feature_map[feature_key]["min"]["features"][feature_key]
                    ):
                        feature_map[feature_key]["min"] = v
                    if (
                        curr_feature
                        > feature_map[feature_key]["max"]["features"][feature_key]
                    ):
                        feature_map[feature_key]["max"] = v
                    feature_map[feature_key]["sum"] += curr_feature

        for k, v in feature_map.items():
            feature_map[k]["avg"] = round(
                feature_map[k]["sum"]
                / len(self.playlist_info["track_breakdown"].keys()),
                2,
            )

        with open("./resources/metrics/metrics.json", "w+", encoding="utf-8") as f:
            json.dump(feature_map, f, ensure_ascii=False, indent=4)
