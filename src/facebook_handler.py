import requests

from config_manager import ConfigManager


class FacebookHandler:
    def __init__(self, config: ConfigManager):
        self.page_id = config.fb_page_id
        self.access_token = config.fb_access_token

    def post(self, message: str, link: str):
        host = "https://graph.facebook.com"
        version = "v8.0"
        endpoint = f"/{version}/{self.page_id}/feed?message={message}&link={link}&access_token={self.access_token}"
        response = requests.post(
            f"{host}{endpoint}"
        )
        assert response.status_code == 200
