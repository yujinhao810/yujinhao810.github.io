---
title: Vue2 权限控制与动态路由实现，以及 Vue Router 原理解析
category: vue
description: 基于 Vue2、Vue Router 3 与 Vuex，梳理 RBAC、动态路由、导航守卫、菜单和按钮权限，以及 Hash、History 模式的原理与部署配置。
date: "2026-10-27"
publishedAt: "2026-10-27T17:03:03+08:00"
tags:
  - Vue2
  - Vue Router
  - Vuex
  - 权限控制
  - 前端八股
---

# Vue2 权限控制与动态路由实现，以及 Vue Router 原理解析

## 一、前言

在 Vue2 项目中，权限管理和路由控制是后台管理系统中非常重要的功能。例如，管理员可以访问用户管理、角色管理等页面，而普通员工只能访问工作台和业务查询页面。

为了实现这种差异化的访问控制，通常需要结合 Vue Router、Vuex、导航守卫和后端权限接口，完成动态路由加载、菜单权限控制和按钮权限控制。

此外，Vue Router 还提供了 Hash 和 History 两种路由模式。理解它们的实现原理以及对后端部署的要求，有助于解决页面刷新后出现 404 等问题。

本文主要介绍以下内容：

1. Vue2 中如何实现权限控制和动态路由加载。
2. 如何基于 RBAC 模型实现多角色权限管理。
3. 如何控制不同角色的菜单、页面和按钮权限。
4. Vue Router 的核心实现原理。
5. Hash 模式和 History 模式的区别，以及后端需要进行的配置。

本文基于 Vue2、Vue Router 3 和 Vuex 进行讲解。

## 二、Vue2 项目中的权限控制

### 2.1 权限控制的整体思路

一个完整的权限管理系统通常包含身份认证、路由权限、菜单权限、按钮权限和后端接口权限。

**身份认证**：验证用户是否已经登录，通常通过 Token 或 Session 实现。

**路由权限**：控制用户是否能够访问某个页面。

**菜单权限**：控制侧边栏中哪些菜单可以显示。

**按钮权限**：控制用户是否可以执行新增、删除、编辑等操作。

**接口权限**：由后端校验用户是否有权访问数据或执行操作。

整体流程如下：

```text
用户登录
   ↓
获取 Token
   ↓
请求用户信息和权限数据
   ↓
获取用户角色、菜单和权限标识
   ↓
根据权限生成动态路由
   ↓
注册动态路由
   ↓
根据权限渲染菜单和按钮
   ↓
后端再次校验接口权限
```

需要注意，前端权限控制主要用于界面展示和路由导航，真正的安全控制必须由后端实现。

即使前端隐藏了某个按钮，用户仍然可能通过浏览器控制台直接调用接口。因此，后端必须独立校验用户的身份和权限。

### 2.2 静态路由与动态路由

在实际项目中，通常将路由分为静态路由和动态路由。

**静态路由**是所有用户都可以访问的路由，例如登录页、首页框架、无权限提示页等。

**动态路由**是根据用户权限决定是否注册的路由，例如用户管理、角色管理和系统配置等页面。

首先定义静态路由和动态路由。

```js
// router/index.js
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export const constantRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: () => import('@/views/403.vue')
  }
]

export const asyncRoutes = [
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      roles: ['admin', 'user']
    }
  },
  {
    path: '/system/users',
    name: 'UserManagement',
    component: () => import('@/views/system/Users.vue'),
    meta: {
      roles: ['admin']
    }
  },
  {
    path: '/system/roles',
    name: 'RoleManagement',
    component: () => import('@/views/system/Roles.vue'),
    meta: {
      roles: ['admin']
    }
  }
]

const router = new Router({
  mode: 'history',
  routes: constantRoutes
})

export default router
```

这里通过 `meta.roles` 定义每个路由允许访问的角色。

`meta` 是 Vue Router 提供的路由元信息字段，但 `roles` 是开发者自定义的属性，需要自行编写权限判断逻辑。

### 2.3 根据用户角色筛选路由

假设系统中存在管理员和普通员工两种角色：

- 管理员可以访问所有系统管理页面。
- 普通员工只能访问工作台。

可以通过递归筛选路由的方式生成用户有权访问的路由表。

```js
// permission.js
import router, { asyncRoutes } from './router'

function hasPermission(route, roles) {
  if (!route.meta || !route.meta.roles) {
    return true
  }

  return route.meta.roles.some(role =>
    roles.includes(role)
  )
}

function filterRoutes(routes, roles) {
  return routes
    .filter(route => hasPermission(route, roles))
    .map(route => ({
      ...route,
      children: route.children
        ? filterRoutes(route.children, roles)
        : undefined
    }))
}

export function generateRoutes(roles) {
  const accessedRoutes = filterRoutes(
    asyncRoutes,
    roles
  )

  router.addRoutes(accessedRoutes)

  return accessedRoutes
}
```

这里涉及两个核心方法。

**`hasPermission()`**

判断当前路由是否允许用户访问。

使用 `some()` 表示只要用户拥有路由要求的任意一个角色，就可以通过该角色校验。

**`filterRoutes()`**

递归处理路由表，不仅筛选一级路由，也会筛选子路由，适用于具有多级菜单的后台管理系统。

**`router.addRoutes()`**

这是 Vue Router 3 中用于动态添加路由的 API。

需要注意，Vue Router 3 的 `addRoutes()` 和 Vue Router 4 的 `addRoute()` 不同。开发 Vue2 项目时，需要根据实际使用的 Vue Router 版本选择对应的 API。

另外，生产项目还需要处理重复注册、动态路由清理和无权限路由等问题。

## 三、通过导航守卫实现路由权限控制

### 3.1 什么是导航守卫？

Vue Router 提供导航守卫，用于在路由跳转过程中进行检查、重定向或取消导航。

常见的导航守卫包括：

- 全局前置守卫：`router.beforeEach()`
- 全局解析守卫：`router.beforeResolve()`
- 全局后置钩子：`router.afterEach()`
- 路由独享守卫：`beforeEnter`
- 组件内守卫：`beforeRouteEnter`、`beforeRouteUpdate` 和 `beforeRouteLeave`

在权限管理中，最常使用的是全局前置守卫 `beforeEach()`。

### 3.2 实现登录校验和动态路由加载

下面通过一个简化示例说明如何将登录校验与动态路由结合起来。

```js
// permission-guard.js
import router from './router'
import store from './store'
import { generateRoutes } from './permission'

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')

  // 登录页无需登录即可访问
  if (to.path === '/login') {
    return next()
  }

  // 未登录时跳转到登录页
  if (!token) {
    return next({
      path: '/login',
      query: {
        redirect: to.fullPath
      }
    })
  }

  // 首次登录后，先加载用户信息和权限
  if (!store.state.permission.routesLoaded) {
    try {
      // 这里假设用户信息已由 Vuex 异步获取
      const roles = store.state.user.roles

      const routes = generateRoutes(roles)

      store.commit(
        'permission/SET_ROUTES_LOADED',
        true
      )

      store.commit(
        'permission/SET_ROUTES',
        routes
      )

      // 动态路由注册完成后重新匹配目标地址
      return next({
        ...to,
        replace: true
      })
    } catch (error) {
      return next('/login')
    }
  }

  next()
})
```

这段代码展示了权限路由的核心流程，但实际项目需要保证用户信息已经成功加载后，才能读取角色并生成路由。

其中，`routesLoaded` 用于记录动态路由是否已经加载，避免每次导航都重新注册。

`next({ ...to, replace: true })` 则用于在动态路由注册后重新匹配目标地址。否则，首次访问某个尚未注册的动态路由时，可能无法正确匹配页面。

还需要注意：

1. `store.state.permission` 和 `store.state.user` 是示例中的 Vuex 模块，需要在项目中自行定义。
2. 如果获取用户信息失败，应清理无效的登录状态，并跳转到登录页或错误页。
3. 如果用户退出登录或切换账号，需要重置用户权限和动态路由状态，避免旧账号的权限残留。
4. 应为未知路径配置 404 页面，并确保路由匹配顺序正确。

## 四、多角色权限管理：RBAC 模型

### 4.1 什么是 RBAC？

RBAC 是 Role-Based Access Control 的缩写，即基于角色的访问控制。

其核心思想是：不直接为每个用户单独配置所有权限，而是先定义角色，再将权限分配给角色，最后将角色分配给用户。

例如：

| 角色 | 权限 |
|---|---|
| 管理员 admin | 用户管理、角色管理、业务查询、数据导出 |
| 普通员工 user | 工作台、业务查询 |
| 审核人员 auditor | 业务查询、业务审核 |

一个用户可以拥有多个角色，而多个角色可以共享相同的权限。

常见的数据关系如下：

```text
用户 User
   ↓
用户角色关联 UserRole
   ↓
角色 Role
   ↓
角色权限关联 RolePermission
   ↓
权限 Permission
```

在实际系统中，权限可以进一步细分为菜单权限、页面权限、按钮权限、接口权限和数据范围权限。

### 4.2 多角色权限如何合并？

假设某个用户同时拥有 `user` 和 `auditor` 两个角色。

可以将两个角色对应的权限合并，形成用户最终拥有的权限集合。

```js
const rolePermissions = {
  admin: [
    'user:list',
    'user:create',
    'user:delete',
    'order:list',
    'order:audit'
  ],

  user: [
    'order:list'
  ],

  auditor: [
    'order:list',
    'order:audit'
  ]
}

function getUserPermissions(roles) {
  const permissions = new Set()

  roles.forEach(role => {
    const currentPermissions =
      rolePermissions[role] || []

    currentPermissions.forEach(permission => {
      permissions.add(permission)
    })
  })

  return [...permissions]
}

const roles = ['user', 'auditor']

console.log(getUserPermissions(roles))
// ['order:list', 'order:audit']
```

这里使用 `Set` 对权限进行去重。

需要强调，这段代码主要用于解释合并逻辑。生产环境中，角色与权限的真实映射应以服务端的授权结果为准，不能将前端硬编码的权限映射作为安全依据。

如果业务包含拒绝规则、数据范围限制或职责分离规则，还需要定义明确的冲突处理方式，不能简单地将所有权限合并。

### 4.3 使用权限标识控制功能

相比在组件中频繁判断角色名称，更推荐使用权限标识控制具体操作。

例如：

```js
const permissions = [
  'user:list',
  'user:create',
  'order:list'
]

function hasPermission(permission) {
  return permissions.includes(permission)
}

console.log(hasPermission('user:create'))
// true

console.log(hasPermission('user:delete'))
// false
```

这种方式将业务角色与具体功能解耦。

如果未来新增一个具有用户查询和订单查询权限的角色，只需要调整服务端授权配置，而不必在每个页面中增加新的角色判断。

## 五、根据不同角色控制菜单和按钮

### 5.1 菜单权限控制

菜单一般有两种生成方式。

**方式一：前端定义菜单，后端返回权限标识。**

前端维护菜单配置，根据权限标识筛选出用户可以看到的菜单。

**方式二：后端返回菜单树。**

后端根据当前用户的角色和权限返回菜单数据，前端负责渲染。

第二种方式更适合需要动态配置菜单的管理系统，但前端仍然需要校验数据格式，并保证路由注册与菜单展示使用一致的权限规则。

示例菜单配置：

```js
const menus = [
  {
    title: '工作台',
    path: '/dashboard',
    permission: 'dashboard:view'
  },
  {
    title: '用户管理',
    path: '/system/users',
    permission: 'user:list'
  },
  {
    title: '订单管理',
    path: '/orders',
    permission: 'order:list'
  }
]

function filterMenus(menus, permissions) {
  return menus.filter(menu =>
    permissions.includes(menu.permission)
  )
}
```

如果菜单存在父子层级，应递归过滤子菜单，并处理父级菜单没有任何可见子菜单的情况。

此外，菜单可见并不代表用户一定有权访问页面，因此菜单过滤和路由鉴权必须使用一致的权限规则。

### 5.2 使用自定义指令控制按钮权限

后台管理系统经常需要控制新增、编辑、删除等按钮。

Vue2 可以通过自定义指令实现按钮权限控制。

```js
// permission.js
import store from './store'

function checkPermission(permission) {
  const permissions =
    store.state.user.permissions

  return permissions.includes(permission)
}

export default {
  inserted(el, binding) {
    if (!checkPermission(binding.value)) {
      if (el.parentNode) {
        el.parentNode.removeChild(el)
      }
    }
  }
}
```

在 `main.js` 中注册指令：

```js
import Vue from 'vue'
import permission from './directives/permission'

Vue.directive('permission', permission)
```

在组件中使用：

```html
<el-button
  v-permission="'user:create'"
>
  新增用户
</el-button>

<el-button
  v-permission="'user:delete'"
>
  删除用户
</el-button>
```

如果当前用户不具有对应的权限标识，按钮就不会显示。

这里需要注意，自定义指令的 `inserted` 钩子主要处理元素首次插入时的权限判断。如果权限数据会在运行过程中变化，还应通过 `update` 钩子或响应式条件渲染处理更新。

此外，隐藏按钮只是前端交互控制，不能阻止用户直接构造请求。后端仍然必须验证操作权限。

## 六、Vue Router 的实现原理

### 6.1 Vue Router 的核心组成

Vue Router 是 Vue 官方的路由管理库。对于 Vue2 项目，通常使用 Vue Router 3。

其主要组成包括：

| 组成部分 | 作用 |
|---|---|
| 路由配置 | 定义 URL 与组件之间的映射关系 |
| 路由匹配器 | 根据当前 URL 匹配路由记录 |
| History 管理 | 管理 URL 变化、前进和后退 |
| 导航守卫 | 控制导航是否继续、重定向或取消 |
| `router-link` | 提供声明式导航 |
| `router-view` | 渲染当前匹配的路由组件 |

例如：

```js
const routes = [
  {
    path: '/home',
    component: Home
  },
  {
    path: '/user/:id',
    component: User
  }
]
```

当用户访问 `/user/123` 时，路由匹配器会找到 `/user/:id` 对应的路由记录，并解析出参数 `id = 123`。

随后，`router-view` 根据当前匹配结果渲染 `User` 组件。

### 6.2 一次路由跳转经历什么过程？

以 `router.push('/user/123')` 为例，可以将核心过程理解为：

```text
触发路由导航
      ↓
解析目标 URL
      ↓
匹配目标路由
      ↓
执行相关导航守卫
      ↓
确认导航
      ↓
更新当前路由状态
      ↓
router-view 渲染对应组件
```

具体执行流程还会涉及组件离开守卫、全局前置守卫、路由独享守卫、组件进入守卫等步骤。不同类型的导航并不一定执行完全相同的守卫。

### 6.3 Vue Router 如何更新视图？

Vue Router 会维护当前路由状态，并根据路由变化更新匹配结果。

`router-view` 是一个特殊的路由渲染组件，它根据当前匹配到的路由记录渲染对应组件。

当用户从 `/home` 跳转到 `/user/123` 时，通常不会重新加载整个 HTML 文档，而是更新前端路由状态，并由 Vue 的响应式系统和组件渲染机制更新相关视图。

需要注意，路由切换是否复用组件取决于匹配结果和组件结构。例如，同一个组件从 `/user/1` 切换到 `/user/2` 时，组件可能被复用，此时可以通过监听 `$route` 或使用 `beforeRouteUpdate` 处理参数变化。

## 七、Hash 模式和 History 模式

### 7.1 Hash 模式的原理

Hash 模式的 URL 通常如下：

```text
https://example.com/#/home
https://example.com/#/user/123
```

其中，`#` 后面的内容称为 URL 片段。

浏览器不会将 Hash 及其后面的内容作为 HTTP 请求路径发送给服务器。因此，从 `/#/home` 切换到 `/#/user/123` 时，通常只需要在前端更新路由状态。

Vue Router 3 中可以这样配置：

```js
const router = new VueRouter({
  mode: 'hash',
  routes
})
```

Hash 模式的主要特点：

1. URL 中包含 `#`。
2. 可以通过监听 Hash 变化实现路由切换。
3. 一般不需要针对每个前端路由额外配置服务器回退规则。
4. 刷新页面时，浏览器请求的是基础页面地址，前端应用再根据 Hash 恢复对应路由。

需要注意，Hash 模式仍然需要服务器提供 `index.html`、JavaScript 和 CSS 等静态资源，只是通常不需要为 Hash 对应的路径额外配置回退。

### 7.2 History 模式的原理

History 模式利用 HTML5 History API 实现 URL 更新。

例如：

```text
https://example.com/home
https://example.com/user/123
```

配置方式如下：

```js
const router = new VueRouter({
  mode: 'history',
  routes
})
```

常用的浏览器 API 包括：

```js
history.pushState({}, '', '/user/123')

history.replaceState({}, '', '/home')
```

`pushState()` 可以在不重新加载整个文档的情况下添加历史记录，`replaceState()` 则可以替换当前历史记录。

但需要注意，这两个 API 本身不会自动完成 Vue Router 的路由匹配、导航守卫和组件渲染，这些工作由 Vue Router 负责。

### 7.3 Hash 和 History 的区别

| 对比维度 | Hash 模式 | History 模式 |
|---|---|---|
| URL 格式 | `/#/home` | `/home` |
| 核心机制 | Hash 变化 | HTML5 History API |
| 站内导航 | 通常不刷新整个页面 | 通常不刷新整个页面 |
| 深层路由刷新 | 一般无需额外回退配置 | 需要服务器支持 SPA 回退 |
| URL 美观程度 | 包含 `#` | 更简洁 |
| 前进、后退 | 支持 | 支持 |

两种模式都可以实现单页面应用的前端导航。主要区别在于 URL 表现形式和服务器部署要求。

## 八、History 模式为什么需要后端配合？

这是 Vue Router 面试中的高频问题。

假设前端应用配置了 `/user/123` 路由。

当用户在应用内点击链接跳转时，Vue Router 可以通过 History API 更新 URL，并渲染对应组件，而不需要重新请求整个页面。

但是，如果用户直接在浏览器地址栏输入：

```text
https://example.com/user/123
```

或者在该页面刷新，浏览器就会向服务器请求 `/user/123`。

如果服务器只部署了 `index.html`，没有对应的 `/user/123` 文件或服务端路由，服务器就可能返回 404。

因此，History 模式需要配置服务器，将不存在的前端页面路径回退到 `index.html`。

### 8.1 Nginx 配置示例

假设前端项目打包后的文件部署在 `/usr/share/nginx/html`，可以使用：

```nginx
server {
    listen 80;
    server_name example.com;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

其中：

```nginx
try_files $uri $uri/ /index.html;
```

表示先尝试查找对应文件或目录。如果不存在，则返回 `index.html`，让前端路由接管页面路径。

生产环境中，还需要正确配置后端 API 的代理或转发规则，不能让所有 API 请求都被错误地回退到 `index.html`。静态资源路径和真实服务端路由也需要根据项目实际部署结构处理。

## 九、总结

Vue2 项目中的权限管理通常结合 Vue Router、Vuex 和后端授权接口实现。

通过 RBAC 模型，可以将用户、角色和权限进行解耦。前端根据用户权限生成动态路由、过滤菜单并控制按钮显示，后端则负责真正的接口鉴权。

Vue Router 的核心工作是根据 URL 匹配路由记录、执行导航守卫、更新当前路由状态，并通过 `router-view` 渲染对应组件。

Hash 模式通过 URL 片段实现前端导航，通常不需要额外配置深层路由回退。History 模式利用 HTML5 History API 实现更简洁的 URL，但需要服务器在刷新或直接访问前端路由时正确返回 `index.html`。

理解这些内容，不仅能够帮助我们实现后台管理系统的权限控制，也能让我们更深入地理解前端路由的工作机制和部署原理。

## 十、参考资料

- [Vue Router 3 中文文档](https://v3.router.vuejs.org/zh/)
- [Vue Router 3：导航守卫](https://v3.router.vuejs.org/zh/guide/advanced/navigation-guards.html)
- [Vue Router 3：HTML5 History 模式](https://v3.router.vuejs.org/zh/guide/essentials/history-mode.html)
- [MDN：History API](https://developer.mozilla.org/zh-CN/docs/Web/API/History_API)
