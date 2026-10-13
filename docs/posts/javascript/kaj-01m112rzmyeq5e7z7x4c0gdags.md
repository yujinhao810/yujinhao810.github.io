---
title: "CSS双栏布局"
description: "双栏布局的实现可以分为四种：浮动 + 外边距、浮动 + BFC、flex布局、绝对定位"
date: "2026-08-27"
publishedAt: "2026-08-27T15:45:15.492048+08:00"
source: "https://kajspace.cn/articles/01M112RZMYEQ5E7Z7X4C0GDAGS/"
tags: ["前端"]
---

# CSS双栏布局

双栏布局的实现可以分为四种：**浮动 + 外边距、浮动 + BFC、flex布局、绝对定位**

## 1. 第一种：`float + margin-left` {#kaj-h-04c9b365-6005-446d-8be7-988cb89960e0}

核心代码：

```text
.left {
    width: 200px;
    float: left;
}

.right {
    margin-left: 200px;
}
```

### 第一步：左边浮动 {#kaj-h-785a8963-5995-4581-ac9e-5081daa787e9}

```text
.left {
    width: 200px;
    float: left;
}
```

`float: left` 会让 `.left` **脱离普通文档流**，并向左浮动。

可以理解成：

```text
正常文档流：

┌──────────────────────┐
│ left                 │
├──────────────────────┤
│ right                │
└──────────────────────┘
```

变成：

```text
left 脱离普通文档流
↓
┌────────┐
│  left  │
│ 200px  │
└────────┘
```

然后 `.right` 仍然按照普通文档流布局。

### 第二步：`margin-left: 200px` {#kaj-h-51985cb1-93b4-41a9-8fa3-d03ca4f142b1}

```text
.right {
    margin-left: 200px;
}
```

因为左边已经占据了左侧 `200px` 的视觉空间，所以给右边：

```text
margin-left: 200px;
```

相当于告诉右边：

> **你从左边 200px 的位置开始布局。**

最终：

```text
┌────────────┬─────────────────┐
│    left    │      right      │
│   200px    │    剩余空间      │
└────────────┴─────────────────┘
```

## 2. 第二种：`float + BFC` {#kaj-h-1e277fcf-c656-4302-a83b-6b200ab7d1c2}

代码：

```text
.left {
    width: 200px;
    float: left;
}

.right {
    overflow: hidden;
}
```

这里和第一种最大的区别是：

> **右侧没有设置** `margin-left: 200px`**。**

那它为什么还能自动跑到右边？

关键就是：

```text
.right {
    overflow: hidden;
}
```

它会让 `.right` **形成 BFC**。

---

## BFC 在这里解决了什么？ {#kaj-h-0752d972-0bdf-42a8-9480-6905e1f3e068}

浮动元素：

```text
┌────────┐
│  left  │
│ float  │
└────────┘
```

普通块级元素可能会认为：

> 左边这个浮动元素不在正常文档流里，我的盒子还是可以占满整行。

但是 BFC 有一个非常重要的特性：

> **BFC 区域不会与浮动元素重叠。**

所以：

```text
          left
        ┌──────┐
        │      │
        └──────┘
             \
              \  right BFC
               ┌─────────────────┐
               │                 │
               │      right      │
               │                 │
               └─────────────────┘
```

浏览器发现：

```text
left 占了 200px
```

于是 `.right` 这个 BFC 就会自动避开左边的浮动元素，使用剩余空间。

最终：

```text
┌────────────┬──────────────────┐
│    left    │       right      │
│   200px    │      剩余空间     │
└────────────┴──────────────────┘
```

所以第二种的核心是：

> **左边 float，右边通过建立 BFC 避开浮动元素，从而占据剩余空间。**
> 
> 
> 
> ## 第三种：Flex {#kaj-h-99e60e09-89ba-431a-b7c2-7b934d9f8ff3}
> 
> 
> 
> 这是现在开发中最推荐、也最好理解的方式之一。

> ```text
> .container {
>     display: flex;
> }
> 
> .left {
>     width: 200px;
> }
> 
> .right {
>     flex: 1;
> }
> ```
> 
> 
> 
> 这里就非常直接了。
> 
> 
> 
> ---
> 
> 
> 
> ## `display: flex` {#kaj-h-84e79290-b14a-4205-94d4-25ab25c84211}

> ```text
> .container {
>     display: flex;
> }
> ```
> 
> 
> 
> 把父元素变成 Flex 容器：

> ```text
> container
>     ↓
> ┌──────────────────────────────┐
> │                              │
> │       Flex 容器               │
> │                              │
> └──────────────────────────────┘
> ```
> 
> 
> 
> 里面的 `.left` 和 `.right` 成为 Flex 项目。
> 
> 
> 
> 默认主轴方向是：

> ```text
> 左 → 右
> ```
> 
> 
> 
> 所以：

> ```text
> ┌────────────┬──────────────────┐
> │    left    │       right      │
> └────────────┴──────────────────┘
> ```
> 
> 
> 
> ---
> 
> 
> 
> ## `left: width: 200px` {#kaj-h-9bc9e546-af62-4869-9a39-ec165caade18}

> ```text
> .left {
>     width: 200px;
> }
> ```
> 
> 
> 
> 左边占：

> ```text
> 200px
> ```
> 
> 
> 
> ---
> 
> 
> 
> ## `right: flex: 1` {#kaj-h-19a1cd43-d330-4aa4-9f6b-580009a39818}

> ```text
> .right {
>     flex: 1;
> }
> ```
> 
> 
> 
> `flex: 1` 可以简单理解成：
> 
> 
> 
> > **让 right 占据剩余空间，并参与剩余空间的分配。**
> 
> 
> 
> 比如容器宽度：

> ```text
> 1000px
> ```
> 
> 
> 
> 左边：

> ```text
> 200px
> ```
> 
> 
> 
> 那么右边：

> ```text
> 1000 - 200 = 800px
> ```
> 
> 
> 
> 最终：

> ```text
> ┌──────200px──────┬────────800px────────┐
> │       left       │        right        │
> └──────────────────┴────────────────────┘
> ```
> 
> 
> 
> 所以 Flex 的思路最简单：

> **左边固定宽度，右边** `flex: 1` **吃掉剩余空间。**
> 
> 
> 
> ## 第四种：绝对定位 {#kaj-h-fa73c231-7b99-4ee4-9a04-76ed7aa5ac2e}
> 
> 
> 
> 代码：

> ```text
> .container {
>     position: relative;
> }
> 
> .left {
>     width: 200px;
> }
> 
> .right {
>     position: absolute;
>     right: 0;
>     top: 0;
>     left: 200px;
> }
> ```
> 
> 
> 
> 这个思路和前面三种完全不同。
> 
> 
> 
> ---
> 
> 
> 
> ## 第一步：建立定位参考系 {#kaj-h-9c80481c-bced-4fc3-814a-3aec0cd04eea}

> ```text
> .container {
>     position: relative;
> }
> ```
> 
> 
> 
> 意思是：
> 
> 
> 
> > `.container` 成为 `.right` 绝对定位时的参考父元素。
> 
> 
> 
> ---
> 
> 
> 
> ## 第二步：右边脱离文档流 {#kaj-h-a4fda8de-0ed7-4d7f-b480-22b3ec10c717}

> ```text
> .right {
>     position: absolute;
> }
> ```
> 
> 
> 
> `.right` 脱离正常文档流。
> 
> 
> 
> 然后：

> ```text
> left: 200px;
> right: 0;
> top: 0;
> ```
> 
> 
> 
> 这三个条件共同确定了 `.right` 的位置和宽度：

> ```text
> container
> ┌──────────────────────────────┐
> │ ← 200px →│                  │
> │          │      right        │
> │   left   │                  │
> │          │                  │
> └──────────┴──────────────────┘
>            ↑                 ↑
>          left:200px       right:0
> ```
> 
> 
> 
> 也就是说：

> ```text
> right 左边 = container 左边 + 200px
> right 右边 = container 右边
> ```
> 
> 
> 
> 所以：

> ```text
> right width
> = container width - 200px
> ```
> 
> 
> 
> 于是实现右侧自适应。
> 
> 
> 
> 容易遗忘的知识点：哪些定位脱离文档流？
> 
> 
> 
> `relative` 不脱流，留坑位；`absolute` 脱流，坑位没；`fixed` 脱流，跟着视口；`static` 正常流；`sticky` 先正常，滚动后特殊。
