from src.aws_uploader import AWSUploader
from src.config_manager import ConfigManager
from src.gcloud_uploader import GCloudUploader


class UploaderFactory:
    def __init__(self, config: ConfigManager):
        self._config = config

    def get_uploader(self):
        if self._config.cloud_provider == "AWS":
            return AWSUploader()
        if self._config.cloud_provider == "gcloud":
            return GCloudUploader(config=self._config)
        raise RuntimeError(
            "CLOUD_PROVIDER was missing from your environment or "
            "didn't match any known options."
        )
