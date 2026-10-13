---
title: "Vue2和Vue3的响应式区别"
description: "Vue 2 的响应式基于 Object.defineProperty，需要递归遍历对象的已有属性，并为每个属性分别定义 getter/setter，因此无法直接监听属性的新增、删除，以及数组索引和 length 的变化，只能通过 $set、"
date: "2026-08-13"
publishedAt: "2026-08-13T16:34:29.927376+08:00"
source: "https://kajspace.cn/articles/01KZX44273V6PEMS39YKK9KC8F/"
tags: ["前端"]
---

# Vue2和Vue3的响应式区别

**Vue 2 的响应式基于** `Object.defineProperty`**，需要递归遍历对象的已有属性，并为每个属性分别定义 getter/setter，因此无法直接监听属性的新增、删除，以及数组索引和 length 的变化，只能通过** `$set`**、**`$delete` **和重写数组方法等方式弥补。**

**Vue 3 使用** `Proxy` **代理整个对象，通过拦截对象的 get、set、delete 等操作实现响应式，不需要初始化时递归遍历所有属性，并且嵌套对象采用惰性代理，因此解决了 Vue 2 的一些响应式限制。**

**Vue 2 是「给每个属性装监控器」，Vue 3 是「给整个对象装代理」。**

什么是 **getter/setter ？**

getter 和 setter 是描述属性访问和修改行为的概念，而 get/set 是 JavaScript 中定义 getter 和 setter 的语法关键字。Vue2 基于 Object.defineProperty 重写对象属性，通过 getter 收集依赖，通过 setter 派发更新，所以通常称为 getter/setter 响应式。

把Proxy和Vue响应式串起来：

![正文图片](/images/kajspace/7604028abe03c2ea.png)
