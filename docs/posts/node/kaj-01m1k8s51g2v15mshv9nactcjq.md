---
title: "Node.js考点"
description: "可以把 Node.js 面试题分成 8 大模块："
date: "2026-09-03"
publishedAt: "2026-09-03T17:15:01.208009+08:00"
source: "https://kajspace.cn/articles/01M1K8S51G2V15MSHV9NACTCJQ/"
tags: ["后端"]
---

# Node.js考点

## 一、Node.js 面试考点总览 {#kaj-h-4deb0fab-0221-435c-ad65-46a09a8f6c45}

可以把 Node.js 面试题分成 **8 大模块**：

| 模块 | 重要程度 | 常见程度 |
| --- | --- | --- |
| 1. Node.js 基础 | ⭐⭐⭐ | 高频 |
| 2. Event Loop 事件循环 | ⭐⭐⭐⭐⭐ | **必问** |
| 3. 异步编程 | ⭐⭐⭐⭐⭐ | **必问** |
| 4. Node.js 高并发原理 | ⭐⭐⭐⭐⭐ | **高频追问** |
| 5. 模块系统 | ⭐⭐⭐⭐ | 常问 |
| 6. Stream / Buffer | ⭐⭐⭐⭐ | 中高频 |
| 7. HTTP / Web 服务 | ⭐⭐⭐⭐ | 高频 |
| 8. 数据库 / JWT / 项目实践 | ⭐⭐⭐⭐ | 项目追问 |

---

## 二、Node.js 基础 {#kaj-h-2dc20d46-6178-4870-94e8-a165836b14d0}

## 1. Node.js 是什么？ {#kaj-h-597694ca-b783-43d6-bc62-4bc9b84e9a68}

这是最基础的问题。

你需要知道：

> Node.js 是一个基于 Chrome V8 JavaScript 引擎的 JavaScript 运行时，使 JavaScript 可以脱离浏览器运行在服务器端。

面试官可能继续问：

### Node.js 和浏览器中的 JavaScript 有什么区别？ {#kaj-h-0b4e1bc4-64ca-41c1-8b04-a8b309d4b494}

核心：

```text
JavaScript
    ↓
V8
    ↓
Node.js
    ↓
操作系统
```

浏览器：

```text
JavaScript
    ↓
V8
    ↓
浏览器
    ↓
DOM / BOM / Web API
```

Node.js：

```text
JavaScript
    ↓
V8
    ↓
Node.js
    ↓
文件系统 / 网络 / 操作系统
```

所以：

- 浏览器 JS 可以操作 DOM
- Node.js 没有 DOM
- Node.js 可以操作文件
- Node.js 可以创建 HTTP 服务器
- Node.js 可以连接数据库
- Node.js 可以访问操作系统资源

---

## 三、Node.js 为什么能做服务端？ {#kaj-h-14917ea7-853d-4785-92c5-f2bbc7799e7a}

这个非常重要。

面试官可能直接问：

> **Node.js 为什么可以支持高并发？**

你要掌握这句话：

> Node.js 采用**单线程 + 事件驱动 + 非阻塞 I/O + 事件循环**的模型。当程序执行 I/O 操作时，不会一直阻塞 JavaScript 主线程，而是将 I/O 交给底层处理，完成后通过事件循环执行对应的回调，从而可以用较少的线程处理大量并发请求。

理解这个流程：

```text
客户端请求
     ↓
Node.js 主线程
     ↓
遇到 I/O
     ↓
交给底层系统 / libuv
     ↓
主线程继续处理其他请求
     ↓
I/O 完成
     ↓
回调进入任务队列
     ↓
Event Loop
     ↓
执行回调
```

例如：

```js
fs.readFile('./test.txt', (err, data) => {
    console.log(data);
});

console.log('hello');
```

不会：

```text
读取文件
 ↓
一直等
 ↓
读取完成
 ↓
hello
```

而是：

```text
发起读取
 ↓
交给底层
 ↓
hello
 ↓
文件读取完成
 ↓
执行回调
```

---

## 四、Node.js 事件循环 ⭐⭐⭐⭐⭐ {#kaj-h-75c3aef7-f182-4752-ad7c-74218efa2de4}

这是 **Node.js 最重要的考点之一**。

一定要重点掌握。

## 1. 什么是 Event Loop？ {#kaj-h-60a7bf3f-a026-4ff7-a371-92ef53aa9ca0}

面试回答：

> Event Loop 是 Node.js 实现异步非阻塞 I/O 的核心机制。JavaScript 主线程执行同步代码，当遇到异步 I/O 操作时交给底层处理，操作完成后对应的回调进入任务队列，事件循环不断检查这些任务并安排它们执行。

---

## 五、Node.js Event Loop 执行顺序 {#kaj-h-48286773-bfcb-493b-8e0c-311f176257b7}

你至少要知道：

```text
同步代码
↓
process.nextTick
↓
微任务 Promise
↓
Event Loop 各阶段
```

Node.js 的 Event Loop 阶段可以简单记：

```text
timers
   ↓
pending callbacks
   ↓
poll
   ↓
check
   ↓
close callbacks
```

重点：

### timers {#kaj-h-7efb520c-8cbb-43d4-a05e-bcb71b9439c1}

处理：

```text
setTimeout()
setInterval()
```

### poll {#kaj-h-c60f28b1-2b8f-48a9-bd2b-e9e38cb8e9c9}

处理很多 I/O 回调。

### check {#kaj-h-d99ccdc9-f75b-4248-86d3-e8b91cb9a27c}

处理：

```text
setImmediate()
```

---

## 六、setTimeout、setImmediate、Promise、nextTick {#kaj-h-ae4512ef-61b6-4d01-942f-6e3020b9a88b}

这是非常经典的面试题。

例如：

```js
console.log(1);

setTimeout(() => {
    console.log(2);
}, 0);

setImmediate(() => {
    console.log(3);
});

Promise.resolve().then(() => {
    console.log(4);
});

process.nextTick(() => {
    console.log(5);
});

console.log(6);
```

你至少应该知道：

```text
1
6
5
4
...
```

也就是：

```text
同步代码
↓
nextTick
↓
Promise 微任务
↓
Event Loop
```

至于 `setTimeout(0)` 和 `setImmediate()` 谁先执行，需要结合代码所在环境判断，**不要死记“setTimeout 一定先执行”**。

---

## 七、异步编程 {#kaj-h-79fd85fa-475f-46af-9ab5-c9d6dcc52c71}

Node.js 很喜欢问异步。

需要掌握：

### 1. Callback {#kaj-h-e6c5098b-abec-48bb-8e67-4d2a435c2491}

```js
fs.readFile('./a.txt', (err, data) => {
    console.log(data);
});
```

### 2. Promise {#kaj-h-3eda0c4f-7178-4b06-9a74-aceaa32b72df}

```js
fs.promises.readFile('./a.txt')
    .then(data => {
        console.log(data);
    });
```

### 3. async / await {#kaj-h-8fd282ab-5e8e-4757-9d4e-2985e3d726a1}

```js
async function test() {
    const data = await fs.promises.readFile('./a.txt');
    console.log(data);
}
```

面试官可能问：

> async/await 是同步还是异步？

正确理解：

> `async/await` 本质上还是基于 Promise 的异步机制。`await` 会让当前 async 函数暂停执行，但不会阻塞整个 JavaScript 主线程。

---

## 八、Node.js 模块系统 ⭐⭐⭐⭐ {#kaj-h-8b6952c5-9b9c-4279-8da0-d347345092a7}

需要知道两套：

## CommonJS {#kaj-h-a276e042-f9d0-486b-a7cf-6b5b66ad91a2}

Node.js 传统模块系统：

```js
const fs = require('fs');

module.exports = {
    name: 'hello'
};
```

导入：

```js
const test = require('./test');
```

## ES Module {#kaj-h-56e7f28b-42ce-4253-95d7-412c6dc7fc38}

```text
import fs from 'fs';

export default {
    name: 'hello'
};
```

导入：

```text
import test from './test.js';
```

面试官可能问：

> CommonJS 和 ES Module 有什么区别？

重点知道：

```text
CommonJS
require
module.exports
运行时加载
通常同步加载

ES Module
import
export
静态模块结构
支持静态分析
```

---

## 九、Node.js 全局对象 {#kaj-h-11662ff2-5e8f-4a64-b195-9cf009067ac8}

需要知道：

```text
global
process
__dirname
__filename
```

例如：

```js
console.log(process.cwd());
console.log(__dirname);
console.log(__filename);
```

面试官可能问：

### process 是干什么的？ {#kaj-h-5113a6d3-3cf2-480f-9174-d1437e84fee2}

`process` 可以获取和控制 Node.js 进程信息。

例如：

```text
process.env
process.argv
process.pid
process.cwd()
```

特别是：

```text
process.env
```

非常常用。

例如：

```js
const port = process.env.PORT || 3000;
```

---

## 十、Buffer ⭐⭐⭐⭐ {#kaj-h-3508b86b-cab3-4b9b-8cd6-6757d0c54394}

Buffer 是 Node.js 很重要的概念。

因为 Node.js 经常处理：

```text
文件
网络
图片
音视频
TCP
二进制数据
```

例如：

```js
const buf = Buffer.from('hello');

console.log(buf);
```

Buffer 可以理解成：

> Node.js 用来处理二进制数据的一种数据结构。

例如读取图片、文件、网络数据时，都可能使用 Buffer。

---

## 十一、Stream 流 ⭐⭐⭐⭐ {#kaj-h-c42ba278-c756-4ce4-ae17-f5aebd07fc70}

这是 Node.js 很经典的知识。

比如一个 **10GB 文件**：

错误思路：

```text
fs.readFile('10GB.txt', ...)
```

相当于：

```text
10GB文件
 ↓
一次性读取
 ↓
内存占用巨大
```

Stream：

```text
10GB文件
 ↓
一小块
 ↓
处理
 ↓
下一块
 ↓
下一块
```

所以 Stream 的核心思想：

> **流式处理，避免一次性将大量数据加载到内存。**

例如：

```js
const readStream = fs.createReadStream('./test.txt');

readStream.on('data', chunk => {
    console.log(chunk);
});
```

还要知道：

```text
pipe()
```

例如：

```text
readStream.pipe(writeStream);
```

---

## 十二、HTTP 模块 ⭐⭐⭐⭐ {#kaj-h-b5a6cb66-1fc4-4717-bd7b-656f32ee390d}

Node.js 可以直接创建 HTTP 服务：

```js
const http = require('http');

const server = http.createServer((req, res) => {
    res.end('Hello Node.js');
});

server.listen(3000);
```

面试官可能问：

> Node.js 怎么实现一个 HTTP 服务器？

你需要能说出：

```text
http.createServer()
        ↓
request
        ↓
req
res
        ↓
server.listen()
```

---

## 十三、Express / Koa {#kaj-h-eaed9fd2-0c5b-4361-b29c-844b9cfc36f5}

如果简历或者项目里写了 Express/Koa，面试官可能会问。

比如：

> Express 中间件是什么？

核心：

```js
app.use((req, res, next) => {
    console.log('middleware');

    next();
});
```

请求：

```text
Request
  ↓
中间件1
  ↓
中间件2
  ↓
中间件3
  ↓
Controller
  ↓
Response
```

所以：

> 中间件本质上是请求和响应处理过程中的一系列函数，可以对请求进行拦截、处理，并通过 `next()` 将控制权交给后续中间件。

---

## 十四、Node.js 怎么连接数据库 ⭐⭐⭐⭐ {#kaj-h-17c3b1fd-1cf5-48e2-b536-9ee7cbddc243}

这个也是你之前问过的。

Node.js 本身不是数据库。

关系是：

```text
Node.js
   ↓
数据库驱动 / ORM
   ↓
MySQL / PostgreSQL / MongoDB
```

例如 MySQL：

```text
Node.js
   ↓
mysql2
   ↓
MySQL
```

或者：

```text
Node.js
   ↓
Prisma / Sequelize
   ↓
MySQL
```

面试回答可以说：

> Node.js 通常通过数据库驱动或者 ORM 连接数据库。例如使用 mysql2 连接 MySQL，也可以使用 Prisma、Sequelize 等 ORM 对数据库进行操作。

---

## 十五、JWT / Cookie / Session {#kaj-h-54bdc8f9-a5c5-42a8-9000-4a8a216cb61d}

如果 Node.js 做登录系统，非常容易被问。

需要理解：

```text
Cookie
Session
JWT
```

### Cookie {#kaj-h-6a5d91bc-c323-4c18-8e1c-703aa3af65a6}

浏览器保存：

```text
token/sessionId
```

每次请求自动携带。

### Session {#kaj-h-d969fe40-a5a5-4893-9a45-f0f66dd1e637}

```text
浏览器
 ↓
sessionId
 ↓
服务器
 ↓
Session数据
```

### JWT {#kaj-h-208d6620-15a9-46fc-a36e-09bdf6e3fa0a}

```text
登录
 ↓
服务器生成 JWT
 ↓
客户端保存
 ↓
后续请求携带 JWT
 ↓
服务器验证 JWT
```

---

## 十六、Node.js 文件系统 {#kaj-h-36c68b56-fcec-4d92-819b-081cdb88d77a}

常见 API：

```text
fs.readFile()
fs.writeFile()
fs.appendFile()
fs.unlink()
fs.mkdir()
fs.readdir()
```

同步：

```text
fs.readFileSync()
```

异步：

```text
fs.readFile()
```

面试官可能问：

> 为什么服务器代码不推荐大量使用同步 API？

因为同步 API 会：

> **阻塞当前 JavaScript 主线程。**

例如：

```js
const data = fs.readFileSync('./big.txt');
```

读取过程中当前线程会一直等待。

---

## 十七、Node.js 错误处理 {#kaj-h-cc0c35ea-45c9-44c1-b163-385b3b047c6a}

需要知道：

```text
try {
    
} catch (error) {

}
```

Promise：

```js
try {
    await test();
} catch (err) {
    console.log(err);
}
```

还需要知道：

```text
process.on('uncaughtException', ...)
process.on('unhandledRejection', ...)
```

但面试时不要说：

> 所有错误都用 uncaughtException 捕获。

这是不合理的。

更重要的是：

> 在业务代码中应该尽早处理错误，避免出现未捕获异常。

---

## 十八、Node.js 高并发 ⭐⭐⭐⭐⭐ {#kaj-h-5ba77068-e298-410c-a37b-9852706988e0}

这是你作为**前端开发**比较容易被追问的一个方向。

面试官：

> Node.js 是单线程，为什么还能支持高并发？

建议直接背这个：

> Node.js 的 JavaScript 执行本身主要运行在单线程上，但是 I/O 操作并不需要一直占用这个线程。Node.js 基于事件驱动和非阻塞 I/O，将网络、文件等 I/O 操作交给底层的 libuv 和操作系统处理，I/O 完成后再通过 Event Loop 执行对应回调。因此在大量 I/O 密集型场景下，可以用较少的线程处理大量并发请求。

---

## 十九、Node.js 单线程是不是完全只有一个线程？ {#kaj-h-b8753804-b7e7-4519-9154-3d2d82fb221f}

这是一个很容易被追问的问题。

**不是。**

应该理解成：

> Node.js 的 JavaScript 执行主要是单线程的，但 Node.js 底层的 libuv 存在线程池，同时操作系统也会参与异步 I/O。

例如：

```text
Node.js
│
├── JS 主线程
│
├── Event Loop
│
└── libuv
      └── Thread Pool
```

默认 libuv 线程池一般是：

```text
4
```

可以通过：

```text
UV_THREADPOOL_SIZE
```

调整。

---

## 二十、Node.js 哪些场景不适合？ {#kaj-h-407e4ec6-7e08-455e-a8f8-779060915f2e}

这是非常好的进阶问题。

Node.js 特别适合：

```text
I/O 密集型
API 服务
WebSocket
实时通信
BFF
SSR
中间层
```

但如果大量执行：

```text
CPU 密集型计算
图片复杂处理
视频编码
大型数学计算
```

可能导致：

```text
JS 主线程
     ↓
CPU计算
     ↓
一直占用
     ↓
Event Loop 被阻塞
     ↓
其他请求无法及时处理
```

所以 Node.js 最大的问题之一：

> **CPU 密集型任务会阻塞事件循环。**

解决方案可以提：

```text
Worker Threads
Child Process
Cluster
任务队列
拆分到独立服务
```

---

## 二十一、Worker Threads {#kaj-h-b15b80d5-7a4a-4378-801b-270da1739c57}

这是 Node.js 进阶高频点。

如果：

```text
主线程
 ↓
CPU密集计算
 ↓
Event Loop阻塞
```

可以使用：

```text
Worker Thread
```

把 CPU 密集任务放到 Worker 中执行。

核心理解：

```text
Main Thread
    │
    ├── Event Loop
    │
    └── Worker Thread
            ↓
         CPU计算
```

---

## 二十二、Node.js Cluster {#kaj-h-4433ae61-6208-4afc-9d9e-b7297a01a8f7}

如果面试官问：

> Node.js 单线程，那怎么利用多核 CPU？

可以回答：

> 可以通过 Cluster 创建多个 Node.js 进程，让多个进程利用多核 CPU。

例如：

```text
CPU
├── Core 1 → Node进程1
├── Core 2 → Node进程2
├── Core 3 → Node进程3
└── Core 4 → Node进程4
```

现在实际项目中也经常结合：

```text
PM2
Docker
Kubernetes
```

进行进程管理和水平扩展。

---

## 二十三、Node.js 性能优化 {#kaj-h-5709ee62-494e-425a-8682-eaa335b78849}

面试官可能问：

> Node.js 服务性能怎么优化？

可以从这几个方向回答：

### 1. 避免阻塞 Event Loop {#kaj-h-76964999-a8e5-4d18-b7ba-314de7b9f65b}

```text
CPU密集任务 → Worker
```

### 2. 使用缓存 {#kaj-h-74d8b913-5c26-4be5-845a-b2a77566edc4}

```text
Redis
```

### 3. 数据库优化 {#kaj-h-d3e4b902-4772-463d-9945-2076322a45bf}

```text
索引
连接池
避免N+1查询
分页
```

### 4. 流式处理 {#kaj-h-3d87ad03-9d9e-4668-b6ee-957346b11ac2}

```text
Stream
```

### 5. 集群 / 水平扩展 {#kaj-h-239e955b-b903-402a-b457-0c263311f272}

```text
Cluster
PM2
Docker
```

### 6. HTTP 优化 {#kaj-h-37a7e95b-0a2f-4ca9-87dc-dc01df0a23f5}

```text
Keep-Alive
压缩
缓存
CDN
```

---

## 二十四、前端面试最可能问你的 Node.js 问题 {#kaj-h-103ff224-2ac5-4666-9b44-6e3ff81d968c}

如果你的目标是**前端秋招**，不用一上来就把 Node.js 学成后端开发。

我建议你优先准备下面 **20 道**：

### 第一梯队：必须掌握 {#kaj-h-11d89b65-e584-49ca-a042-2c188314871a}

1. **Node.js 是什么？**
2. **Node.js 和浏览器 JavaScript 有什么区别？**
3. **Node.js 为什么能支持高并发？**
4. **Node.js 是单线程吗？**
5. **什么是 Event Loop？**
6. **Node.js Event Loop 有哪些阶段？**
7. **Promise、process.nextTick、setTimeout、setImmediate 的执行顺序？**
8. **Node.js 为什么是非阻塞 I/O？**
9. **Node.js 怎么处理异步操作？**
10. **Node.js 为什么适合 I/O 密集型应用？**

### 第二梯队：常问 {#kaj-h-2defb166-1a5a-4e97-ba14-006700c8c2c6}

11. **CommonJS 和 ES Module 区别？**
12. **require 和 import 区别？**
13. **Buffer 是什么？**
14. **Stream 是什么？**
15. **Stream 有什么作用？**
16. **Node.js 如何创建 HTTP 服务器？**
17. **Express/Koa 中间件是什么？**
18. **Node.js 如何连接 MySQL？**
19. **Cookie、Session、JWT 区别？**
20. **Node.js 如何进行性能优化？**

---

## 二十五、结合你的前端面试，建议这样准备 {#kaj-h-5249bd5e-99d6-4d4e-a445-f7db2752ae27}

你的 Node.js 不需要按照后端岗深度准备。

可以分成三个层级：

```text
Level 1：⭐⭐⭐⭐⭐
前端必须掌握
```

```text
Node.js是什么
↓
非阻塞I/O
↓
Event Loop
↓
异步
↓
Promise
↓
高并发
↓
Buffer
↓
Stream
↓
HTTP
```

然后：

```text
Level 2：⭐⭐⭐⭐
项目开发能力
```

```text
Express / Koa
↓
中间件
↓
MySQL
↓
Redis
↓
JWT
↓
Cookie / Session
↓
文件系统
```

最后：

```text
Level 3：⭐⭐⭐
进阶追问
```

```text
libuv
↓
线程池
↓
Worker Threads
↓
Cluster
↓
PM2
↓
Node.js性能优化
```

**你现在最应该重点吃透的是** `Node.js 高并发 → 非阻塞 I/O → Event Loop → 微任务/宏任务 → libuv` **这一整条链。**

因为面试官非常喜欢沿着这一条连续追问：

> Node.js 是什么？  
>   
> ↓  
>   
> 为什么 Node.js 能高并发？  
>   
> ↓  
>   
> 什么是非阻塞 I/O？  
>   
> ↓  
>   
> I/O 到底交给谁处理？  
>   
> ↓  
>   
> libuv 是什么？  
>   
> ↓  
>   
> Event Loop 是什么？  
>   
> ↓  
>   
> Event Loop 有哪些阶段？  
>   
> ↓  
>   
> Promise 和 setTimeout 谁先执行？  
>   
> ↓  
>   
> Node.js 明明单线程，为什么还能利用多核 CPU？  
>   
> ↓  
>   
> CPU 密集型任务怎么办？

这条链如果你能完整讲下来，**Node.js 前端面试基本就有比较扎实的应对能力了。**
