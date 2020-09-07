# onsen_api

*Note: This script is updated for the current version of onsen.ag. Enjoy~*

A python library for [Onsen(音泉)](http://onsen.ag) API.

## Feature

- Get current available program list
- Get information of program
- Download a program

## Installation

```shell
pip install pipenv
pipenv install
```

## Sample

```python
from onsen_api import OnsenClient

# create a client
c = OnsenClient()

# get current available program list
l = c.program_list()
print(l['kokuradio'])

# download a program
m = c.get_program('kokuradio')
print(m.download_url)
print('start download')
m.download_latest()
```
