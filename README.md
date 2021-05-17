# 开黑啦机器人

## 介绍

khlbot是[开黑啦](https://www.kaiheila.cn)的一款机器人框架，支持协程和多进程

## 使用机器人

### 创建机器人实例

```python
from khlbot import Bot

bot = Bot(token="", _config={})
```

创建是机器人时，`token`是必须的（目前只支持websocket），同时接收一个包含配置信息的dict对象，目前支持如下配置项：

+ `MAX_PROCESSING_NUMBER`: 工作进程的最大数目，默认为cpu的核心数
+ `MAX_CONSUMER_NUMBER`: 每个工作进程中的消费者数目，消费者都是协程， 所以一个进程中可以运行多个，默认为4
+ `MAX_EVENT_QUEUE_SIZE`: 事件队列的最大长度，从KHL接收的消息都会先放入事件队列，默认为10000
+ `PROCESSING_IDLE_TIMEOUT`: 工作进程的最大空闲时间，默认为60秒，当工作进程长时间没有处理消息时，将自动关闭进程中的所有消费者以节省资源

默认配置如下：

```python
import os

{
    "MAX_PROCESSING_NUMBER": os.cpu_count(),
    "MAX_CONSUMER_NUMBER": 4,
    "MAX_EVENT_QUEUE_SIZE": 10000,
    "PROCESSING_IDLE_TIMEOUT": 60
}
```

### 设置机器人任务

```python
from khlbot import Commander

commander = Commander(prefix="-")
```

`Commander`类用来设置指令以及各种任务的设置，实例化`Commander`时需要指定一个前缀

#### 添加指令

```python
@commander.command("hello", "name", "id")
async def handle_function(name, _id, **kwargs):
    pass
```

添加指令可以使用`commander.command`修饰器，修饰器的第一个参数应该为 具体的指令， 其后便是指令的参数 ，机器人解析命令后将会把解析到的参数按修饰器中的顺序传给`handle_function`
。除此之外，`handle_function`还接收一个`kwargs`，用于传递额外的信息，在任何时候，都可以通过`kwargs["event"]`来获取完整的事件对象（可按json对象使用)。
> 注意，`handle_function`必须使用`async def`来定义

修饰器可以对同一个`handle_function`多次使用，而且可以用类似`functools.partial`的方法来设置偏函数的参数，如：

```python
@commander.command("hello", partial=(1,))
@commander.command("hello2", partial=(2,))
def handle_function(_type):
    print(_type)
```

> 注意：`partial`中的参数将会按顺序自动传递到`handle_function`的最前面

#### 添加周期任务

周期任务可以使用`commander.interval`修饰器来创建：

```python
@commander.interval(period=5, times=10)
async def handle_function():
    pass
```

修饰器只接收两个参数:

+ `period`: 运行周期，单位为秒
+ `times`: 运行的次数，如果为0则表示没有次数限制

> 周期任务没有额外的`kwargs`

#### 订阅系统消息

订阅系统消息可以使用`commander.subscribe`修饰器：

```python
import khlbot.config as CONFIG


@commander.subscribe(_type=CONFIG.KHL_EVENT_TYPE_GUILD_MEMBER_ONLINE, conditions={})
async def handle_function(**kwargs):
    pass
```

修饰器接收两个参数：

+ `_type`: 系统消息的类型
+ `conditions`: 过滤系统消息的条件

> 订阅任务有额外的`kwargs`，可以通过`kwargs["event"]`来获取完整的事件对象（可按json对象使用）。

## TODO
+ [ ] 完善周期任务的过滤条件
+ 封装接口:
  + [x] 服务器相关接口
  + [ ] 频道相关接口
  + [x] 频道消息相关接口
  + [ ] 私信聊天会话接口
  + [ ] 用户私聊消息接口
  + [ ] 用户相关接口
  + [ ] 媒体模块
  + [ ] 服务器角色权限相关接口
  + [ ] 亲密度相关接口
  + [ ] 服务器表情相关接口
  
+ 封装事件结构：
  + [ ] 频道相关事件
  + [ ] 私聊消息事件
  + [ ] 服务器成员相关事件
  + [ ] 服务器角色相关事件
  + [ ] 服务器相关事件
  + [ ] 消息相关事件
  + [ ] 用户相关事件

## 使用样例
见 `sample.py`