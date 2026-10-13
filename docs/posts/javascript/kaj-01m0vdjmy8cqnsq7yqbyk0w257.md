---
title: "设计一个 ChatStream class"
description: "如果让我设计一个ChatStream class，我会把 ChatStream 定义成一个负责流式通信的类，它主要维护请求状态、读取流、解析数据、取消请求以及通知外部。内部通过 fetch 获取 ReadableStream，再通过 Tex"
date: "2026-09-23"
publishedAt: "2026-09-23T09:44:23.380994+08:00"
source: "https://kajspace.cn/articles/01M0VDJMY8CQNSQ7YQBYK0W257/"
tags: ["前端"]
---

# 设计一个 ChatStream class

如果让我设计一个ChatStream class，我会把 ChatStream 定义成一个负责流式通信的类，它主要维护请求状态、读取流、解析数据、取消请求以及通知外部。内部通过 fetch 获取 ReadableStream，再通过 TextDecoder 读取 chunk。数据解析我会单独抽象成 parser，避免把 SSE 格式写死在 ChatStream 里。ChatStream 通过 message、done、error 等事件把结果通知给外部，Vue 组件只需要订阅这些事件并更新响应式数据，这样通信层和 UI 层就是解耦的。

从职责上，我会把它拆成几个部分：  
第一部分是**请求管理**，比如保存请求地址、请求参数、headers，以及通过AbortController管理请求取消。

第二部分**流式读取。**发送请求以后，通过response.body.getReader()不断读取服务端返回的chunk，再通过TextDecoder把二进制数据转换成字符串。

第三部分是**数据解析**。因为后端可能返回SSE、JSON Lines或者其他协议，所以我不会把解析逻辑直接写死再ChatStream里面，而是抽象成parser，这样以后更换协议的时候不用修改核心逻辑。

第四部分是**事件通知**。比如提供message、done、error这些事件，让组件只需要订阅事件就可以实时更新消息内容，这样ChatStream和UI就解耦了。  
第五部分是**生命周期管理**，比如start（）、abort（）、destroy（），同时维护idle，connecting、streaming、done、error这些状态。

### 完整结构 {#kaj-h-043bf03e-96d1-4574-9a9c-b23768159f6e}

class ChatStream {

constructor(options) {

[this.events](http://this.events) = {}

}

async start(message) {

// 发请求

// 读取流

// 收到数据后：

this.emit('message', chunk)

}

on(event, callback) {

// 订阅事件

}

emit(event, data) {

// 通知订阅者

}

abort() {

// 取消当前请求

}

destroy() {

// 清理监听器和其他资源

}

}

**其中：**

start

↓

产生各种事件

↓

emit

↓

on 订阅的 callback 被执行

而：

destroy

↓

清理事件监听

+

取消请求

+

释放其他资源

### **面试回答模板** {#kaj-h-c373e687-bb10-4b29-b25b-a096c9229688}

如果面试官问：

> “`on` 是干嘛的？”

你可以直接回答：

> `on` 我会把它设计成事件订阅机制。调用方可以通过 `on('message', callback)` 订阅 ChatStream 的消息事件，当 ChatStream 内部接收到新的流式数据时，通过 `emit('message', data)` 通知所有订阅者。这样 ChatStream 不需要直接依赖 Vue，而是通过事件把数据传给外部。

如果继续问：

> “那 destroy 呢？”

你回答：

> `destroy` 主要负责实例销毁和资源清理，比如取消还没结束的请求、清理 reader、移除事件监听以及释放其他内部资源，避免组件卸载以后还存在无效引用或者内存泄漏。  
>   
>   
> 回答思路：
> 
> 
> 
> **我会采用发布订阅模式设计流式模块。ChatStream 内部负责请求、ReadableStream 读取、SSE 解析和生命周期管理，对外通过** `on/off` **提供事件订阅能力。**
> 
> 
> 
> **当模块开始请求时** `emit('start')`**，每解析出一个完整的 SSE 数据块时** `emit('message', chunk)`**，正常结束时** `emit('done')`**，异常时** `emit('error')`**，用户调用** `stop()` **后触发** `emit('abort')`**。外部的 Vue 或 React 组件只需要订阅这些事件，在** `message` **事件中更新自己的响应式状态即可。这样流式模块不依赖具体 UI 框架，实现了网络层、流解析层和 UI 层的解耦。**
> 
> 
> 
> **其中 buffer 的作用是暂存不完整的数据。因为一次** `reader.read()` **得到的是任意大小的网络 chunk，并不保证对应一个完整 SSE 事件，所以我会根据 SSE 的事件分隔符不断累积 buffer，只解析已经形成完整事件的数据，把最后一个可能不完整的片段继续保留到下一次读取。**
