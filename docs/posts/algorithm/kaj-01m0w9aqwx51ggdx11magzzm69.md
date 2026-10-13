---
title: "JS算法题：根据权限过滤菜单树，并处理父子节点的依赖关系。"
description: "const menus = ["
date: "2026-08-25"
publishedAt: "2026-08-25T19:04:41.452897+08:00"
source: "https://kajspace.cn/articles/01M0W9AQWX51GGDX11MAGZZM69/"
tags: ["算法"]
---

# JS算法题：根据权限过滤菜单树，并处理父子节点的依赖关系。

`const menus = [`

`  {`

`    id: 1,`

`    name: "系统管理",`

`    permission: true,`

`    children: [`

`      { id: 2, name: "用户管理", permission: true },`

`      { id: 3, name: "角色管理", permission: false }`

`    ]`

`  },`

`  {`

`    id: 4,`

`    name: "数据管理",`

`    permission: false,`

`    children: [`

`      { id: 5, name: "数据列表", permission: true }`

`    ]`

`  }`

`];`

**要求：**

> 没有权限的菜单删除；如果父级没有权限，那么整个父级及其子菜单都删除。

> 这是一个树形结构的递归过滤问题。对于每个菜单节点，先判断当前节点是否有权限；如果没有权限，直接返回 false，整个子树都会被过滤掉。如果有权限，再递归处理 children，最终返回过滤后的菜单树。
> 
> 
> 
> **递归写法：**
> 
> ![正文图片](/images/kajspace/48db1b2e300b8892.png)

> 这道题本质上是一个树形结构的递归遍历。`filter()` 负责决定当前菜单节点是否保留：没有权限就返回 `false`，有权限就最终返回 `true`。对于有权限且存在 `children` 的节点，由于 `children` 本身仍然是和顶层菜单相同结构的菜单数组，因此可以**递归调用**同一个 `filterMenus` 函数，对子菜单进行同样的权限过滤。最后返回 `true` 是为了告诉 `filter()` 当前节点本身有权限，需要保留。
