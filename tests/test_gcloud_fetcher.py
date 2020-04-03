from src.gcloud_fetcher import GCloudFetcher


def test_aws_fetcher():
    fetcher = GCloudFetcher()

    real_subscribers = fetcher.fetch_real_subscribers()
    assert type(real_subscribers) is list
    assert real_subscribers

    test_subscribers = fetcher.fetch_test_subscribers()
    assert type(test_subscribers) is list
    assert test_subscribers
