# HexShell

A simple webshell written in Python3 using [http.server](https://docs.python.org/3/library/http.server.html)

---

```diff
- Warning: http.server is not recommended for production.
```

It only implements [basic security checks](https://docs.python.org/3/library/http.server.html#http-server-security).

---

## Getting started

Define your password in [main.py](https://github.com/Falcn8/HexShell/blob/master/main.py#L8)

Run `main.py`

When a POST request is made it will append data of the request in `hexshell.access.log`
