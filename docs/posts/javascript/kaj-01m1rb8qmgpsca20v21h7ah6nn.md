---
title: "如何原生实现轮播图？"
description: "一个最简单的原生轮播图，本质上就是："
date: "2026-09-05"
publishedAt: "2026-09-05T16:34:27.147389+08:00"
source: "https://kajspace.cn/articles/01M1RB8QMGPSCA20V21H7AH6NN/"
tags: ["前端"]
---

# 如何原生实现轮播图？

一个最简单的原生轮播图，本质上就是：

> **定时器 + 当前图片索引 + 切换图片。**

例如有：

```js
const images = [
  '1.jpg',
  '2.jpg',
  '3.jpg'
]
```

维护一个：

```js
let index = 0
```

每隔 2 秒：

```js
setInterval(() => {
  index++

  if (index >= images.length) {
    index = 0
  }

  img.src = images[index]
}, 2000)
```

就可以实现最简单的自动轮播。

---

### 如果要实现真正的“滑动” {#kaj-h-c6be746e-c6ef-4ffd-97d1-515f93fc5428}

例如：

```text
┌─────┬─────┬─────┐
│  1  │  2  │  3  │
└─────┴─────┴─────┘
        ←
```

可以把图片横向排列：

```text
.wrapper {
  width: 500px;
  overflow: hidden;
}

.container {
  display: flex;
  transition: transform 0.3s;
}

.container img {
  width: 500px;
  flex-shrink: 0;
}
```

然后通过：

```js
let index = 0

setInterval(() => {
  index++

  container.style.transform =
    `translateX(-${index * 500}px)`
}, 2000)
```

不断改变 `transform`。

所以你面试时可以这样答：

> 原生实现轮播图，我会维护一个当前图片的索引，通过 `setInterval` 定时切换索引，然后修改图片 `src`；如果需要实现滑动效果，可以将多张图片横向排列，通过 `transform: translateX()` 配合 `transition` 实现动画，同时还需要处理左右切换、首尾循环、圆点指示器以及定时器清除等逻辑。

这个回答已经比较完整了。
