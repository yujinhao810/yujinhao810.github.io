---
title: "CSS水平垂直居中"
description: "可以把这几种方案按照**“实现原理 + 是否需要固定宽高 + 推荐程度”**来记。"
date: "2026-08-28"
publishedAt: "2026-08-28T11:26:02.296627+08:00"
source: "https://kajspace.cn/articles/01M136E8EX92QYJA9NCDEHQFFY/"
tags: ["前端"]
---

# CSS水平垂直居中

可以把这几种方案按照\*\*“实现原理 + 是否需要固定宽高 + 推荐程度”\*\*来记。

| 方案 | 核心原理 | 是否需要固定宽高 | 推荐度 |
| --- | --- | --- | --- |
| **绝对定位 + transform** | `top/left: 50%` 定位左上角，再 `translate(-50%, -50%)` 拉回自身一半 | ❌ 不需要 | ⭐⭐⭐⭐⭐ |
| **绝对定位 + 四边 0 + margin:auto** | 上下左右都为 0，剩余空间由 `margin:auto` 平分 | ✅ 需要 | ⭐⭐⭐⭐ |
| **绝对定位 + 负 margin** | `top/left:50%` 定位到中心，再用负 `margin` 移动自身一半 | ✅ 需要 | ⭐⭐⭐ |
| **Flex** | 父元素通过 `justify-content:center` + `align-items:center` 直接让子元素居中 | ❌ 不需要 | ⭐⭐⭐⭐⭐ |

### 1. 最常用：absolute + transform {#kaj-h-7e3252ce-95e8-42aa-89d9-874748476ed6}

```text
.parent {
  position: relative;
}

.child {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
```

记忆：

> **先把左上角放到中心，再把自己往左、往上移动自身的一半。**

最大优点是**不知道子元素宽高也可以居中**。

---

### 2. absolute + `top/right/bottom/left: 0` + `margin: auto` {#kaj-h-8dd16284-2598-48ca-97a4-603aed60e3f8}

```text
.child {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
}
```

可以理解成：

> 上下左右都贴住父元素，然后浏览器把剩余空间平均分给 `margin`。

这种方式一般要求元素有明确的宽高。

---

### 3. absolute + 负 margin {#kaj-h-2081ddee-5f02-4307-95ae-c42b6f9c17e2}

```text
.child {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100px;
  height: 100px;
  margin-left: -50px;
  margin-top: -50px;
}
```

原理和第一种非常像：

> `top:50%; left:50%` → 左上角到中心  
>   
> `margin` 负值 → 向左、向上移动自身的一半

缺点是**必须知道宽高**，而且宽高变化时还要修改 margin。

---

### 4. Flex：现在开发中非常常用 {#kaj-h-17bde1c9-9d6f-4c97-a277-90f95648dbe2}

```text
.parent {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

这里一定要记住：

- `justify-content`：**主轴方向**居中
- `align-items`：**交叉轴方向**居中

默认 `flex-direction: row` 时：

- `justify-content: center` → **水平居中**
- `align-items: center` → **垂直居中**

所以两者一起就是水平垂直居中。

---

### 面试可以直接这么总结 {#kaj-h-d8b070c7-ad65-4382-a6f8-ad1c9f84cf1f}

> **水平垂直居中常见有四种方式：**
> 
> 
> 
> 1. **absolute + transform**：`top:50%; left:50%`，再通过 `transform: translate(-50%, -50%)` 修正自身尺寸，不需要知道元素宽高。
> 2. **absolute + 四边为 0 + margin:auto**：利用剩余空间平均分配实现居中，一般需要元素有明确宽高。
> 3. **absolute + 负 margin**：先通过 `top/left:50%` 定位到中心，再通过负 margin 移动自身宽高的一半，需要知道元素宽高。
> 4. **Flex**：父元素设置 `display:flex`，通过 `justify-content:center` 和 `align-items:center` 实现，是现代开发中比较常用的方式。

**最值得你重点记住的是：**

> `absolute + transform`：**移动自己的中心点**  
>   
> `absolute + margin:auto`：**让剩余空间平均分配**  
>   
> `absolute + 负margin`：**移动自己的固定一半**  
>   
> `flex`：**直接控制子元素的对齐方式**
