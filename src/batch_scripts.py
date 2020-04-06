import os

from src.config_manager import ConfigManager
from src.content_merger import merge
from src.gcloud_uploader import GCloudUploader


def batch_edit():
    batch_merge()
    batch_upload()


def batch_merge():
    for file in os.listdir("resources/episodes"):
        print(f"Merging {file}...")
        merge(
            path_to_template="resources/template_web.html",
            path_to_content=f"resources/episodes/{file}",
            path_to_output_directory="resources/polished_episodes",
        )


def batch_upload():
    uploader = GCloudUploader(config=ConfigManager())
    for file in os.listdir("resources/polished_episodes"):
        print(f"Uploading {file}...")
        uploader.upload(f"resources/polished_episodes/{file}")
        uploader.tag(f"resources/polished_episodes/{file}")
