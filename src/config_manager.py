import os


class ConfigManager:
    def __init__(self):
        self.cloud_provider = os.environ["CLOUD_PROVIDER"]  # raises error if not found
        self.gcloud_project = os.environ.get("GCLOUD_PROJECT")
        self.static_4tf_bucket = os.environ.get("STATIC_4TF_BUCKET")
