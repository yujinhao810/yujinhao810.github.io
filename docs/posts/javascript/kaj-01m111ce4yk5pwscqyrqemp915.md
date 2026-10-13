---
title: "px、em、rem 的区别及使用场景"
description: "px 是 CSS 中常用的绝对长度单位。"
date: "2026-08-27"
publishedAt: "2026-08-27T15:19:24.048192+08:00"
source: "https://kajspace.cn/articles/01M111CE4YK5PWSCQYRQEMP915/"
tags: ["前端"]
---

# px、em、rem 的区别及使用场景

#### 1. px：绝对长度单位 {#kaj-h-cebf2a1d-04ec-44fa-9406-03243211d64c}

`px` 是 CSS 中常用的绝对长度单位。

```text
.box {
  width: 200px;
  font-size: 16px;
}
```

它不会因为父元素字体大小变化而自动变化。

但是要注意：

> **px 并不是“页面大小变化就完全不会变”。**

例如 CSS 中的 `1px` 是一个 CSS 像素，它和设备物理像素不是简单的 1:1 关系，在不同设备的设备像素比（DPR）下会有不同表现。

所以面试时不要说：

> px 一旦设置就无法因为页面大小而改变。

更准确的是：

> **px 本身是固定的长度单位，不会根据父元素或根元素的字体大小进行计算。**

---

#### 2. em：相对单位 {#kaj-h-9cbe7a6e-9f8f-4dd8-90ef-6773cc19e77c}

`em` 是相对于**当前元素的字体大小**计算的。

例如：

```text
.parent {
  font-size: 20px;
}

.child {
  font-size: 2em;
  width: 10em;
}
```

对于 `child`：

```text
font-size: 2em
→ 2 × 父元素字体大小
→ 2 × 20px
→ 40px
```

但是这里有一个非常容易搞错的地方：

> `em` **不一定永远是相对于父元素。**

对于 `font-size` 属性：

```text
.child {
  font-size: 2em;
}
```

它参考的是**父元素的** `font-size`。

而对于其他属性：

```text
.child {
  width: 10em;
  padding: 2em;
  margin: 1em;
}
```

通常参考的是**当前元素自己的** `font-size`。

例如：

```text
.child {
  font-size: 20px;
  width: 10em;
}
```

那么：

```text
width = 10 × 20px = 200px
```

所以你原来的：

> em 是相对于其父元素来设置字体大小

这个说法**只适用于** `font-size` **的计算，不能概括所有** `em`**。**

---

#### 3. rem：相对于根元素 {#kaj-h-f45f656e-33ad-4517-95d6-6c7839901cfa}

`rem` 是 `root em`，相对于根元素 `<html>` 的 `font-size`。

例如：

```text
html {
  font-size: 16px;
}

.box {
  width: 10rem;
}
```

那么：

```text
10rem = 10 × 16px = 160px
```

无论 `.box` 的父元素字体大小是多少，都不会影响这个 `10rem`。

所以 `rem` 相比 `em` 的一个优势就是：

> **参考标准统一，避免了多层嵌套导致的尺寸计算复杂问题。**
> 
> ![正文图片](/images/kajspace/dabc5069ae7c30e7.png)
> 
> ## 使用场景 {#kaj-h-f9fb473c-afa3-40d2-8fe7-fafe04fb562b}
> 
> 
> 
> ### px {#kaj-h-a69474a1-0672-4ea6-bd47-f5f036a2b934}
> 
> 
> 
> 适合：
> 
> 
> 
> - 边框
> - 图标尺寸
> - 一些不希望随着字体缩放而变化的固定尺寸
> - 对尺寸要求比较明确的场景

### em {#kaj-h-e53a22df-4804-483f-bf2a-0feba5a211b3}

适合：

> **需要随着当前字体大小一起缩放的组件。**

例如一个按钮：

```text
.button {
  font-size: 16px;
  padding: 0.5em 1em;
}
```

如果字体变成：

```text
font-size: 20px;
```

那么 padding 也会跟着变化。

这种情况下 `em` 很方便。

### rem {#kaj-h-4407c1da-6fa8-45a0-bc91-344f87ed8dda}

`rem` 比较适合：

> **需要统一控制尺寸，并且希望根据根元素字体大小进行整体缩放的场景。**

例如：

```text
html {
  font-size: 16px;
}

.title {
  font-size: 2rem;
}

.container {
  width: 20rem;
}
```

如果通过媒体查询等方式改变：

```text
html {
  font-size: 20px;
}
```

那么：

```text
2rem → 40px
20rem → 400px
```

整个页面可以按照统一比例进行缩放。
