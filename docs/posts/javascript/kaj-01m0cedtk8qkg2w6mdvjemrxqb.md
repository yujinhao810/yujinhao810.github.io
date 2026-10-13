---
title: "JavaScript 中的 Array 方法分类及用法"
description: "先看这张分类表，建立整体认识。"
date: "2026-10-12"
publishedAt: "2026-10-12T11:01:57.094286+08:00"
source: "https://kajspace.cn/articles/01M0CEDTK8QKG2W6MDVJEMRXQB/"
tags: ["前端"]
---

# JavaScript 中的 Array 方法分类及用法

## 一、Array 方法总览 {#kaj-h-0906d6b7-3240-4158-8cd8-3dd27eba0443}

先看这张分类表，建立整体认识。

| 分类 | 常用方法 | 核心作用 |
| --- | --- | --- |
| 增删元素 | `push`、`pop`、`shift`、`unshift`、`splice` | 添加、删除元素 |
| 截取与拼接 | `slice`、`concat`、`join` | 截取、合并、拼接字符串 |
| 遍历与转换 | `forEach`、`map`、`flat`、`flatMap` | 遍历、转换、扁平化 |
| 查找元素 | `find`、`findIndex`、`indexOf`、`includes` | 查找元素或判断是否存在 |
| 条件判断 | `some`、`every` | 判断部分或全部元素是否满足条件 |
| 数组过滤与计算 | `filter`、`reduce` | 筛选元素、归约计算 |
| 排序与反转 | `sort`、`reverse` | 排序、反转 |
| 创建数组 | `Array.from`、`Array.of`、`fill` | 转换、创建、填充数组 |
| 迭代器 | `keys`、`values`、`entries` | 获取索引、值、键值对 |
| 其他 | `at`、`toReversed`、`toSorted`、`toSpliced`、`with` | 安全访问、非破坏性修改 |

## 二、先掌握一个核心分类：是否修改原数组？ {#kaj-h-f0b6846b-e79e-46e4-8d18-cb87163365b2}

这是面试中最容易考察的知识点。

### 2.1 会修改原数组的方法 {#kaj-h-eff40df4-bfe5-4817-865f-a89eece2ef47}

| 方法 | 作用 | 返回值 |
| --- | --- | --- |
| `push()` | 末尾添加元素 | 新数组长度 |
| `pop()` | 删除末尾元素 | 被删除的元素 |
| `unshift()` | 开头添加元素 | 新数组长度 |
| `shift()` | 删除开头元素 | 被删除的元素 |
| `splice()` | 删除、插入或替换元素 | 被删除元素组成的数组 |
| `sort()` | 排序 | 排序后的原数组 |
| `reverse()` | 反转 | 反转后的原数组 |
| `fill()` | 填充指定范围 | 被修改的原数组 |
| `copyWithin()` | 将数组内部一段复制到另一位置 | 被修改的原数组 |

示例：

```js
const arr = [1, 2, 3];

arr.push(4);
console.log(arr); // [1, 2, 3, 4]

arr.splice(1, 1);
console.log(arr); // [1, 3, 4]
```

注意：`splice()` 的第二个参数表示删除的元素数量，而不是结束索引。

### 2.2 不修改原数组的方法 {#kaj-h-fdf8bc39-30f4-4c66-a204-1b95d2cda942}

常见方法包括：

- `slice()`：截取数组。
- `concat()`：合并数组。
- `map()`：映射成新数组。
- `filter()`：筛选出符合条件的元素。
- `flat()`、`flatMap()`：扁平化数组。
- `toSorted()`、`toReversed()`、`toSpliced()`、`with()`：返回修改后的新数组。

例如：

```js
const arr = [3, 1, 2];

const result = arr.toSorted((a, b) => a - b);

console.log(result); // [1, 2, 3]
console.log(arr);    // [3, 1, 2]
```

补充：`toSorted()` 等较新的方法在现代 JavaScript 环境中可用，但旧版浏览器可能不支持。

## 三、增删元素：push、pop、shift、unshift、splice {#kaj-h-2a8afa1c-bb08-401c-aeb5-a33d379b3992}

JavaScript Array Pop: Bí Quyết Sử Dụng Hiệu Quả Trong Lập Trình

1. `push()` 和 `pop()`

操作数组末尾。

```js
const arr = [1, 2];

arr.push(3); // 返回 3，即新长度
arr.pop();   // 返回 3，即被删除的元素
```

JS数组操作示意图（shift，unshift，pop，push） - osimly - 博客园

2. `shift()` 和 `unshift()`

操作数组开头。

```js
const arr = [2, 3];

arr.unshift(1); // 返回 3，即新长度
arr.shift();    // 返回 1，即被删除的元素
```

### 3.1 splice：删除、插入、替换 {#kaj-h-3c756879-4b10-4682-9c99-35f1f9680aaa}

语法：

```text
arr.splice(start, deleteCount, item1, item2, ...);
```

例如：

```js
const arr = [10, 20, 30, 40];

// 删除
arr.splice(1, 1);
console.log(arr); // [10, 30, 40]

// 插入
arr.splice(1, 0, 20);
console.log(arr); // [10, 20, 30, 40]

// 替换
arr.splice(1, 1, 25);
console.log(arr); // [10, 25, 30, 40]
```

记忆方法：

- `start`：从哪里开始操作。
- `deleteCount`：删除多少个元素。
- 后面的参数：插入到该位置的元素。

## 四、截取与合并：slice、concat、join {#kaj-h-687c98ee-e7a3-4188-8bd5-75faf90be922}

### 4.1 slice：截取数组 {#kaj-h-010f1b29-8263-454b-8e12-0336e56b03b9}

```js
const arr = [10, 20, 30, 40];

const result = arr.slice(1, 3);

console.log(result); // [20, 30]
console.log(arr);    // [10, 20, 30, 40]
```

`slice(start, end)` 的特点：

- 包含 `start` 索引。
- 不包含 `end` 索引。
- 不修改原数组。
- `end` 可以省略，表示截取到末尾。
- 支持负索引。

```text
arr.slice(-2); // [30, 40]
```

### 4.2 concat：合并数组 {#kaj-h-fd627eaa-ef4c-4136-bf78-49d777590de1}

```js
const a = [1, 2];
const b = [3, 4];

const result = a.concat(b);

console.log(result); // [1, 2, 3, 4]
```

`concat()` 不修改原数组，返回合并后的新数组。

### 4.3 join：数组转字符串 {#kaj-h-5b056996-f706-405f-8fd8-b796e1f65ebb}

```js
const arr = ['Vue', 'React', 'Node'];

console.log(arr.join('-'));
// Vue-React-Node
```

如果不传分隔符，默认使用逗号。

## 五、遍历与转换：forEach、map、flat、flatMap {#kaj-h-d293e41c-ea27-4294-a303-7820d7b50c6a}

这类方法在前端业务开发中使用频率很高。

### 5.1 forEach：遍历数组 {#kaj-h-f5c9000a-5a16-40e5-a314-44b9f0004cf3}

```js
const arr = [1, 2, 3];

arr.forEach((item, index) => {
    console.log(index, item);
});
```

特点：

- 用于执行回调操作。
- 返回值始终是 `undefined`。
- 不会因为调用本身而修改原数组。
- 不能直接使用 `break` 终止遍历。

### 5.2 map：映射成新数组 {#kaj-h-6ddb9983-4d18-4db7-aefe-893360a28551}

```js
const arr = [1, 2, 3];

const result = arr.map(item => item * 2);

console.log(result); // [2, 4, 6]
```

特点：

- 收集回调函数的返回值。
- 返回一个新数组。
- 常用于接口数据转换、提取属性和生成组件列表数据。

### 5.3 flat：数组扁平化 {#kaj-h-49b81dc6-d8a4-4149-a2c2-65b1866e9845}

```js
const arr = [1, [2, [3, 4]]];

console.log(arr.flat());    // [1, 2, [3, 4]]
console.log(arr.flat(2));   // [1, 2, 3, 4]
console.log(arr.flat(Infinity)); // [1, 2, 3, 4]
```

默认只扁平化一层。

### 5.4 flatMap：映射后扁平化一层 {#kaj-h-716d25ce-bc00-4209-b388-d90593020e89}

```js
const arr = [1, 2, 3];

const result = arr.flatMap(item => [item, item * 2]);

console.log(result);
// [1, 2, 2, 4, 3, 6]
```

可以理解为先执行 `map()`，再执行 `flat(1)`。

## 六、查找元素：find、findIndex、indexOf、includes {#kaj-h-a6c4ebfc-90a6-493a-9823-cb47c8d7095d}

| 方法 | 返回值 | 用途 |
| --- | --- | --- |
| `find()` | 找到的元素，未找到返回 `undefined` | 查找符合条件的第一个元素 |
| `findIndex()` | 找到的索引，未找到返回 `-1` | 查找符合条件元素的索引 |
| `indexOf()` | 元素索引，未找到返回 `-1` | 查找指定值 |
| `includes()` | `true` 或 `false` | 判断是否包含指定值 |
| `lastIndexOf()` | 最后一次出现的位置，未找到返回 `-1` | 从后向前查找指定值 |

示例：

```js
const nums = [10, 20, 30, 20];

nums.find(item => item > 15);      // 20
nums.findIndex(item => item > 15); // 1
nums.indexOf(20);                  // 1
nums.includes(30);                 // true
nums.lastIndexOf(20);              // 3
```

面试易错点：

```js
const arr = [1, 2, 3];

arr.find(item => item > 10);      // undefined
arr.findIndex(item => item > 10); // -1
arr.indexOf(10);                  // -1
arr.includes(10);                 // false
```

`find()` 返回的是元素本身，而 `findIndex()` 返回的是索引。

## 七、条件判断：some 和 every {#kaj-h-e5212a93-6e12-41e0-9eff-a7ed5d377405}

### 7.1 some：至少一个元素满足条件 {#kaj-h-4bcea86f-fe41-4af3-bbfc-db0ecdd79c6d}

```js
const arr = [1, 3, 5, 8];

const result = arr.some(item => item % 2 === 0);

console.log(result); // true
```

只要有一个元素满足条件，就返回 `true`。

### 7.2 every：所有元素都满足条件 {#kaj-h-1df8c110-d1ff-4f65-8dd3-ae8c99d72354}

```js
const arr = [2, 4, 6];

const result = arr.every(item => item % 2 === 0);

console.log(result); // true
```

只要有一个元素不满足条件，就返回 `false`。

特别注意： 空数组调用 `some()` 返回 `false`，调用 `every()` 返回 `true`。

## 八、数组筛选与计算：filter 和 reduce {#kaj-h-7c6a5c5f-bf46-47a4-a6f7-d51a1c7f963a}

### 8.1 filter：筛选元素 {#kaj-h-8f06f62c-ec10-4249-b21e-266586749d02}

```js
const arr = [1, 2, 3, 4, 5];

const result = arr.filter(item => item > 3);

console.log(result); // [4, 5]
```

`filter()` 返回一个新数组，其中包含所有满足条件的元素。

### 8.2 reduce：归约计算 {#kaj-h-54a7ee33-a10c-4a11-80d2-fb16e2efde57}

语法：

```js
arr.reduce((accumulator, currentValue, index, array) => {
    return nextAccumulator;
}, initialValue);
```

其中：

- `accumulator`：上一次回调返回的累积结果。
- `currentValue`：当前元素。
- `initialValue`：初始累积值。

例如，计算数组总和：

```js
const arr = [1, 2, 3, 4];

const sum = arr.reduce((acc, cur) => {
    return acc + cur;
}, 0);

console.log(sum); // 10
```

执行过程：

| 当前元素 `cur` | 原累积值 `acc` | 新累积值 |
| --- | --- | --- |
| 1 | 0 | 1 |
| 2 | 1 | 3 |
| 3 | 3 | 6 |
| 4 | 6 | 10 |

`reduce()` 不仅能求和，还可以用于统计频次、分组、数组转对象等操作。

例如统计元素出现次数：

```js
const arr = ['A', 'B', 'A', 'C', 'B', 'A'];

const counts = arr.reduce((acc, item) => {
    acc[item] = (acc[item] || 0) + 1;
    return acc;
}, {});

console.log(counts);
// { A: 3, B: 2, C: 1 }
```

建议调用 `reduce()` 时明确提供初始值，这样更容易理解，也能避免空数组在没有初始值时抛出异常。

## 九、排序与反转：sort 和 reverse {#kaj-h-60459399-7f56-42fe-ad7f-980f9750e90e}

### 9.1 sort：排序 {#kaj-h-1d3ea896-06ab-460f-9938-50f9f09efcf0}

`sort()` 会修改原数组，并返回排序后的原数组。

```js
const arr = [10, 2, 30];

arr.sort();

console.log(arr); // [10, 2, 30]
```

这里容易误解：默认排序会把元素转换成字符串，再按 UTF-16 码元顺序比较，因此不能直接用于一般的数字升序排序。

数字升序：

```js
const arr = [10, 2, 30];

arr.sort((a, b) => a - b);

console.log(arr); // [2, 10, 30]
```

数字降序：

```js
arr.sort((a, b) => b - a);
```

### 9.2 reverse：反转 {#kaj-h-da7ac7bd-308c-4349-8343-983124f45bb2}

```js
const arr = [1, 2, 3];

arr.reverse();

console.log(arr); // [3, 2, 1]
```

`reverse()` 会修改原数组。

如果不希望修改原数组，可以使用：

```js
const arr = [1, 2, 3];

const result = arr.toReversed();

console.log(result); // [3, 2, 1]
console.log(arr);    // [1, 2, 3]
```

## 十、创建与转换：Array.from、Array.of、fill {#kaj-h-35be224b-19f3-44d5-a966-000d97225887}

### 10.1 Array.from：将可迭代对象或类数组对象转换为数组 {#kaj-h-ed9009e3-832c-484d-a6a8-119ca6028613}

```text
Array.from('hello');
// ['h', 'e', 'l', 'l', 'o']

Array.from(new Set([1, 2, 2, 3]));
// [1, 2, 3]

Array.from({ 0: 'a', 1: 'b', length: 2 });
// ['a', 'b']
```

还可以同时进行映射：

```js
Array.from([1, 2, 3], item => item * 2);
// [2, 4, 6]
```

### 10.2 Array.of：根据参数创建数组 {#kaj-h-394e7f11-fe7f-4eec-a2e6-26322104ce21}

```text
Array.of(3);       // [3]
Array.of(1, 2, 3); // [1, 2, 3]
```

与之对比：

```text
Array(3);    // [空槽 × 3]
Array.of(3); // [3]
```

`Array(3)` 创建的是长度为 3 的稀疏数组，而 `Array.of(3)` 创建的是只包含数字 `3` 的数组。

### 10.3 fill：填充数组 {#kaj-h-fbb2c8d8-205c-4dd8-b70a-4476565691f0}

```js
const arr = new Array(3).fill(0);

console.log(arr); // [0, 0, 0]
```

可以指定填充范围：

```js
const arr = [1, 2, 3, 4];

arr.fill(0, 1, 3);

console.log(arr); // [1, 0, 0, 4]
```

注意：`fill()` 会修改原数组。如果填充的是对象，同一个对象引用会被重复填入。

```js
const arr = new Array(3).fill({ count: 0 });

arr[0].count = 1;

console.log(arr);
// 三个位置引用的是同一个对象，count 都变成 1
```

如果需要三个独立对象，可以使用：

```js
const arr = Array.from({ length: 3 }, () => ({ count: 0 }));
```

## 十一、迭代器方法：keys、values、entries {#kaj-h-485ad022-ac85-41da-a56d-ecfdce2de9dc}

这三个方法返回迭代器，而不是普通数组。

```js
const arr = ['a', 'b', 'c'];

console.log([...arr.keys()]);
// [0, 1, 2]

console.log([...arr.values()]);
// ['a', 'b', 'c']

console.log([...arr.entries()]);
// [[0, 'a'], [1, 'b'], [2, 'c']]
```

它们分别用于遍历索引、值和索引值对。

例如：

```js
const arr = ['Vue', 'React'];

for (const [index, value] of arr.entries()) {
    console.log(index, value);
}
```

## 十二、现代数组方法：不修改原数组的替代方案 {#kaj-h-8872e7ab-21dd-48ed-982c-9d30dfbc9365}

现代 JavaScript 提供了几种非破坏性方法，适合在不想直接修改原数组时使用。

| 方法 | 作用 | 类似的传统写法 |
| --- | --- | --- |
| `toSorted()` | 返回排序后的新数组 | `[...arr].sort()` |
| `toReversed()` | 返回反转后的新数组 | `[...arr].reverse()` |
| `toSpliced()` | 返回执行插入、删除或替换后的新数组 | `[...arr]` 后再 `splice()` |
| `with(index, value)` | 返回替换指定索引后的新数组 | 复制数组后修改指定位置 |

示例：

```js
const arr = [1, 2, 3];

const a = arr.with(1, 100);
const b = arr.toReversed();
const c = arr.toSpliced(1, 1);

console.log(a); // [1, 100, 3]
console.log(b); // [3, 2, 1]
console.log(c); // [1, 3]
console.log(arr); // [1, 2, 3]
```

这些方法都返回新数组，不会直接修改原数组。使用前要确认运行环境支持它们。

## 十三、前端面试高频对比 {#kaj-h-868cb7a3-2895-429f-990a-39cdf02a70bd}

| 对比 | 核心区别 |
| --- | --- |
| `slice` vs `splice` | `slice` 截取且不修改原数组；`splice` 增删改且修改原数组 |
| `map` vs `forEach` | `map` 返回映射结果数组；`forEach` 返回 `undefined` |
| `find` vs `filter` | `find` 返回第一个符合条件的元素；`filter` 返回所有符合条件的元素组成的数组 |
| `find` vs `findIndex` | 一个返回元素，一个返回索引 |
| `some` vs `every` | `some` 判断至少一个满足；`every` 判断全部满足 |
| `indexOf` vs `includes` | 一个返回索引或 `-1`；一个返回布尔值 |
| `sort` vs `toSorted` | 前者修改原数组；后者返回排序后的新数组 |
| `Array.from` vs `Array.of` | 前者转换可迭代或类数组对象；后者根据参数创建数组 |
| `push` vs `concat` | `push` 修改原数组；`concat` 返回合并后的新数组 |

## 十四、学习顺序建议 {#kaj-h-e7056c17-3223-4a59-9248-2305ec05a8a1}

如果是为了前端面试，建议按以下顺序掌握：

1. 第一优先级： `map`、`forEach`、`filter`、`reduce`、`find`、`some`、`every`。
2. 第二优先级： `slice`、`splice`、`push`、`pop`、`shift`、`unshift`。
3. 第三优先级： `sort`、`reverse`、`concat`、`includes`、`indexOf`。
4. 第四优先级： `Array.from`、`Array.of`、`flat`、`flatMap`、迭代器方法。
5. 补充了解： `toSorted`、`toReversed`、`toSpliced`、`with`。

最终要形成的思维方式是：先判断要遍历、查找、筛选、转换还是修改数组，再选择合适的方法；同时明确它是否修改原数组、返回什么值，以及是否会提前结束遍历。
