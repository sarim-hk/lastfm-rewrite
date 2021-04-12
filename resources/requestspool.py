import requests
import threading
from PIL import Image

class ImageRequestPool:
    def __init__(self, url_list):
        self._url_list = url_list
        self._return_list = []
        self.main()

    def main(self):
        self.create_threads()

        while len(self._return_list) != len(self._url_list):
            pass
        self._return_list = sorted(self._return_list, key=lambda x: x[1])

    def create_threads(self):
        index = 0
        for url in self._url_list:
            thread = threading.Thread(target=self.get_image, args=(url, index))
            thread.start()
            index += 1

    def get_image(self, url, index):
        try:
            req = Image.open(requests.get(url, stream=True).raw)
        except Exception:
            req = Image.new('RGB', (300,300))
        self._return_list.append([req, index])

    @property
    def output(self):
        return self._return_list


if __name__ == "__main__":
    url_list = []
    placeholder_url = "https://via.placeholder.com/"

    for i in range(275, 325, 1):
        url_list.append(placeholder_url+str(i))

    pool = ImageRequestPool(url_list)
