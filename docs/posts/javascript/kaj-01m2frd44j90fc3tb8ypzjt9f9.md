---
title: "闭包"
description: "闭包是指一个函数能够访问并持有其定义时所在作用域中的变量，即使这个函数已经离开了原来的作用域，这些变量仍然可以被访问。"
date: "2026-09-14"
publishedAt: "2026-09-14T18:52:39.086687+08:00"
source: "https://kajspace.cn/articles/01M2FRD44J90FC3TB8YPZJT9F9/"
tags: ["前端"]
---

# 闭包

### 1. 什么是闭包？ {#kaj-h-f12be46d-0388-47d0-99ae-18faeb8ebf5f}

> **闭包是指一个函数能够访问并持有其定义时所在作用域中的变量，即使这个函数已经离开了原来的作用域，这些变量仍然可以被访问。**

简单来说：

> **函数 + 它能够访问的外部变量环境，就可以理解为闭包。**

例如：

```js
function outer() {
  let count = 0;

  return function inner() {
    count++;
    console.log(count);
  };
}

const fn = outer();

fn(); // 1
fn(); // 2
```

这里 `outer()` 执行结束以后，按正常理解它的局部变量 `count` 应该不能再访问。

但是 `inner` 函数仍然引用着 `count`，所以 `count` 不会被回收。

因此：

```text
outer()
  ↓
创建 count
  ↓
返回 inner
  ↓
outer 执行结束
  ↓
inner 仍然引用 count
  ↓
count 被保留下来
```

这就是闭包。

---

## 2. 闭包为什么能够保存变量？ {#kaj-h-8c81ee60-e31b-4d20-bfbc-2579b5bf0084}

面试官如果继续问，可以这样回答：

> **JavaScript 使用词法作用域，函数在定义的时候就确定了它能够访问哪些外部变量。函数执行时会通过作用域链查找这些变量。只要仍然有函数引用着这些外部变量，这些变量就不会被垃圾回收，因此可以在函数调用之间保持状态。**

可以进一步说：

```js
function outer() {
  let count = 0;

  return function () {
    count++;
  };
}
```

`inner` 函数内部需要访问 `count`，所以 `count` 被 `inner` 的闭包环境保留下来。

---

## 3. 闭包有哪些使用场景？ {#kaj-h-322caa69-095e-440f-b28a-2e6316aac8e2}

这个问题面试中很常见，可以重点记 **4 个场景**。

### 场景一：数据私有化 / 封装 {#kaj-h-97b9965d-4f38-4816-92f4-1f45504e71e2}

闭包可以让变量只能通过指定函数访问。

```js
function createCounter() {
  let count = 0;

  return {
    increment() {
      count++;
    },
    getCount() {
      return count;
    }
  };
}

const counter = createCounter();

counter.increment();
console.log(counter.getCount()); // 1

console.log(counter.count); // undefined
```

这里 `count` 没有暴露到外部。

面试可以说：

> **闭包可以模拟私有变量，实现数据封装。**

---

### 场景二：函数工厂 {#kaj-h-b221c7d6-cbda-4e1e-a3ca-088757b357b5}

根据不同参数创建具有不同功能的函数。

```js
function multiply(x) {
  return function (y) {
    return x * y;
  };
}

const double = multiply(2);
const triple = multiply(3);

double(5); // 10
triple(5); // 15
```

这里 `double` 一直保存着 `x = 2`，`triple` 保存着 `x = 3`。

所以可以说：

> **闭包可以用于函数工厂，让创建出来的函数拥有独立的状态。**

---

### 场景三：防抖和节流 {#kaj-h-6907ea45-31ad-42da-9baa-a0ca80daef16}

前端开发中非常常见。

例如防抖：

```js
function debounce(fn, delay) {
  let timer;

  return function (...args) {
    clearTimeout(timer);

    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}
```

这里返回的函数一直需要访问：

```text
timer
```

所以 `timer` 被闭包保存。

面试可以说：

> **防抖函数需要在多次调用之间保存定时器 ID，这个状态就可以通过闭包保存。**

---

### 场景四：异步操作中保存状态 {#kaj-h-8005564c-7fed-48d2-b5ba-6cefebccde02}

例如：

```js
function request(url) {
  let retryCount = 0;

  return function () {
    retryCount++;
    console.log(`第 ${retryCount} 次请求：${url}`);
  };
}
```

返回的函数每次执行都能够访问之前保存的 `retryCount` 和 `url`。

实际前端开发中，事件处理函数、定时器、Promise、异步回调等地方都经常涉及闭包。

---

## 4. 闭包有什么缺点？ {#kaj-h-6fd119ff-a803-44a5-962b-d2cd774b1fad}

面试官很可能继续追问这个。

可以回答：

> **闭包本身没有问题，但如果闭包长期持有一些不再需要的大对象或者大量数据，就可能导致这些数据无法及时被垃圾回收，从而造成内存占用过高。**

例如：

```js
function create() {
  const bigData = new Array(1000000);

  return function () {
    console.log(bigData.length);
  };
}

const fn = create();
```

只要 `fn` 还存在，`bigData` 就可能一直被引用。

所以实际开发中：

> **如果闭包不再需要，应该及时解除对它的引用，让相关数据能够被垃圾回收。**

---

## 5. 一段完整的面试回答 {#kaj-h-4eedcc96-9e23-4edf-b3e8-52e143bb0d1b}

如果面试官直接问：

**“什么是闭包？有哪些使用场景？”**

你可以直接这样回答：

> **闭包是指函数能够访问并持有其定义时所在作用域中的变量，即使这个函数离开了原来的作用域，这些变量仍然可以被访问。**
> 
> 
> 
> **它的本质是函数和它能够访问的词法环境形成了一种关联。只要还有函数引用这些外部变量，这些变量就不会被垃圾回收，因此可以实现状态的持久化。**
> 
> 
> 
> **常见的使用场景主要有几个：第一，用闭包实现数据私有化和封装；第二，用于函数工厂，让不同函数保存不同的状态；第三，在防抖、节流中保存定时器等状态；第四，在异步回调中保存调用时需要的数据。**
> 
> 
> 
> **需要注意的是，如果闭包长期引用大量数据，可能导致这些数据无法及时被垃圾回收，从而造成内存占用，所以不再使用时应该及时解除引用。**

---

## 6. 你可以重点记住这句话 {#kaj-h-4f3469f2-72f9-49c9-b8e0-3fa7f2f52ef3}

如果面试紧张，先记这一版：

> **闭包就是函数能够记住并访问它定义时所在作用域中的变量，即使外部函数已经执行结束，这些变量仍然可以被访问。常用于数据封装、函数工厂、防抖节流以及异步回调中。**

然后面试官如果追问：

**“为什么变量不会被回收？”**

就接：

> **因为返回的函数仍然引用这些变量，垃圾回收器发现这些变量仍然可达，所以不会回收。**

这两句话基本就是**闭包面试题的核心**。
