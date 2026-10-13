---
title: "TypeScript 面试高频问题总结"
description: "TypeScript 是 JavaScript 的超集，在 JavaScript 的基础上增加了静态类型系统以及接口、泛型、类型别名等特性，最终会被编译成 JavaScript 执行。"
date: "2026-09-18"
publishedAt: "2026-09-18T11:53:50.693573+08:00"
source: "https://kajspace.cn/articles/01M2SAC6HC4MQG72Z5VP8R3QSZ/"
tags: ["前端"]
---

# TypeScript 面试高频问题总结

<span id="kaj-h-9f17aca3-0151-4581-a89a-4d86f48334ae"></span>

## 一、TypeScript 是什么？为什么使用？ {#kaj-h-71d34a36-a3dc-4e74-a7d8-641dee0f9906}

### 1. 什么是 TypeScript？ {#kaj-h-2afe49e0-0e2f-4019-8e67-22891f2f8c64}

> TypeScript 是 JavaScript 的超集，在 JavaScript 的基础上增加了**静态类型系统**以及接口、泛型、类型别名等特性，最终会被编译成 JavaScript 执行。

核心特点：

```text
TypeScript
   ↓
静态类型检查
   ↓
编译 / 转译
   ↓
JavaScript
   ↓
浏览器 / Node.js
```

---

### 2. TypeScript 的类型检查什么时候进行？ {#kaj-h-a980a38b-add8-407e-97b7-81bc323ea762}

主要发生在**开发阶段和编译阶段**，不是 JavaScript 运行时才检查。

例如：

```js
let num: number = "hello";
```

IDE 就可以直接提示：

```text
Type 'string' is not assignable to type 'number'.
```

最终运行时执行的是 JavaScript。

---

## 二、`any`、`unknown`、`never` {#kaj-h-3d551afd-849f-49b5-878c-1ae461514b00}

## 3. `any` 和 `unknown` 的区别 {#kaj-h-5440d48b-0459-4fca-845b-0f4b0d9fe864}

### `any` {#kaj-h-d17f345a-7b56-45bb-9612-240c122da17d}

相当于：

> “我不进行类型检查，你随便用。”

```js
let value: any = 10;

let str: string = value; // ✅
value.foo();             // ✅
value.bar();             // ✅
```

问题是容易失去 TypeScript 的类型安全。

---

### `unknown` {#kaj-h-ffd65b36-c56f-44a2-971b-748278a35154}

表示：

> “我不知道这个值是什么类型，但是你必须先证明它是什么类型。”

```js
let value: unknown = 10;

let num: number = value; // ❌
```

需要先进行类型缩小：

```js
if (typeof value === "number") {
  let num: number = value; // ✅
}
```

### 面试总结 {#kaj-h-0d891f7f-2565-48ae-914f-47802a85e27e}

> `any` 会关闭类型检查，而 `unknown` 是安全的顶层类型，使用前必须经过类型检查或类型断言进行类型缩小。

---

## 4. `unknown` 为什么不能直接赋值？ {#kaj-h-27bc7097-98d2-44a6-bb36-d3a2d83329ae}

因为：

```js
let value: unknown;
let num: number = value; // ❌
```

TypeScript 无法证明：

```text
value 是 number
```

因为它可能是：

```text
number
string
boolean
object
null
undefined
...
```

---

## 5. 做了不完整的类型检查可以吗？ {#kaj-h-d6da032e-e326-4017-a6ed-328ee684263f}

例如：

```js
let value: unknown = 10;

if (typeof value !== "string") {
  let num: number = value; // ❌
}
```

仍然不可以。

因为：

```text
unknown
 ↓
排除 string
 ↓
number | boolean | object | null | ...
```

仍然不能证明一定是 `number`。

核心：

> **不是做了类型检查就一定可以赋值，而是检查结果必须足以证明目标类型。**

---

## 6. 什么是 `never`？ {#kaj-h-53890cab-7ebf-464b-8d5d-55bf12c1d5e4}

`never` 表示：

> **永远不会正常产生值的类型。**

例如：

```js
function throwError(): never {
  throw new Error("error");
}
```

或者：

```js
function infiniteLoop(): never {
  while (true) {}
}
```

### `void` 和 `never` {#kaj-h-3849ed08-6157-486f-a895-e679ce8c9908}

```text
void
 ↓
函数正常执行结束
 ↓
没有返回值


never
 ↓
函数根本不会正常结束
 ↓
抛异常 / 无限循环
```

---

## 三、类型守卫与类型缩小 {#kaj-h-193d020c-d647-4a2e-b980-4e495b6db91e}

## 7. 什么是类型守卫？ {#kaj-h-20aaf8f4-dab1-40a5-bb4f-cca2c6591941}

类型守卫就是：

> **通过运行时检查，让 TypeScript 在特定代码分支中缩小变量的静态类型。**

例如：

```js
function print(value: string | number) {
  if (typeof value === "number") {
    value.toFixed(2);
  }
}
```

开始：

```text
value: string | number
```

进入：

```js
typeof value === "number"
```

之后：

```text
value: number
```

这叫**类型缩小（Narrowing）**。

---

## 8. 常见的类型守卫有哪些？ {#kaj-h-9f633329-dc4e-44ab-94a5-adcb849e0f24}

### `typeof` {#kaj-h-9a0e4160-49aa-4091-ae3a-fadfc61a6f17}

```js
if (typeof value === "string") {
}
```

适合：

```text
string
number
boolean
bigint
symbol
undefined
```

---

### `instanceof` {#kaj-h-84287c3e-e0ee-4156-a03c-6d83984508a9}

```js
if (animal instanceof Dog) {
  animal.bark();
}
```

可以判断对象是否属于某个类的实例。

---

### 自定义类型守卫 {#kaj-h-b43c596c-7b50-4df9-a4b7-25395518653f}

```js
function isNumber(value: unknown): value is number {
  return typeof value === "number";
}
```

这里：

```text
value is number
```

叫做**类型谓词（Type Predicate）**。

它告诉 TypeScript：

> 如果这个函数返回 `true`，那么把 `value` 当成 `number`。

---

## 9. `typeof` 和 `value is number` 有什么区别？ {#kaj-h-3fb0e0c9-380d-40ee-a098-6a41d71c7c36}

```js
typeof value === "number"
```

是**真正执行的 JavaScript 运行时检查**。

而：

```text
value is number
```

主要是告诉 TypeScript：

> “这个函数返回 true 时，变量应该被缩小成 number。”

所以：

```text
typeof
 ↓
运行时真的检查


value is number
 ↓
告诉 TS 如何进行类型缩小
```

---

## 四、类型断言 {#kaj-h-05beff7b-420b-4f39-8f09-57c28cdd28e6}

## 10. 什么是类型断言？ {#kaj-h-f86b2572-cebf-4b99-ba23-d0e1630dc4eb}

类型断言：

```text
value as string
```

意思是：

> **开发者确定这个值是什么类型，告诉 TypeScript 按指定类型处理。**

例如：

```js
let value: unknown = "hello";

let str: string = value as string;
```

---

## 11. 类型断言会进行类型转换吗？ {#kaj-h-20b1d032-6b66-473c-8e8f-1b7d8cea172a}

**不会。**

```js
let value: unknown = 123;

let str = value as string;
```

不会把：

```text
123
```

转换成：

```text
"123"
```

它只是影响 TypeScript 的类型检查。

真正的类型转换是：

```text
String(value)
```

所以：

```text
as string
→ 类型断言
→ 不改变运行时值


String(value)
→ 类型转换
→ 产生新的字符串值
```

---

## 12. 类型断言和类型守卫有什么区别？ {#kaj-h-066cff6a-dc30-4adc-9f27-cc723d3774ca}

|  | 类型守卫 | 类型断言 |
| --- | --- | --- |
| 方式 | `typeof` / `instanceof` | `as Type` |
| 是否真的检查 | ✅ | ❌ |
| 是否改变值 | ❌ | ❌ |
| 是否影响 TS 类型 | ✅ | ✅ |
| 安全性 | 更高 | 依赖开发者判断 |

一句话：

> **类型守卫是“证明”，类型断言是“告诉 TS，相信我”。**

---

## 五、泛型 {#kaj-h-8938e929-c33b-49c2-a83d-7f5cad59f8f8}

## 13. 什么是泛型？ {#kaj-h-d7339ea2-201f-49a3-872c-72ec4212506a}

泛型的核心作用：

> **在保证类型安全的同时，让代码能够复用，并保留具体类型信息。**

例如：

```js
function identity<T>(value: T): T {
  return value;
}
```

调用：

```js
const a = identity("hello");
// a: string

const b = identity(123);
// b: number
```

---

## 14. 泛型为什么比 `any` 好？ {#kaj-h-490ac940-28a6-4c6a-85ae-12f6e0a5a628}

如果：

```js
function identity(value: any): any {
  return value;
}
```

类型信息丢失。

而：

```js
function identity<T>(value: T): T {
  return value;
}
```

输入什么类型，输出就保留什么类型。

```text
string
  ↓
T = string
  ↓
返回 string


number
  ↓
T = number
  ↓
返回 number
```

---

## 15. `T extends` 是什么意思？ {#kaj-h-31b540fe-f15a-4557-bf62-d7fb7c7a1583}

例如：

```js
function getLength<T extends { length: number }>(
  arg: T
) {
  return arg.length;
}
```

意思不是：

> T 继承这个类型。

而是：

> **T 必须满足** `{ length: number }` **这个约束。**

所以：

```text
getLength("hello");      // ✅
getLength([1, 2, 3]);    // ✅
```

因为：

```text
string
→ 有 length

array
→ 有 length
```

而：

```text
getLength(123); // ❌
```

因为 number 没有 `length`。

---

## 16. 泛型必须使用 `extends` 吗？ {#kaj-h-beb2855d-9415-49af-babc-7f371f130c73}

**不需要。**

```js
function identity<T>(value: T): T {
  return value;
}
```

完全合法。

只有当泛型内部需要使用某些特定能力时，才需要约束：

```js
function getLength<T>(value: T) {
  return value.length; // ❌
}
```

因为 TS 不知道 `T` 有 `length`。

加约束：

```js
function getLength<T extends { length: number }>(
  value: T
) {
  return value.length; // ✅
}
```

---

## 17. `T extends` 和 `T =` 的区别 {#kaj-h-a861672c-4f34-4445-86de-a5d6f6a95cab}

非常高频。

```html
<T extends string>
```

表示：

> **约束**

```html
<T = string>
```

表示：

> **默认类型**

例如：

```js
function wrap<T = string>(value: T): T {
  return value;
}
```

如果：

```text
wrap(123);
```

TS 会推断：

```text
T = number
```

不会因为默认值是 string 就变成 string。

### 记忆 {#kaj-h-0e2d7710-129f-41cd-b06e-c6d052ffd8bc}

```text
extends → 限制 T
=       → 默认 T
```

---

## 六、条件类型 {#kaj-h-c5bbe5bf-730b-4e7d-a450-1b1e8b5813a9}

## 18. 什么是条件类型？ {#kaj-h-b39fabe9-079b-452f-b342-b7aab657a111}

形式：

```text
T extends U ? A : B
```

意思是：

> 如果 `T` 满足 `U`，返回 `A`，否则返回 `B`。

例如：

```ts
type IsString<T> =
  T extends string ? "Yes" : "No";
```

那么：

```ts
type A = IsString<string>;
// "Yes"

type B = IsString<number>;
// "No"
```

这里的 `extends` 不是继承，而是在进行**类型关系判断**。

---

## 七、Interface {#kaj-h-3c31d1ef-2095-4d86-8fbb-b4224b57b2ab}

## 19. interface 是什么？ {#kaj-h-9e4696a3-a7d5-494f-abd3-0fc55dbdfe37}

`interface` 主要用来描述一个对象应该具有怎样的结构。

```ts
interface Person {
  name: string;
  age: number;
}
```

使用：

```js
const person: Person = {
  name: "Alice",
  age: 20
};
```

如果缺少：

```text
age
```

就会报错。

---

## 20. interface 可以描述函数吗？ {#kaj-h-76fef861-501a-4af7-a401-6d8292bd8bde}

可以。

```ts
interface Sum {
  (a: number, b: number): number;
}
```

这叫**调用签名（Call Signature）**。

表示：

> 这个值必须是一个可以接收两个 number，并返回 number 的函数。

例如：

```js
const add: Sum = (a, b) => {
  return a + b;
};
```

---

## 八、`extends` 的多个作用 {#kaj-h-4e4e368f-cedf-4cc4-a5f0-18b1a6e1400b}

这是很容易被面试官问到的。

### ① 类继承 {#kaj-h-2e0ce2d1-a395-424d-aa45-e4394142b1eb}

```text
class Dog extends Animal {}
```

表示：

> Dog 继承 Animal。

---

### ② 接口继承 {#kaj-h-8c2d7957-0086-4121-980c-78f8fa65af02}

```ts
interface Dog extends Animal {
  breed: string;
}
```

表示：

> Dog 在 Animal 的结构基础上增加属性。

---

### ③ 泛型约束 {#kaj-h-e1aa7f4d-6f5b-42df-96b8-51280de0881a}

```js
function fn<T extends Animal>(value: T) {}
```

表示：

> T 必须满足 Animal 的类型约束。

---

### ④ 条件类型 {#kaj-h-6dcfa67e-244a-4445-9d54-546dc16d2b2c}

```ts
type Result<T> =
  T extends string ? "Yes" : "No";
```

表示：

> 判断 T 是否满足 string。

所以面试时可以说：

> **TypeScript 中** `extends` **并不只有类继承一个含义，在类中表示继承，在接口中表示接口扩展，在泛型中表示类型约束，在条件类型中表示类型关系判断。**

---

## 九、Class、属性、方法、继承 {#kaj-h-75b4b340-69ff-4daa-802f-2c771819e854}

## 21. class 中的属性和方法是什么？ {#kaj-h-d26947ad-978e-4f80-9d6d-5cb98b1bab34}

例如：

```js
class Person {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  sayHello() {
    console.log(this.name);
  }
}
```

这里：

```text
name
→ 属性
→ 保存对象的数据

sayHello()
→ 方法
→ 对象可以执行的行为
```

---

## 22. 属性一定要写在 constructor 中吗？ {#kaj-h-0d4f8ffd-7383-4e31-97a1-80a97291f4e3}

**不一定。**

可以：

```text
class Person {
  name: string;

  constructor(name: string) {
    this.name = name;
  }
}
```

也可以：

```text
class Person {
  name = "Tom";
  age = 18;
}
```

第二种属于**实例字段初始化**。

---

## 23. `this.name = name` 是什么？ {#kaj-h-4daffcd7-30a4-4e45-8a4e-e7515da7e76d}

例如：

```text
class Person {
  name: string;

  constructor(name: string) {
    this.name = name;
  }
}
```

执行：

```js
const p = new Person("Alice");
```

构造函数中的：

```text
this
```

指向正在创建的实例：

```js
this === p
```

所以：

```text
this.name = name;
```

实际上就是：

```text
p.name = "Alice"
```

因此 `name` 最终是：

> **实例自己的属性。**

---

## 十、Class 继承和原型链 {#kaj-h-ca76260c-1d2e-4411-b0da-d50177053166}

## 24. 子类继承父类到底发生了什么？ {#kaj-h-a32a9012-3bf5-42d5-8072-7c352115d27e}

例如：

```js
class Animal {
  eat() {
    console.log("Eating");
  }
}

class Dog extends Animal {
  bark() {
    console.log("Barking");
  }
}
```

```js
const dog = new Dog();
```

`Dog` 和 `Animal` 建立继承关系。

方法主要通过原型链查找：

```js
dog
 ↓
Dog.prototype
 ↓
Animal.prototype
 ↓
Object.prototype
 ↓
null
```

所以：

```text
dog.eat();
```

虽然 `Dog` 没有定义 `eat()`，但可以沿着原型链找到：

```js
Animal.prototype.eat
```

---

## 25. 父类的属性是怎么被子类继承的？ {#kaj-h-9a5bf41a-704d-41c1-a8f2-641951bde518}

这是你刚刚重点问的问题。

例如：

```text
class Animal {
  name: string;

  constructor(name: string) {
    this.name = name;
  }
}

class Dog extends Animal {
  constructor(name: string) {
    super(name);
  }
}
```

执行：

```js
const dog = new Dog("Max");
```

过程：

```text
new Dog("Max")
      ↓
Dog constructor
      ↓
super("Max")
      ↓
Animal constructor
      ↓
this.name = "Max"
      ↓
this 指向 dog
      ↓
dog.name = "Max"
```

所以：

> **父类 constructor 中通过** `this.xxx` **创建的属性，是在创建子类实例时写入子类实例的。**

而父类的方法：

```text
eat() {}
```

主要是通过：

```js
Animal.prototype
```

被子类通过原型链访问。

---

## 十一、`super` {#kaj-h-2868bba9-2f21-41ae-b30c-3d2a068ce758}

## 26. `super()` 是干什么的？ {#kaj-h-bf5cf598-8654-4607-9312-a6c90dcd888b}

子类有自己的 constructor 时：

```text
class Dog extends Animal {
  constructor(name: string) {
    super(name);
  }
}
```

`super(name)`：

> **调用父类的 constructor。**

所以：

```text
extends
→ 建立继承关系

super()
→ 调用父类 constructor

this.name = ...
→ 真正给实例创建属性
```

---

## 十二、私有成员 {#kaj-h-00e45536-4a2f-45b1-8bfe-290930df4e22}

## 27. `#` 是什么意思？ {#kaj-h-b22b5a14-7b41-45f2-8966-6b5a9adf3fc7}

```js
class Person {
  #password = "123";

  #checkPassword() {
    return true;
  }
}
```

`#` 表示 JavaScript 原生的**私有成员**。

包括：

```text
#password
```

私有属性，以及：

```text
#checkPassword()
```

私有方法。

外部不能直接访问：

```text
person.#password; // ❌
```

---

## 28. 为什么需要私有方法？ {#kaj-h-7af0f750-bd50-4096-b5c3-71b8fe913824}

因为不是所有方法都应该成为类的公共 API。

例如：

```text
class User {
  login() {
    this.#validate();
    this.#encrypt();
  }

  #validate() {
    // 内部校验
  }

  #encrypt() {
    // 内部加密
  }
}
```

外部只需要：

```text
user.login();
```

而不需要知道：

```text
#validate()
#encrypt()
```

具体怎么实现。

这就是：

> **封装：隐藏内部实现，只暴露必要的公共接口。**

---

## 十三、最终知识体系 {#kaj-h-00dcca99-0b06-40c6-9061-b7be433cd8a1}

你现在可以把前面这些 TS 知识串成这一张图：

```html
                         TypeScript
                              │
              ┌───────────────┼────────────────┐
              ↓               ↓                ↓
           基础类型         类型系统          面向对象
              │               │                │
        string/number       any               class
        boolean/array       unknown             │
        tuple/enum          never               ├── 属性
                              │                  ├── 方法
                              ↓                  ├── extends
                         类型缩小                ├── super
                              │                  ├── private
                    ┌─────────┼─────────┐        └── #
                    ↓         ↓         ↓
                  typeof  instanceof  类型守卫
                                      │
                                      ↓
                                   value is


类型系统
   │
   ├── interface
   ├── type
   ├── union
   ├── intersection
   ├── 泛型
   │     ├── <T>
   │     ├── <T extends X>
   │     └── <T = X>
   │
   └── 条件类型
          └── T extends U ? A : B
```

### 你目前尤其应该记牢的 10 个点 {#kaj-h-979ba4b9-7443-4bf6-b4c3-bccb77902602}

1. **TS 是 JS 的超集，主要提供静态类型系统。**
2. **类型检查主要发生在开发/编译阶段，而不是运行时。**
3. `any` **放弃类型安全，**`unknown` **要求先进行类型缩小。**
4. **类型守卫通过运行时检查帮助 TS 缩小静态类型。**
5. **类型断言** `as` **不检查、不转换值，只告诉 TS 按指定类型处理。**
6. `never` **表示不存在正常返回值/不可能的类型。**
7. **泛型** `<T>` **用于复用代码并保留具体类型信息。**
8. `T extends X` **是泛型约束，**`T = X` **是默认类型。**
9. `extends` **在 class、interface、泛型、条件类型中的含义不同。**
10. **class 中属性是数据，方法是行为；父类方法主要通过原型链访问，父类 constructor 中的** `this.xxx` **会在创建子类实例时初始化实例属性。**
