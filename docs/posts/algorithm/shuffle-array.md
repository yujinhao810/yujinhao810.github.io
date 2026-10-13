---
title: "384. 打乱数组"
description: 使用 Fisher-Yates 洗牌算法实现均匀随机打乱，并保证 reset 始终恢复原始排列
date: 2026-10-12
publishedAt: "2026-10-12T15:55:01.941492+08:00"
source: "https://kajspace.cn/articles/01M4QHQ4JHD8ZERV1GS2XEEP2J/"
tags:
  - 算法
  - 数组
  - Fisher-Yates
  - JavaScript
---

# 384. 打乱数组

## 一、题目描述

设计一个类 `Solution`，实现以下两个方法：

- `reset()`：将数组恢复为最初的排列，并返回该数组。
- `shuffle()`：将数组随机打乱，并返回打乱后的数组。

每次调用 `shuffle()` 时，都应该基于原始数组进行随机打乱，而不是直接在上一次打乱的结果上继续操作。

```js
const solution = new Solution([1, 2, 3])

solution.shuffle() // 可能返回 [3, 1, 2]
solution.reset()   // 返回 [1, 2, 3]
solution.shuffle() // 可能返回 [2, 3, 1]
```

随机打乱的结果不唯一，上面的排列仅用于说明调用方式。

## 二、解题思路

### 1. 保存原始数组

在构造函数中使用 `slice()` 创建原始数组的副本：

```js
this.original = nums.slice()
```

这样可以保存数组最初的排列，避免后续操作影响原始数据。

### 2. 使用 Fisher-Yates 洗牌算法

Fisher-Yates 算法从数组末尾向前处理，每一步都在还没有固定的位置中随机选择一个元素进行交换。在随机选择均匀的前提下，每一种排列出现的概率相同。

具体步骤如下：

1. 从数组最后一个元素开始，令下标 `i = n - 1`。
2. 在 `0` 到 `i` 之间随机选择一个下标 `j`。
3. 交换 `arr[i]` 和 `arr[j]`。
4. 将 `i` 减一，继续处理前面的元素。
5. 当 `i === 0` 时结束。

```js
for (let i = arr.length - 1; i > 0; i--) {
  const j = Math.floor(Math.random() * (i + 1))
  ;[arr[i], arr[j]] = [arr[j], arr[i]]
}
```

### 3. 为什么随机下标是 `Math.random() * (i + 1)`？

`Math.random()` 返回大于等于 `0` 且小于 `1` 的随机数。因此：

```js
Math.floor(Math.random() * (i + 1))
```

得到的整数范围是：

```text
j ∈ [0, i]
```

这里必须使用 `i + 1`，因为随机范围需要包含下标 `i` 本身。当 `i = 2` 时，`j` 可能是 `0`、`1` 或 `2`，每个位置都有机会被选中。

## 三、JavaScript 完整代码

```js
/**
 * @param {number[]} nums
 */
var Solution = function (nums) {
  this.original = nums.slice()
}

/**
 * 将数组恢复为原始排列
 * @return {number[]}
 */
Solution.prototype.reset = function () {
  return this.original.slice()
}

/**
 * 随机打乱数组
 * @return {number[]}
 */
Solution.prototype.shuffle = function () {
  const arr = this.original.slice()

  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }

  return arr
}
```

## 四、关键代码分析

### `this.original = nums.slice()`

`slice()` 会创建一个新的数组对象。直接赋值只会复制数组引用：

```js
this.original = nums
```

如果之后修改了数组，原始数据也可能受到影响。使用 `slice()` 后，两个变量指向不同的数组对象。对于本题的数字数组，这样的浅拷贝已经足够。

### `const arr = this.original.slice()`

每次调用 `shuffle()` 都从原始排列创建一个新数组，因此可以保证：

- 原始数组始终保持不变。
- 每次打乱都从原始排列开始。
- 连续调用 `shuffle()` 不会在上一次结果上继续打乱。

### `[arr[i], arr[j]] = [arr[j], arr[i]]`

这是 JavaScript 的解构赋值写法，用于交换两个位置的元素：

```js
const arr = [1, 2, 3]
const i = 2
const j = 0

;[arr[i], arr[j]] = [arr[j], arr[i]]
console.log(arr) // [3, 2, 1]
```

它等价于使用临时变量：

```js
const temp = arr[i]
arr[i] = arr[j]
arr[j] = temp
```

### 为什么可以省略 `this.nums = arr`？

有些实现会把打乱后的数组保存到实例属性：

```js
this.nums = arr
return arr
```

本题每次打乱都通过 `this.original.slice()` 创建新数组，后续操作也不依赖当前数组状态，因此不需要额外维护 `this.nums`。`reset()` 同样可以直接返回原始数组的副本：

```js
Solution.prototype.reset = function () {
  return this.original.slice()
}
```

## 五、为什么不能简单地使用 `sort()` 打乱？

常见但不推荐的写法是：

```js
arr.sort(() => Math.random() - 0.5)
```

这种方式虽然简短，但比较函数不满足排序算法所需要的一致比较规则，无法保证所有排列具有相同的概率。不同 JavaScript 引擎和排序实现也可能产生不同的分布。

Fisher-Yates 则通过逐个位置进行随机选择和交换，在理想的均匀随机选择条件下保证排列均匀，时间复杂度也更清晰。

## 六、复杂度分析

设数组长度为 `n`：

| 操作 | 时间复杂度 | 额外空间复杂度 |
| --- | --- | --- |
| 构造函数 | `O(n)` | `O(n)` |
| `reset()` | `O(n)` | `O(n)` |
| `shuffle()` | `O(n)` | `O(n)` |

`shuffle()` 中的循环最多执行 `n - 1` 次，每次只进行常数次操作，因此时间复杂度为 `O(n)`。额外空间主要用于创建数组副本。

## 七、总结

本题主要考查三个知识点：

1. **Fisher-Yates 洗牌算法**：从后向前遍历，每次随机选择一个尚未固定的位置并交换。
2. **数组浅拷贝**：使用 `slice()` 创建新的数组，保护原始排列。
3. **对象属性与返回值的区别**：`this.original` 用于保存原始状态，`return arr` 用于返回计算结果；只有确实需要保存当前状态时，才需要维护 `this.nums`。

面试时可以重点解释：为什么每次打乱都从原始数组开始、随机下标的范围为什么是 `[0, i]`，以及 Fisher-Yates 为什么比随机排序更可靠。
