---
title: "TS基础"
description: "你可以先记住这一张关系："
date: "2026-09-10"
publishedAt: "2026-09-10T15:37:51.814638+08:00"
source: "https://kajspace.cn/articles/01M2540DG7BP6YG3MQ5SENWYXF/"
tags: ["前端"]
---

# TS基础

## 一、先建立总图 {#kaj-h-96007e37-bce2-43ea-b828-2640b6973bb3}

你可以先记住这一张关系：

```ts
                TypeScript 类型系统
                       │
          ┌────────────┴────────────┐
          ↓                         ↓
      interface                  type
     定义对象结构              定义类型/类型组合
          │                         │
          └────────────┬────────────┘
                       ↓
                     泛型
              让类型可以“传参数”
                       │
                 ┌─────┴─────┐
                 ↓           ↓
              extends      keyof
             类型约束      获取 key
                 │           │
                 └─────┬─────┘
                       ↓
                    typeof
                 获取类型信息
                       ↓
                   条件类型
              根据类型进行判断
```

但这个图有一个地方要注意：

> `typeof` 既可以用于 JS 运行时，也有 TS 类型位置中的 `typeof`。我们这里主要讲 **TS 类型系统中的 typeof**。

---

## 二、第一步：interface —— 描述一个对象长什么样 {#kaj-h-bf7d0f36-9d8e-4119-9509-b624527f8c9d}

你在 JS 里可能这样写：

```js
const user = {
    name: "Tom",
    age: 20
};
```

JS 不会告诉你：

```text
user 必须有什么属性
name 必须是什么类型
age 必须是什么类型
```

TS 可以：

```ts
interface User {
    name: string;
    age: number;
}
```

这相当于告诉 TS：

```text
User 对象必须：
name → string
age  → number
```

然后：

```js
const user: User = {
    name: "Tom",
    age: 20
};
```

如果：

```js
const user: User = {
    name: "Tom",
    age: "20"
};
```

TS 就会报错，因为：

```text
age 要 number
你给了 string
```

### 所以 interface 是什么？ {#kaj-h-f6317608-da8b-4972-bd1f-fe61d7adaae0}

> **interface 主要用来描述对象的结构。**

你可以暂时把它理解成：

```text
interface = 给对象定义一个“结构规范”
```

---

## 三、第二步：type —— 给类型起名字 {#kaj-h-4d9ab2a2-0a76-4d29-afba-dc714caa0b17}

`type` 和 `interface` 有很多相似之处。

例如：

```ts
type User = {
    name: string;
    age: number;
};
```

然后：

```js
const user: User = {
    name: "Tom",
    age: 20
};
```

所以你会发现：

```ts
interface User {
    name: string;
    age: number;
}
```

和：

```ts
type User = {
    name: string;
    age: number;
};
```

在这种简单场景下效果非常接近。

---

## 那为什么两个都存在？ {#kaj-h-641120a4-b096-435e-9cac-ea8b2173ac92}

因为 `type` 能表达的东西更多。

例如：

```ts
type ID = string | number;
```

表示：

```text
ID 可以是 string
或者 number
```

还可以：

```ts
type Status = "success" | "error" | "loading";
```

这叫**联合类型**。

所以你现在可以先这样记：

```text
interface
→ 更常用于描述对象结构

type
→ 更通用，可以给各种类型起别名
```

实际开发中两者都会大量使用。

---

## 四、第三步：泛型 —— 类型也可以传参数 {#kaj-h-112e3176-58a6-4e0a-91a9-d6058b55072d}

这是 TS 非常核心的概念。

你熟悉 JS 函数：

```js
function identity(value) {
    return value;
}
```

你传：

```text
identity("hello");
identity(123);
identity(true);
```

同一个函数可以接受不同类型。

TS 如果直接写：

```js
function identity(value: string): string {
    return value;
}
```

只能传字符串。

如果写：

```js
function identity(value: number): number {
    return value;
}
```

只能传数字。

那怎么办？

**泛型。**

```js
function identity<T>(value: T): T {
    return value;
}
```

这里：

```html
<T>
```

就是一个**类型参数**。

调用：

```text
identity("hello");
```

TS 自动推断：

```text
T = string
```

所以：

```text
输入 string
↓
T = string
↓
返回 string
```

调用：

```text
identity(123);
```

则：

```text
T = number
```

---

## 五、把泛型和 interface 连起来 {#kaj-h-3d628495-3759-4c5f-afee-e22768e83383}

现在假设：

```ts
interface User {
    name: string;
    age: number;
}
```

我们写：

```js
function getUser<T>(user: T): T {
    return user;
}
```

那么：

```js
const user = getUser({
    name: "Tom",
    age: 20
});
```

这里：

```text
T = {
    name: string;
    age: number;
}
```

所以泛型实际上就是：

> **让一个函数、类或者类型，不需要提前写死具体类型，而是使用时再确定。**

---

## 六、第四步：extends —— 给泛型加限制 {#kaj-h-8dfa6e3b-e2cb-416d-becf-61f7baea7860}

但是刚才的：

```js
function getUser<T>(user: T): T
```

T 可以是任何类型。

例如：

```text
getUser(123);
getUser("hello");
getUser(true);
```

如果我们希望：

> T 必须是一个有 `length` 属性的类型。

就可以：

```js
function getLength<T extends { length: number }>(arg: T): number {
    return arg.length;
}
```

这里：

```text
T extends { length: number }
```

不是在说：

> T 继承某个类。

而是在说：

> **T 必须满足这个类型约束。**

所以：

```text
getLength("hello");    // ✅
getLength([1, 2, 3]);  // ✅
```

因为：

```text
string
→ 有 length:number

number[]
→ 有 length:number
```

但是：

```text
getLength(123); // ❌
```

因为：

```text
number
→ 没有 length
```

---

## 七、这里 interface 又可以参与进来 {#kaj-h-a3d8a442-3995-41de-a9a9-6a06f6da9cc8}

我们可以把限制单独定义出来：

```ts
interface HasLength {
    length: number;
}
```

然后：

```js
function getLength<T extends HasLength>(arg: T): number {
    return arg.length;
}
```

现在你应该能看懂了：

```ts
interface HasLength
        ↓
规定一种结构
        ↓
必须有 length:number
        ↓
泛型 T
        ↓
T extends HasLength
        ↓
T 必须满足这个结构
```

这就是它们开始串起来了。

---

## 八、第五步：keyof —— 获取一个类型的所有 key {#kaj-h-81955892-2d48-4b7f-99a8-78e424b06cf4}

假设：

```ts
interface User {
    name: string;
    age: number;
    email: string;
}
```

我们想获得：

```text
"name" | "age" | "email"
```

怎么办？

```text
keyof User
```

结果就是：

```text
"name" | "age" | "email"
```

所以：

```ts
type UserKey = keyof User;
```

相当于：

```ts
type UserKey = "name" | "age" | "email";
```

---

## 九、keyof 最重要的用途：限制对象属性名 {#kaj-h-6f1002fa-40e1-45c0-901a-b61cc8710658}

例如：

```js
function getProperty<T, K extends keyof T>(
    obj: T,
    key: K
) {
    return obj[key];
}
```

这段代码看起来比较吓人，但拆开就简单了。

假设：

```js
const user = {
    name: "Tom",
    age: 20
};
```

调用：

```text
getProperty(user, "name");
```

TS 推断：

```text
T = User
K = "name"
```

调用：

```text
getProperty(user, "age");
```

也可以。

但是：

```text
getProperty(user, "xxx");
```

就会报错。

因为：

```text
keyof User
=
"name" | "age"
```

`"xxx"` 不在里面。

---

## 十、把这个例子翻译成人话 {#kaj-h-fdc6263c-6254-4312-98dc-0448a57cc4b9}

```js
function getProperty<T, K extends keyof T>(
    obj: T,
    key: K
) {
    return obj[key];
}
```

就是：

> **传进来一个对象 T，再传一个 key K，但是 K 必须是 T 对象中存在的属性名。**

这其实就是把 JS：

```text
obj[key]
```

做了类型安全限制。

---

## 十一、第六步：typeof —— 从“值”得到“类型” {#kaj-h-fdfe0aa1-09cc-427c-9e0c-388a11168363}

这里开始非常有意思。

JS 中你已经见过：

```text
typeof "hello"
// "string"

typeof 123
// "number"
```

这是**运行时的 typeof**。

TS 中还有一种：

```ts
const user = {
    name: "Tom",
    age: 20
};

type User = typeof user;
```

这里的：

```text
typeof user
```

意思是：

> **获取变量** `user` **的类型。**

所以：

```ts
type User = typeof user;
```

得到类似：

```text
{
    name: string;
    age: number;
}
```

注意：

```text
JS typeof
→ 运行时判断值的类型

TS typeof
→ 类型位置中提取一个变量的类型
```

---

## 十二、为什么 typeof 很有用？ {#kaj-h-48e7b84a-8bd3-4e1a-817f-b2e905396e91}

比如你已经有一个对象：

```js
const config = {
    host: "localhost",
    port: 3000
};
```

你不想重新写：

```ts
type Config = {
    host: string;
    port: number;
};
```

可以直接：

```ts
type Config = typeof config;
```

这样以后 `config` 修改结构时，类型也能跟着变化。

---

## 十三、第七步：条件类型 —— 根据类型做判断 {#kaj-h-ee227f09-c13a-49f4-923e-e112b96aad53}

现在前面的东西终于可以串起来了。

我们已经知道：

```text
T extends U
```

可以表示：

> T 是否满足 U？

于是：

```text
T extends U ? X : Y
```

就是：

> **如果 T 满足 U，就得到 X，否则得到 Y。**

例如：

```ts
type IsString<T> =
    T extends string
        ? true
        : false;
```

于是：

```ts
type A = IsString<string>;
// true

type B = IsString<number>;
// false
```

你可以把它直接类比 JS：

```js
typeof value === "string"
    ? true
    : false
```

区别是：

```text
JS：
判断值

TS：
判断类型
```

---

## 十四、现在把七个概念全部串起来 {#kaj-h-e4719643-8912-45b9-8f59-eb299955b9fd}

我们来写一个稍微完整的例子。

先定义对象：

```ts
interface User {
    name: string;
    age: number;
}
```

### ① interface {#kaj-h-409b6519-8e75-4f5d-b2ab-4ed344184239}

描述 User：

```text
User
├── name: string
└── age: number
```

---

### ② keyof {#kaj-h-81fbde4c-8d1c-4d72-8a7d-532bb9a09da3}

获取 User 的 key：

```ts
type UserKey = keyof User;
```

结果：

```text
"name" | "age"
```

---

### ③ 泛型 {#kaj-h-60472d9e-3f10-45c2-803a-3eb0a747d88a}

让函数可以适用于不同类型：

```js
function getProperty<T, K extends keyof T>(
    obj: T,
    key: K
) {
    return obj[key];
}
```

---

### ④ extends {#kaj-h-a20720e0-052f-48d9-9368-545b6894f10e}

这里：

```text
K extends keyof T
```

意思：

> K 必须是 T 的 key。

---

### ⑤ typeof {#kaj-h-c25445b4-7fe0-4716-be84-7037c70199c9}

现在：

```js
const user = {
    name: "Tom",
    age: 20
};
```

可以：

```ts
type UserType = typeof user;
```

获取 `user` 的类型。

---

### ⑥ 条件类型 {#kaj-h-6d9a9af6-0fe2-457e-a81a-47544f866814}

我们还可以判断：

```ts
type IsUser<T> =
    T extends User
        ? true
        : false;
```

于是：

```ts
type A = IsUser<User>;
// true

type B = IsUser<string>;
// false
```

---

### ⑦ type {#kaj-h-3d5fbbba-c9d0-407a-ab6f-14e309e04b74}

最后你会发现：

```ts
type UserKey = keyof User;
type UserType = typeof user;
type IsUser<T> = T extends User ? true : false;
```

这些本身都是通过 `type` 定义的。

所以 **type 是一个非常重要的“类型定义工具”**。

---

## 十五、最终形成一条学习路线 {#kaj-h-227fe7e8-5a8c-4442-b5b0-e60841593c91}

你现在从 JS 过来，我建议按照这个顺序理解：

```html
JS
│
├── 基本类型
│
├── 对象
│
↓
TypeScript
│
├── interface
│     ↓
│   描述对象结构
│
├── type
│     ↓
│   给类型起名字 / 组合类型
│
├── 泛型 <T>
│     ↓
│   类型也可以传参数
│
├── extends
│     ↓
│   给类型参数加限制
│
├── keyof
│     ↓
│   获取对象类型的 key
│
├── typeof
│     ↓
│   获取变量的类型
│
└── 条件类型
      ↓
    根据类型做判断
```

### 你现阶段最应该背的不是语法，而是这 7 句话： {#kaj-h-1080e793-a1aa-483c-90d8-a94c61ff2d61}

```html
interface → 描述对象结构

type → 定义/组合类型

泛型 <T> → 类型参数

extends → 类型约束

keyof → 获取类型的 key

typeof → 获取变量的类型

条件类型 → 根据类型进行判断
```

然后你会发现，后面很多 TS 高级类型其实都是在**组合这几个基础工具**。

例如你以后看到：

```ts
type GetType<T, K extends keyof T> =
    T[K] extends string
        ? "字符串"
        : "其他";
```

虽然看起来很吓人，但实际上就是：

```text
T        → 泛型
K        → 泛型
extends  → 约束
keyof    → 获取 T 的 key
T[K]     → 获取属性类型
extends  → 判断类型
? :      → 条件类型
```
