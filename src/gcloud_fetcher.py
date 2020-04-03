import json
from typing import List

from google.cloud import storage

from src.fetcher import Fetcher
from src.subscriber import Subscriber


class GCloudFetcher(Fetcher):
    def __init__(self):
        self.bucket = storage.Client(project="four-track-friday-2").bucket(
            bucket_name="static.4trackfriday.com"
        )

    def fetch_real_subscribers(self) -> List[Subscriber]:
        return self.fetch_subscribers(
            path_to_names_and_emails="subscribers/real_email_list.json"
        )

    def fetch_test_subscribers(self) -> List[Subscriber]:
        return self.fetch_subscribers(
            path_to_names_and_emails="subscribers/test_email_list.json"
        )

    def fetch_subscribers(self, path_to_names_and_emails: str) -> List[Subscriber]:
        names_and_emails = json.loads(
            self.fetch_string_content(episode_key=path_to_names_and_emails)
        )
        subscribers = []
        for name, email in names_and_emails.items():
            subscribers.append(Subscriber(name=name, email=email))
        return subscribers

    def fetch_string_content(self, episode_key: str) -> str:
        return (
            storage.blob.Blob(name=episode_key, bucket=self.bucket)
            .download_as_string()
            .decode("utf-8")
        )
