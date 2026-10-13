---
title: "Vue Diff算法原理"
description: "Diff 算法的核心目的就是："
date: "2026-09-14"
publishedAt: "2026-09-14T16:17:04.240725+08:00"
source: "https://kajspace.cn/articles/01M2FF8STH30YMMG6PD91R3DW7/"
tags: ["前端"]
---

# Vue Diff算法原理

### Diff 算法的原理 {#kaj-h-e0abc3b4-9ed9-4468-996b-e883ade6593b}

Diff 算法的核心目的就是：

> **对比新旧虚拟 DOM，找出最小的变化，并只更新发生变化的部分，从而提高页面更新效率。**

其基本流程可以概括为：

```text
新旧虚拟 DOM 对比
        ↓
判断节点是否相同
        ↓
   ┌────┴────┐
   ↓         ↓
不同节点    相同节点
   ↓         ↓
直接替换   patchVnode
             ↓
       对比子节点
             ↓
      updateChildren
             ↓
      同层级节点比较
             ↓
       找到可复用节点
             ↓
      移动 / 新增 / 删除
```

#### 1. 判断新旧节点是否相同 {#kaj-h-3bda8eab-1dd1-47a4-8ab6-b2bcaffad8a0}

首先比较新旧虚拟 DOM 的节点。

如果不是同一个节点：

```text
旧节点
  ↓
删除

新节点
  ↓
创建
```

直接用新节点替换旧节点。

如果是相同节点，则进入下一步。

#### 2. patchVnode {#kaj-h-5e7464e5-79b9-4937-89c7-e1dfe6fbc2bd}

如果新旧节点相同，则不需要重新创建整个 DOM，而是继续比较节点内部的数据和子节点。

```text
相同节点
   ↓
patchVnode
   ↓
比较属性、文本、children
```

其中子节点的比较是 Diff 算法的核心。

#### 3. 判断子节点情况 {#kaj-h-2b16ad8b-f04d-49cd-8efa-4ad330f19561}

主要分为几种情况：

```text
旧节点无 children
新节点有 children
→ 创建新 children


旧节点有 children
新节点无 children
→ 删除旧 children


新旧节点都有 children
→ updateChildren
```

当新旧 `children` 都存在多个节点时，就进入核心的 Diff 比较。

#### 4. updateChildren {#kaj-h-61cee5aa-9291-416b-8a54-308d1069cac0}

`updateChildren` 主要负责：

> **对新旧子节点进行同层级比较，尽可能复用已有节点。**

例如：

```text
旧 children：

A  B  C


新 children：

B  A  D
```

Diff 会尝试找到可以复用的节点：

```text
B → 复用
A → 复用
C → 删除
D → 新增
```

而不是把整个列表全部删除后重新创建。

---

### Diff 算法最重要的特点 {#kaj-h-24f8c69b-3f7c-4ece-ae0e-4980fb815088}

**只进行同层级比较，不进行跨层级比较。**

例如：

```text
旧：

      A
     / \
    B   C


新：

      A
       \
        B
```

Diff 不会去大量寻找：

> “B 是不是从原来的第二层移动到了第一层？”

而是按照同层级进行比较。

这样可以大幅减少比较次数。

O(1)O(log n)O(n)O(n log n)O(n²)O(2ⁿ)n=4:(1,log2​n,n)=(1,2,4)(nlog2​n,n2)=(8,16)2n=16n4816326448163264提供反馈

---

### 一句话总结 {#kaj-h-b0112110-d1a8-4744-bb04-52ad3beac30b}

> **Vue 的 Diff 算法会先比较新旧节点是否相同，不同则直接替换，相同则通过 patchVnode 继续比较其内容和子节点。当新旧节点都有多个子节点时，通过 updateChildren 进行同层级比较，尽可能复用已有节点，并根据比较结果执行节点的新增、删除和移动，从而减少真实 DOM 的更新。**

### 面试版 {#kaj-h-ec808dd6-3e9f-4fab-bc1c-8df1272c04e8}

如果面试官问 **“Vue 的 Diff 算法原理是什么？”**，可以直接回答：

> Vue 的 Diff 算法主要用于比较新旧虚拟 DOM。首先判断新旧节点是否为同一节点，如果不同就直接替换，如果相同则通过 patchVnode 继续比较节点内容和子节点。当新旧节点都有多个子节点时，会进入 updateChildren，对新旧 children 进行同层级比较，通过复用、移动、新增和删除节点，尽可能减少真实 DOM 操作。它主要采用同层比较的策略，不进行跨层级比较，从而降低比较的复杂度。
