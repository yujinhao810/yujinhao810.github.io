---
title: "54. 螺旋矩阵"
description: "这道题首先想到的是维护 上、下、左、右四个边界变量，分别用 top、bottom、left、right 表示当前还没有遍历的区域。"
date: "2026-08-26"
publishedAt: "2026-08-26T12:17:04.565335+08:00"
source: "https://kajspace.cn/articles/01M0Y3MRR3NFESPN1YZY322E0H/"
tags: ["算法"]
---

# 54. 螺旋矩阵

![正文图片](/images/kajspace/2e6984253bb19c5b.png)

这道题首先想到的是维护 **上、下、左、右四个边界变量**，分别用 `top`、`bottom`、`left`、`right` 表示当前还没有遍历的区域。

然后按照 **top → right → bottom → left** 的顺序依次遍历，每遍历完一条边，就收缩对应的边界。由于这个过程会不断重复，所以可以在四个 `for` 循环外套一个 `while (true)`。

每遍历完一条边，就更新对应的边界，并判断边界是否发生交叉。如果交叉，说明当前区域已经没有元素可以继续遍历，就通过 `break` 跳出 `while` 循环，最后返回 `ans`。

需要注意的是，**遍历完 top 行之后应该是** `++top`**，而不是** `--top`。因为 `top` 表示上边界，遍历完当前上边界后，需要向下移动一行：

```js
if (++top > bottom) break;
```

也就是：

```text
遍历 top 行
   ↓
top 向下移动一格
   ↓
判断 top 是否超过 bottom
   ↓
如果超过，说明没有剩余区域
   ↓
break
```

整体思路可以概括为：

> **维护四个边界 → 按上、右、下、左依次遍历 → 每遍历完一条边就收缩对应边界 → 判断边界是否交叉 → 交叉则结束，否则继续遍历下一圈。**
> 
> ![正文图片](/images/kajspace/0364670d76df9e76.png)
