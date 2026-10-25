---
title: iframe + postMessage 如何保证通信安全？
category: browser
description: 理解 iframe 窗口引用与跨源通信，通过 targetOrigin、event.origin、event.source、消息内容校验及权限控制构建安全的 postMessage 通信。
date: "2026-10-25"
publishedAt: "2026-10-25T20:35:20+08:00"
tags:
  - postMessage
  - iframe
  - 浏览器安全
  - 跨源通信
  - 前端八股
---

# iframe + postMessage 如何保证通信安全？

在前端开发中，父页面与 iframe 子页面经常需要进行跨窗口通信。例如，主应用需要获取嵌入页面的数据，或者嵌入的第三方页面需要向主应用发送操作结果。

浏览器提供了 `window.postMessage()` API 来解决跨源窗口之间的通信问题。但是，跨窗口通信也存在安全风险。如果接收方没有正确校验消息来源和消息内容，恶意页面就可能伪造消息，诱导应用执行非预期操作。

本文将从 `postMessage` 的基本原理出发，介绍通信过程中常见的安全问题，以及如何通过 `targetOrigin`、`event.origin`、`event.source` 和消息内容校验来提高通信安全性。

## 一、什么是 iframe + postMessage？

### 1. iframe 的基本概念

`iframe` 是 HTML 提供的内嵌框架，可以在当前页面中嵌入另一个 HTML 页面。

例如：

```html
<iframe
  id="myIframe"
  src="https://child.example.com"
></iframe>
```

这里，父页面运行在 `https://app.example.com`，而 iframe 加载的是 `https://child.example.com`。

由于两个页面的域名不同，它们属于不同源。浏览器的同源策略会限制它们直接访问对方的 DOM 和部分 JavaScript 数据。

### 2. postMessage 的作用

`postMessage()` 允许不同源的窗口之间安全地传递消息。

父页面可以通过 `iframe.contentWindow` 获取 iframe 对应的窗口对象，并向其发送消息：

```js
const iframe = document.querySelector('#myIframe');

iframe.contentWindow.postMessage(
  {
    type: 'GET_USER_INFO',
    payload: {}
  },
  'https://child.example.com'
);
```

子页面通过监听 `message` 事件接收消息：

```js
window.addEventListener('message', (event) => {
  console.log(event.data);
});
```

其中，`event.data` 是接收到的消息内容。

需要注意：`postMessage` 解决的是跨窗口通信问题，并不意味着接收到的消息天然可信。接收方仍然需要校验消息来源和内容。

## 二、理解窗口引用：iframe.contentWindow

要理解 iframe 通信的安全问题，首先需要理解什么是窗口引用。

### 1. 什么是窗口引用？

父页面可以通过以下代码获取 iframe 对应的窗口对象：

```js
const iframe = document.querySelector('#myIframe');

const childWindow = iframe.contentWindow;
```

这里的 `iframe.contentWindow` 是 iframe 对应的浏览上下文的窗口对象。

可以简单地将它理解为一个房间的地址：父页面通过这个引用，可以向对应的窗口发送消息。

例如：

```js
childWindow.postMessage(
  { type: 'HELLO' },
  'https://child.example.com'
);
```

这里，`childWindow` 表示消息要发送到哪个窗口，而第二个参数指定允许接收消息的目标来源。

### 2. 为什么窗口引用不能单独证明来源可信？

假设 iframe 最初加载的是：

```html
<iframe
  id="myIframe"
  src="https://child.example.com"
></iframe>
```

父页面获取窗口引用：

```js
const iframe = document.querySelector('#myIframe');
const childWindow = iframe.contentWindow;
```

此时，iframe 中加载的是可信网页 `child.example.com`。

但是，如果 iframe 后续导航到另一个网页：

```js
iframe.src = 'https://evil.example.com';
```

浏览器就会尝试在这个 iframe 中加载新的网页。

在普通的 iframe 页面导航过程中，`iframe.contentWindow` 通常仍然指向同一个浏览上下文，但其中加载的文档已经发生变化。

因此，下面的代码存在安全隐患：

```js
window.addEventListener('message', (event) => {
  if (event.source === iframe.contentWindow) {
    // 不能仅凭这一条件就信任消息
  }
});
```

为什么？

因为 `event.source` 主要用于判断消息来自哪个窗口。即使消息来自预期的 iframe 窗口，也不能仅凭这一点证明发送消息的网页仍然是可信网页。

**核心结论：窗口引用可以帮助确认通信窗口，但不能单独证明该窗口中当前发送消息的文档来自可信来源。**

## 三、postMessage 中三个重要的安全属性

### 1. targetOrigin：限制消息的目标来源

调用 `postMessage()` 时，可以指定第二个参数 `targetOrigin`。

例如：

```js
iframe.contentWindow.postMessage(
  { type: 'GET_USER_INFO' },
  'https://child.example.com'
);
```

这里的 `targetOrigin` 指定了消息允许发送到的目标来源。

如果目标窗口在消息发送时的来源与指定值不匹配，浏览器就不会将消息发送给该文档。

不推荐这样写：

```js
iframe.contentWindow.postMessage(
  { type: 'GET_USER_INFO' },
  '*'
);
```

使用 `'*'` 意味着不限制目标来源。如果 iframe 被导航到了其他来源，消息就可能被发送给非预期的页面。

因此，在目标来源明确时，应使用精确的来源地址。

### 2. event.origin：校验消息发送方的来源

接收方可以通过 `event.origin` 获取发送消息时发送方文档的来源。

例如：

```js
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://app.example.com') {
    return;
  }

  console.log('收到允许来源发送的消息');
});
```

这里，只有来源严格匹配 `https://app.example.com` 的消息才会继续处理。

来源通常由协议、主机名和端口构成，因此以下地址并不等价：

- `https://app.example.com`
- `http://app.example.com`
- `https://app.example.com:8443`
- `https://evil.example.com`

必须注意，`event.origin` 表示发送消息时发送方文档的来源，而不是接收方当前的来源。

### 3. event.source：校验消息来自哪个窗口

父页面接收 iframe 消息时，可以检查 `event.source` 是否为预期 iframe 的窗口对象。

```js
const iframe = document.querySelector('#myIframe');

window.addEventListener('message', (event) => {
  if (event.source !== iframe.contentWindow) {
    return;
  }

  console.log('消息来自预期的 iframe 窗口');
});
```

这可以避免将其他窗口发送的消息误认为来自预期 iframe。

但是，正如前文所述，iframe 内部可以加载不同来源的网页，因此还必须检查 `event.origin`。

综合来看：

| 属性 | 主要作用 | 不能单独解决的问题 |
|---|---|---|
| `targetOrigin` | 限制消息的目标来源 | 不能代替接收方对消息的校验 |
| `event.origin` | 校验发送方文档的来源 | 不能证明消息内容和业务参数一定可信 |
| `event.source` | 校验发送消息的窗口对象 | 不能单独证明窗口中加载的文档来源可信 |

三者配合使用，才能更可靠地控制跨窗口通信。

## 四、如何编写更安全的通信代码？

下面以父页面 `https://app.example.com` 和子页面 `https://child.example.com` 为例。

### 1. 父页面向 iframe 发送消息

```js
const iframe = document.querySelector('#myIframe');

iframe.contentWindow.postMessage(
  {
    type: 'GET_USER_INFO',
    payload: {}
  },
  'https://child.example.com'
);
```

关键点：

1. 使用 `iframe.contentWindow` 指定目标窗口。
2. 使用精确的 `targetOrigin`。
3. 不将敏感数据随意发送给来源不确定的页面。

### 2. iframe 子页面接收消息

```js
const ALLOWED_ORIGIN = 'https://app.example.com';

window.addEventListener('message', (event) => {
  // 1. 校验发送方来源
  if (event.origin !== ALLOWED_ORIGIN) {
    return;
  }

  // 2. 校验发送窗口
  if (event.source !== window.parent) {
    return;
  }

  // 3. 校验消息结构
  const data = event.data;

  if (
    data === null ||
    typeof data !== 'object' ||
    Array.isArray(data)
  ) {
    return;
  }

  // 4. 校验消息类型
  if (data.type !== 'GET_USER_INFO') {
    return;
  }

  // 5. 执行允许的业务逻辑
  console.log('处理获取用户信息的请求');
});
```

子页面通过 `event.origin` 确认发送方来源，通过 `event.source` 确认消息来自父窗口，再检查消息结构和类型。

如果消息包含更复杂的参数，还应进一步校验必需字段、字段类型、字符串长度和允许的取值范围。

### 3. 父页面接收 iframe 消息

安全校验是双向的。父页面不能因为消息来自 iframe，就直接信任其内容。

```js
const iframe = document.querySelector('#myIframe');
const CHILD_ORIGIN = 'https://child.example.com';

window.addEventListener('message', (event) => {
  // 1. 校验来源
  if (event.origin !== CHILD_ORIGIN) {
    return;
  }

  // 2. 校验窗口
  if (event.source !== iframe.contentWindow) {
    return;
  }

  // 3. 校验消息格式
  const data = event.data;

  if (
    data === null ||
    typeof data !== 'object' ||
    Array.isArray(data)
  ) {
    return;
  }

  // 4. 只接受白名单消息类型
  if (data.type !== 'USER_INFO') {
    return;
  }

  // 5. 处理经过基础校验的消息
  console.log(data.payload);
});
```

以上代码展示了基本的防护结构。生产环境中，还应对 `payload` 使用更严格的结构校验，并根据实际业务限制消息频率和可执行操作。

## 五、除了来源校验，还需要注意什么？

### 1. 不要将消息来源校验等同于身份认证

即使 `event.origin` 正确，也不意味着消息中的用户身份、用户 ID 或业务参数一定可信。

例如：

```js
{
  type: 'DELETE_USER',
  payload: {
    userId: 1001
  }
}
```

不能因为消息来自可信域名，就直接执行删除用户操作。

如果涉及删除数据、修改账户信息、支付等敏感操作，还需要：

- 校验当前用户的身份和权限。
- 检查业务参数是否合法。
- 在服务端再次进行授权和业务校验。
- 对重要操作实施必要的审计和防重放措施。

### 2. 不要直接执行接收到的 HTML 或 JavaScript

以下代码存在风险：

```js
element.innerHTML = event.data.html;
```

```js
eval(event.data.code);
```

如果消息内容可被攻击者控制，就可能造成跨站脚本攻击（XSS）或任意代码执行。

更安全的做法是定义固定的消息协议，只接收明确的消息类型和数据字段，并优先使用 `textContent` 等安全的 DOM API 展示文本。

### 3. 使用消息类型白名单

不应让接收方根据任意传入的字符串执行函数：

```js
// 不推荐
handlers[event.data.type](event.data.payload);
```

如果 `handlers` 中包含敏感操作，或者没有检查消息类型是否属于允许范围，就可能导致非预期的函数调用。

更推荐显式分支：

```js
switch (data.type) {
  case 'GET_USER_INFO':
    // 执行允许的操作
    break;

  case 'CLOSE_DIALOG':
    // 执行允许的操作
    break;

  default:
    // 拒绝未知消息
    return;
}
```

### 4. 不能把消息内容当作可信凭证

即使来源正确，也不要直接信任消息中携带的角色、权限或身份标识。

例如，以下数据不能直接作为授权依据：

```js
{
  type: 'USER_INFO',
  payload: {
    role: 'admin'
  }
}
```

真正的权限判断应建立在可靠的身份认证和服务端授权机制上，而不是仅依赖前端传递的数据。

## 六、总结

`iframe + postMessage` 通信安全的核心，是明确通信双方的身份边界，并对接收到的消息进行多层校验。

可以总结为以下五点：

1. **校验目标来源：** 发送消息时使用精确的 `targetOrigin`，避免不必要地使用 `'*'`。
2. **校验发送方来源：** 接收消息时检查 `event.origin`。
3. **校验发送窗口：** 检查 `event.source` 是否为预期的窗口对象。
4. **校验消息内容：** 对消息结构、类型、参数和允许执行的操作进行白名单校验。
5. **实施权限控制：** 对敏感业务在服务端进行身份认证、授权和参数校验。

其中最容易混淆的是 `event.source` 和 `event.origin`：前者用于判断消息来自哪个窗口，后者用于判断发送消息时该文档属于哪个来源。

由于 iframe 可以在同一个浏览上下文中导航到其他页面，窗口引用并不能单独证明当前消息来自可信来源。因此，二者需要结合使用。

最后需要牢记：**来源校验解决的是消息来自哪里的问题，消息校验解决的是消息是否合法的问题，权限校验解决的是这项操作是否允许执行的问题。** 三者共同构成了更完整的跨窗口通信安全方案。

参考资料：[MDN：Window.postMessage()](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/postMessage)
