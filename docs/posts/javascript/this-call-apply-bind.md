---
title: JavaScript 中的 this、call、apply、bind 详解
description: 梳理 this 的绑定规则，比较 call、apply、bind 的差异，并通过手写实现理解它们的工作原理。
date: "2026-10-14"
tags:
  - JavaScript
  - this
  - call
  - apply
  - bind
  - 前端八股
---

# JavaScript 中的 this、call、apply、bind 详解

## 一、this 的理解

`this` 是 JavaScript 中的一个关键字，用于指向函数执行时所关联的对象。对于普通函数来说，`this` 的指向主要取决于**函数的调用方式，而不是函数的定义位置**。

JavaScript 中常见的 `this` 绑定规则包括默认绑定、隐式绑定、显式绑定和 `new` 绑定。

### 1. 默认绑定：普通函数调用

当函数没有通过对象的方法形式调用，也没有使用 `call`、`apply`、`bind` 或 `new` 时，通常采用默认绑定。

```javascript
function foo() {
    console.log(this);
}

foo();
```

在浏览器的非严格模式下，`this` 指向全局对象 `window`；在严格模式下，`this` 为 `undefined`。

需要注意，ES Module 默认采用严格模式，因此不能认为普通函数调用时的 `this` 一定指向 `window`。

### 2. 隐式绑定：对象方法调用

当函数通过对象的方法形式调用时，`this` 通常指向调用该方法的对象。

```javascript
const obj = {
    name: "张三",
    foo() {
        console.log(this.name);
    }
};

obj.foo(); // 张三
```

这里通过 `obj.foo()` 调用函数，因此 `this` 指向 `obj`。

需要注意，`this` 并不是由函数最初定义在哪个对象中决定的，而是由实际调用方式决定的。

```javascript
const obj = {
    name: "张三",
    foo() {
        console.log(this.name);
    }
};

const fn = obj.foo;

fn(); // 非严格模式下通常输出 undefined
```

将 `obj.foo` 赋值给变量 `fn` 后，再通过 `fn()` 调用，已经不再是通过 `obj` 调用方法，因此 `this` 发生了变化。

### 3. 显式绑定：call、apply、bind

`call`、`apply` 和 `bind` 都可以显式指定普通函数的 `this`。

```javascript
function foo() {
    console.log(this.name);
}

const obj = {
    name: "张三"
};

foo.call(obj);  // 张三
foo.apply(obj); // 张三

const fn = foo.bind(obj);
fn();           // 张三
```

三者的区别主要在于函数是否立即执行，以及参数的传递方式，后文会详细介绍。

### 4. new 绑定：构造函数调用

使用 `new` 调用构造函数时，JavaScript 会创建一个新对象，并将构造函数内部的 `this` 指向这个对象。

```javascript
function Person(name) {
    this.name = name;
}

const p = new Person("张三");

console.log(p.name); // 张三
```

使用 `new` 调用构造函数时，可以简单理解为以下过程：

1. 创建一个新的对象。
2. 将新对象的原型关联到构造函数的 `prototype`。
3. 以新对象作为 `this` 执行构造函数。
4. 如果构造函数返回一个对象，则返回该对象；否则返回新创建的对象。

### 5. this 绑定的优先级

对于普通函数，常见的绑定规则优先级可以概括为：

**new 绑定 > 显式绑定 > 隐式绑定 > 默认绑定**

其中，`call`、`apply` 和 `bind` 都属于显式绑定。

但需要注意，箭头函数没有自己的 `this`，它使用定义时外层作用域的 `this`，不能简单套用上述规则。另外，使用 `new` 调用绑定函数时，原先通过 `bind` 指定的 `this` 会被忽略。

---

## 二、call、apply、bind 的区别

### 1. call() 方法

`call()` 用于指定函数执行时的 `this`，并立即调用函数。

语法：

```javascript
fn.call(thisArg, arg1, arg2, ...);
```

* `thisArg`：指定函数执行时的 `this`。
* 后续参数：依次传递给被调用的函数。

示例：

```javascript
function introduce(age, city) {
    console.log(
        `我叫${this.name}，今年${age}岁，来自${city}`
    );
}

const person = {
    name: "张三"
};

introduce.call(person, 22, "杭州");
// 我叫张三，今年22岁，来自杭州
```

这里通过 `call()` 将 `introduce` 函数中的 `this` 指定为 `person`，同时将 `22` 和 `"杭州"` 作为函数参数传入。

### 2. apply() 方法

`apply()` 的作用与 `call()` 基本相同，同样可以指定 `this` 并立即调用函数。

区别在于，`apply()` 将函数参数放在一个数组或类数组对象中传递。

语法：

```javascript
fn.apply(thisArg, [arg1, arg2, ...]);
```

示例：

```javascript
function introduce(age, city) {
    console.log(
        `我叫${this.name}，今年${age}岁，来自${city}`
    );
}

const person = {
    name: "张三"
};

introduce.apply(person, [22, "杭州"]);
// 我叫张三，今年22岁，来自杭州
```

`apply()` 会将参数集合中的元素依次作为参数传递给函数。

### 3. bind() 方法

`bind()` 用于创建一个新的函数，并将该函数的 `this` 绑定到指定对象。

与 `call()` 和 `apply()` 不同，`bind()` **不会立即执行原函数，而是返回一个绑定后的新函数**。

语法：

```javascript
const newFn = fn.bind(thisArg, arg1, arg2, ...);
```

示例：

```javascript
function introduce(age, city) {
    console.log(
        `我叫${this.name}，今年${age}岁，来自${city}`
    );
}

const person = {
    name: "张三"
};

const newFn = introduce.bind(person, 22);

newFn("杭州");
// 我叫张三，今年22岁，来自杭州
```

这里通过 `bind()` 预先绑定了 `this` 和年龄参数 `22`，调用 `newFn()` 时只需要传入城市即可。

这种预先绑定部分参数的功能称为**偏函数应用**。

### 4. 三者的区别总结

| 对比项     | call      | apply   | bind         |
| ------- | --------- | ------- | ------------ |
| 指定 this | 是         | 是       | 是            |
| 是否立即执行  | 是         | 是       | 否            |
| 参数传递    | 逐个传递      | 数组或类数组  | 逐个传递，可预设参数   |
| 返回值     | 原函数执行结果   | 原函数执行结果 | 绑定后的新函数      |
| 常见用途    | 临时改变 this | 批量传递参数  | 延迟调用、固定 this |

补充：如果传入的 `thisArg` 为 `null` 或 `undefined`，普通非严格函数通常会使用全局对象作为 `this`，严格模式函数则保留 `null` 或 `undefined`。传入其他原始值时，普通函数与严格模式函数的行为也可能不同。

---

## 三、手写 call()

### 1. 实现思路

`call()` 的核心是让目标函数以指定对象的方法形式执行。

例如：

```javascript
function foo() {
    console.log(this.name);
}

const obj = {
    name: "张三"
};
```

如果执行：

```javascript
obj.fn = foo;
obj.fn();
```

那么 `foo` 就会以 `obj` 的方法形式调用，函数中的 `this` 指向 `obj`。

因此，可以利用这个原理实现 `call()`：

1. 判断调用者是否为函数。
2. 处理传入的 `thisArg`。
3. 将当前函数临时设置为目标对象的属性。
4. 通过目标对象调用这个函数。
5. 删除临时属性。
6. 返回函数执行结果。

### 2. 代码实现

```javascript
Function.prototype.myCall = function(context, ...args) {
    if (typeof this !== "function") {
        throw new TypeError("调用对象必须是函数");
    }

    context ??= globalThis;
    context = Object(context);

    const key = Symbol("fn");
    context[key] = this;

    try {
        return context[key](...args);
    } finally {
        delete context[key];
    }
};
```

测试：

```javascript
function add(a, b) {
    return this.num + a + b;
}

const obj = {
    num: 10
};

console.log(add.myCall(obj, 1, 2)); // 13
```

### 3. 实现原理

当执行：

```javascript
add.myCall(obj, 1, 2);
```

此时 `myCall` 内部的 `this` 指向函数 `add`。

接下来将 `add` 临时挂载到 `obj` 上，相当于：

```javascript
obj[key] = add;
obj[key](1, 2);
```

由于函数是通过 `obj` 的属性调用的，所以函数中的 `this` 指向 `obj`。

执行完成后，再删除临时属性，避免污染原对象。

这里使用 `Symbol` 作为临时属性名，是为了降低与对象已有属性发生命名冲突的风险。`try...finally` 则可以确保函数执行后清理临时属性，即使执行过程中抛出异常也一样。

需要注意：这是一种用于理解原理的简化实现，并非完全符合 ECMAScript 规范的原生 `call()` 实现。

---

## 四、手写 apply()

### 1. 实现思路

`apply()` 的实现思路与 `call()` 基本一致，区别在于参数的传递方式。

* `call()`：将参数逐个传入。
* `apply()`：将数组或类数组中的元素作为参数传入。

在 JavaScript 中，可以使用展开运算符 `...` 将数组元素展开为独立参数。

### 2. 代码实现

```javascript
Function.prototype.myApply = function(context, args) {
    if (typeof this !== "function") {
        throw new TypeError("调用对象必须是函数");
    }

    context ??= globalThis;
    context = Object(context);

    const key = Symbol("fn");
    context[key] = this;

    try {
        return context[key](...(args ?? []));
    } finally {
        delete context[key];
    }
};
```

测试：

```javascript
function add(a, b) {
    return this.num + a + b;
}

const obj = {
    num: 10
};

console.log(add.myApply(obj, [1, 2])); // 13
```

### 3. 为什么使用展开运算符？

假设传入的参数是：

```javascript
const args = [1, 2, 3];
```

调用：

```javascript
fn(...args);
```

相当于：

```javascript
fn(1, 2, 3);
```

因此，`apply()` 可以通过展开参数集合，实现与 `call()` 类似的函数调用效果。

---

## 五、手写 bind()

### 1. 实现思路

`bind()` 比 `call()` 和 `apply()` 更复杂，因为它不立即执行函数，而是返回一个新的绑定函数。

实现时需要考虑以下问题：

1. 保存原函数。
2. 保存指定的 `this`。
3. 保存预设参数。
4. 返回一个新函数。
5. 调用新函数时，将预设参数与后续参数合并。
6. 如果新函数通过 `new` 调用，则忽略预先绑定的 `this`，并支持构造函数行为。

### 2. 代码实现

```javascript
Function.prototype.myBind = function(context, ...args1) {
    if (typeof this !== "function") {
        throw new TypeError("调用对象必须是函数");
    }

    const fn = this;

    function boundFn(...args2) {
        const isNew = new.target !== undefined;

        return fn.apply(
            isNew ? this : context,
            [...args1, ...args2]
        );
    }

    if (fn.prototype) {
        boundFn.prototype = Object.create(fn.prototype);
    }

    return boundFn;
};
```

这份代码用于理解 `bind()` 的核心原理，并没有完整实现原生 `bind()` 的所有规范细节。

### 3. 普通调用示例

```javascript
function greet(age, city) {
    console.log(
        `${this.name}，${age}岁，来自${city}`
    );
}

const person = {
    name: "张三"
};

const newFn = greet.myBind(person, 22);

newFn("杭州");
// 张三，22岁，来自杭州
```

这里：

* `person` 是预先绑定的 `this`。
* `22` 是预设参数。
* `"杭州"` 是调用新函数时传入的参数。

最终传入原函数的参数为 `[22, "杭州"]`。

### 4. 为什么 bind 需要处理 new？

考虑以下代码：

```javascript
function Person(name, age) {
    this.name = name;
    this.age = age;
}

const obj = {
    name: "其他对象"
};

const BoundPerson = Person.bind(obj, "张三");

const p = new BoundPerson(20);

console.log(p.name); // 张三
console.log(p.age);  // 20
```

虽然 `Person.bind(obj, "张三")` 绑定了 `obj`，但在执行 `new BoundPerson(20)` 时，构造函数内部的 `this` 指向新创建的实例，而不是 `obj`。

原因是：**当绑定函数通过 `new` 调用时，`new` 创建的新对象具有更高的优先级，原先绑定的 `this` 不再生效。**

这也是手写 `bind()` 时必须考虑的关键问题。

---

## 六、箭头函数与 this

箭头函数是 `this` 面试中经常考查的特殊情况。

箭头函数没有自己的 `this`，而是使用定义时外层作用域中的 `this`。

```javascript
const obj = {
    name: "张三",

    foo() {
        const fn = () => {
            console.log(this.name);
        };

        fn();
    }
};

obj.foo(); // 张三
```

箭头函数 `fn` 定义在 `foo()` 内部，因此它使用外层 `foo()` 执行时的 `this`，也就是 `obj`。

即使使用 `call()`，也无法改变箭头函数已经确定的词法 `this`：

```javascript
const obj1 = {
    name: "张三"
};

const obj2 = {
    name: "李四"
};

const fn = () => {
    console.log(this);
};

fn.call(obj1);
fn.call(obj2);
```

两次调用都不会因为 `call()` 而改变箭头函数的 `this`。

---

## 七、面试总结

### 1. 如何理解 this？

`this` 指向函数执行时所关联的对象。普通函数的 `this` 主要由调用方式决定，常见规则包括默认绑定、隐式绑定、显式绑定和 `new` 绑定。箭头函数没有自己的 `this`，而是继承外层作用域的 `this`。

### 2. call 和 apply 有什么区别？

两者都能显式指定 `this` 并立即调用函数，区别在于参数传递方式：`call()` 将参数逐个传入，`apply()` 则将参数放在数组或类数组对象中传入。

### 3. bind 和 call 有什么区别？

`call()` 会立即调用函数并返回执行结果，而 `bind()` 不会立即执行函数，它会返回一个绑定了 `this` 的新函数，并且支持预设参数。

### 4. 如何手写 call、apply、bind？

* `call()`：利用临时属性，将函数作为目标对象的方法调用。
* `apply()`：实现思路与 `call()` 相同，只是需要展开参数集合。
* `bind()`：返回一个新函数，保存原函数、绑定对象和预设参数，并处理普通调用与 `new` 调用的区别。

### 5. 最后记住

| 方法      | 核心特点                   |
| ------- | ---------------------- |
| `this`  | 普通函数的指向由调用方式决定         |
| `call`  | 指定 `this`，逐个传参，立即执行    |
| `apply` | 指定 `this`，数组传参，立即执行    |
| `bind`  | 指定 `this`，返回新函数，支持预设参数 |

理解这几个概念的关键，不是死记语法，而是掌握两个问题：**函数是如何被调用的？调用时的 `this` 是如何确定的？**
