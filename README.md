# onsen-api

A python library for [Onsen(音泉)](http://onsen.ag) API.

## Feature
- Get current available program list
- Get information of program
- Download a program

## installation

```
pip install pipenv
pipenv install
```

## Sample
```python
from onsen_api.client import OnsenClient

# create a client
c = OnsenClient()

# get current available program list
l = c.shown_moives()
print(l[0])

# download a program
m = c.moive_info('wa2')
print(m.download_url)
print('start download')
m.download('wa2.mp3')
```
