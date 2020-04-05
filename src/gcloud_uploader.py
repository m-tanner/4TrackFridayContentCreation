from bs4 import BeautifulSoup
from google.cloud import storage

from src.config_manager import ConfigManager
from src.uploader import Uploader


class GCloudUploader(Uploader):
    def __init__(self, config: ConfigManager):
        self.bucket = storage.Client(project=config.gcloud_project).bucket(
            bucket_name=config.static_4tf_bucket
        )

    def upload(self, path_to_file: str) -> None:
        file_name = self.get_file_name(path_to_file)
        with open(path_to_file, "rb") as html_file:
            storage.blob.Blob(
                name=f"episodes/{file_name}", bucket=self.bucket
            ).upload_from_file(file_obj=html_file, content_type="text/html")

    def tag(self, path_to_file: str) -> None:
        file_name = self.get_file_name(path_to_file)
        with open(path_to_file, "r") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")
            author = soup.select("[name~=author]")[0].attrs.get("content")
            episode = soup.select("[name~=episode]")[0].attrs.get("content")
            date = soup.select("[name~=date]")[0].attrs.get("content")
        blob = storage.blob.Blob(name=f"episodes/{file_name}", bucket=self.bucket)
        blob.metadata = {
            "author": author,
            "episode": episode,
            "date": date,
        }
        blob.patch()

    @staticmethod
    def get_file_name(path_to_file: str) -> str:
        return path_to_file.split("/")[-1]
