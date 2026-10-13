---
title: "Vue中key的作用"
description: "key 是 Vue 给 VNode 提供的一个唯一标识。"
date: "2026-09-14"
publishedAt: "2026-09-14T16:18:29.377680+08:00"
source: "https://kajspace.cn/articles/01M2FFXY9TXD8WB9DJ9ZT44JYT/"
tags: ["前端"]
---

# Vue中key的作用

<span id="kaj-h-6d2f6a2f-2d0f-4806-8f45-a5fbee8ce88c"></span>

## 1. key 是什么？ {#kaj-h-89e0ac7d-ad4c-4095-a12a-8c42f99451ef}

`key` 是 Vue 给 VNode 提供的一个**唯一标识**。

例如：

```html
<div v-for="item in list" :key="item.id">
  {{ item.name }}
</div>
```

Diff 算法在比较新旧 VNode 时，会结合 `key` 判断：

> **新旧两个 VNode 是不是代表同一个节点。**

可以简单理解为：

```text
旧 VNode
   ↓
key = 1
   ↓
    Diff
   ↓
新 VNode
   ↓
key = 1

→ 可以认为是同一个节点，优先复用
```

如果：

```text
旧 VNode：key = 1
新 VNode：key = 2

→ 不是同一个节点
→ 不直接复用
```

---

## 2. key 的第一个作用：控制节点复用 {#kaj-h-dfce9972-d324-4705-b305-5fcba0efa7aa}

最经典的场景是 `v-if`。

例如：

```js
<input v-if="type === 'username'">
<input v-else>
```

当 `type` 发生变化时，两个 `input` 的标签类型相同。

Vue 在 Diff 时可能认为：

```text
旧：input
新：input

→ 可以复用
```

因此原来的 DOM 元素可能继续被使用。

如果希望两个 `input` 被认为是完全不同的节点，可以添加不同的 `key`：

```js
<input v-if="type === 'username'" key="username">

<input v-else key="email">
```

此时：

```text
旧：input + key=username
新：input + key=email

→ key 不同
→ 不认为是同一个节点
→ 不复用原来的 DOM
→ 创建新的 input
```

因此：

> **在这种场景下，key 可以用来强制 Vue 区分两个节点。**

例如切换不同输入框时，可以避免复用之前输入框的状态。

---

## 3. key 的第二个作用：帮助列表 Diff {#kaj-h-ded505cb-7fa4-4297-862c-530988cdc8cf}

这是 `key` 最重要的使用场景。

例如：

```html
<div v-for="item in list" :key="item.id">
  {{ item.name }}
</div>
```

假设原来的数据：

```text
A
B
C
```

对应：

```text
key=1 → A
key=2 → B
key=3 → C
```

现在数据变成：

```text
C
A
B
```

如果有 `key`：

```text
旧：

1 → A
2 → B
3 → C


新：

3 → C
1 → A
2 → B
```

Vue 可以通过 `key` 知道：

```text
key=3 → 原来的 C
key=1 → 原来的 A
key=2 → 原来的 B
```

因此可以直接**复用并移动原来的 DOM 节点**。

而不是把整个列表重新创建。

---

## 4. 为什么 key 能提高 Diff 的准确性？ {#kaj-h-72c7826f-2de4-4a68-ba47-96de3afbf7f2}

Diff 的核心之一就是判断：

> 新旧两个 VNode 是否是同一个节点？

可以简单理解为：

```js
旧节点.key === 新节点.key
```

再结合节点类型等条件进行判断。

所以：

```text
key 相同
+
节点类型相同

→ 更有可能是同一个节点
→ 可以复用
```

而：

```text
key 不同

→ 不认为是同一个节点
→ 不进行这种复用
```

所以 `key` 的核心作用可以概括成：

> **帮助 Vue 准确识别节点身份。**

---

## 5. 为什么 key 能提高 Diff 的效率？ {#kaj-h-c7c757a5-710b-4d48-85e9-9d18494544f5}

假设旧列表：

```text
A B C D
```

新列表：

```text
D A B C
```

如果没有稳定的 `key`，Vue 很难知道：

> D 是原来的哪个节点？

而有：

```text
A → key=1
B → key=2
C → key=3
D → key=4
```

Vue 就可以根据 key 快速定位对应节点。

可以简单理解为：

```text
key
 ↓
建立节点映射
 ↓
快速找到对应旧节点
 ↓
复用 / 移动 / 删除 / 创建
```

因此：

> **key 不仅帮助 Vue 判断节点身份，也能够提高列表 Diff 的效率。**

---

## 6. 为什么不建议使用 index 作为 key？ {#kaj-h-efeb273d-d832-4ecb-8d01-0eafd751ce57}

例如：

```html
<div v-for="(item, index) in list" :key="index">
  {{ item.name }}
</div>
```

假设：

```text
旧：

index=0 → A
index=1 → B
index=2 → C
```

现在在头部插入一个 D：

```text
新：

index=0 → D
index=1 → A
index=2 → B
index=3 → C
```

注意：

```text
旧 index=0 → A
新 index=0 → D
```

key 都是：

```text
0
```

Vue 会认为：

```text
旧 key=0
新 key=0

→ 可以复用
```

于是原来属于 A 的 DOM 可能被复用给 D。

接下来：

```text
旧 key=1 → B
新 key=1 → A

旧 key=2 → C
新 key=2 → B
```

也会发生类似情况。

所以：

> **index 不是数据本身稳定的身份标识。**

---

## 7. index 什么时候可以使用？ {#kaj-h-b6b9ac18-e83a-4472-bce2-380e3f67a426}

并不是说 `index` **绝对不能作为 key**。

如果列表满足：

- 列表不会发生排序
- 不会在中间插入数据
- 不会删除数据
- 列表项没有自身状态
- 列表只是简单展示

那么使用：

```text
:key="index"
```

通常不会产生明显问题。

但是在实际开发中，**如果数据本身存在唯一 ID，优先使用 ID。**

例如：

```text
:key="item.id"
```

比：

```text
:key="index"
```

更加可靠。

---

## 8. key 最推荐怎么写？ {#kaj-h-fee34cc3-cc68-4a50-a89b-cfa31231d1c1}

推荐：

```html
<div
  v-for="item in list"
  :key="item.id"
>
  {{ item.name }}
</div>
```

核心原则：

> **key 应该具有稳定性、唯一性和与数据身份的对应关系。**

例如：

```text
用户列表 → user.id
商品列表 → product.id
订单列表 → order.id
```

而不是：

```text
index
随机数
Math.random()
```

尤其不要：

```text
:key="Math.random()"
```

因为每次渲染都会产生新的 key：

```text
第一次：key=123
第二次：key=456

→ Vue 认为是完全不同的节点
→ 无法复用
→ 可能导致大量 DOM 重建
```

---

## 9. 最终总结 {#kaj-h-7f4b319c-a718-4ea6-830a-618d7ed023f2}

可以直接记这一张：

```text
                    Vue key
                       │
          ┌────────────┴────────────┐
          ↓                         ↓
       v-if 场景                 v-for 场景
          ↓                         ↓
   区分不同节点身份          标识列表项身份
          ↓                         ↓
   控制节点是否复用          帮助 Diff 定位节点
                                    ↓
                         复用 / 移动 / 删除 / 创建
```

### 面试回答 {#kaj-h-07668220-da7a-4a7c-b9fd-1c92c6048f2a}

> **key 是 Vue 中 VNode 的唯一标识，主要用于 Diff 算法识别新旧节点的身份。在 v-for 列表中，Vue 可以根据稳定的 key 找到对应的旧节点，从而进行节点复用和移动，避免不必要的 DOM 创建。在 v-if 场景中，不同的 key 可以让 Vue 将两个相同类型的节点识别为不同节点，从而避免不合适的复用。实际开发中一般使用数据本身的唯一 ID 作为 key，不推荐使用 index 作为 key，因为列表发生插入、删除或排序时，index 会发生变化，可能导致节点复用错误。**
