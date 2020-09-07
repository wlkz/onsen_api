import abc
import json
import subprocess

from .errors import ProgramNotFoundException, UnexpectedResponseException
from .urls import PROGRAMS_URL
from .utils import download_from_url


class Base:
    def __init__(self, id):
        self._id = id
        self._data = None

    @property
    def data(self):
        return self._data

    def __getitem__(self, k):
        return self.data[k]

    def __repr__(self):
        id_ = '' if self._id is None else ' ' + self._id
        return '<{}{}>'.format(type(self).__name__, id_)

    __str__ = __repr__


class RemoteBase(Base):
    _url = ''
    _method = 'GET'

    def __init__(self, id, session):
        super().__init__(id)
        self._session = session

    def refresh(self):
        self._get_data()

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
                self._url, res, 'a json dict')


class ProgramList(RemoteBase):
    _url = PROGRAMS_URL

    def _get_data(self):
        super()._get_data()
        d = {}
        for p in self._data:
            d[p['directory_name']] = Program.from_program_list_item(
                p, self._session)
        self._data = d

    def __iter__(self):
        return self.data.values()


class Program(RemoteBase):
    program_key = (
        'id',
        'directory_name',
        'program_info',
        'topics',
        'pickups',
        'current_episode',
        'personality_groups',
        'events',
        'selling_items',
        'galleries',
        'corners',
        'performers',
        'contents',
    )

    def _get_data(self):
        old_data = None
        if self._data:
            old_data = self._data

        try:
            super()._get_data()
        except UnexpectedResponseException as e:
            if e.res.status_code == 404:
                raise ProgramNotFoundException(self._id)
            raise e
        
        if old_data:
            old_data.update(self._data)
            self._data = old_data
        
        self.process_contents()

    def __getitem__(self, k):
        if k in self.program_key:
            out = self.data.get(k)
            if out is None:
                self._get_data()
            return self.data[k]

    @classmethod
    def from_program_list_item(cls, item, session):
        instance = cls(item['directory_name'], session)
        data = {}
        for k, v in item.items():
            if k in cls.program_key:
                data[k] = v
            else:
                data['program_info'] = v

        instance._data = data
        return instance

    def process_contents(self):
        contents = [Episode.from_content(self._id, c) for c in self._data['contents']]
        self._data['contents'] = contents

    def download_latest(self, target=None):
        self.data['contents'][0].download(target)

    @property
    def _url(self):
        return f'{PROGRAMS_URL}/{self._id}'


class Episode(Base):
    @classmethod
    def from_content(cls, program_id, content):
        date = content["delivery_date"].replace('/', '.')
        out = cls(f'{program_id}_{date}')
        out._data = content
        return out

    @property
    def can_download(self):
        return not self['streaming_url'] is None

    @property
    def download_url(self):
        return self['streaming_url']

    def download(self, target=None):
        if target is None:
            target = f'{self._id}.mp4'
        if self.can_download:
            subprocess.run(
                ['ffmpeg', '-i', self.download_url, '-c', 'copy', target])
        else:
            raise NotImplementedError(
                'premium episode does not support in this version')
