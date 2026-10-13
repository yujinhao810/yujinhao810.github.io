---
title: "CSS三栏布局"
description: "经典的三栏布局："
date: "2026-08-27"
publishedAt: "2026-08-27T16:37:30.780881+08:00"
source: "https://kajspace.cn/articles/01M115VRNM2SFGAKCR9VW9G6Z7/"
tags: ["前端"]
---

# CSS三栏布局

经典的**三栏布局**：

```text
┌──────200px──────┬────── 自适应 ──────┬──────200px──────┐
│      left       │       center       │      right      │
└─────────────────┴────────────────────┴─────────────────┘
```

核心要求：

> **左边固定 200px，中间自适应，右边固定 200px。**

## 方案一：绝对定位 {#kaj-h-91796d6e-7d31-4d24-8071-5307ba954e9d}

```text
.container {
    position: relative;
}

.left {
    position: absolute;
    left: 0;
    top: 0;
    width: 200px;
}

.right {
    position: absolute;
    right: 0;
    top: 0;
    width: 200px;
}

.center {
    position: absolute;
    left: 200px;
    right: 200px;
    top: 0;
}
```

## 核心思路 {#kaj-h-d77a57e2-623c-462e-95b0-1d68578b4d3b}

三个元素都使用绝对定位。

左右两边直接固定：

```text
left:
left: 0
width: 200px

right:
right: 0
width: 200px
```

中间：

```text
left: 200px;
right: 200px;
```

相当于：

> **从左边 200px 开始，到右边 200px 结束。**

所以中间自动占据剩余空间：

```text
container
┌──────────┬──────────────────┬──────────┐
│   left   │      center      │  right   │
│  200px   │      自适应       │  200px   │
└──────────┴──────────────────┴──────────┘
            ↑                ↑
         left:200px       right:200px
```

### 特点 {#kaj-h-01ff822a-925e-4ca5-8649-5e6c9d73e707}

三个元素都：

```text
position: absolute;
```

所以**都脱离文档流**。

这意味着父元素的高度不会自动被这些元素撑开，需要额外处理高度。

## 方案二：Flex {#kaj-h-7e32e32f-eef4-40e6-8332-47ad9e8bef86}

这个是现代开发中非常常见的方案。

```text
.container {
    display: flex;
}

.left {
    width: 200px;
}

.center {
    flex: 1;
}

.right {
    width: 200px;
}
```

## 核心思路 {#kaj-h-44f1dda7-b0ab-45d0-93b3-bfa7f9795e0c}

父元素：

```text
display: flex;
```

让三个元素成为 Flex 项目。

然后：

```text
left    → 200px
center  → flex: 1
right   → 200px
```

假设容器宽度是 `1000px`：

```text
1000 - 200 - 200 = 600
```

所以：

```text
┌────200────┬────────600────────┬────200────┐
│   left    │      center       │   right   │
└───────────┴───────────────────┴───────────┘
```

这里的核心和你前面学习的双栏布局完全一致：

> **固定宽度 +** `flex: 1` **吃掉剩余空间。**

### 这个方案最值得记 {#kaj-h-5ec6bc51-8113-4015-81f8-a873b7d4bd6b}

```text
三栏 Flex：

左：width: 200px
中：flex: 1
右：width: 200px
```

这是实际开发中非常推荐的写法。

## 方案三：Float 浮动 {#kaj-h-844af9f8-20e8-4aaa-8242-180cd2fbf320}

代码：

```text
.left {
    width: 200px;
    float: left;
}

.right {
    width: 200px;
    float: right;
}

.center {
    /* 普通文档流 */
}
```

这里最关键的就是：

```text
left  → float: left
right → float: right
center → 正常文档流
```

最终：

```text
┌──────────┬──────────────────┬──────────┐
│   left   │      center      │  right   │
│  float   │    正常文档流     │  float   │
└──────────┴──────────────────┴──────────┘
```

---

## 为什么中间能自适应？ {#kaj-h-aec1ae49-bc9b-4e4b-b5c1-ecff80fd6086}

因为：

```text
.left {
    float: left;
}

.right {
    float: right;
}
```

左右两个元素分别占据：

```text
左边 200px
右边 200px
```

而 `.center` 是普通块级元素：

```text
.center {
    background-color: darkorange;
}
```

它的宽度默认是：

```text
width: auto;
```

因此它会利用剩余空间。

### 但是这里有一个容易踩的坑 {#kaj-h-17ecda6a-b618-452d-ab70-9f2628c03c6d}

你这个例子中：

```html
<div class="left">...</div>
<div class="right">...</div>
<div class="center">...</div>
```

**顺序很重要。**

通常浮动三栏布局会把：

```text
left
right
center
```

这样排列。

因为需要让左右两个浮动元素先浮到两边，然后中间普通流元素利用剩余空间。

---

### `overflow: hidden` 是干什么？ {#kaj-h-dbb9ddfe-8df8-4e24-bd5c-6cc572dbaaa6}

```text
.container {
    overflow: hidden;
}
```

主要是为了让父容器能够**包含浮动元素的高度**，也就是常说的利用 BFC 清除/包含浮动影响。

所以浮动方案的记忆：

```text
左 → float left
右 → float right
中 → 普通流
父 → 清除/包含浮动
```

这是比较经典的传统 CSS 三栏布局。

## 方案四：Grid {#kaj-h-f1afeda4-332b-48d6-b042-609bcced8570}

```text
.container {
    display: grid;
    grid-template-columns: 200px auto 200px;
}
```

这个其实是四种里面**语义最直接的**。

直接告诉浏览器：

```text
第一列：200px
第二列：auto
第三列：200px
```

所以：

```text
grid-template-columns:
        200px   auto   200px
          ↓       ↓       ↓
        左边    中间    右边
```

假设容器：

```text
1000px
```

那么：

```text
200 + auto + 200 = 1000
```

所以：

```text
auto = 600px
```

最终：

```text
┌────200────┬────────600────────┬────200────┐
│   left    │      center       │   right   │
└───────────┴───────────────────┴───────────┘
```

## 四种方案放一起 {#kaj-h-c6c21389-c3a6-4a18-b27e-72fb6d777273}

| 方案 | 左 | 中 | 右 | 核心 |
| --- | --- | --- | --- | --- |
| **绝对定位** | `absolute + 200px` | `left:200 + right:200` | `absolute + 200px` | 用定位边界确定位置 |
| **Flex** | `width:200px` | `flex:1` | `width:200px` | Flex 分配剩余空间 |
| **Float** | `float:left` | 正常流 | `float:right` | 左右浮动，中间占剩余空间 |
| **Grid** | `200px` | `auto` | `200px` | 直接定义三列宽度 |

## 面试怎么总结？ {#kaj-h-e346b4e4-2f94-4058-884e-a0ba897c6b12}

如果面试官问：

> **“三栏布局有哪些实现方式？”**

你可以这样回答：

> 三栏布局常见有绝对定位、Flex、浮动和 Grid 四种实现方式。绝对定位可以让左右两栏固定在容器两侧，中间通过 `left:200px` 和 `right:200px` 占据剩余空间；Flex 可以设置左右固定 `200px`，中间 `flex:1` 占据剩余空间；传统浮动方案是左右分别 `float:left` 和 `float:right`，中间保持正常文档流；Grid 则可以直接通过 `grid-template-columns: 200px auto 200px` 定义三列。
