from src.config_manager import ConfigManager


def test_config_manager():
    config = ConfigManager()
    assert config.cloud_provider
    assert config.gcloud_project
    assert config.static_4tf_bucket
