---
title: "236. 二叉树的最近公共祖先"
description: "这是理解这道题最重要的一点。"
date: "2026-09-09"
publishedAt: "2026-09-09T18:43:21.301984+08:00"
source: "https://kajspace.cn/articles/01M22W5R8T9HR37QV5ZPP8MXQX/"
tags: ["算法"]
---

# 236. 二叉树的最近公共祖先

![正文图片](/images/kajspace/2cbffe51d6eba460.png)

## 1. 先理解递归函数“返回什么” {#kaj-h-e133fe5d-f218-45c1-a647-321cc93be184}

这是理解这道题最重要的一点。

```text
lowestCommonAncestor(root, p, q)
```

这个函数返回的不是简单的 `true / false`，而是：

> **在以** `root` **为根的这棵子树中，如果找到了** `p` **或** `q`**，就返回找到的那个节点；如果** `root` **本身就是** `p` **或** `q`**，就直接返回它；如果什么都没找到，返回** `null`**。**

所以可以把递归函数理解成：

```text
“帮我在这棵子树里找 p 和 q，
找到一个就把那个节点告诉我。”
```

---

## 2. 第一部分：递归终止条件 {#kaj-h-6fd6fe78-ca1b-4b86-b28f-6f2b0a3df5ff}

```js
if(root === null || root === p || root === q) {
    return root;
}
```

有三种情况：

### 情况一：走到空节点 {#kaj-h-a39b2d9c-b47c-4f37-876e-840798401556}

```js
root === null
```

说明这条路走到底了，没有找到目标：

```js
return null
```

---

### 情况二：当前节点就是 p {#kaj-h-5d0eb230-4e0f-45e3-a4e3-21d1a7069371}

```js
root === p
```

直接返回：

```text
p
```

---

### 情况三：当前节点就是 q {#kaj-h-3703179a-7cba-4529-b2f2-a4fc84bdd4a7}

同理：

```js
return q
```

所以这一句可以理解成：

> **如果当前节点没了，返回 null；如果当前节点就是目标节点，直接把目标节点返回给上一层。**

---

## 3. 递归向左右子树寻找 {#kaj-h-8d9cf72c-e94c-4969-9606-dfa806e5b2d9}

```js
const left = lowestCommonAncestor(root.left, p, q);
const right = lowestCommonAncestor(root.right, p, q);
```

这里非常关键。

当前节点 `root` 会问自己的左右子树：

```text
左子树：你那里有没有 p 或 q？
右子树：你那里有没有 p 或 q？
```

然后得到：

```text
left
right
```

---

## 4. `left` 和 `right` 到底代表什么？ {#kaj-h-f2fe5b09-1a31-4119-8cae-5aa5141064da}

假设：

```text
left = p
```

意思是：

> **左子树里面找到了 p。**

如果：

```text
right = q
```

意思是：

> **右子树里面找到了 q。**

那么：

```js
if(left && right) {
    return root;
}
```

就意味着：

```text
        root
       /    \
      p      q
```

或者更复杂：

```text
          root
         /    \
       ...    ...
       p       q
```

此时 `p` 和 `q` 分别出现在 `root` 的左右两边。

所以：

> **root 就是最近公共祖先。**

---

## 5. 为什么 `left && right` 就能确定 root 是答案？ {#kaj-h-c4947ac4-fb31-49ab-a811-011b0af7ac11}

这是整个算法最核心的地方。

例如：

```text
          3
        /   \
       5     1
      / \   / \
     6   2 0   8
```

寻找：

```text
p = 6
q = 2
```

在节点 `5`：

```text
        5
       / \
      6   2
```

递归：

```text
left = 6
right = 2
```

所以：

```js
if(left && right)
```

成立。

于是：

```js
return 5;
```

节点 `5` 就是最近公共祖先。

---

## 6. 如果只有一边找到呢？ {#kaj-h-218a1acd-0408-4a4f-8682-897230bf753a}

假设：

```text
          3
        /   \
       5     1
      / \
     6   2
```

寻找：

```text
p = 6
q = 1
```

对于根节点 `3`：

```text
左子树 → 找到了 6
右子树 → 找到了 1
```

所以：

```text
left = 6
right = 1
```

最终：

```js
return root;
```

返回 `3`。

---

但如果当前节点是 `5`：

```text
        5
       / \
      6   2
```

寻找 `6` 和 `1`：

```text
left = 6
right = null
```

这时候：

```js
if(left && right)
```

不成立。

于是执行：

```js
return left ?? right;
```

得到：

```text
6
```

也就是说：

> **如果左右只有一边找到目标，就把找到的那个结果继续向上传递。**

---

## 7. `return left ?? right` 是什么意思？ {#kaj-h-13176bac-8bb7-4239-9668-35cfeb5a32d3}

```js
return left ?? right;
```

等价于：

```js
if(left !== null && left !== undefined) {
    return left;
}

return right;
```

也就是：

```text
左边找到了 → 返回左边
左边没找到 → 返回右边
```

例如：

```text
left  = p
right = null
```

返回：

```text
p
```

或者：

```text
left  = null
right = q
```

返回：

```text
q
```

如果：

```text
left  = null
right = null
```

返回：

```text
null
```

---

## 8. 整个递归过程可以理解成“信息向上汇报” {#kaj-h-86d95517-a306-48af-ade5-9e16e1829ceb}

这是我比较推荐你理解这类递归题的方式。

假设：

```text
             3
           /   \
          5     1
         / \   / \
        6   2 0   8
```

寻找：

```text
p = 6
q = 2
```

递归会一直向下：

```text
3
├── 5
│   ├── 6 → 返回 6
│   └── 2 → 返回 2
└── 1
    ├── 0 → null
    └── 8 → null
```

然后节点 `5` 收到：

```text
left  = 6
right = 2
```

发现：

```text
left && right
```

于是：

```text
5 → “我就是最近公共祖先”
```

返回：

```text
5
```

然后 `5` 的结果继续向上传递给 `3`。

---

## 9. 最重要的递归关系 {#kaj-h-4ffda84c-8538-407d-865e-65bdb7a38331}

你可以把整个算法浓缩成下面这个逻辑：

```text
当前节点 root
      ↓
是不是 null / p / q？
      ↓
    是 → 返回 root
      ↓
    否
      ↓
去左子树找 → left
去右子树找 → right
      ↓
 ┌───────────────┐
 │               │
left && right    只有一边找到
 │               │
 ↓               ↓
root         返回找到的那一边
```

所以代码：

```js
const left = lowestCommonAncestor(root.left, p, q);
const right = lowestCommonAncestor(root.right, p, q);

if(left && right) {
    return root;
}

return left ?? right;
```

其实就是：

> **左边找到一个，右边找到一个 → 当前节点是公共祖先。**

> **只有左边找到 → 把左边的结果继续往上交。**

> **只有右边找到 → 把右边的结果继续往上交。**

> **两边都没找到 → 返回 null。**

---

## 10. 一句话记忆这个递归 {#kaj-h-46c5bbf3-fea1-416f-a203-4b11eb1f3430}

面试时可以这样说：

> **递归遍历左右子树，让左右子树分别返回是否找到** `p` **或** `q`**。如果左右子树都返回非空，说明两个目标节点分别位于当前节点两侧，因此当前节点就是最近公共祖先；如果只有一侧非空，就将这一侧的结果继续向上返回。**

你真正需要掌握的不是这几行代码，而是这个**递归返回值的含义**：

**“我这棵子树有没有找到 p/q？如果找到了，把找到的节点交给我的父节点。”**

这也是二叉树递归题里非常常见的“**子问题向父问题返回信息**”的思维。

![正文图片](/images/kajspace/421cd404dbfe9180.png)
