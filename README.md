EXEMPLE
--------
This repo is used to diplay a small example of usage of OWAF to give an idea to what can be done with it

# <img src="https://github.com/OWAF-Only-Web-Async-Framework/OWAF-Exemple/assets/63317845/36712a27-bbff-4b87-b4c8-e5988141015a" alt="" width="25"/> OWAF-core
OWAF Core is a lightweight performance oriented ASGI web application framework. It is designed to fullfill needs of scalability and modularity while staying as easy to understand as possible and enforcing typing and documenting as much as possible while not being too intrusive. This project started as an extension of quart "without flask" but as quickly derived from it. The philosophy of this framework is makes you able to still use all the things you know about Flask and Quart while also giving new approches for bigger applications that are segmented and/or modulable.

# Two simple exemple
Using the OWAF approach (aimed at bigger project).
```python
from OWAF import Shard

def somewrapper(arg1: int):
    def wrapper(func: callable):
        async def inner(*args, **kwargs):
            print('test1', g)
            return await func(*args, **kwargs)
        return inner
    return wrapper

class Index(Shard):
  shard_decorators = [somewrapper]

  async def hello(self):
      """:route: GET: /"""
      return await self.render_template("index.html")

  async def json(self):
      """
      :route: GET, POST: /api 
      :somewrapper: arg1=1
        :route: POST: /api2
      :end somewrapper:
      """
      return {"hello": "world"}

  async def websocket(self):
    """:websocket: /websocket"""
      while True:
          await self.websocket.send("hello")
          await self.websocket.send_json({"hello": "world"})

if __name__ == "__main__":
    Shard(debug=True, auto_import='other_stuff')
```

Keeping the quart approach (aimed to smaller sized projects and standalone controllers).
```python
from OWAF import OnlyWebAsync, render_template, websocket
from other_stuff.a import Home
from other_stuff.b import OtherHome

def somewrapper(arg1: int):
    def wrapper(func: callable):
        async def inner(*args, **kwargs):
            print('test1', g)
            return await func(*args, **kwargs)
        return inner
    return wrapper

app = OnlyWebAsync(__name__)

@app.route("/index/")
async def hello():
    return await render_template("index.html")

@app.route("/index/api2", methods=["POST"])
@somewrapper(arg1 = 1) 
async def json():
    return {"hello": "world"}

@app.route("/index/api", methods=["GET, POST"])
async def json():
    return {"hello": "world"}

@app.websocket("/index/websocket")
async def websocket():
    while True:
        await websocket.send("hello")
        await websocket.send_json({"hello": "world"})

if __name__ == "__main__":
    app.run()
```

# The strength of OWAF
In another file it is perfectly possible to use another Shard instance or class element without any form of import or python's gymnastic.
```python
from OWAF import Shard
# other_stuff/a.py

class Home(Shard):
    async def home(self):
        """
        :somewrapper: arg1=2
        :route: GET: /
        :end somewrapper:
        """
        return self.env.index.hello()

from OWAF import Shard
# other_stuff/b.py

class OtherHome(Shard):
    async def home(self):
        """
        :somewrapper: arg1=2
        :route: GET: /
        :end somewrapper:
        """
        return await self.env.index.hello()
```
