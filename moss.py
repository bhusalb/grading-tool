import requests as req
import os

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
basic = HTTPBasicAuth(os.getenv('MOSS_USER'), os.getenv('MOSS_PASSWORD'))


def get_moss_results(lab):
    d = req.get(f"{os.getenv('MOSS_URL')}/lab{lab}/results/", auth=basic)
