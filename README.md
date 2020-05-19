# cache_anthology
A collection of cache implementations in python.

## LRU cache

### Usage

Clone the repo: `git clone git@github.com:jayakrishnandingit/cache_anthology.git`

```
>> from cache_anthology.lru import Cache as LRUCache

>> cache = LRUCache()
>> cache.set('name', 'George Clooney')
>> cache.get('name')
George Clooney
>> cache.delete('name')
```

### Running tests

```
>> cd cache_anthology
>> python3 -m unittest
```
