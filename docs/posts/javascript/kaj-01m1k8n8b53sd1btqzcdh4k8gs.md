---
title: "ES6 模块和 CommonJS 模块的区别"
description: "ES6 Module（ESM）是 JavaScript 官方标准模块系统，使用 import/export；CommonJS 是 Node.js 传统的模块系统，使用 require/module.exports。"
date: "2026-09-03"
publishedAt: "2026-09-03T17:13:02.883149+08:00"
source: "https://kajspace.cn/articles/01M1K8N8B53SD1BTQZCDH4K8GS/"
tags: ["前端"]
---

# ES6 模块和 CommonJS 模块的区别

## 一句话先记住 {#kaj-h-4600b040-04af-40a6-b17b-0f585e5e02c0}

> **ES6 Module（ESM）是 JavaScript 官方标准模块系统，使用** `import/export`**；CommonJS 是 Node.js 传统的模块系统，使用** `require/module.exports`**。**

---

## 1. 语法不同 {#kaj-h-f5af503c-e812-4e2e-9542-831ba6cb2542}

### ES6 Module {#kaj-h-374674a2-2b92-4d9c-bc50-524325dfb762}

导出：

```js
// math.js
export const add = (a, b) => a + b;
export const sub = (a, b) => a - b;
```

导入：

```js
// main.js
import { add, sub } from './math.js';

console.log(add(1, 2));
```

也可以默认导出：

```js
export default function add(a, b) {
    return a + b;
}
```

导入：

```text
import add from './math.js';
```

---

### CommonJS {#kaj-h-1f97b83d-1f8f-4313-a28a-c99aa5d34f0f}

导出：

```js
// math.js
function add(a, b) {
    return a + b;
}

module.exports = {
    add
};
```

导入：

```js
const { add } = require('./math.js');

console.log(add(1, 2));
```

所以最基本的区别：

```text
ES Module
import / export

CommonJS
require / module.exports
```

---

## 2. 加载方式不同：静态 vs 动态 {#kaj-h-f9079826-16d2-4821-a650-74d28a7a21e0}

这是**面试最重要的区别之一**。

### ES Module：静态加载 {#kaj-h-8b5ae2f3-2e82-4ec0-9979-688e7a2c012e}

```text
import { add } from './math.js';
```

`import` 通常必须写在模块顶层。

```js
// ❌ 普通情况下不能这样
if (condition) {
    import { add } from './math.js';
}
```

因为 ES Module 的依赖关系可以在代码**真正执行之前**就被分析出来。

所以：

```text
ESM
 ↓
先分析依赖关系
 ↓
再执行代码
```

这也是为什么 ESM 更方便做：

- Tree Shaking
- 静态分析
- 打包优化

---

### CommonJS：运行时加载 {#kaj-h-3a219e95-e4fe-490d-afc7-87cec0e4eeab}

```js
const math = require('./math.js');
```

`require()` 本质上是运行时函数调用，因此可以放在条件里面：

```js
if (condition) {
    const math = require('./math.js');
}
```

所以：

```text
ESM
静态分析

CommonJS
运行时加载
```

---

## 3. 执行时机不同 {#kaj-h-ba50b404-97a4-42ee-89a8-57d7a3598678}

CommonJS：

```js
const a = require('./a.js');
```

执行到这里的时候，才加载 `a.js`。

而 ESM 在模块执行前，就会先处理模块之间的依赖关系。

可以简单理解：

```text
CommonJS：

执行 main.js
    ↓
执行到 require()
    ↓
加载模块
    ↓
执行模块
    ↓
继续 main.js
```

ESM：

```text
解析模块
 ↓
分析 import 依赖
 ↓
建立模块依赖关系
 ↓
加载模块
 ↓
执行模块
```

---

## 4. 导出值的机制不同 {#kaj-h-da2e6c39-1361-4ba7-8dbc-15ccc3b03dd7}

这是稍微进阶一点的面试点。

ESM 使用的是**实时绑定（live binding）**。

例如：

```js
// counter.js
export let count = 0;

export function add() {
    count++;
}
```

```js
// main.js
import { count, add } from './counter.js';

console.log(count); // 0

add();

console.log(count); // 1
```

`count` 是模块中的实时绑定。

而 CommonJS：

```text
module.exports = {
    count: 0
};
```

本质上是导出一个对象。

所以面试时可以简单说：

> **ES Module 的导入是对导出绑定的引用，而 CommonJS 更接近于导出对象/值。**

---

## 5. CommonJS 主要用于 Node.js {#kaj-h-945ab06b-3b39-47d2-afa3-00eb12f91966}

传统 Node.js：

```js
const fs = require('fs');

const express = require('express');
```

大量 Node.js 项目以前都是 CommonJS。

例如：

```text
module.exports = {
    name: 'Tom'
};
```

然后：

```js
const user = require('./user');

console.log(user.name);
```

---

## 6. ES Module 主要是现代 JavaScript 标准 {#kaj-h-24644156-e54e-4be9-b6d5-0c64b5333c1d}

浏览器原生支持：

```html
<script type="module" src="./main.js"></script>
```

然后：

```js
// main.js
import { add } from './math.js';

console.log(add(1, 2));
```

所以 ESM 是**JavaScript 官方标准模块化方案**。

现代 Node.js 也支持 ESM。

---

## 7. 两者都可以解决什么问题？ {#kaj-h-ae88df74-c7f8-4982-9f19-19588628d1ae}

模块化主要解决：

### ① 避免全局变量污染 {#kaj-h-142f576f-b289-4274-a8e2-d87945be18c3}

没有模块化：

```js
var name = 'Tom';
var age = 20;
```

不同 JS 文件可能互相覆盖变量。

模块化之后：

```js
// user.js
export const name = 'Tom';
```

只有显式：

```text
import { name } from './user.js';
```

才能使用。

---

### ② 拆分代码 {#kaj-h-05f4c310-da51-4076-85c5-940d678f724a}

例如：

```text
src/
├── main.js
├── user.js
├── request.js
├── utils.js
└── math.js
```

每个模块负责不同功能。

---

### ③ 管理依赖关系 {#kaj-h-1a86718f-c5e6-43b4-90d1-f97b9b14f412}

例如：

```text
import { request } from './request.js';
import { formatDate } from './utils.js';
```

可以非常清楚地看到：

> `main.js` 依赖 `request.js` 和 `utils.js`。

---

## 8. 面试对比表 {#kaj-h-a7bb1099-f1ba-4006-88eb-3992851072f3}

|  | ES Module | CommonJS |
| --- | --- | --- |
| 标准 | JS 官方标准 | Node.js 传统模块规范 |
| 导入 | `import` | `require()` |
| 导出 | `export` | `module.exports` / `exports` |
| 加载 | 静态 | 运行时 |
| 依赖分析 | 编译/解析阶段可分析 | 执行时分析 |
| Tree Shaking | 支持，比较友好 | 较难做 |
| 浏览器 | 原生支持 | 浏览器不能直接运行 |
| Node.js | 支持 | 支持 |
| 常见扩展 | `.mjs` / 配置决定 | `.cjs` / Node 默认传统模式 |

---

## 9. 面试直接这样回答 {#kaj-h-e1de7d0f-4110-459b-b718-3f87586d2ead}

如果面试官问：

> **ES6 模块和 CommonJS 模块有什么区别？**

你可以直接回答：

> **ES6 Module 是 JavaScript 官方标准的模块化方案，使用** `import/export`**；CommonJS 是 Node.js 传统的模块化方案，使用** `require` **和** `module.exports`**。**
> 
> 
> 
> **最大的区别之一是加载机制：ES Module 是静态加载，模块依赖关系可以在代码执行前确定，因此更利于静态分析和 Tree Shaking；CommonJS 是运行时加载，**`require` **可以根据运行时条件动态执行。**
> 
> 
> 
> **另外，ES Module 在浏览器中可以原生使用，而 CommonJS 主要用于 Node.js 环境。现代 Node.js 两种模块系统都支持。**

### 你现在重点记这条就够了： {#kaj-h-ebf95e54-390b-4ad5-81c5-2db87dd41533}

```text
ESM：
import / export
静态加载
官方标准
浏览器原生支持
Tree Shaking 友好

CommonJS：
require / module.exports
运行时加载
Node.js 传统方案
```

这道题在你准备前端秋招时，**“静态加载 vs 运行时加载”** 是最值得展开讲的点。
