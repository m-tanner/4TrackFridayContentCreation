import os


class ConfigManager:
    def __init__(self):
        self.cloud_provider = os.environ["CLOUD_PROVIDER"]  # raises error if not found
        self.gcloud_project = os.environ.get("GCLOUD_PROJECT")
        self.static_4tf_bucket = os.environ.get("STATIC_4TF_BUCKET")
        self.spotify_client_id = os.environ.get("SPOTIFY_CLIENT_ID")
        self.spotify_client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
