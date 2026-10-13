---
title: "46. 全排列"
description: "题目："
date: "2026-09-03"
publishedAt: "2026-09-03T11:07:58.398486+08:00"
source: "https://kajspace.cn/articles/01M1JKSAFGCZM3SH7HTE6PPJVK/"
tags: ["算法"]
---

# 46. 全排列

![正文图片](/images/kajspace/5add14a484fab52b.png)

## 全排列问题：回溯算法总结 {#kaj-h-8d6f10ee-9cf6-4600-8905-2f8403c2bf3b}

题目：

```text
nums = [1, 2, 3]
```

要求得到：

```text
[
    [1,2,3],
    [1,3,2],
    [2,1,3],
    [2,3,1],
    [3,1,2],
    [3,2,1]
]
```

---

## 一、核心思路 {#kaj-h-4eade174-6590-49ee-ae35-5a37e244e506}

全排列的本质是：

> **每一个位置都从“还没有使用过的数字”中选择一个。**

例如：

```text
第 0 个位置 → 选择一个数字
第 1 个位置 → 再选择一个没用过的数字
第 2 个位置 → 再选择一个没用过的数字
```

所以可以把整个过程看成一棵**决策树**：

```text
                 []
          /       |       \
         1        2        3
       /   \    /   \    /   \
      2     3  1     3  1     2
      |     |  |     |  |     |
      3     2  3     1  2     1
```

---

## 二、递归函数到底传什么参数？ {#kaj-h-b35d8b2f-af6a-4c92-95b1-539a4383b1a5}

这是你目前最需要熟练的地方。

我们定义：

```text
dfs(depth)
```

其中：

> `depth` **表示当前正在确定** `path` **的第几个位置。**

例如：

```text
dfs(0)
```

表示：

```text
正在确定 path[0]
```

然后选择一个数字以后：

```text
dfs(depth + 1)
```

进入下一层：

```text
dfs(1)
```

表示：

```text
正在确定 path[1]
```

所以：

```text
dfs(0)
  ↓
确定 path[0]

dfs(1)
  ↓
确定 path[1]

dfs(2)
  ↓
确定 path[2]

dfs(3)
  ↓
所有位置都确定了
```

---

## 三、什么时候 push 到 ans？ {#kaj-h-3eb5212b-5bdc-47d6-a321-75047b50cba6}

这是这道题**最关键的判断条件**。

如果：

```js
depth === n
```

说明：

```text
path[0]
path[1]
path[2]
...
path[n - 1]
```

全部已经确定。

也就是说：

> **当前** `path` **已经形成了一个完整的排列。**

所以：

```js
if (depth === n) {
    ans.push([...path]);
    return;
}
```

注意你刚才说：

> depth 等于 n 时，超出了数组长度

这个理解**稍微修正一下**。

不是说：

> “超出了数组长度”

而是：

> `depth === n` **表示已经完成了前面** `n` **个位置的选择，因此排列已经构造完成。**

例如：

```text
nums.length = 3

path：
下标 0 → 已确定
下标 1 → 已确定
下标 2 → 已确定

depth = 3
```

此时虽然 `path[3]` 确实不存在，但**我们根本不是要访问** `path[3]`。

`depth === n` 实际上是一个：

> **递归终止条件 / 叶子节点判断。**

---

## 四、每一次递归到底干什么？ {#kaj-h-d0d2c6e8-f023-4db0-be73-9cd0ef143fb1}

每一次 `dfs(depth)` 都只做一件核心事情：

> **确定** `path[depth]` **应该放哪个数字。**

例如：

```js
for (let i = 0; i < n; i++) {
    if (!onPath[i]) {
        path[depth] = nums[i];
        onPath[i] = true;

        dfs(depth + 1);

        onPath[i] = false;
    }
}
```

拆开：

### ① 尝试选择一个数字 {#kaj-h-4fc13e65-867a-4946-a2c3-1eef5bbccba0}

```text
path[depth] = nums[i];
```

例如：

```text
path[0] = 1
```

---

### ② 标记这个数字已经使用 {#kaj-h-c2066996-3b03-45c2-bd8b-9e0570faaac8}

```text
onPath[i] = true;
```

防止后面的递归再次使用这个数字。

---

### ③ 递归进入下一层 {#kaj-h-08f6b8fa-f257-4c32-a12d-c2a83423427f}

```text
dfs(depth + 1);
```

意思：

> 当前这个位置已经确定了，现在去确定下一个位置。

---

### ④ 回溯 {#kaj-h-b9aac31d-e267-4853-b983-0cf276dc07c8}

```text
onPath[i] = false;
```

意思：

> 刚才选择的数字我不要了，把它恢复成“未使用”，然后尝试其他数字。

---

## 五、所以整个算法可以浓缩成这句话 {#kaj-h-e85ae4af-f40e-4ff2-a003-7550c0263d8f}

> **每层递归负责确定一个位置，每次从未使用的数字中选择一个，选择后递归进入下一层；当** `depth === n` **时，说明所有位置都已经确定，当前** `path` **是一个完整排列，将其复制后加入** `ans`**；递归返回后撤销选择，继续尝试其他数字。**

这个就是你这道题最应该掌握的算法思想。

---

## 六、标准代码 {#kaj-h-b617debb-c8ce-4cf1-a935-d2d969d3afc8}

```js
var permute = function(nums) {
    const n = nums.length;
    const path = Array(n);
    const onPath = Array(n).fill(false);
    const ans = [];

    function dfs(depth) {
        // 所有位置都确定，得到一个完整排列
        if (depth === n) {
            ans.push([...path]);
            return;
        }

        // 尝试把每一个未使用的数字放到当前位置
        for (let i = 0; i < n; i++) {
            if (!onPath[i]) {
                // 做选择
                path[depth] = nums[i];
                onPath[i] = true;

                // 递归确定下一个位置
                dfs(depth + 1);

                // 撤销选择
                onPath[i] = false;
            }
        }
    }

    dfs(0);

    return ans;
};
```

---

## 七、你以后遇到回溯题，可以按照这 5 个问题想 {#kaj-h-ce76531f-937a-44c7-a929-ba8da3b79489}

这个非常重要，建议你以后**不要一上来就写代码**，先问自己：

```text
① 一层递归代表什么？
       ↓
② 当前这一层我要做什么选择？
       ↓
③ 选择之后进入哪一层？
       ↓
④ 什么情况下说明答案已经完成？
       ↓
⑤ 返回之后要撤销什么选择？
```

对于这道全排列：

```js
① 一层递归
→ 确定一个位置

② 当前选择
→ 从没使用过的数字中选一个

③ 递归
→ dfs(depth + 1)

④ 终止条件
→ depth === n

⑤ 回溯
→ onPath[i] = false
```

你现在其实已经**理解回溯的核心了**，目前不熟练的主要是把“递归参数、终止条件、选择/撤销”这几个固定模块写出来。

可以把它进一步记成一个万能框架：

```js
dfs(当前状态)
    ↓
判断是否到达终点
    ↓
是 → 保存答案 → return
    ↓
否
    ↓
遍历所有可能的选择
    ↓
做选择
    ↓
dfs(下一个状态)
    ↓
撤销选择
    ↓
尝试下一个选择
```
