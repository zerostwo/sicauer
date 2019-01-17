import requests


class HTTP:
    def get(self, url, return_json=True):
        """
        Get api.
        :param url:
        :param return_json:
        :return:
        """
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
