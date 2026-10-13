---
title: "手写Promise.all"
description: "这段代码是在手写 Promise.all()，核心作用是：接收多个 Promise，等待它们全部成功后，按照原来的顺序返回所有结果；只要有一个失败，就让最终返回的 Promise 失败。"
date: "2026-10-12"
publishedAt: "2026-10-12T09:52:36.324138+08:00"
source: "https://kajspace.cn/articles/01KZQYVBZFR38YCPYX6PV88PGC/"
tags: ["前端"]
---

# 手写Promise.all

![正文图片](/images/kajspace/9a5033d091de9091.png)![正文图片](/images/kajspace/6e0c80399938e3c7.png)

这段代码是在手写 `Promise.all()`，核心作用是：接收多个 Promise，等待它们全部成功后，按照原来的顺序返回所有结果；只要有一个失败，就让最终返回的 Promise 失败。

理解这段代码，最关键的是分清楚三个东西：

- `resolve`：让当前 Promise 成功完成。
- `reject`：让当前 Promise 失败。
- `.then()` 和 `.catch()`：分别处理 Promise 成功和失败的情况。

下面我们逐行分析，重点解释每个 `resolve` 的作用，以及什么时候进入 `then` 和 `catch`。

## 一、先看完整代码 {#kaj-h-4a9ab5e4-ff73-40b9-be10-a7ad9fc08ad5}

```js

function myPromiseAll(promises) {
    return new Promise((resolve, reject) => {
        let count = 0;
        const results = [];

        promises.forEach((promise, index) => {
            Promise.resolve(promise)
                .then(value => {
                    results[index] = value;
                    count++;

                    if (count === promises.length) {
                        resolve(results);
                    }
                })
                .catch(reject);
        });
    });
}
```

例如：

```js
const p1 = Promise.resolve('A');
const p2 = Promise.resolve('B');
const p3 = Promise.resolve('C');

myPromiseAll([p1, p2, p3]).then(results => {
    console.log(results); // ['A', 'B', 'C']
});
```

三个 Promise 全部成功后，最终得到 `['A', 'B', 'C']`。

## 二、最外层的 `new Promise((resolve, reject) => {})` {#kaj-h-45c0d854-4cc9-4762-9239-88d87aaf2e9c}

先看这一行：

```js
return new Promise((resolve, reject) => {
    // ...
});
```

这里创建了一个新的 Promise，我们暂且称它为 `P`。

JavaScript 会立即执行 `new Promise()` 中的执行器函数，并传入两个函数：

- `resolve`：用于将 `P` 兑现为成功结果。
- `reject`：用于将 `P` 以失败状态拒绝。

可以把它理解为：

```js
const P = new Promise((resolve, reject) => {
    // 这里决定 P 最终成功还是失败
});

return P;
```

注意：这两个函数不是我们自己定义的普通业务函数，而是创建 Promise 时由 JavaScript 提供的函数。

此时，`P` 初始处于 `pending` 状态，也就是等待状态。

接下来，代码会遍历传入的 `promises`，逐个处理它们。

## 三、`Promise.resolve(promise)` 是什么意思？ {#kaj-h-466ed4ae-cc32-4448-ab53-b37c9f4b50ac}

代码：

```js
Promise.resolve(promise)
    .then(value => {
        // 成功处理
    })
    .catch(reject);
```

这里的 `Promise.resolve()` 是一个静态方法，它的作用是把传入的值转换成 Promise。

具体分为三种情况：

| 传入的值 | `Promise.resolve()` 的结果 |
| --- | --- |
| 普通值，例如 `123` | 返回一个成功的 Promise，结果为 `123` |
| 已经成功的 Promise | 采用该 Promise 的最终状态和结果 |
| 尚未完成的 Promise | 等待它最终成功或失败 |

例如：

```js
Promise.resolve(123).then(value => {
    console.log(value); // 123
});
```

即使传入的是普通数字，也可以使用 `.then()` 处理它。

为什么这里需要 `Promise.resolve(promise)`？

因为调用者传入的数组不一定全部由 Promise 组成：

```text
myPromiseAll([
    Promise.resolve(1),
    2,
    'hello'
]);
```

通过 `Promise.resolve()`，这三项都可以使用统一的 `.then()` 和 `.catch()` 处理方式。

注意：如果传入的 Promise 最终失败，`Promise.resolve(promise)` 不会把它变成成功状态，而是会采用它的失败状态。

## 四、什么时候进入 `.then()`？ {#kaj-h-133352db-e183-4777-94d7-f80deb37069b}

代码：

```js
.then(value => {
    results[index] = value;
    count++;

    if (count === promises.length) {
        resolve(results);
    }
})
```

`.then()` 的第一个回调，通常称为成功回调。当它前面的 Promise 成功兑现时，回调就会进入微任务队列，并在适当时机执行。

例如：

```js
const p1 = Promise.resolve('A');

p1.then(value => {
    console.log(value); // A
});
```

`p1` 成功兑现，`.then()` 的回调就会执行，`value` 接收到 Promise 的成功结果 `'A'`。

对于你的代码：

```js
Promise.resolve(promise).then(value => {
    results[index] = value;
    count++;
});
```

只要当前这项 `promise` 最终成功兑现，就会进入这个 `.then()`。

### 1. 如果传入的是已经成功的 Promise {#kaj-h-060a0c51-ca31-4375-8ba8-dcf556efb632}

```js
const p1 = Promise.resolve('A');
```

执行：

```js
Promise.resolve(p1).then(value => {
    console.log(value);
});
```

这里 `Promise.resolve(p1)` 会采用 `p1` 的成功结果，随后 `.then()` 的成功回调执行，`value` 为 `'A'`。

注意，即使 `p1` 已经成功，`.then()` 的回调也不会在注册时同步执行，而是通过微任务机制调度执行。

### 2. 如果传入的是还没完成的 Promise {#kaj-h-a3367b93-02c6-44c9-9acb-ee3425513ba2}

```js
const p1 = new Promise(resolve => {
    setTimeout(() => {
        resolve('A');
    }, 1000);
});
```

此时：

1. `p1` 初始处于 `pending` 状态。
2. `Promise.resolve(p1)` 等待它的最终结果。
3. 约 1 秒后，内部的 `resolve('A')` 被调用。
4. `p1` 成功兑现为 `'A'`。
5. `.then()` 的成功回调随后执行，`value` 为 `'A'`。

### 3. 如果传入的是失败的 Promise 呢？ {#kaj-h-cb696e4d-80c7-44fe-be6d-71dd20e763d0}

```js
const p1 = Promise.reject('出错了');

Promise.resolve(p1).then(value => {
    console.log(value);
});
```

这里不会正常执行成功回调，因为 `p1` 是失败状态。

如果后面没有处理失败的回调，就可能产生未处理的 Promise 拒绝。

而你的代码在 `.then()` 后面还接了 `.catch(reject)`，所以失败会交给 `catch` 处理。

## 五、`results[index] = value` 和 `count++` 的作用 {#kaj-h-68f7fa70-3825-44cc-8ff2-b91300a928c2}

```text
results[index] = value;
count++;
```

这两行分别解决两个问题。

### 1. `results[index] = value`：保存结果并保持顺序 {#kaj-h-a30106a8-42d4-4d96-ba18-3233e61816ab}

例如：

```js
const promises = [
    Promise.resolve('A'),
    Promise.resolve('B'),
    Promise.resolve('C')
];
```

假设三个 Promise 的完成顺序是：

```text
第二项先完成
第三项第二个完成
第一项最后完成
```

也就是完成顺序为 `B → C → A`。

如果使用：

```text
results.push(value);
```

就可能得到：

```text
['B', 'C', 'A']
```

但 `Promise.all()` 要求结果按照输入数组的顺序排列。

因此代码使用：

```text
results[index] = value;
```

每个 Promise 都写入自己的原始索引位置，最终结果仍然是：

```text
['A', 'B', 'C']
```

### 2. `count++`：统计已经成功的 Promise 数量 {#kaj-h-6681e98c-754e-4758-a886-3592006677c5}

每进入一次成功回调，就执行：

```text
count++;
```

例如，三个 Promise 成功后，`count` 会依次变成：

```text
第一个成功：count = 1
第二个成功：count = 2
第三个成功：count = 3
```

当成功数量等于输入数组长度时，说明全部成功了。

```js
if (count === promises.length) {
    resolve(results);
}
```

这就引出了这段代码中最重要的 `resolve`。

## 六、两个 `resolve` 到底有什么区别？ {#kaj-h-3107f431-a054-4256-9c5d-913895172946}

这段代码容易混淆的地方，是把 `Promise.resolve()` 和 `resolve()` 当成同一个东西。

它们不是一回事。

### 1. `Promise.resolve(promise)` {#kaj-h-42ef3b9d-be16-4a36-b413-63c6f2bf1a7c}

静态方法

把传入的值转换为 Promise，或让返回的 Promise 采用传入 Promise 的最终状态和结果。

```js
Promise.resolve(123).then(console.log);
// 输出 123
```

### 2. `resolve(results)` {#kaj-h-8f4a2d63-4cd1-4249-ae85-a8754a5ba9f4}

外层 Promise 的成功函数

将 `myPromiseAll()` 返回的那个 Promise 成功兑现，结果就是整个 `results` 数组。

```text
resolve(['A', 'B', 'C']);
```

之后，调用者注册的成功回调就能拿到整个数组。

可以把两者的关系理解为：

```js
每一项 Promise
    ↓
Promise.resolve(promise)
    ↓
等待当前项成功或失败
    ↓
成功时进入 then，失败时进入 catch
    ↓
每次成功都记录结果并增加 count
    ↓
所有项都成功
    ↓
resolve(results)
    ↓
myPromiseAll 返回的外层 Promise 成功
    ↓
调用者的 .then(results => ...) 执行
```

关键点： `Promise.resolve(promise)` 负责统一处理单项输入；`resolve(results)` 负责宣布整个 `myPromiseAll()` 的任务已经成功完成。

## 七、什么时候进入 `.catch(reject)`？ {#kaj-h-c08081d2-598c-4146-8f88-9ae4f486c3fb}

代码：

```js
Promise.resolve(promise)
    .then(value => {
        results[index] = value;
        count++;

        if (count === promises.length) {
            resolve(results);
        }
    })
    .catch(reject);
```

先记住一个原则：

- `.then()` 的成功回调：前面的 Promise 成功时执行。
- `.catch()` 的回调：前面的 Promise 链发生未处理的拒绝时执行。

### 1. 单项 Promise 失败时 {#kaj-h-c215d9a7-22f2-4a70-b6f4-7bad38f69732}

例如：

```js
const p1 = Promise.reject('请求失败');

Promise.resolve(p1)
    .then(value => {
        console.log('成功：', value);
    })
    .catch(error => {
        console.log('失败：', error);
    });
```

执行结果：

```text
失败： 请求失败
```

原因是：

1. `p1` 已经是 rejected 状态。
2. `Promise.resolve(p1)` 会采用它的失败状态。
3. `.then()` 没有提供失败回调，因此不会进入其中的成功回调。
4. 拒绝继续向后传递，最终进入 `.catch()`。

### 2. `.catch(reject)` 为什么可以直接传 `reject`？ {#kaj-h-8f4b0436-1952-4277-b998-51513f2c4879}

你可能会疑惑，为什么这里不是：

```js
.catch(error => {
    reject(error);
});
```

而是直接写：

```text
.catch(reject);
```

因为这两种写法在这里效果相同。

`.catch(reject)` 相当于将外层 Promise 的 `reject` 函数作为错误处理回调传进去。当错误到来时，JavaScript 会将错误原因作为参数传给它。

例如：

```text
.catch(reject);
```

可以理解为：

```js
.catch(error => {
    reject(error);
});
```

这样，当前某一项 Promise 的失败就会传递给外层 Promise。

例如：

```js
myPromiseAll([
    Promise.resolve('A'),
    Promise.reject('B 失败'),
    Promise.resolve('C')
]).then(results => {
    console.log('成功：', results);
}).catch(error => {
    console.log('失败：', error);
});
```

结果：

```text
失败： B 失败
```

外层 Promise 被拒绝后，调用者的 `.then()` 成功回调不会执行，而 `.catch()` 会接收到失败原因。

注意：`.catch()` 不只会捕获原 Promise 的拒绝，也会捕获前面 `.then()` 回调中抛出的异常。例如，若成功回调中的代码执行时报错，错误同样可以传递到这个 `.catch()`。

## 八、用一个完整的例子串联整个执行过程 {#kaj-h-cc751f7f-4bbd-4d63-a264-fa0d02388aaf}

```js
function myPromiseAll(promises) {
    return new Promise((resolve, reject) => {
        let count = 0;
        const results = [];

        promises.forEach((promise, index) => {
            Promise.resolve(promise)
                .then(value => {
                    results[index] = value;
                    count++;

                    if (count === promises.length) {
                        resolve(results);
                    }
                })
                .catch(reject);
        });
    });
}

const p1 = new Promise(resolve => {
    setTimeout(() => resolve('A'), 1000);
});

const p2 = new Promise(resolve => {
    setTimeout(() => resolve('B'), 500);
});

myPromiseAll([p1, p2]).then(results => {
    console.log(results);
});
```

执行过程：

## 0.5 秒 {#kaj-h-fc273fb6-8630-4054-b154-4e50794ecfc3}

`p2` 成功

进入对应的 `.then()`，保存 `results[1] = 'B'`，`count` 变为 1。由于还没有全部成功，不调用外层 `resolve`。

## 1 秒 {#kaj-h-765b9442-aaed-408c-98b9-c78ec3fa87f1}

`p1` 成功

进入对应的 `.then()`，保存 `results[0] = 'A'`，`count` 变为 2。此时 `count === promises.length`，调用 `resolve(results)`。

外层 Promise 成功

调用者注册的 `.then(results => ...)` 执行，打印 `['A', 'B']`。尽管 `p2` 先完成，最终结果仍然按输入顺序排列。

## 九、这段代码还有一个边界问题 {#kaj-h-c8983c4d-5d70-4792-adba-2872dcde89ee}

如果传入空数组：

```text
myPromiseAll([]);
```

那么 `forEach()` 一次也不会执行，`count` 也不会变化，外层 Promise 就会一直处于 `pending` 状态。

而真正的 `Promise.all([])` 会立即兑现为一个空数组。

可以在代码开始时补充：

```js
if (promises.length === 0) {
    resolve([]);
    return;
}
```

这样就能处理空数组的情况。

## 十、面试总结 {#kaj-h-d8093133-a108-4d3c-a21e-f93484587ace}

建议重点记住这几个知识点：

| 代码 | 作用 |
| --- | --- |
| `new Promise((resolve, reject) => {})` | 创建外层 Promise |
| `Promise.resolve(promise)` | 将输入统一转换为 Promise |
| `.then(value => {})` | 当前 Promise 成功时处理结果 |
| `results[index] = value` | 保存结果，并保持输入顺序 |
| `count++` | 统计成功的数量 |
| `resolve(results)` | 所有项成功后，兑现外层 Promise |
| `.catch(reject)` | 将失败传递给外层 Promise 的 `reject` |

最重要的理解是：每个输入 Promise 各自决定进入自己的 `then` 还是 `catch`；外层 Promise 则由 `resolve(results)` 或 `reject(error)` 决定最终状态。

这也是手写 `Promise.all()` 的核心逻辑。
