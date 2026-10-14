---
title: JavaScript 对象创建与继承方式总结
description: 梳理八种对象创建方式、六种经典继承模式与 class extends，理解原型链、属性共享和方法复用。
date: "2026-10-14"
tags:
  - JavaScript
  - 原型链
  - 继承
  - 前端八股
---

# JavaScript 对象创建与继承方式总结

## 一、对象创建的方式

JavaScript 是一门基于原型的语言，对象可以通过多种方式创建。不同的创建方式在代码复用、属性共享和继承关系上有所区别。

### 1. 工厂模式

工厂模式通过普通函数创建并返回对象。

```js
function createPerson(name, age) {
    return {
        name,
        age,
        sayHi() {
            console.log(`你好，我是${this.name}`);
        }
    };
}

const p1 = createPerson('小明', 20);
const p2 = createPerson('小红', 21);

p1.sayHi(); // 你好，我是小明
```

**优点：**

* 创建对象简单，调用时不需要使用 `new`。
* 可以根据传入参数灵活地创建对象。

**缺点：**

* 无法通过 `instanceof` 直接判断对象是否由该工厂函数创建。
* 每次调用都会创建新的方法函数，无法通过原型自动共享方法。

**适用场景：** 创建结构相似但不需要特定构造函数身份的对象。

### 2. 构造函数模式

构造函数用于初始化对象，通常配合 `new` 使用。

```js
function Person(name, age) {
    this.name = name;
    this.age = age;

    this.sayHi = function() {
        console.log(`你好，我是${this.name}`);
    };
}

const p1 = new Person('小明', 20);
const p2 = new Person('小红', 21);

console.log(p1 instanceof Person); // true
```

使用 `new` 调用构造函数时，主要会发生以下过程：

1. 创建一个新对象。
2. 将新对象的原型关联到构造函数的 `prototype`。
3. 将构造函数内部的 `this` 指向新对象。
4. 执行构造函数中的代码。
5. 如果构造函数显式返回对象或函数，则 `new` 表达式的结果为该返回值；否则返回新创建的对象。

**优点：**

* 可以通过 `instanceof` 判断实例与构造函数之间的关系。
* 适合创建具有相同属性结构的多个对象。

**缺点：**

* 如果方法定义在构造函数内部，每个实例都会创建自己的方法函数，造成不必要的重复。

### 3. 原型模式

JavaScript 中，每个普通函数通常都有一个 `prototype` 属性。通过构造函数创建的实例，可以沿原型链访问构造函数原型上的属性和方法。

```js
function Person() {}

Person.prototype.name = '小明';

Person.prototype.sayHi = function() {
    console.log(`你好，我是${this.name}`);
};

const p1 = new Person();
const p2 = new Person();

p1.sayHi(); // 你好，我是小明

console.log(p1.sayHi === p2.sayHi); // true
```

**优点：**

* 原型上的方法由多个实例共享，节省内存。
* 适合定义多个实例共同使用的方法。

**缺点：**

* 如果原型上存放数组、对象等引用类型数据，多个实例可能共享同一个引用，修改时容易相互影响。
* 实例自身的属性不适合全部放在原型上，否则可能出现共享状态问题。

例如：

```js
function Person() {}

Person.prototype.hobbies = ['篮球', '音乐'];

const p1 = new Person();
const p2 = new Person();

p1.hobbies.push('阅读');

console.log(p2.hobbies); // ['篮球', '音乐', '阅读']
```

这是因为 `p1` 和 `p2` 访问的是原型上的同一个数组。

### 4. 构造函数与原型组合模式

组合模式结合构造函数模式和原型模式，是经典 JavaScript 继承体系中常见的对象创建方式。

```js
function Person(name, age) {
    this.name = name;
    this.age = age;
}

Person.prototype.sayHi = function() {
    console.log(`你好，我是${this.name}`);
};

const p1 = new Person('小明', 20);
const p2 = new Person('小红', 21);

p1.sayHi();
p2.sayHi();

console.log(p1.sayHi === p2.sayHi); // true
```

构造函数负责定义实例独有的属性，原型负责定义实例共享的方法。

**优点：**

* 实例属性相互独立。
* 原型方法可以共享。
* 兼顾对象状态隔离与方法复用。

**缺点：**

* 需要分别维护构造函数和原型上的定义，代码相对分散。

### 5. 动态原型模式

动态原型模式在构造函数内部检查原型方法是否存在，如果不存在，就统一添加。

```js
function Person(name) {
    this.name = name;

    if (typeof this.sayHi !== 'function') {
        Person.prototype.sayHi = function() {
            console.log(`你好，我是${this.name}`);
        };
    }
}

const p1 = new Person('小明');
const p2 = new Person('小红');

p1.sayHi();
p2.sayHi();
```

**特点：**

* 将实例属性和原型方法的定义集中在构造函数中。
* 原型方法只需要初始化一次。

这种方式属于经典创建模式，现在实际项目中不如 `class` 常见。

### 6. 寄生构造函数模式

寄生构造函数模式看起来像构造函数，但函数内部显式返回一个新对象。

```js
function SpecialArray() {
    const arr = [];

    arr.push.apply(arr, arguments);

    arr.show = function() {
        console.log(this.join(','));
    };

    return arr;
}

const a = new SpecialArray(1, 2, 3);

a.show(); // 1,2,3

console.log(a instanceof SpecialArray); // false
```

虽然调用时使用了 `new`，但由于构造函数返回了另一个对象，最终得到的是该数组，而不是通常意义上以 `SpecialArray.prototype` 为原型的实例。

**特点：**

* 可以返回自定义类型的对象。
* 返回的对象不一定与构造函数建立原型继承关系。
* 可能让 `instanceof` 和对象身份判断变得不直观。

### 7. Object.create() 创建对象

`Object.create()` 可以指定新对象的原型。

```js
const person = {
    name: '小明',
    sayHi() {
        console.log(`你好，我是${this.name}`);
    }
};

const p1 = Object.create(person);

p1.sayHi(); // 你好，我是小明

console.log(Object.getPrototypeOf(p1) === person); // true
```

这里的 `p1` 是新创建的对象，其原型指向 `person`。

需要注意：

```js
p1.prototype; // undefined
Object.getPrototypeOf(p1) === person; // true
```

`prototype` 通常是构造函数上的属性，而普通对象的原型应使用 `Object.getPrototypeOf()` 查看。

### 8. ES6 class 创建对象

现代 JavaScript 中，可以使用 `class` 定义类，并通过 `new` 创建实例。

```js
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    sayHi() {
        console.log(`你好，我是${this.name}`);
    }
}

const p1 = new Person('小明', 20);
const p2 = new Person('小红', 21);

console.log(p1.sayHi === p2.sayHi); // true
```

类中的普通实例方法定义在 `Person.prototype` 上，由实例共享；`constructor` 则负责初始化实例属性。

`class` 是 JavaScript 基于原型的对象模型之上的语法抽象，并不是完全不同于原型机制的一套继承体系。

---

## 二、对象继承的方式

继承的核心是让一个对象能够访问另一个对象的属性和方法。JavaScript 主要通过原型链实现对象之间的继承关系。

以下以 `Parent` 和 `Child` 为例，介绍六种经典继承方式。

### 1. 原型链继承

将父构造函数的实例赋值给子构造函数的原型。

```js
function Parent() {
    this.hobbies = ['篮球', '音乐'];
}

Parent.prototype.sayHi = function() {
    console.log('你好');
};

function Child() {}

Child.prototype = new Parent();

const c1 = new Child();
const c2 = new Child();

c1.sayHi(); // 你好

c1.hobbies.push('阅读');

console.log(c2.hobbies); // ['篮球', '音乐', '阅读']
```

**原理：**

`Child.prototype` 是一个 `Parent` 的实例，因此子类实例可以沿原型链访问父类实例的属性和父类原型上的方法。

**优点：** 实现简单，可以继承父类原型上的方法。

**缺点：**

* 引用类型属性被多个子实例共享。
* 创建子实例时，无法通过原型链继承方式向父构造函数传递实例化参数。

### 2. 构造函数继承

在子构造函数中调用父构造函数，并通过 `call` 或 `apply` 将 `this` 指向当前子实例。

```js
function Parent(name) {
    this.name = name;
    this.hobbies = ['篮球', '音乐'];
}

Parent.prototype.sayHi = function() {
    console.log(`你好，我是${this.name}`);
};

function Child(name, score) {
    Parent.call(this, name);
    this.score = score;
}

const c1 = new Child('小明', 90);
const c2 = new Child('小红', 95);

c1.hobbies.push('阅读');

console.log(c2.hobbies); // ['篮球', '音乐']
console.log(c1.score);   // 90
```

**原理：**

`Parent.call(this, name)` 会在创建子实例时执行父构造函数，让父构造函数中的属性初始化在当前子实例上。

**优点：**

* 可以向父构造函数传递参数。
* 每个实例拥有独立的引用类型属性。

**缺点：**

* 无法通过这种方式直接继承父原型上的方法。
* 如果父构造函数中定义方法，每个实例都可能重复创建方法函数。

### 3. 组合继承

组合继承结合原型链继承和构造函数继承。

```js
function Parent(name) {
    this.name = name;
    this.hobbies = ['篮球', '音乐'];
}

Parent.prototype.sayHi = function() {
    console.log(`你好，我是${this.name}`);
};

function Child(name, score) {
    Parent.call(this, name);
    this.score = score;
}

Child.prototype = new Parent();

Child.prototype.constructor = Child;

const c1 = new Child('小明', 90);
const c2 = new Child('小红', 95);

c1.sayHi();

c1.hobbies.push('阅读');

console.log(c2.hobbies); // ['篮球', '音乐']
```

**优点：**

* 实例属性相互独立。
* 能够继承父原型上的方法。
* 兼顾参数传递和原型方法复用。

**缺点：**

父构造函数会被调用两次：

1. 执行 `Child.prototype = new Parent()` 时调用一次。
2. 执行 `Parent.call(this, name)` 创建子实例时再调用一次。

第一次调用产生的父实例属性会存在于 `Child.prototype` 上，但实例通常会通过自己的同名属性覆盖它们，造成不必要的初始化。

### 4. 原型式继承

原型式继承基于一个现有对象创建新对象，让新对象将现有对象作为原型。

```js
const person = {
    name: '小明',
    hobbies: ['篮球', '音乐']
};

const p1 = Object.create(person);
const p2 = Object.create(person);

console.log(p1.name); // 小明

p1.name = '小红';

console.log(p1.name); // 小红
console.log(p2.name); // 小明

p1.hobbies.push('阅读');

console.log(p2.hobbies); // ['篮球', '音乐', '阅读']
```

**优点：**

* 不需要构造函数即可建立原型关系。
* 适合基于已有对象创建其他对象。

**缺点：**

* 引用类型属性可能被多个对象共享。
* 不负责定义构造函数式的实例初始化流程。

### 5. 寄生式继承

寄生式继承在原型式继承的基础上，将对象创建和功能增强封装在函数中。

```js
const person = {
    name: '小明'
};

function createAnother(original) {
    const clone = Object.create(original);

    clone.sayHi = function() {
        console.log(`你好，我是${this.name}`);
    };

    return clone;
}

const p1 = createAnother(person);

p1.sayHi(); // 你好，我是小明
```

**优点：**

* 可以基于现有对象创建新对象。
* 可以在创建过程中为新对象添加额外属性或方法。

**缺点：**

* 每次调用函数时，新增的方法可能都会重新创建。
* 不直接解决构造函数之间的完整继承问题。

### 6. 寄生式组合继承

寄生式组合继承结合构造函数继承和原型继承，是经典 JavaScript 继承模式中比较完善的一种方式。

```js
function Parent(name) {
    this.name = name;
    this.hobbies = ['篮球', '音乐'];
}

Parent.prototype.sayHi = function() {
    console.log(`你好，我是${this.name}`);
};

function Child(name, score) {
    // 继承父构造函数的实例属性
    Parent.call(this, name);
    this.score = score;
}

// 继承父原型上的方法
Child.prototype = Object.create(Parent.prototype);

// 修正 constructor 指向
Child.prototype.constructor = Child;

Child.prototype.study = function() {
    console.log(`${this.name}正在学习`);
};

const c1 = new Child('小明', 90);
const c2 = new Child('小红', 95);

c1.sayHi();
c1.study();

c1.hobbies.push('阅读');

console.log(c2.hobbies); // ['篮球', '音乐']
console.log(c1 instanceof Child);  // true
console.log(c1 instanceof Parent); // true
```

**核心原理：**

第一步，使用 `Parent.call(this, name)` 继承父构造函数的实例属性。

第二步，使用 `Object.create(Parent.prototype)` 创建一个新对象，并将它的原型指向 `Parent.prototype`，从而继承父类的原型方法。

第三步，使用 `Child.prototype.constructor = Child` 修正 `constructor` 属性。

**为什么不使用 `Child.prototype = new Parent()`？**

因为 `new Parent()` 会额外执行一次父构造函数。使用 `Object.create(Parent.prototype)` 只建立原型关系，不执行父构造函数，从而避免组合继承中父构造函数被重复调用的问题。

---

## 三、六种经典继承方式对比

| 继承方式    | 父实例属性      | 父原型方法  | 引用类型属性是否独立 | 主要问题             |
| ------- | ---------- | ------ | ---------- | ---------------- |
| 原型链继承   | 可以访问，但通常共享 | 可以     | 否          | 引用属性共享，不能直接传参初始化 |
| 构造函数继承  | 可以         | 不会自动继承 | 是          | 父原型方法无法直接复用      |
| 组合继承    | 可以         | 可以     | 是          | 父构造函数执行两次        |
| 原型式继承   | 可以访问，但通常共享 | 可以访问   | 否          | 引用属性共享           |
| 寄生式继承   | 可以访问，但通常共享 | 可以访问   | 否          | 增强方法可能重复创建       |
| 寄生式组合继承 | 可以         | 可以     | 是          | 代码相对复杂           |

这里的“父实例属性”指父构造函数初始化的属性；表中的“可以”表示能够继承或访问相应能力，而不是所有属性都必然以同一种方式存储。

---

## 四、现代 JavaScript 的继承方式：class extends

在现代 JavaScript 项目中，通常使用 `class` 和 `extends` 实现继承。

```js
class Parent {
    constructor(name) {
        this.name = name;
        this.hobbies = ['篮球', '音乐'];
    }

    sayHi() {
        console.log(`你好，我是${this.name}`);
    }
}

class Child extends Parent {
    constructor(name, score) {
        super(name);
        this.score = score;
    }

    study() {
        console.log(`${this.name}正在学习`);
    }
}

const c1 = new Child('小明', 90);
const c2 = new Child('小红', 95);

c1.sayHi();
c1.study();

console.log(c1 instanceof Child);  // true
console.log(c1 instanceof Parent); // true
```

其中：

* `extends` 建立子类与父类之间的继承关系。
* `super(name)` 调用父类构造函数，初始化父类定义的实例属性。
* `sayHi()` 定义在父类原型上，可以被子类实例访问。
* `study()` 定义在子类原型上。
* 每个实例都有独立的 `hobbies` 数组。

对于派生类，必须先调用 `super()`，才能在构造函数中使用 `this`。

`class extends` 可以看作对原型继承机制的现代语法封装。理解原型链，有助于理解 `extends`、`super` 和 `instanceof` 的行为。

---

## 五、必须区分的三个概念

### 1. prototype

`prototype` 是普通构造函数用于提供实例原型的属性。

```js
function Person() {}

console.log(typeof Person.prototype); // object
```

通过 `new Person()` 创建的实例，会将 `Person.prototype` 作为自己的原型。

### 2. 对象的原型

对象的原型可以通过 `Object.getPrototypeOf()` 获取。

```js
function Person() {}

const p1 = new Person();

console.log(Object.getPrototypeOf(p1) === Person.prototype); // true
```

普通对象通常没有自动创建的 `prototype` 属性：

```js
console.log(p1.prototype); // undefined
```

### 3. constructor

`constructor` 通常是原型对象上的一个属性，指向创建该原型的构造函数。

```js
function Person() {}

const p1 = new Person();

console.log(p1.constructor === Person); // true
```

这里 `p1.constructor` 通常是沿着原型链找到的，并不是 `p1` 自己的属性。

需要注意，`constructor` 可以被修改，因此不能单独依赖它判断对象是否真正由某个构造函数创建。`instanceof` 则检查指定构造函数的 `prototype` 是否存在于对象的原型链上。

---

## 六、总结与面试记忆

### 对象创建方式

* **工厂模式：** 普通函数创建并返回对象。
* **构造函数模式：** 使用 `new` 创建实例。
* **原型模式：** 将共享属性和方法放在原型上。
* **构造函数与原型组合模式：** 构造函数保存实例属性，原型保存共享方法。
* **动态原型模式：** 在构造函数内部按需初始化原型方法。
* **寄生构造函数模式：** 构造函数显式返回一个对象。
* **`Object.create()`：** 指定新对象的原型。
* **`class`：** 使用现代类语法创建对象。

### 继承方式

* **原型链继承：** `Child.prototype = new Parent()`。
* **构造函数继承：** `Parent.call(this)`。
* **组合继承：** `Parent.call(this)` + `Child.prototype = new Parent()`。
* **原型式继承：** `Object.create(original)`。
* **寄生式继承：** 基于现有对象创建新对象，并为其添加功能。
* **寄生式组合继承：** `Parent.call(this)` + `Object.create(Parent.prototype)`。
* **现代继承：** `class Child extends Parent` + `super()`。

面试中最值得掌握的是构造函数与原型的关系、原型链继承的引用属性共享问题、组合继承为什么会调用父构造函数两次，以及寄生式组合继承为什么使用 `Object.create(Parent.prototype)`。

理解这些原理后，再学习 Vue、React 生态和其他 JavaScript 库中的对象模型时，会更容易理解方法共享、原型链查找与类继承机制。
