---
title: "Promise 基础知识"
description: "Promise 是 JavaScript 中用于处理异步操作的一种解决方案，最早由社区提出，后来被纳入 ECMAScript 标准。"
date: "2026-10-10"
publishedAt: "2026-10-10T09:30:48.979354+08:00"
source: "https://kajspace.cn/articles/01M4HPY254CYHYEP7FV6QDEN3M/"
tags: ["前端"]
---

# Promise 基础知识

<span id="kaj-h-92cbf944-ec17-4f95-b215-13902294c0fb"></span>

Promise 是 JavaScript 中用于处理异步操作的一种解决方案，最早由社区提出，后来被纳入 ECMAScript 标准。

## 1. Promise 的基本概念 {#kaj-h-5ced71ac-bf6b-41b5-9ac1-59dce8b30fb1}

Promise 是一个构造函数，接收一个执行器函数（executor）作为参数，并返回一个 Promise 实例。

```js
const promise = new Promise((resolve, reject) => {
    // 执行器函数中的代码会立即执行
});
```

执行器函数接收两个参数：

- `resolve(value)`：用于将 Promise 兑现为成功状态，并传递成功结果。
- `reject(reason)`：用于将 Promise 变为失败状态，并传递失败原因。

## 2. Promise 的三种状态 {#kaj-h-4df331e6-c688-4589-8783-634bafa55ff5}

Promise 有三种状态：

- `pending`：待定状态，表示操作尚未确定结果。
- `fulfilled`：已兑现状态，表示操作成功。
- `rejected`：已拒绝状态，表示操作失败。

Promise 的状态只能从 `pending` 转变为 `fulfilled` 或 `rejected`。一旦进入 `fulfilled` 或 `rejected` 状态，就不能再改变。

注意：`resolved` 经常被用来描述 Promise 已经确定了结果，但它不完全等同于 `fulfilled`。在规范中，Promise 的三种状态是 `pending`、`fulfilled` 和 `rejected`。

## 3. Promise 的 then 方法 {#kaj-h-f427af95-5ef1-49bd-a304-b3f22d4f0e28}

Promise 实例的原型上定义了 `then()` 方法，用于注册成功和失败时的回调函数。

```js
const promise = new Promise((resolve, reject) => {
    resolve('成功');
});

promise.then(
    result => {
        console.log(result);
    },
    error => {
        console.log(error);
    }
);
```

`then()` 的第一个参数是成功回调，第二个参数是失败回调。

当相应的回调需要执行时，它们会被安排为微任务，而不是立即同步执行。

## 4. Promise 构造函数的执行时机 {#kaj-h-8464a9dc-6e56-48a7-b884-347076b0b35d}

创建 Promise 实例时，传入的执行器函数会立即同步执行。

```js
console.log('1');

const promise = new Promise((resolve, reject) => {
    console.log('2');
    resolve();
});

promise.then(() => {
    console.log('4');
});

console.log('3');

// 输出：
// 1
// 2
// 3
// 4
```

原因：

1. 输出 `1`。
2. 创建 Promise，执行器函数同步执行，输出 `2`。
3. `resolve()` 使 Promise 成功，`then()` 注册的回调会被安排为微任务。
4. 同步代码继续执行，输出 `3`。
5. 当前同步代码执行完毕后，执行微任务，输出 `4`。

因此，Promise 的执行器函数是同步执行的，而 `then()` 注册的回调是在相应的微任务中执行的。

## 你需要特别理解的三个细节 {#kaj-h-b32dae25-21c7-40ef-aadd-0a6187ea4dac}

### 1. `resolved` 和 `fulfilled` 有什么区别？ {#kaj-h-ced89fa1-ba9c-44f3-a4f6-cba31990db10}

这是最容易混淆的知识点。

- `fulfilled`：Promise 已经成功兑现。
- `resolved`：Promise 的结果已经确定，或者已经被锁定为跟随另一个 Promise 的结果。

例如：

```js
const p1 = new Promise(resolve => {
    resolve(
        new Promise(resolve2 => {
            setTimeout(() => resolve2('成功'), 1000);
        })
    );
});
```

调用 `resolve()` 后，`p1` 已经确定要跟随内部 Promise 的状态，但它不会立即变成 `fulfilled`，而是要等内部 Promise 成功后才兑现。

所以，日常讲解可以把 `resolved` 粗略理解为已确定结果，但描述 Promise 的标准三种状态时，建议使用 `pending`、`fulfilled` 和 `rejected`。

### 2. 调用 `resolve()` 后，代码会立即停止吗？ {#kaj-h-48e8f9e2-0516-4de5-a120-4858d12b0d6f}

不会。

```js
const p = new Promise(resolve => {
    console.log('A');
    resolve();
    console.log('B');
});

console.log('C');
```

输出：

```text
A
B
C
```

`resolve()` 不会终止当前函数的执行，也不会让后面的同步代码跳过。它只是尝试确定 Promise 的结果。

如果想提前结束当前执行器函数，需要使用 `return`：

```js
const p = new Promise(resolve => {
    console.log('A');
    resolve();
    return;
    console.log('B'); // 不执行
});
```

### 3. 为什么 `then()` 的回调属于微任务？ {#kaj-h-70db8461-23ab-4e7b-a652-c507ebb18dab}

因为 Promise 的回调执行遵循 JavaScript 的微任务调度机制。

```js
console.log('开始');

Promise.resolve().then(() => {
    console.log('Promise 回调');
});

console.log('结束');
```

执行顺序：

1

输出 `开始`

2

注册 Promise 回调，安排微任务

3

输出 `结束`

4

同步代码执行完毕，执行微任务，输出 `Promise 回调`

记住这句话：创建 Promise 时，执行器同步执行；调用 `then()` 注册的回调，不会作为同步代码立即执行，而是通过微任务调度执行。

另外，微任务并不是严格意义上的“事件循环末尾才执行”：在浏览器中，更准确的说法是，当前同步执行栈清空后，会在适当的事件循环检查点清空微任务队列，期间新加入的微任务通常也会继续执行。
