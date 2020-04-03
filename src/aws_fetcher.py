from typing import List

import boto3

from src.fetcher import Fetcher
from src.subscriber import Subscriber


class AWSFetcher(Fetcher):
    def __init__(self):
        self.s3 = boto3.client("s3")

    def fetch_real_subscribers(self) -> List[Subscriber]:
        pass

    def fetch_test_subscribers(self) -> List[Subscriber]:
        pass
