Requirements
------------
* [Serpent](https://github.com/ethereum/serpent)
* [pyethereum](https://github.com/ethereum/pyethereum) Python Ethereum (needed to run tests)


#### Running tests

Exclude slow tests:
```
py.test test/ -s -m "not slow"
```

Run slow tests without veryslow tests
```
py.test test/ -s -m "slow and not veryslow"
```

All tests:
```
py.test test/ -s
```
