---
title: "JS数据类型检测方式"
description: "JS 中常见的数据类型检测方式主要有 4 种，面试很常问。你可以先记住：typeof、instanceof、Object.prototype.toString.call()、Array.isArray()。"
date: "2026-09-02"
publishedAt: "2026-09-02T10:28:18.117995+08:00"
source: "https://kajspace.cn/articles/01M18SE93W30HE8GC3DN8Z9BMP/"
tags: ["前端"]
---

# JS数据类型检测方式

JS 中常见的数据类型检测方式主要有 **4 种**，面试很常问。你可以先记住：`typeof`**、**`instanceof`**、**`Object.prototype.toString.call()`**、**`Array.isArray()`。

---

## 1. `typeof` —— 最常用，但有局限 {#kaj-h-ff514780-cda4-44dd-8979-642ef1ec9c89}

```js
typeof 123          // "number"
typeof "hello"      // "string"
typeof true         // "boolean"
typeof undefined    // "undefined"
typeof 123n         // "bigint"
typeof Symbol()     // "symbol"
typeof function(){}  // "function"
typeof {}           // "object"
typeof []            // "object"
typeof null         // "object"
```

### 能检测哪些？ {#kaj-h-2800a97d-fc9a-4b5d-b665-5b34e4f9afa3}

| 类型 | typeof 结果 |
| --- | --- |
| number | `"number"` |
| string | `"string"` |
| boolean | `"boolean"` |
| undefined | `"undefined"` |
| bigint | `"bigint"` |
| symbol | `"symbol"` |
| function | `"function"` |
| object | `"object"` |

最大的两个坑：

```text
typeof null   // "object"
typeof []     // "object"
```

所以：

```js
typeof [] === "object"
```

**无法判断是不是数组。**

---

## 2. `instanceof` —— 判断对象是否属于某个构造函数的实例 {#kaj-h-7b81fc21-4446-446b-af0b-488bc1ef60c5}

例如：

```js
const arr = [];

arr instanceof Array
// true

arr instanceof Object
// true
```

为什么 `arr instanceof Object` 也是 `true`？

因为原型链：

```js
arr
 ↓ __proto__
Array.prototype
 ↓ __proto__
Object.prototype
 ↓
null
```

所以：

```text
arr instanceof Array
```

本质上是在检查：

> `Array.prototype` 是否出现在 `arr` 的原型链上。

---

### 常见用法 {#kaj-h-92badb96-1b71-475d-8aa5-375c5d0f3f9b}

```text
[] instanceof Array              // true
{} instanceof Object             // true
new Date() instanceof Date       // true
new Person() instanceof Person   // true
```

但是 `instanceof` 有一个重要局限：

**它主要用于判断对象和构造函数之间的关系，不能检测基本数据类型。**

比如：

```text
123 instanceof Number
// false
```

因为：

```text
123
```

是基本类型，不是 `Number` 对象。

---

## 3. `Object.prototype.toString.call()` —— 最全面 {#kaj-h-4c58639b-0dd2-4061-b0f6-c630d567bd6e}

这是面试中非常重要的一种。

```js
Object.prototype.toString.call(123)
// "[object Number]"

Object.prototype.toString.call("hello")
// "[object String]"

Object.prototype.toString.call(true)
// "[object Boolean]"

Object.prototype.toString.call(undefined)
// "[object Undefined]"

Object.prototype.toString.call(null)
// "[object Null]"

Object.prototype.toString.call([])
// "[object Array]"

Object.prototype.toString.call({})
// "[object Object]"

Object.prototype.toString.call(function(){})
// "[object Function]"
```

因此它可以比较准确地判断类型。

例如：

```js
const type = Object.prototype.toString.call([]);

console.log(type === "[object Array]");
// true
```

---

## 为什么要 `.call()`？ {#kaj-h-c10d432d-6c5c-4964-b19a-6602a63101f8}

这里其实涉及你刚刚学的**原型**。

`toString` 本身来自：

```js
Object.prototype
```

也就是：

```js
Object.prototype.toString
```

如果直接：

```js
Object.prototype.toString()
```

它检测的是当前调用上下文中的对象。

我们希望让它检测：

```text
arr
```

所以：

```js
Object.prototype.toString.call(arr)
```

相当于：

> **借用** `Object.prototype.toString` **方法，让它的** `this` **指向** `arr`**。**

例如：

```js
const arr = [];

Object.prototype.toString.call(arr);
```

得到：

```text
"[object Array]"
```

这个和你刚刚学的原型链是直接联系起来的。

---

## 4. `Array.isArray()` —— 专门判断数组 {#kaj-h-8b73451d-d523-4ec4-9015-d78c52d84759}

```text
Array.isArray([])
// true

Array.isArray({})
// false

Array.isArray("hello")
// false
```

如果你只是想判断：

> **是不是数组？**

直接：

```text
Array.isArray(arr)
```

是最推荐的。

而不是：

```js
typeof arr === "object"
```

---

## 5. 四种方法放一起比较 {#kaj-h-82cd0772-2175-42bb-b5b2-c6fd1f4c3bbf}

| 方法 | 能检测基本类型 | 能区分数组 | 判断原型链 | 推荐场景 |
| --- | --- | --- | --- | --- |
| `typeof` | ✅ | ❌ | ❌ | 基本类型快速判断 |
| `instanceof` | ❌ | ✅ | ✅ | 判断实例/原型关系 |
| `Object.prototype.toString.call()` | ✅ | ✅ | ❌ | 精确判断类型 |
| `Array.isArray()` | — | ✅ | ❌ | 专门判断数组 |

---

## 6. 面试最容易问的几个坑 {#kaj-h-0c21ed82-4e1d-4b74-b6be-4a65e6a2e754}

### `typeof null` {#kaj-h-9c0f22dc-72c1-4fd6-9bc3-0990fee62351}

```text
typeof null
// "object"
```

这是 JS 历史遗留问题。

所以判断 `null`：

```js
value === null
```

---

### `typeof []` {#kaj-h-2c36975f-057f-4f68-adba-53582b8e0447}

```text
typeof []
// "object"
```

所以：

```text
Array.isArray([])
```

才是正确方式。

---

### `instanceof` 和基本类型 {#kaj-h-7663ba4b-a416-4582-9b65-e10a14460ee7}

```text
"hello" instanceof String
// false
```

因为：

```text
"hello"
```

是基本类型。

而：

```text
new String("hello") instanceof String
// true
```

这里才是真正的 `String` 对象。

---

## 7. 你可以这样形成一个“数据类型检测”思维 {#kaj-h-fd07d497-5a23-409a-9994-b9b35533c63d}

看到一个值：

```js
const value = ???;
```

先问自己：

### ① 只是想知道大类型？ {#kaj-h-e44851d7-10e3-414d-bda7-ed3c5015a510}

```text
typeof value
```

例如：

```js
typeof value === "string"
```

---

### ② 想判断是不是数组？ {#kaj-h-d039e4ad-4cb6-462c-94b5-f6edc43c85a4}

```text
Array.isArray(value)
```

---

### ③ 想判断是不是某个构造函数的实例？ {#kaj-h-ceb52cef-1f11-4d37-b8ba-70ff5d8ad197}

```text
value instanceof Person
```

---

### ④ 想精确判断具体类型？ {#kaj-h-fc367537-3e72-4b77-9ef6-724f1b3bd4bb}

```js
Object.prototype.toString.call(value)
```

例如：

```js
Object.prototype.toString.call(value) === "[object Date]"
```

---

## 最后记一个面试版答案 {#kaj-h-27a9b5f7-bbd4-41c7-9f15-2eb9b415e693}

如果面试官问：

> **JS 中有哪些数据类型检测方式？**

你可以回答：

> JS 常见的数据类型检测方式有 `typeof`、`instanceof`、`Object.prototype.toString.call()` 和 `Array.isArray()`。`typeof` 适合检测基本数据类型，但 `null` 会返回 `"object"`，数组和普通对象也都返回 `"object"`；`instanceof` 是通过检查原型链来判断对象是否是某个构造函数的实例；`Object.prototype.toString.call()` 可以比较准确地区分各种数据类型；如果只是判断数组，推荐直接使用 `Array.isArray()`。
