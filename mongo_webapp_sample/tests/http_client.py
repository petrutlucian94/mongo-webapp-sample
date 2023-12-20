import requests

from mongo_webapp_sample import exception


class HttpClient:
    def __init__(self, endpoint, timeout=None):
        self._session = requests.Session()

        self._base_url = endpoint
        self._timeout = timeout

    def set_timeout(self, timeout):
        self._timeout = timeout

    def request(self, url, method, **kwargs):
        if url.startswith('/'):
            if not self._base_url:
                raise ValueError("No API url specified.")

            url = '/'.join((self._base_url.strip('/'),
                            url.strip('/')))

        if self._timeout and not kwargs.get('timeout'):
            kwargs['timeout'] = self._timeout

        response = self._session.request(method, url, **kwargs)
        if not response.ok:
            raise exception.RequestFailed(
                code=response.status_code,
                details=response.text)

        return response

    def get(self, url, **kwargs):
        return self.request(url, 'GET', **kwargs)

    def head(self, url, **kwargs):
        return self.request(url, 'HEAD', **kwargs)

    def post(self, url, **kwargs):
        return self.request(url, 'POST', **kwargs)

    def put(self, url, **kwargs):
        return self.request(url, 'PUT', **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, 'DELETE', **kwargs)
