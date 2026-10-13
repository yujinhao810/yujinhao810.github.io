---
title: "Map和forEach的区别"
description: "map() 和 forEach() 都是 JavaScript 数组的迭代方法，可以遍历数组，并对数组中的每个元素执行回调函数。"
date: "2026-10-12"
publishedAt: "2026-10-12T10:02:40.630774+08:00"
source: "https://kajspace.cn/articles/01KZZ34KNR45JZY20Y2FRHKN0J/"
tags: ["前端"]
---

# Map和forEach的区别

## JavaScript 中 map 和 forEach 的区别详解 {#kaj-h-ffba1e4a-66e5-46e1-ac18-8badc6795b70}

## 一、map 和 forEach 是什么？ {#kaj-h-6339fbd8-0b5e-4b37-97ae-2d6511c9e857}

`map()` 和 `forEach()` 都是 JavaScript 数组的迭代方法，可以遍历数组，并对数组中的每个元素执行回调函数。

它们最大的区别是：

- `map()`**：遍历数组并根据回调函数的返回值，生成一个新数组。**
- `forEach()`**：遍历数组并执行回调函数，本身不生成用于接收映射结果的新数组。**

例如：

```js
const arr = [1, 2, 3];

const result1 = arr.map(item => item * 2);
const result2 = arr.forEach(item => item * 2);

console.log(result1); // [2, 4, 6]
console.log(result2); // undefined
```

虽然两者都执行了 `item * 2`，但结果不同。

`map()` 会收集每次回调函数的返回值，组成新数组；`forEach()` 不会收集这些返回值。

## 二、map 的用法和实现原理 {#kaj-h-817992e3-6d1d-4d05-893f-034cdd2f32a5}

### 2.1 基本语法 {#kaj-h-9b75ce8f-24f2-42b8-b351-e734e8268ec0}

```js
const newArray = array.map(callback);
```

回调函数可以接收三个参数：

```js
array.map((element, index, array) => {
    return newValue;
});
```

- `element`：当前正在处理的元素。
- `index`：当前元素的索引。
- `array`：调用 `map()` 的原数组。

其中，`element` 是最常用的参数。

### 2.2 map 如何生成新数组？ {#kaj-h-202dd74f-4c6c-4702-8703-c17935befe5f}

```js
const arr = [1, 2, 3];

const result = arr.map(item => {
    return item * 2;
});

console.log(result); // [2, 4, 6]
console.log(arr);    // [1, 2, 3]
```

执行过程可以理解为：

1. 遍历第一个元素 `1`，回调返回 `2`，将 `2` 放入新数组。
2. 遍历第二个元素 `2`，回调返回 `4`，将 `4` 放入新数组。
3. 遍历第三个元素 `3`，回调返回 `6`，将 `6` 放入新数组。
4. 返回新数组 `[2, 4, 6]`。

可以简化理解为：

```text
原数组：[1, 2, 3]
          ↓ map
回调结果：2、4、6
          ↓ 收集返回值
新数组：[2, 4, 6]
```

### 2.3 map 的返回值由什么决定？ {#kaj-h-e8ae1934-c31a-4bde-ab4b-086edb186ef2}

`map()` 返回的新数组中，每个元素对应回调函数的返回值。

```js
const arr = [1, 2, 3];

const a = arr.map(item => item + 1);
const b = arr.map(item => item > 1);

console.log(a); // [2, 3, 4]
console.log(b); // [false, true, true]
```

如果回调函数没有显式返回值，那么对应位置会是 `undefined`：

```js
const arr = [1, 2, 3];

const result = arr.map(item => {
    item * 2;
});

console.log(result); // [undefined, undefined, undefined]
```

原因是使用了带花括号的箭头函数，却没有写 `return`。

正确写法：

```js
const result = arr.map(item => {
    return item * 2;
});
```

或者：

```js
const result = arr.map(item => item * 2);
```

### 2.4 map 的常见应用场景 {#kaj-h-20948247-72c1-4474-b903-027fd2d12cb8}

**场景一：转换数组元素**

```js
const prices = [10, 20, 30];

const discountedPrices = prices.map(price => price * 0.8);

console.log(discountedPrices); // [8, 16, 24]
```

**场景二：提取对象属性**

```js
const users = [
    { id: 1, name: '张三' },
    { id: 2, name: '李四' },
    { id: 3, name: '王五' }
];

const names = users.map(user => user.name);

console.log(names); // ['张三', '李四', '王五']
```

**场景三：转换前端展示数据**

```js
const users = [
    { id: 1, name: '张三', age: 20 },
    { id: 2, name: '李四', age: 25 }
];

const options = users.map(user => ({
    label: user.name,
    value: user.id
}));

console.log(options);
// [
//   { label: '张三', value: 1 },
//   { label: '李四', value: 2 }
// ]
```

在 Vue、React 等前端开发中，`map()` 经常用于将接口返回的数据转换成下拉框选项、表格数据或其他展示结构。

## 三、forEach 的用法和实现原理 {#kaj-h-28f09759-1f15-48b7-9bbd-72214ef7577c}

### 3.1 基本语法 {#kaj-h-72e7e8fa-6134-4380-8dc5-7adce4643e1a}

```text
array.forEach(callback);
```

回调函数同样可以接收三个参数：

```js
array.forEach((element, index, array) => {
    // 执行操作
});
```

- `element`：当前元素。
- `index`：当前索引。
- `array`：原数组。

### 3.2 forEach 如何执行？ {#kaj-h-ae36cc73-ed1a-4712-9bfa-8ed73daa0cec}

```js
const arr = [1, 2, 3];

arr.forEach(item => {
    console.log(item * 2);
});
```

输出：

```text
2
4
6
```

`forEach()` 会依次执行回调函数，但不会把回调函数的返回值收集起来形成一个新数组。

例如：

```js
const arr = [1, 2, 3];

const result = arr.forEach(item => {
    return item * 2;
});

console.log(result); // undefined
```

这里虽然回调函数返回了 `2`、`4`、`6`，但是 `forEach()` 会忽略这些返回值，因此 `result` 是 `undefined`。

注意：这并不意味着 `forEach()` 的回调函数不能写 `return`。它可以写，但返回值不会成为 `forEach()` 的结果。

### 3.3 forEach 的常见应用场景 {#kaj-h-eb635926-b9dc-4d55-8440-a09133cbe7af}

**场景一：打印数据或执行日志**

```js
const arr = [1, 2, 3];

arr.forEach(item => {
    console.log(item);
});
```

**场景二：执行副作用操作**

```js
const users = [
    { name: '张三', active: false },
    { name: '李四', active: false }
];

users.forEach(user => {
    user.active = true;
});

console.log(users);
```

这里直接修改了原数组中对象的属性。

**场景三：批量执行操作**

```js
const buttons = document.querySelectorAll('button');

buttons.forEach(button => {
    button.disabled = true;
});
```

这个例子中，`forEach()` 用于依次操作按钮，并不需要生成一个新数组。

## 四、map 和 forEach 的核心区别 {#kaj-h-4f2d1f58-32f2-42de-bb48-bb7f8c09089e}

| 对比维度 | map() | forEach() |
| --- | --- | --- |
| 主要用途 | 转换数据、生成新数组 | 遍历数据、执行操作 |
| 返回值 | 新数组 | `undefined` |
| 是否收集回调返回值 | 是 | 否 |
| 是否自动修改原数组 | 否 | 否 |
| 回调函数的返回值 | 决定新数组对应元素 | 通常被忽略 |
| 是否适合链式转换 | 适合 | 不适合直接接着进行数组转换 |
| 是否能用 break 中断 | 不能直接使用 | 不能直接使用 |

这里需要特别注意：`map()` **和** `forEach()` **本身都不会自动修改原数组，但回调函数可以主动修改原数组或其中的对象。**

例如：

```js
const arr = [1, 2, 3];

arr.map((item, index, array) => {
    array[index] = item * 2;
    return item * 2;
});

console.log(arr); // [2, 4, 6]
```

虽然使用了 `map()`，但由于回调函数显式修改了原数组，原数组也发生了变化。

因此，不能简单地认为 `map()` 一定不会修改原数组。准确的说法是：`map()` **不会自动修改原数组，但回调函数可能产生修改原数组的副作用。**

## 五、为什么 forEach 不能直接使用 break？ {#kaj-h-e17f5c33-a280-488a-9ea3-bf8305fd5f53}

下面的写法会报语法错误：

```js
const arr = [1, 2, 3, 4];

arr.forEach(item => {
    if (item === 3) {
        break;
    }
});
```

`break` 不能用于直接终止 `forEach()` 的遍历。

如果需要根据条件提前结束遍历，可以使用普通 `for` 循环：

```js
for (const item of arr) {
    if (item === 3) {
        break;
    }

    console.log(item);
}
```

如果只是希望找到符合条件的第一个元素，可以使用 `find()`：

```js
const result = arr.find(item => item === 3);

console.log(result); // 3
```

如果需要判断是否存在符合条件的元素，可以使用 `some()`；如果需要判断所有元素是否都符合条件，可以使用 `every()`。

## 六、map 和 forEach 的常见面试题 {#kaj-h-7b334699-557f-493c-be40-46083be0aef1}

### 6.1 map 一定返回新数组吗？ {#kaj-h-90cef2d5-e65d-419b-9d64-1ce95eb4bda5}

`map()` 正常执行完成后，会返回一个新的数组。即使回调函数没有返回值，新数组中也会保留相应位置，只是元素为 `undefined`。

```js
const result = [1, 2, 3].map(item => {});

console.log(result); // [undefined, undefined, undefined]
```

### 6.2 forEach 的回调函数有返回值，为什么结果还是 undefined？ {#kaj-h-e1442db5-f234-4894-a006-ca4f88c3a3cd}

```js
const result = [1, 2, 3].forEach(item => item * 2);

console.log(result); // undefined
```

因为 `forEach()` 的设计目的在于执行回调操作，而不是收集回调返回值。回调函数的返回值会被忽略。

### 6.3 map 和 forEach 谁的性能更好？ {#kaj-h-9ffd1ff3-c78a-4873-93b7-99c10f33e966}

不能简单地说哪一个一定更快。

`map()` 需要创建新数组并保存回调结果；`forEach()` 不需要创建用于保存映射结果的新数组。但实际性能取决于回调操作、数据规模、JavaScript 引擎优化等因素。

因此，日常开发中应优先根据用途选择方法，而不是为了微小的性能差异牺牲代码可读性。

### 6.4 map 和 forEach 都是同步执行的吗？ {#kaj-h-4dce16c6-75d4-49db-a4dc-1c187ec2af80}

两者对数组元素的遍历和回调调用都是同步进行的。但是，如果回调函数内部使用了异步操作，异步操作本身不会因此变成同步操作。

例如：

```js
const arr = [1, 2, 3];

arr.forEach(async item => {
    await fetch(`/api/${item}`);
});

console.log('执行结束');
```

这里 `forEach()` 不会等待这些异步回调完成，`console.log()` 可能在请求完成之前执行。

如果需要等待所有异步任务完成，可以使用：

```js
await Promise.all(
    arr.map(item => fetch(`/api/${item}`))
);
```

这里利用 `map()` 生成 Promise 数组，再由 `Promise.all()` 等待这些 Promise 全部成功。

注意，如果其中一个请求失败，`Promise.all()` 返回的 Promise 就会拒绝；它也不会自动取消其他请求。

## 七、总结 {#kaj-h-4a0a1631-6065-44af-9e2b-22ed75aa08a7}

`map()` 和 `forEach()` 都可以遍历数组，但设计目的不同。

- 当你需要把原数组转换成另一个数组时，使用 `map()`。
- 当你只需要遍历元素并执行操作时，使用 `forEach()`。
- `map()` 收集回调函数的返回值，`forEach()` 忽略回调函数的返回值。
- 两者都不会因为调用本身而自动修改原数组，但回调函数可以修改原数组或其内部对象。
- 两者都不能直接通过 `break` 提前终止遍历。

**面试一句话总结：** `map()` 是映射方法，通过回调函数的返回值生成新数组；`forEach()` 是遍历方法，用于执行回调操作，本身返回 `undefined`，不会收集回调函数的返回值。
