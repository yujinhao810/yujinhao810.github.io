---
title: "Flex布局"
description: "Flex（弹性布局）是一种一维布局模型，通过主轴和交叉轴控制子元素的排列、对齐、换行以及空间分配"
date: "2026-08-28"
publishedAt: "2026-08-28T11:45:06.633579+08:00"
source: "https://kajspace.cn/articles/01M137H4FGMZBDZ5K6YGPFNTXB/"
tags: ["前端"]
---

# Flex布局

**Flex（弹性布局）是一种一维布局模型，通过主轴和交叉轴控制子元素的排列、对齐、换行以及空间分配**

核心关系可以记成：

```text
父元素：Flex Container
        │
        ├── flex-direction → 决定主轴方向
        ├── flex-wrap      → 决定是否换行
        ├── justify-content → 主轴对齐
        ├── align-items     → 交叉轴对齐
        └── align-content   → 多行之间的交叉轴对齐

子元素：Flex Item
        │
        ├── order       → 排列顺序
        ├── flex-grow   → 有剩余空间时怎么放大
        ├── flex-shrink → 空间不足时怎么缩小
        ├── flex-basis  → 分配空间前的基础大小
        ├── flex        → 上面三个的简写
        └── align-self  → 单独修改自己的交叉轴对齐
```

## 一、先搞懂 Flex 最核心的两个概念：主轴和交叉轴 {#kaj-h-290a0bbb-570d-4550-a23d-14fb62d109ce}

默认：

```text
.container {
    display: flex;
}
```

默认相当于：

```text
flex-direction: row;
```

所以：

```text
主轴 main axis
────────────────────────→

┌─────────────────────────────┐
│  A     B     C              │
└─────────────────────────────┘
            │
            ↓
       交叉轴 cross axis
```

### `flex-direction` {#kaj-h-bc4c1e1d-d31e-4424-b53b-15313e0c035c}

决定**主轴方向**：

```text
flex-direction: row;            /* 默认，左 → 右 */
flex-direction: row-reverse;    /* 右 → 左 */
flex-direction: column;         /* 上 → 下 */
flex-direction: column-reverse; /* 下 → 上 */
```

这里特别容易犯一个错误：

> `justify-content` 不是永远控制水平，`align-items` 也不是永远控制垂直。

它们实际上是：

> **justify-content → 主轴**  
>   
> **align-items → 交叉轴**

比如：

```text
flex-direction: column;
```

这时候：

```text
主轴 ↓
     A
     B
     C

交叉轴 →
```

所以此时：

```text
justify-content: center;
```

变成了**垂直居中**。

这是面试很喜欢问的点。

## 二、容器上的属性重点掌握 5 个 {#kaj-h-18088592-9256-48c1-ae5a-177cde9283d2}

### ① `flex-direction` {#kaj-h-40bdbd7b-14a4-4089-80e2-fbb1ce330386}

> **决定主轴方向。**

```text
flex-direction: row;
```

---

### ② `flex-wrap` {#kaj-h-51c05e35-7565-4c46-8717-50d1964d295b}

> **一行放不下时要不要换行。**

```text
flex-wrap: nowrap; /* 默认，不换行 */
flex-wrap: wrap;   /* 换行 */
```

例如：

```text
nowrap：

A B C D E F
────────────────
   超出容器


wrap：

A B C
D E F
```

---

### ③ `justify-content` {#kaj-h-83e972c6-c243-463d-b84e-6da51c01a7e2}

> **控制项目在主轴上的对齐方式。**

常见：

```text
justify-content: flex-start;
justify-content: center;
justify-content: flex-end;
justify-content: space-between;
justify-content: space-around;
justify-content: space-evenly;
```

例如：

```text
space-between

A        B        C
```

两端没有间距，中间平均分配。

---

### ④ `align-items` {#kaj-h-d9de7955-ef6a-4a9a-a1e9-add054057c9b}

> **控制项目在交叉轴上的对齐方式。**

最常见：

```text
align-items: center;
```

比如默认 `row`：

```text
┌─────────────────────┐
│                     │
│    A   B   C        │
│                     │
└─────────────────────┘
          ↑
      垂直居中
```

所以你之前学的**水平垂直居中**：

```text
.parent {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

本质就是：

> 默认主轴是水平 → `justify-content` 水平居中  
>   
> 交叉轴是垂直 → `align-items` 垂直居中

---

### ⑤ `align-content` {#kaj-h-96b29a42-b836-4606-9431-013f32ec3a70}

这个和 `align-items` **非常容易混淆**。

记住：

> `align-items`：**一行里面，项目怎么对齐**  
>   
> `align-content`：**多行之间怎么对齐**

所以：

```text
flex-wrap: wrap;
```

产生多行以后，`align-content` 才有明显作用。

## 三、项目上的属性 {#kaj-h-211591c8-00c3-4a9c-a593-fa43c808679e}

最重要的是：

```text
order
flex
align-self
```

以及 `flex` 内部的：

```text
flex-grow
flex-shrink
flex-basis
```

---

## ① `order` {#kaj-h-b16ba65a-c119-4f9b-a811-edf73a0a4ffe}

控制排列顺序：

```text
.item {
    order: 1;
}
```

默认：

```text
order: 0;
```

**数字越小越靠前。**

例如：

```text
A: order 0
B: order 2
C: order 1
```

最终：

```text
A C B
```

## 四、重点：`flex-grow / flex-shrink / flex-basis` {#kaj-h-292a9451-23e5-4325-a9f0-03edef96aff5}

这三个建议你重点理解，因为面试很容易问。

## `flex-grow` {#kaj-h-490e26cc-984d-433f-a07d-e6a54e9c3e2e}

> **有剩余空间时，我要不要变大，以及变大多少。**

例如父元素：

```text
500px
```

两个子元素：

```text
A = 100px
B = 100px
```

还有：

```text
500 - 100 - 100 = 300px
```

如果：

```text
A {
    flex-grow: 1;
}

B {
    flex-grow: 2;
}
```

剩余的 300px 按：

```text
1 : 2
```

分配。

所以：

```text
A 得 100px
B 得 200px
```

最终：

```text
A = 200px
B = 300px
```

---

## `flex-shrink` {#kaj-h-7fd87121-3533-48cf-a6b9-dd38536cb79d}

和 `grow` 正好相反：

> **空间不够的时候，我缩小多少。**

例如父元素只有：

```text
300px
```

两个子元素原本：

```text
A = 200px
B = 200px
```

总共：

```text
400px
```

但是只有：

```text
300px
```

所以需要缩小。

默认：

```text
flex-shrink: 1;
```

表示允许缩小。

## 五、`flex-basis` 到底是什么？ {#kaj-h-c30a7326-2d99-4e92-8ea3-11a82dd00f41}

你可以把它理解成：

> **在计算 grow/shrink 之前，项目的“基础尺寸”。**

例如：

```text
.item {
    flex-basis: 200px;
}
```

如果主轴是水平的，就可以简单理解成：

> 先把这个元素的基础宽度看成 200px，然后再考虑剩余空间怎么分配。

所以：

```text
flex-basis
    ↓
先确定基础尺寸
    ↓
计算有没有剩余空间/空间不足
    ↓
grow / shrink
```

## 六、重点：`flex: 1` 到底是什么？ {#kaj-h-81d695d5-738f-4290-a221-813c4a5918d6}

这是面试**非常高频**的问题。

```text
.item {
    flex: 1;
}
```

可以理解为：

```text
flex: 1 1 0%;
```

也就是：

```text
flex-grow   = 1
flex-shrink = 1
flex-basis  = 0%
```

最重要的含义：

> **让多个 Flex 子元素按照相同的比例瓜分剩余空间。**

例如：

```text
.left {
    flex: 1;
}

.right {
    flex: 1;
}
```

父元素：

```text
1000px
```

那么两个元素最终基本各占：

```text
500px
```

如果：

```text
.left {
    flex: 1;
}

.right {
    flex: 2;
}
```

就可以理解为：

```text
1 : 2
```

最终：

```text
left  ≈ 333px
right ≈ 667px
```

## 七、`flex: 1` 和 `width: 50%` 不完全一样 {#kaj-h-bcc5c871-ee0e-4e68-949b-8d0901995757}

比如：

```text
.left {
    flex: 1;
}

.right {
    flex: 1;
}
```

这种写法特别适合：

> **两栏等分、三栏等分、剩余空间填充。**

例如：

```text
┌─────────────────────────────┐
│           │                 │
│   left    │      right      │
│   flex:1  │      flex:1     │
│           │                 │
└─────────────────────────────┘
```

而：

```text
width: 50%;
```

只是直接规定：

> 宽度是父容器的 50%。

Flex 更强调的是：

> **参与 Flex 容器的空间分配。**

---

## 八、`align-self` {#kaj-h-ec2d2307-d36f-4adf-8a59-8f86b088e776}

这个很好理解：

父元素：

```text
.container {
    align-items: center;
}
```

所有子元素都垂直居中。

但我突然想让其中一个：

```text
.item {
    align-self: flex-start;
}
```

那么这个元素就可以**覆盖父元素的** `align-items`。

所以记：

> `align-items`：统一控制所有项目  
>   
> `align-self`：单独控制某一个项目

---

## 九、最终建议你把 Flex 记成这张图 {#kaj-h-acd5ba17-6fc3-4562-9de3-72bf3a849f95}

```text
                    Flex
                     │
             display: flex
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
       容器属性                项目属性
          │                     │
   ┌──────┼──────┐       ┌──────┼────────┐
   ↓      ↓      ↓       ↓      ↓        ↓
direction wrap  对齐     order   flex    align-self
                 │               │
          ┌──────┼──────┐        │
          ↓      ↓      ↓        │
       justify  align  align     │
       content  items  content   │
                                 │
                         ┌───────┼───────┐
                         ↓       ↓       ↓
                       grow   shrink   basis
```

### 面试最核心的记忆口诀 {#kaj-h-5c2174bb-6eb7-4868-a888-18d2c217817d}

> **容器管排列，项目管自身。**
> 
> 
> 
> 容器：
> 
> 
> 
> - `flex-direction` → **主轴方向**
> - `flex-wrap` → **是否换行**
> - `justify-content` → **主轴对齐**
> - `align-items` → **交叉轴对齐**
> - `align-content` → **多行的交叉轴对齐**
> 
> 
> 
> 项目：
> 
> 
> 
> - `order` → **顺序**
> - `flex-grow` → **空间多了怎么长**
> - `flex-shrink` → **空间少了怎么缩**
> - `flex-basis` → **基础尺寸**
> - `flex` → **grow + shrink + basis**
> - `align-self` → **单独修改自己的交叉轴对齐**

最后，`flex: 1` **一定单独记住**：

> `flex: 1` ≈ `flex: 1 1 0%`，表示项目可以放大、可以缩小，并以 `0%` 作为基础尺寸，多个 `flex:1` 的项目会共同分配可用空间。
