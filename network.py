import requests

class BlacklistDownloader:
    def __init__(self, url, username, password):
        self.url = url
        self.auth = (username, password)

    def fetch_blacklist(self):
        response = requests.get(self.url, auth=self.auth, timeout=10)
        response.raise_for_status()
        return {line.strip() for line in response.text.splitlines() if line.strip()}