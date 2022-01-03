import os

from src.config_manager import ConfigManager
from src.fetcher_factory import FetcherFactory
from src.sender import Sender
from src.uploader_factory import UploaderFactory
from src.content_merger import merge


def main(episode_name: str) -> None:
    config = ConfigManager()

    fetcher = FetcherFactory(config=config).get_fetcher()
    subscribers = fetcher.fetch_real_subscribers()

    email = merge(
        path_to_template="resources/template_email.html",
        path_to_content=f"resources/episodes/{episode_name}.html",
    )
    sender = Sender(email_content=email)
    sender.send_to(subscribers=subscribers)

    merge(
        path_to_template="resources/template_web.html",
        path_to_content=f"resources/episodes/{episode_name}.html",
        path_to_output_directory=f"resources/polished_episodes",
    )

    uploader = UploaderFactory(config=config).get_uploader()
    uploader.upload_episode(
        path_to_file=os.path.join("resources/polished_episodes", f"{episode_name}.html")
    )
    uploader.tag_episode(
        path_to_file=os.path.join("resources/polished_episodes", f"{episode_name}.html")
    )


if __name__ == "__main__":
    main(episode_name="")
