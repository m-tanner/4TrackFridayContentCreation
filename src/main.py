import os

from src.config_manager import ConfigManager
from src.fetcher_factory import FetcherFactory
from src.sender import Sender
from src.uploader_factory import UploaderFactory


def main():
    config = ConfigManager()
    fetcher = FetcherFactory(config=config).get_fetcher()
    subscribers = fetcher.fetch_real_subscribers()
    sender = Sender(
        path_to_email_content=os.path.join("resources/episodes", "3Apr20_email.html")
    )
    sender.send_to(subscribers=subscribers)
    uploader = UploaderFactory(config=config).get_uploader()
    uploader.upload(path_to_file=os.path.join("resources/episodes", "3Apr20_web.html"))
    uploader.tag(path_to_file=os.path.join("resources/episodes", "3Apr20_web.html"))


if __name__ == "__main__":
    main()
