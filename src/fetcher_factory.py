from src.aws_fetcher import AWSFetcher
from src.config_manager import ConfigManager
from src.gcloud_fetcher import GCloudFetcher


class FetcherFactory:
    def __init__(self, config: ConfigManager):
        self._config = config

    def get_fetcher(self):
        if self._config.cloud_provider == "AWS":
            return AWSFetcher()
        elif self._config.cloud_provider == "gcloud":
            return GCloudFetcher()
        return RuntimeError(
            "CLOUD_PROVIDER was missing from your environment or "
            "didn't match any known options."
        )
