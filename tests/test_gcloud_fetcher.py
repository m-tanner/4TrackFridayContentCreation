from src.config_manager import ConfigManager
from src.gcloud_fetcher import GCloudFetcher


def test_aws_fetcher():
    fetcher = GCloudFetcher(config=ConfigManager())

    real_subscribers = fetcher.fetch_real_subscribers()
    assert isinstance(real_subscribers, list)
    assert real_subscribers

    test_subscribers = fetcher.fetch_test_subscribers()
    assert isinstance(test_subscribers, list)
    assert test_subscribers
