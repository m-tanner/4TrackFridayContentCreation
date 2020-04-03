import os


class ConfigManager:
    def __init__(self):
        self.cloud_provider = os.environ["CLOUD_PROVIDER"]
