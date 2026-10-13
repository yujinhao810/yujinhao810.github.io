---
title: "如何解决跨域？"
description: "其实跨域只需要先抓住一个核心："
date: "2026-09-18"
publishedAt: "2026-09-18T20:18:23.436282+08:00"
source: "https://kajspace.cn/articles/01M2T782E81SK0C6BBZ4PJDTT0/"
tags: ["前端"]
---

# 如何解决跨域？

其实跨域只需要先抓住一个核心：

> **跨域问题的本质：浏览器的同源策略限制了一个源的网页对另一个源资源的访问。**
> 
> 
> 
> 所谓“解决跨域”，本质就是想办法让**浏览器允许这次通信**，或者让请求**根本不以跨源请求的形式出现**。

---

## 一、先把“跨域”搞明白 {#kaj-h-97ea1b3d-54e0-4ee5-8acf-1d1448bfd242}

假设前端：

```text
http://localhost:3000
```

后端：

```text
http://localhost:8080
```

虽然都是 `localhost`，但是：

```text
协议相同   http
主机相同   localhost
端口不同   3000 ≠ 8080
```

所以：

```text
localhost:3000
       ↓
localhost:8080
```

属于**跨源（cross-origin）**。

---

## 什么是“源”？ {#kaj-h-d394b546-0dce-4ba7-8a2f-f289723b63df}

一个源由三个部分组成：

```text
协议 + 域名 + 端口
```

例如：

```text
https://www.example.com:443
```

如果其中任何一个不同，就是不同源。

```text
https://example.com
http://example.com
https://api.example.com
https://example.com:8080
```

都可能是不同源。

---

## 二、跨域真正限制的是什么？ {#kaj-h-cb88e9fa-9bc6-4619-af5b-99a097a29fdb}

这里特别容易产生误解：

> **同源策略并不是说“跨域请求不能发送”。**

而是浏览器会对**跨源资源的访问和读取**施加限制。

例如：

```text
fetch('http://localhost:8080/users')
```

浏览器可能确实把请求发到了：

```text
localhost:8080
```

但如果服务器没有正确配置 CORS，浏览器会阻止：

```text
前端 JS
  ↓
读取响应
  ❌
```

所以：

```text
跨域
 ↓
浏览器安全策略
 ↓
限制网页脚本访问跨源资源
```

---

## 三、9种方案其实可以分成 4 大类 {#kaj-h-d57357a2-df70-4ce8-a79a-93e423717064}

你没必要把 9 个方案平铺记忆。

可以重新分类：

```text
跨域解决方案
│
├── ① 利用浏览器允许的特殊机制
│   ├── JSONP
│   ├── postMessage
│   └── WebSocket
│
├── ② 让服务器明确允许跨域
│   └── CORS
│
├── ③ 通过代理，让浏览器“看起来没跨域”
│   ├── Nginx
│   └── Node.js
│
└── ④ 历史上的 iframe 技巧
    ├── document.domain
    ├── location.hash
    └── window.name
```

**现代前端最重要的是：**

```text
CORS
代理
postMessage
WebSocket
```

而：

```text
document.domain
location.hash
window.name
```

更多属于历史方案/特定场景方案。

---

## 四、第一类：CORS —— 最重要 {#kaj-h-fa5af4e8-edb0-4cad-ae22-38354e60b131}

这是你现在前端开发最应该掌握的。

## 1. CORS 是什么？ {#kaj-h-78432fd2-a97a-4ba1-88eb-0a5ddeca407c}

CORS：

> Cross-Origin Resource Sharing，跨域资源共享。

本质就是：

> **服务器告诉浏览器：“这个跨域请求，我允许你访问。”**

例如：

前端：

```text
http://localhost:3000
```

请求：

```text
http://localhost:8080/api/user
```

服务器响应：

```text
Access-Control-Allow-Origin: http://localhost:3000
```

浏览器看到：

```text
服务器允许 localhost:3000
        ↓
允许前端 JS 读取响应
        ↓
跨域成功
```

---

## 五、CORS 的核心是谁在做？ {#kaj-h-bb2cdcc1-e69f-418d-8c57-edfec1d43a2a}

非常重要：

> **CORS 主要是服务器通过 HTTP 响应头告诉浏览器允许谁访问。**

不是：

```text
前端 JS → “我要开启 CORS”
```

而是：

```text
浏览器
  ↓
发送跨源请求
  ↓
服务器
  ↓
Access-Control-Allow-Origin
  ↓
浏览器检查
  ↓
允许 / 阻止 JS 读取响应
```

---

## 六、简单请求和预检请求 {#kaj-h-7b7cdc19-d555-48c5-b5c3-9e0b9e7dd1b9}

这是 CORS 面试高频。

### 简单请求 {#kaj-h-ac7639d8-b676-443c-b815-c848af74c5a1}

满足一定条件，例如常见：

```text
GET
POST
HEAD
```

并且请求头、Content-Type 等满足限制。

可能直接：

```text
浏览器
 ↓
正式请求
 ↓
服务器
 ↓
响应
```

---

### 非简单请求 {#kaj-h-eafa297c-17d4-4b6e-951c-e824065b582d}

例如：

```text
PUT
DELETE
```

或者：

```text
Content-Type: application/json
```

浏览器通常会先发送：

```text
OPTIONS
```

这就是：

> **预检请求（Preflight）**

流程：

```text
浏览器
 ↓
OPTIONS /users
“我想用 DELETE，可以吗？”
 ↓
服务器
 ↓
“可以”
Access-Control-Allow-Methods: DELETE
 ↓
浏览器
 ↓
真正的 DELETE
```

所以：

```text
简单请求
→ 直接请求

非简单请求
→ OPTIONS 预检
→ 正式请求
```

---

## 七、Cookie + CORS {#kaj-h-10b43d56-fe4f-4f4a-aa92-4591d240572e}

你刚刚学过 Cookie，这里刚好串起来。

跨域请求默认不会随意携带 Cookie。

如果前端使用：

```text
fetch('https://api.example.com/user', {
  credentials: 'include'
});
```

服务器还需要允许凭证：

```text
Access-Control-Allow-Credentials: true
```

同时：

```text
Access-Control-Allow-Origin: *
```

这种情况下不能和凭证一起使用，需要指定明确的 Origin。

另外，Cookie 自身还受到 `Domain`、`Path`、`SameSite`、`Secure` 等规则约束。

---

## 八、第二类：代理 —— 前端开发特别常见 {#kaj-h-a52540e1-c2ba-4708-8904-b32155d2b479}

这也是你现在做 React / Vue 项目经常遇到的。

假设：

```text
前端：
http://localhost:3000

后端：
http://localhost:8080
```

直接：

```text
fetch('http://localhost:8080/api/user')
```

属于跨域。

那么可以让前端请求：

```text
fetch('/api/user')
```

此时浏览器看到：

```text
localhost:3000/api/user
```

是**同源请求**。

然后：

```text
浏览器
  ↓
localhost:3000/api/user
  ↓
代理服务器
  ↓
localhost:8080/api/user
  ↓
后端
```

---

## 九、Nginx 代理 {#kaj-h-f1ea9cbc-865d-45e9-8126-039ca136a283}

生产环境非常常见。

例如：

```text
浏览器
  ↓
https://www.xxx.com/api/user
```

Nginx 收到以后：

```text
Nginx
  ↓
转发
  ↓
http://backend:8080/api/user
```

所以浏览器眼里：

```text
https://www.xxx.com
        ↓
/api/user
```

仍然是同源。

---

## Nginx 的本质 {#kaj-h-7f919c8e-c66c-4e76-8a38-9fe43d38136d}

不是：

> “Nginx 破解了浏览器同源策略。”

而是：

> **浏览器只请求同源的 Nginx，Nginx 在服务器端再去请求真正的后端。**

服务器之间通信不受浏览器同源策略限制。

所以：

```text
浏览器
 ↓ 同源
Nginx
 ↓ 服务器之间通信
后端
```

---

## 十、Node.js 代理 {#kaj-h-56210c52-fa94-4950-bba9-c8adf7cc2689}

Node.js 代理和 Nginx 的思想基本一样。

例如开发环境：

```text
React
localhost:3000
     ↓
Node/Vite代理
     ↓
localhost:8080
```

浏览器只看到：

```text
localhost:3000
```

所以浏览器不会因为前端直接请求 `8080` 而产生跨源问题。

---

## 十一、第三类：JSONP {#kaj-h-69f4f32c-fffa-4fbb-b9d2-3b301ebc5b8b}

JSONP 是一个比较老的方案。

它利用：

> `<script>` **标签加载跨源脚本不受普通 AJAX 同源限制。**

例如：

```html
<script src="https://api.example.com/user?callback=handleData"></script>
```

服务器返回：

```text
handleData({
  name: "Tom"
});
```

浏览器加载 `<script>` 后，会执行：

```text
handleData(...)
```

于是数据就传到了前端。

---

## 为什么叫 JSONP？ {#kaj-h-64139085-fcfc-44cd-8b1a-e63fe5ac816b}

本质：

```text
JSON
+
Padding
```

服务器不是直接返回：

```text
{"name":"Tom"}
```

而是返回：

```text
handleData({"name":"Tom"})
```

把 JSON 放到了函数调用里面。

---

## JSONP 最大限制 {#kaj-h-a074772f-26b7-4b25-8f3e-38e6bd14dbce}

只能：

```text
GET
```

因为它本质是在加载：

```html
<script src="...">
```

不能用它实现：

```text
POST
PUT
DELETE
```

所以现代开发基本优先使用 CORS。

---

## 十二、第四类：postMessage {#kaj-h-d44d66e5-775a-4bdf-9bee-2da421401501}

这个和 CORS 是完全不同的思路。

`postMessage` 主要解决：

> **不同窗口、iframe、标签页之间的跨源通信。**

例如：

```text
A页面
http://a.com
   │
   │ postMessage
   ↓
iframe
http://b.com
```

A：

```text
iframe.contentWindow.postMessage(
  { name: 'Tom' },
  'http://b.com'
);
```

B：

```js
window.addEventListener('message', (event) => {
  console.log(event.data);
});
```

---

## 它适合什么场景？ {#kaj-h-2db7fc14-7786-474b-a516-b6f423b663ad}

比如：

```text
主页面
   ↓
iframe
   ↓
第三方页面
```

两个页面不同源，但是需要通信。

或者：

```text
窗口 A
   ↕
窗口 B
```

---

## 和 CORS 的区别 {#kaj-h-ec9c05ae-0d07-4e38-ae24-b4926d91c1ba}

非常重要：

```text
CORS
→ 解决“跨源 HTTP 资源访问”

postMessage
→ 解决“跨源窗口之间通信”
```

不要把它们当成同一种方案。

---

## 十三、WebSocket 跨域 {#kaj-h-3b061ea3-5143-4142-89ab-970146c16dc6}

WebSocket 可以建立跨源连接。

例如：

```js
const ws = new WebSocket(
  'wss://api.example.com/chat'
);
```

可以用于：

```text
实时聊天
实时消息
实时数据推送
游戏
```

而且它是：

```text
全双工通信
```

也就是：

```text
客户端 ←→ 服务器
```

双方都可以主动发送消息。

---

## 注意一个容易记错的地方 {#kaj-h-bd23382f-37f5-4533-9af6-45f022ee857c}

你笔记里：

> WebSocket 不是基于 HTTP

这个说法**不够准确**。

更准确：

> **WebSocket 使用 HTTP Upgrade 完成握手，握手成功后升级为 WebSocket 协议进行持续的双向通信。**

---

## 十四、最后三个：document.domain、hash、window.name {#kaj-h-d9e32969-06ec-4ee0-86ec-5f7827fffbcd}

这三个你现在可以放在：

> **“历史跨域方案”**

这一类里面。

---

## 十五、document.domain {#kaj-h-89843357-658b-4712-8ac9-2be7af9df0bd}

主要解决：

```text
a.example.com
b.example.com
```

这种：

> **主域相同，子域不同**

的页面之间通信。

例如：

```text
www.example.com
   ↕
doc.example.com
```

以前可以：

```text
document.domain = 'example.com';
```

让两个页面降低到共同的域。

---

## 但现在不建议重点掌握 {#kaj-h-e42b766d-51ab-4956-8be2-01aa8fe6cd58}

`document.domain` 已经属于比较老的机制，现代 Web 开发更推荐：

```text
postMessage
```

等方案。

所以面试知道：

> **历史上用于相同主域、不同子域页面通信。**

基本够了。

---

## 十六、location.hash {#kaj-h-39225db6-4ea7-4e82-a52b-51d324004e8e}

利用：

```text
URL#后面的部分
```

传数据。

例如：

```text
http://b.com/page.html#hello
```

然后监听：

```text
hashchange
```

来获取变化。

特点：

```text
修改 hash
↓
不会重新向服务器发送 HTTP 请求
```

以前可以利用它实现不同域 iframe 之间通信。

但是：

```text
数据暴露在 URL
数据容量有限
实现复杂
历史记录问题
```

所以现在基本不作为主流方案。

---

## 十七、window.name {#kaj-h-b938fc8b-9aa1-4fa3-8cd0-73afe1e4f85f}

利用 `window.name` 的特殊行为：

```text
页面 A
 ↓
设置 window.name
 ↓
跳转到页面 B
 ↓
window.name 仍然存在
```

以前可以利用 iframe + 页面跳转实现跨域传递数据。

也是一种：

> **历史方案**

现在基本不作为现代项目的首选。

---

## 十八、把9种方案彻底串起来 {#kaj-h-81dce1e4-80e3-4c95-9566-5c88e4f2f2bf}

你可以记成这张图：

```text
                    跨域
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
      CORS          代理       页面间通信
        │            │            │
        │         ┌──┴──┐     ┌───┼────┐
        │         ↓     ↓     ↓   ↓    ↓
        │       Nginx  Node  postMessage
        │                     WebSocket
        │
        ↓
   HTTP响应头
   告诉浏览器
   “我允许这个源”
```

历史方案：

```html
iframe 跨域
├── document.domain
├── location.hash
└── window.name

JSONP
└── <script> 跨域加载
```

---

## 十九、你真正需要掌握的优先级 {#kaj-h-75eb519a-f960-4729-8965-17256412b94c}

如果你是为了**现在的前端秋招**，我建议不要平均用力：

### 第一梯队：一定要理解 {#kaj-h-25921954-12a4-4015-88e7-23d755a889f8}

```text
同源策略
CORS
简单请求
预检 OPTIONS
Cookie + CORS
代理
Nginx
Node/Vite Proxy
```

### 第二梯队：理解使用场景 {#kaj-h-535a95ed-88e8-469d-aa50-5ef32eaee17b}

```text
postMessage
WebSocket
JSONP
```

### 第三梯队：知道原理即可 {#kaj-h-65a3fa97-09aa-45e4-af03-e9002adf511c}

```text
document.domain
location.hash
window.name
```

---

## 二十、面试最核心的一段话 {#kaj-h-8de4d526-7a6b-4715-8b16-ca3a8febf72d}

如果面试官问：

> **“前端跨域怎么解决？”**

可以这样回答：

> **跨域本质上是浏览器同源策略对跨源资源访问的限制。现代开发中主要有三种思路：第一是 CORS，由服务器通过响应头明确允许指定来源的跨域请求；第二是代理，例如开发环境使用 Node/Vite Proxy，生产环境使用 Nginx，让浏览器请求同源的代理服务器，再由代理转发到后端；第三是针对特定场景使用 postMessage 或 WebSocket 等机制。JSONP、document.domain、location.hash、window.name 属于比较传统的跨域方案，其中 JSONP 主要利用 script 标签跨源加载且只支持 GET。**

你现在可以把整个知识点压缩成一句：

> **CORS 是“服务器允许跨域”，代理是“让浏览器不要直接跨域”，postMessage 是“跨域页面之间传消息”，JSONP 是“借助 script 跨域拿数据”。**

这四句话理解了，**“9种跨域方案”就不再是9个孤立的知识点了。**
