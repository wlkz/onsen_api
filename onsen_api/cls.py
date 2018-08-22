import abc
import json

from .errors import ProgramNotFoundException, UnexpectedResponseException
from .urls import GET_MOIVE_INFO_URL, SHOWN_MOVIE_URL
from .utils import download_from_url


class Base(abc.ABC):
    def __init__(self, id, session):
        self._id = id
        self._session = session
        self._data = None

    def refresh(self):
        self._get_data()

    @property
    @abc.abstractmethod
    def _url(self):
        return ''

    @property
    def _method(self):
        return 'GET'

    @property
    def data(self):
        if self._data is None:
            self._get_data()
        return self._data

    def _get_data(self):
        res = self._session.request(self._method, self._url)
        try:
            self._data = res.json()
        except json.JSONDecodeError as e:
            raise UnexpectedResponseException(
                self._url, e.msg, 'a json dict')

    def __getitem__(self, k):
        return self.data[k]

    def __repr__(self):
        id_ = '' if self._id is None else ' ' + self._id
        return '<{}{}>'.format(type(self).__name__, id_)

    __str__ = __repr__


class MoiveInfo(Base):
    def _parser(self, text):
        # callback({....}) -> dict
        t = text.lstrip('callback(').rstrip(');\n')
        ret = json.loads(t)
        return ret

    @property
    def _url(self):
        return GET_MOIVE_INFO_URL + self._id

    def _get_data(self):
        import json
        res = self._session.request(self._method, self._url)
        if res.status_code == 404:
            raise ProgramNotFoundException(self._id)
        try:
            self._data = self._parser(res.text)
        except json.JSONDecodeError as e:
            raise UnexpectedResponseException(
                self._url, e.msg, 'a json dict')

    @property
    def download_url(self):
        return self['moviePath']['pc']

    def download(self, path):
        download_from_url(self.download_url, path)
        # with open(path, 'wb') as f:
        #     f.write(self._session.get(self.download_url()).content)


class ShownMoives(Base):
    @property
    def _url(self):
        return SHOWN_MOVIE_URL

    def _get_data(self):
        super()._get_data()
        self._data = self._data['result']

    def __iter__(self):
        for m in self.data:
            yield MoiveInfo(m, self._session)

    def __getitem__(self, k):
        program_name = self.data[k]
        return MoiveInfo(program_name, self._session)
