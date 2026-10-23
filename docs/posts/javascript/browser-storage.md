---
title: 浏览器本地存储详解：Cookie、LocalStorage、SessionStorage 与 IndexedDB
category: browser
description: 对比 Cookie、LocalStorage、SessionStorage 与 IndexedDB 的生命周期、容量、共享范围和安全边界，梳理浏览器存储的 API 与选型思路。
date: "2026-10-23"
publishedAt: "2026-10-23T16:09:02+08:00"
tags:
  - 浏览器存储
  - Cookie
  - Web Storage
  - IndexedDB
  - 前端八股
---

# 浏览器本地存储详解：Cookie、LocalStorage、SessionStorage 与 IndexedDB

## 一、为什么需要浏览器存储？

浏览器中的 JavaScript 变量通常只存在于当前页面的运行环境中。当页面刷新或重新加载时，变量可能会重新初始化，之前的数据也就丢失了。

例如：

```javascript
let theme = 'dark';
```

如果希望用户刷新页面或下次访问网站时，仍然使用之前选择的深色主题，就需要将数据保存到浏览器存储中。

浏览器提供了多种存储机制，常见的有：

- **Cookie**：常用于 HTTP 状态管理和身份认证。
- **LocalStorage**：用于持久化保存少量键值数据。
- **SessionStorage**：用于保存当前标签页会话期间的数据。
- **IndexedDB**：用于存储大量、结构化的本地数据。

这些技术各有适用场景，不能简单地认为某一种存储方式可以完全替代其他方式。

## 二、Cookie

### 2.1 什么是 Cookie？

Cookie 是浏览器管理的一种小型数据存储机制，最初主要用于解决 HTTP 协议无状态的问题。

HTTP 是无状态协议，服务器默认不会自动记住不同请求之间的用户身份。Cookie 可以帮助服务器关联不同请求，从而维持用户的登录状态。

例如，用户登录成功后，服务器返回：

```http
Set-Cookie: sessionId=abc123; Path=/; HttpOnly; Secure; SameSite=Lax
```

浏览器收到响应后保存 Cookie。在后续符合发送条件的请求中，浏览器会自动携带该 Cookie：

```http
Cookie: sessionId=abc123
```

服务器便可以根据 `sessionId` 查询对应的会话信息。

需要注意，Cookie 本身不一定存储用户的完整信息。传统 Session 方案通常只在 Cookie 中保存会话标识，真正的会话数据保存在服务器端。

### 2.2 Cookie 的常见属性

| 属性 | 作用 |
| --- | --- |
| Name | Cookie 的名称 |
| Value | Cookie 的值 |
| Domain | 控制 Cookie 适用的域名范围 |
| Path | 控制 Cookie 适用的 URL 路径 |
| Expires | 指定 Cookie 的过期时间 |
| Max-Age | 指定 Cookie 的有效时长 |
| Secure | 限制 Cookie 仅通过安全连接发送 |
| HttpOnly | 禁止 JavaScript 通过 `document.cookie` 读取 |
| SameSite | 控制跨站请求中 Cookie 的发送行为 |

其中，`Size` 是浏览器开发者工具中可能展示的信息，不是服务器设置的 Cookie 属性。

### 2.3 Cookie 的特点

1. 容量较小，单个 Cookie 通常约为 4 KB，具体限制取决于浏览器。
2. 可以设置有效期，也可以使用会话 Cookie。
3. 符合条件的 Cookie 会自动随 HTTP 请求发送。
4. Cookie 的发送范围受到域名、路径、安全协议和 SameSite 等规则约束。
5. 可以通过 `HttpOnly` 限制客户端 JavaScript 读取 Cookie。

### 2.4 Cookie 的使用场景

- 维持用户登录状态。
- 保存服务端会话标识。
- 在适当的认证设计中保存访问凭证。
- 保存少量需要随请求发送的状态信息。

需要注意，Cookie 并不天然安全。对于登录凭证，应结合 HTTPS、`HttpOnly`、`Secure`、`SameSite` 等措施降低风险。`HttpOnly` 也不能完全防止 XSS 或其他类型的攻击。

## 三、LocalStorage

### 3.1 什么是 LocalStorage？

LocalStorage 是浏览器提供的 Web Storage API，用于在客户端持久化保存键值数据。

与 Cookie 不同，LocalStorage 中的数据不会因为普通 HTTP 请求而自动发送给服务器。

例如：

```javascript
localStorage.setItem('theme', 'dark');
```

页面刷新后，仍然可以读取：

```javascript
const theme = localStorage.getItem('theme');

console.log(theme); // 'dark'
```

只要数据没有被删除、浏览器清理或存储环境重置，它通常会一直保留。

### 3.2 LocalStorage 的常用 API

```javascript
// 保存数据
localStorage.setItem('username', '张三');

// 读取数据
const username = localStorage.getItem('username');

// 删除指定数据
localStorage.removeItem('username');

// 清空当前源下的全部 LocalStorage 数据
localStorage.clear();

// 根据索引获取键名
const key = localStorage.key(0);
```

如果指定的键不存在，`getItem()` 会返回 `null`。

需要注意，`clear()` 会删除当前源下的全部 LocalStorage 数据，实际开发中应谨慎使用。

### 3.3 LocalStorage 只能直接存储字符串

LocalStorage 的键和值都是字符串。

如果直接存储 JavaScript 对象：

```javascript
const user = {
  name: '张三',
  age: 18
};

localStorage.setItem('user', user);
```

对象会被转换成普通字符串，通常得到 `[object Object]`，而不是完整的对象数据。

正确做法是使用 `JSON.stringify()` 和 `JSON.parse()`：

```javascript
const user = {
  name: '张三',
  age: 18
};

// 对象转换为 JSON 字符串
localStorage.setItem('user', JSON.stringify(user));

// 读取字符串并还原为对象
const data = JSON.parse(localStorage.getItem('user'));

console.log(data.name); // '张三'
console.log(data.age);  // 18
```

对于可能不存在或格式不合法的数据，还需要考虑空值判断和异常处理。

### 3.4 LocalStorage 的特点

- 数据通常可以跨页面刷新和浏览器重启保留。
- 不会自动随 HTTP 请求发送。
- 同源页面通常可以访问同一份 LocalStorage 数据。
- API 简单，但操作是同步的。
- 通常有约 5 MiB 的存储额度，具体限制取决于浏览器。

### 3.5 LocalStorage 的使用场景

- 深色模式、语言等用户偏好设置。
- 表格列显示、布局等非敏感界面配置。
- 少量非敏感的本地缓存数据。
- 不需要每次请求都发送给服务器的持久化状态。

不建议直接在 LocalStorage 中保存密码、银行卡信息等敏感数据。存储在其中的内容可以被用户查看和修改，也可能被同源恶意 JavaScript 读取。

## 四、SessionStorage

### 4.1 什么是 SessionStorage？

SessionStorage 同样属于 Web Storage API，但它主要用于保存当前页面会话期间的数据。

例如，用户正在填写一个多步骤表单，可以将当前步骤保存下来：

```javascript
sessionStorage.setItem('currentStep', '2');
```

页面刷新后：

```javascript
const step = sessionStorage.getItem('currentStep');

console.log(step); // '2'
```

数据仍然存在。

当原有标签页的页面会话结束时，这些数据通常也会被清除。

### 4.2 SessionStorage 的特点

1. 页面刷新后数据通常保留。
2. 同一标签页中的同源页面通常可以访问对应数据。
3. 不同标签页的 SessionStorage 通常相互隔离。
4. 关闭标签页后，原页面会话通常结束。
5. 不会自动随 HTTP 请求发送。
6. 与 LocalStorage 一样，只能直接存储字符串。

需要注意，复制标签页、通过 `window.open()` 打开页面以及浏览器会话恢复等行为可能存在特殊情况，因此不能将 SessionStorage 理解为绝对可靠的数据销毁机制。

### 4.3 SessionStorage 的使用场景

- 多步骤表单的临时进度。
- 当前标签页的临时筛选条件。
- 刷新后需要恢复的短期操作状态。
- 不需要跨标签页长期保存的数据。

如果数据必须长期保存，或者需要多个标签页共享，应考虑其他存储方案。

## 五、Cookie、LocalStorage 和 SessionStorage 的区别

| 对比维度 | Cookie | LocalStorage | SessionStorage |
| --- | --- | --- | --- |
| 主要用途 | HTTP 状态、会话凭证 | 持久化本地数据 | 临时会话数据 |
| 常见容量 | 单个通常约 4 KB | 通常约 5 MiB | 通常约 5 MiB |
| 页面刷新 | 符合有效期时保留 | 保留 | 保留 |
| 关闭标签页 | 取决于有效期及会话行为 | 通常保留 | 原页面会话通常结束 |
| 自动随请求发送 | 符合条件时会 | 不会 | 不会 |
| 同源页面共享 | 取决于 Cookie 的域名、路径等规则 | 通常共享 | 通常按标签页隔离 |
| API 操作 | `document.cookie` 或服务端设置 | `setItem()`、`getItem()` 等 | `setItem()`、`getItem()` 等 |
| 典型用途 | 登录会话 | 主题、语言偏好 | 临时表单状态 |

需要注意，容量只是常见经验值，不同浏览器的具体限制可能有所差异。

## 六、IndexedDB

### 6.1 什么是 IndexedDB？

当需要在浏览器中保存大量数据、复杂对象或文件时，LocalStorage 通常就不够合适了。

IndexedDB 是浏览器提供的客户端数据库，适合保存大量结构化数据，支持索引、事务和异步读写。

例如，一个离线应用可能需要保存：

- 用户操作记录。
- 离线业务数据。
- 图片、文件和二进制数据。
- 需要按字段查询的大量本地记录。

这些场景都可以考虑使用 IndexedDB。

### 6.2 IndexedDB 的主要特点

**1. 支持结构化数据**

IndexedDB 使用对象仓库（Object Store）组织数据。记录通常具有唯一主键，可以保存符合结构化克隆算法要求的多种数据类型。

**2. 异步操作**

IndexedDB 的读写通过异步请求完成，不需要像 LocalStorage 那样同步执行每次读取或写入。

**3. 支持事务**

可以将多项数据库操作放入一个事务中。事务失败或被中止时，数据库不会只提交其中一部分修改，从而保证事务内部操作的原子性。

**4. 支持索引**

可以针对指定字段建立索引，避免大量数据查询时只能逐条遍历。

**5. 存储空间较大**

IndexedDB 通常能够存储远多于 LocalStorage 的数据，但实际配额取决于浏览器、设备空间和存储策略，并不存在适用于所有环境的固定容量。

**6. 受到同源策略限制**

网页通常只能访问自己所属源下的 IndexedDB 数据库，不能直接访问其他源的数据库。

### 6.3 IndexedDB 的基本使用思路

IndexedDB 的原生 API 相对复杂，基本流程如下：

1. 打开或创建数据库。
2. 在数据库升级过程中创建对象仓库。
3. 开启事务。
4. 通过对象仓库执行添加、读取、修改或删除操作。
5. 处理请求成功、失败以及事务完成等事件。

对于实际项目，可以使用封装库简化操作，例如 Dexie.js。

IndexedDB 更适合具有大量本地数据、复杂查询或离线需求的场景，不必为了保存几个简单键值就使用它。

## 七、Web SQL 为什么不推荐使用？

Web SQL 曾经提供基于 SQL 的浏览器本地关系型数据库能力，但该技术已经被废弃，不适合新项目采用。

现代前端开发应优先考虑 LocalStorage、SessionStorage 和 IndexedDB，根据数据结构和使用场景选择方案。

其中，IndexedDB 是需要保存大量结构化本地数据时更值得学习的技术。

## 八、浏览器存储的安全问题

浏览器本地存储不等于安全存储。

### 8.1 XSS 风险

如果攻击者能够在网站同源环境中执行恶意 JavaScript，就可能读取 LocalStorage、SessionStorage 以及非 `HttpOnly` Cookie 中的数据。

因此，不应将 LocalStorage 当作存储高敏感认证信息的安全保险箱。

### 8.2 CSRF 风险

Cookie 会在符合条件的请求中自动发送，因此某些跨站请求可能携带用户的身份凭证。

可以结合 `SameSite`、CSRF Token、Origin 校验等措施进行防护，具体方案需要根据认证架构决定。

### 8.3 HTTPS 与 Secure

`Secure` 限制 Cookie 仅通过安全连接发送，有助于减少传输过程中的凭证暴露风险。

但它不代表 Cookie 的值本身被加密，也不能代替完整的身份认证和安全设计。

### 8.4 不要信任客户端数据

LocalStorage、SessionStorage 和 IndexedDB 中的数据都可能被用户修改。

因此，客户端存储的数据可以用于改善用户体验，但不能代替服务端的权限校验、价格校验或业务规则验证。

## 九、前端项目中如何选择存储方式？

可以根据以下原则选择：

- **需要随 HTTP 请求发送的会话凭证**：考虑 Cookie，并正确设置安全属性。
- **需要长期保存的少量用户偏好**：考虑 LocalStorage。
- **只需要当前标签页暂时保留的数据**：考虑 SessionStorage。
- **需要大量数据、复杂查询、索引或离线能力**：考虑 IndexedDB。
- **需要跨设备同步的用户数据**：通常还需要服务端数据库，不能只依赖浏览器本地存储。

在 Vue 项目中，还需要注意：修改 LocalStorage 或 SessionStorage 不会自动触发 Vue 组件更新。若数据需要参与响应式渲染，应将其与 `ref`、`reactive` 或相应的状态管理逻辑结合使用。

## 十、总结

浏览器存储的核心不是记住所有 API，而是理解不同存储方案解决的问题。

- Cookie 主要服务于 HTTP 状态管理和会话凭证。
- LocalStorage 用于持久化保存少量字符串数据。
- SessionStorage 用于当前标签页会话期间的临时数据。
- IndexedDB 用于大量、结构化且需要异步访问的本地数据。

实际开发中，应综合考虑数据的生命周期、容量、共享范围、安全性以及是否需要发送到服务器，再选择合适的存储方式。

**记忆口诀：Cookie 管请求，LocalStorage 管持久，SessionStorage 管标签页会话，IndexedDB 管大量结构化数据。**
