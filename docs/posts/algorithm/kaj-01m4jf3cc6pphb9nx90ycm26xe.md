---
title: "LeetCode 19. 删除链表的倒数第 N 个结点"
description: "给定一个链表的头节点 head 和一个整数 n，删除链表的倒数第 n 个节点，并返回链表的头节点。"
date: "2026-10-10"
publishedAt: "2026-10-10T16:33:05.647565+08:00"
source: "https://kajspace.cn/articles/01M4JF3CC6PPHB9NX90YCM26XE/"
tags: ["算法"]
---

# LeetCode 19. 删除链表的倒数第 N 个结点

<span id="kaj-h-33169135-10cf-4673-af5b-909ceb9addb9"></span>

## 一、题目描述 {#kaj-h-346d0c2e-41c2-45e7-83cd-aa0a53dd734e}

给定一个链表的头节点 `head` 和一个整数 `n`，删除链表的倒数第 `n` 个节点，并返回链表的头节点。

示例：

```text
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
```

## 二、解题思路：快慢指针 + 哑节点 {#kaj-h-24793761-b623-4166-846f-7e953300d778}

使用快慢指针，让两个指针之间保持固定的距离，从而在一次遍历中找到待删除节点的前一个节点。

### 1. 为什么需要哑节点？ {#kaj-h-54cf5a56-9711-4978-92e2-44325acaf8fe}

创建一个虚拟头节点 `dummy`，让它指向原链表头节点：

```text
dummy → 1 → 2 → 3 → 4 → 5 → null
```

哑节点可以统一处理删除头节点的情况，避免额外判断。

### 2. 为什么 `fast` 先走 `n + 1` 步？ {#kaj-h-455768fd-17b5-4937-b71d-521d70eefa04}

让 `fast` 和 `slow` 都从 `dummy` 出发。

- `fast` 先走 `n + 1` 步。
- 然后 `fast` 和 `slow` 同时向后移动。
- 当 `fast === null` 时，`slow` 正好指向待删除节点的前一个节点。

这里先走 `n + 1` 步，是因为我们要找到**待删除节点的前一个节点**，而不是待删除节点本身。

### 3. 如何删除节点？ {#kaj-h-d03ed013-d34a-451a-8703-13c192a0136d}

找到待删除节点的前一个节点后，执行：

```text
slow.next = slow.next.next;
```

这行代码将前一个节点直接连接到待删除节点的下一个节点，从而跳过待删除节点。

如果删除的是最后一个节点，那么 `slow.next.next` 就是 `null`，因此前一个节点的 `next` 会被设置为 `null`。

## 三、JavaScript 代码 {#kaj-h-a882cca2-fd76-4058-8db7-977d884832b9}

```js
var removeNthFromEnd = function(head, n) {
    const dummy = new ListNode(0, head);

    let fast = dummy;
    let slow = dummy;

    // fast 先走 n + 1 步
    for (let i = 0; i < n + 1; i++) {
        fast = fast.next;
    }

    // 快慢指针同步移动
    while (fast) {
        fast = fast.next;
        slow = slow.next;
    }

    // 删除倒数第 n 个节点
    slow.next = slow.next.next;

    return dummy.next;
};
```

## 四、代码执行过程 {#kaj-h-d2910f1e-e06e-4417-a566-071b30b5fc70}

以 `head = [1,2,3,4,5]，n = 2` 为例。

**第一步：初始化并移动快指针**

```text
dummy → 1 → 2 → 3 → 4 → 5 → null
                         ↑
                        fast
↑
slow
```

`fast` 从 `dummy` 出发，先走 3 步，到达节点 `2`。

**第二步：快慢指针同步移动**

当 `fast` 到达 `null` 时：

```text
dummy → 1 → 2 → 3 → 4 → 5 → null
                   ↑    ↑
                  slow fast（已到 null）
```

此时 `slow` 指向节点 `3`，它是待删除节点 `4` 的前一个节点。

**第三步：删除节点**

```text
slow.next = slow.next.next;
```

节点 `3` 直接连接节点 `5`，最终得到：

```text
1 → 2 → 3 → 5 → null
```

**第四步：返回真正的头节点**

```js
return dummy.next;
```

因为 `dummy` 只是辅助节点，所以返回 `dummy.next`，而不是返回 `dummy`。

## 五、复杂度分析 {#kaj-h-5016135c-31b1-44da-8851-5629fdee36ce}

- **时间复杂度：** ，其中 是链表长度。快指针和慢指针总共只遍历常数次链表。
- **空间复杂度：** ，只使用了几个指针，没有创建与链表长度相关的额外空间。

## 六、易错点总结 {#kaj-h-7807e957-f46b-4ff0-acd1-4316f00d6261}

1. **快指针先走** `n + 1` **步。** 两个指针从 `dummy` 出发，才能让慢指针最终停在待删除节点的前一个位置。
2. **删除节点时使用** `slow.next = slow.next.next`**。** 不需要移动节点，只需要修改指针连接关系。
3. **返回** `dummy.next`**。** 如果删除的是原链表头节点，真正的头节点会发生变化。
4. **删除最后一个节点不需要特殊判断。** 此时 `slow.next.next` 为 `null`，自然就能正确断开最后一个节点。
5. **不要将** `fast` **初始化为** `head` **后直接照搬这套步数。** 指针起点不同，快指针先走的步数也可能不同，要根据指针间距重新推导。

## 七、核心记忆 {#kaj-h-cc7d15e5-d0a7-40b8-9413-ee340e2d9971}

这道题的关键是：**哑节点统一边界情况，快慢指针保持** `n + 1` **个节点的间距，找到待删除节点的前一个节点，再通过修改** `next` **完成删除。**
