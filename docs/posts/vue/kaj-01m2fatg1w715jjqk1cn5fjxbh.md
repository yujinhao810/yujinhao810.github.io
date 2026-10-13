---
title: "关于Vue Router，我们要知道什么？"
description: "Vue Router 是 Vue 官方提供的路由管理库，主要用于实现单页面应用（SPA）中的页面导航、路由匹配、嵌套路由、动态路由、路由参数、导航守卫以及路由懒加载等功能。"
date: "2026-09-14"
publishedAt: "2026-09-14T14:49:14.024904+08:00"
source: "https://kajspace.cn/articles/01M2FATG1W715JJQK1CN5FJXBH/"
tags: ["前端"]
---

# 关于Vue Router，我们要知道什么？

## Vue Router 知识总结 {#kaj-h-fdb039f7-c412-42e6-af88-93514541fc26}

Vue Router 是 Vue 官方提供的路由管理库，主要用于实现单页面应用（SPA）中的**页面导航、路由匹配、嵌套路由、动态路由、路由参数、导航守卫以及路由懒加载**等功能。

---

## 一、什么是 Vue Router {#kaj-h-18c96d8d-de0a-4cfc-9abb-3bf63166826f}

传统多页面应用中，浏览器访问不同 URL，服务器通常返回不同的 HTML 页面。

例如：

```text
/login
/home
/user
/settings
```

而 Vue 单页面应用通常只有一个 HTML：

```text
index.html
```

页面内容的变化主要由 JavaScript 控制。

Vue Router 做的事情就是：

```html
浏览器 URL
    ↓
Vue Router
    ↓
匹配路由
    ↓
确定应该显示哪个 Vue 组件
    ↓
<router-view>
    ↓
渲染组件
```

因此可以简单理解：

> **Vue Router 建立了 URL 与 Vue 组件之间的映射关系。**

例如：

```js
const routes = [
  {
    path: '/home',
    component: Home
  },
  {
    path: '/about',
    component: About
  }
]
```

表示：

```text
/home  → Home.vue
/about → About.vue
```

---

## 二、Vue Router 的基本使用 {#kaj-h-e17cefed-3ce6-4b25-ba50-1061c661fd11}

## 1. 安装 {#kaj-h-c904c12a-7182-41ae-ac92-0f955e2842ce}

```text
npm install vue-router
```

---

## 2. 创建 Router {#kaj-h-5f399b48-f5c0-46e5-a8ba-e277ec477bfb}

Vue Router 4 中通常使用：

```text
import { createRouter, createWebHashHistory } from 'vue-router'
```

然后：

```js
const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})
```

最后在 Vue 应用中注册：

```js
const app = createApp(App)

app.use(router)

app.mount('#app')
```

---

## 三、history 模式 {#kaj-h-1d6a1dd0-90b2-48bb-8efe-abe88de605ff}

Vue Router 常见的两种路由模式：

```text
createWebHashHistory()
createWebHistory()
```

## 1. Hash 模式 {#kaj-h-f716d80f-bfcf-46d8-9580-224784499c3b}

```text
createWebHashHistory()
```

URL：

```text
http://example.com/#/home
```

其中：

```text
#/home
```

就是 Hash。

特点：

- 不需要服务器特殊配置
- URL 中会出现 `#`
- 前端路由变化通常不会导致服务器重新请求页面

---

## 2. History 模式 {#kaj-h-37ec6673-d32c-4972-8a5a-2ec76b222e1c}

```text
createWebHistory()
```

URL：

```text
http://example.com/home
```

没有 `#`，URL 更加美观。

但是需要服务器进行配置。

例如用户直接访问：

```text
/home
```

服务器必须能够正确返回 `index.html`，否则可能出现 404。

---

## 四、路由配置 {#kaj-h-97139dac-7b75-4d32-832e-00a457cd7def}

最基本的路由：

```js
const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home
  }
]
```

每一个路由对象通常包含：

```text
{
  path,
  name,
  component
}
```

### path {#kaj-h-cec92543-4efb-434f-a3ad-99eba63c21e3}

表示 URL 路径：

```text
path: '/home'
```

### name {#kaj-h-cc52f355-ebf6-4560-8cca-f329b7a31cae}

路由名称：

```text
name: 'Home'
```

方便通过名称进行导航。

### component {#kaj-h-dd0330fd-b311-4075-a85d-4b33df89082f}

当前路由对应的 Vue 组件：

```text
component: Home
```

---

## 五、路由匹配的核心过程 {#kaj-h-39db33e1-cebf-43b3-b0c8-0a59df5869cf}

当用户访问：

```text
/home
```

Vue Router 会根据当前 URL 对路由表进行匹配。

例如：

```js
const routes = [
  {
    path: '/home',
    component: Home
  },
  {
    path: '/about',
    component: About
  }
]
```

访问：

```text
/home
```

匹配结果：

```text
/home
 ↓
Home.vue
```

访问：

```text
/about
```

匹配结果：

```text
/about
 ↓
About.vue
```

可以理解为：

```text
URL
 ↓
Router
 ↓
路由匹配
 ↓
找到对应组件
```

---

## 六、`<router-view>` 是什么 {#kaj-h-23c275da-f682-4a0d-ab17-2d83ca75f57b}

这是 Vue Router 最核心的概念之一。

```html
<router-view />
```

可以理解成：

> **路由组件的渲染出口。**

例如：

```html
<template>
  <router-view />
</template>
```

如果当前 URL 是：

```text
/home
```

那么：

```text
router-view
    ↓
Home.vue
```

如果当前 URL 是：

```text
/about
```

那么：

```text
router-view
    ↓
About.vue
```

因此可以把：

```html
<router-view />
```

理解成：

```text
【当前路由组件显示在这里】
```

---

## 七、嵌套路由 {#kaj-h-1b65b833-4fbd-4f29-844e-2e15682f5053}

Vue Router 支持路由嵌套。

例如：

```text
{
  path: '/',
  component: MainLayout,
  children: [
    {
      path: 'home',
      component: Home
    },
    {
      path: 'user',
      component: User
    }
  ]
}
```

形成：

```text
/
└── MainLayout
    ├── /home → Home
    └── /user → User
```

这意味着：

```text
/home
```

实际上对应：

```text
MainLayout
    ↓
Home
```

所以 `MainLayout.vue` 中需要：

```html
<template>
  <div>
    <Header />
    <Sidebar />

    <router-view />
  </div>
</template>
```

这里的：

```html
<router-view />
```

就是子路由组件的渲染位置。

---

## 八、多级嵌套路由 {#kaj-h-c59b684d-0e0b-4034-9d5e-fba3c1354fc0}

例如：

```text
{
  path: '/',
  component: MainLayout,
  children: [
    {
      path: 'goaf',
      component: GoafArea,
      children: [
        {
          path: 'coal',
          component: Coal
        }
      ]
    }
  ]
}
```

访问：

```text
/goaf/coal
```

路由层级为：

```text
/
└── MainLayout
    └── /goaf
        └── GoafArea
            └── /coal
                └── Coal
```

对应组件结构：

```text
MainLayout
    │
    └── router-view
            ↓
        GoafArea
            │
            └── router-view
                    ↓
                  Coal
```

所以：

> **每一层嵌套路由，都需要由对应父组件中的** `<router-view>` **提供渲染出口。**

---

## 九、`router-view` 和 `children` 的关系 {#kaj-h-b3ccd169-9da0-4b6e-9278-42ec3aa9126f}

可以记住：

```text
children
   ↓
定义子路由关系

router-view
   ↓
提供子路由组件的渲染位置
```

例如：

```text
{
  path: '/user',
  component: UserLayout,
  children: [
    {
      path: 'profile',
      component: Profile
    }
  ]
}
```

对应：

```html
UserLayout
    ↓
<router-view>
    ↓
Profile
```

如果 `UserLayout.vue` 没有：

```html
<router-view />
```

那么虽然路由匹配到了：

```text
/user/profile
```

但是没有对应的渲染出口显示 `Profile`。

---

## 十、`router.push()`：进行路由跳转 {#kaj-h-579d84be-a5b3-472d-99ba-5cb3a36d6958}

在 Composition API 中：

```js
const router = useRouter()
```

然后：

```text
router.push('/home')
```

表示：

> **导航到** `/home`**。**

例如：

```js
const handleClick = () => {
  router.push('/home')
}
```

完整过程：

```text
router.push('/home')
        ↓
改变当前路由
        ↓
Vue Router重新匹配
        ↓
匹配 /home
        ↓
找到 Home.vue
        ↓
router-view
        ↓
渲染 Home
```

---

## 十一、`useRouter()` 和 `useRoute()` {#kaj-h-96d461aa-2c41-4e02-8666-0c11eaef1335}

这是 Composition API 中非常重要的一组 API。

```js
const router = useRouter()
const route = useRoute()
```

两者作用完全不同。

## 1. useRouter() {#kaj-h-95718f4a-7da7-404a-aff0-1bfd3c9bc346}

获取 Router 实例。

主要用于：

> **操作路由。**

例如：

```text
router.push('/home')

router.replace('/home')

router.back()

router.go(-1)
```

所以：

```text
useRouter()
    ↓
router
    ↓
操作路由
```

---

## 2. useRoute() {#kaj-h-5dddf4bc-91f6-47a4-ae8b-de5dce85daa3}

获取当前路由对象。

主要用于：

> **读取当前路由信息。**

例如：

```text
route.path
route.name
route.query
route.params
route.fullPath
```

例如：

```js
console.log(route.path)
```

当前 URL：

```text
/home
```

那么：

```text
route.path
```

就是：

```text
/home
```

因此：

```text
useRoute()
    ↓
route
    ↓
读取当前路由状态
```

---

## 十二、`router` 和 `route` 的核心区别 {#kaj-h-3a529895-899b-4402-b9e5-f51c9fbf710a}

可以直接记这个表：

| API | 作用 | 示例 |
| --- | --- | --- |
| `useRouter()` | 操作路由 | `router.push()` |
| `useRoute()` | 读取当前路由 | `route.path` |
| `router` | 路由控制器 | 跳转、返回 |
| `route` | 当前路由状态 | path、query、params |

一句话：

> **router 是“我要去哪”，route 是“我现在在哪”。**

---

## 十三、路由跳转的几种方式 {#kaj-h-6d31110c-bded-4a3b-9484-c9d7698aa275}

## 1. 字符串跳转 {#kaj-h-34094896-d95f-4fad-a064-8da6c2b545af}

```text
router.push('/home')
```

---

## 2. 使用 name {#kaj-h-0c4c5c09-38d0-4aaa-9bbc-16e77a184d2a}

```text
router.push({
  name: 'Home'
})
```

前提是：

```text
{
  path: '/home',
  name: 'Home',
  component: Home
}
```

使用 `name` 的好处是可以减少对具体 URL 的依赖。

---

## 3. 携带 query {#kaj-h-ebf1078f-6bf7-44ed-90dd-e8a869749464}

```text
router.push({
  path: '/user',
  query: {
    id: 123
  }
})
```

URL：

```text
/user?id=123
```

获取：

```js
const route = useRoute()

console.log(route.query.id)
```

---

## 十四、params 和 query {#kaj-h-f74533c2-8f0c-4c0f-99aa-de4cd1808473}

这是面试常问的问题。

## query {#kaj-h-8d921353-a6f1-4652-b943-2bd6851299e1}

```text
router.push({
  path: '/user',
  query: {
    id: 123
  }
})
```

URL：

```text
/user?id=123
```

读取：

```text
route.query.id
```

---

## params {#kaj-h-836962cd-a08f-48ce-893a-10665d879296}

需要在路由中定义动态参数：

```text
{
  path: '/user/:id',
  component: User
}
```

然后：

```text
router.push({
  name: 'User',
  params: {
    id: 123
  }
})
```

URL：

```text
/user/123
```

读取：

```text
route.params.id
```

需要注意：

> **使用 params 对象进行命名路由导航时，应使用** `name`**，而不是依赖** `path`**。**

---

## 十五、`route.path`、`route.fullPath` {#kaj-h-63cc85c1-7bed-46f0-b4c3-2fdd9fd30f5a}

例如当前 URL：

```text
/goaf?coalLayerId=123
```

那么：

```text
route.path
```

得到：

```text
/goaf
```

而：

```text
route.fullPath
```

得到：

```text
/goaf?coalLayerId=123
```

因此：

```text
path
 ↓
路径

fullPath
 ↓
完整路由地址
```

---

## 十六、路由懒加载 {#kaj-h-51215ab5-2e3e-4382-a495-7b87c2dd7404}

实际项目中通常不会直接：

```text
import Home from '../views/Home.vue'
```

而是：

```js
component: () => import('../views/Home.vue')
```

例如：

```js
{
  path: '/home',
  component: () => import('../views/home/Home.vue')
}
```

这叫做：

> **路由组件懒加载。**

只有真正访问 `/home` 时，才加载对应组件的代码。

这样可以减少首次加载 JavaScript 的体积。

---

## 十七、路由重定向 redirect {#kaj-h-872517bf-b406-441d-baca-4599fe22c30d}

例如：

```text
{
  path: '/',
  redirect: '/home'
}
```

表示访问：

```text
/
```

自动跳转：

```text
/home
```

嵌套路由中也可以使用：

```text
{
  path: '/',
  component: MainLayout,
  children: [
    {
      path: '',
      redirect: '/home'
    }
  ]
}
```

这也是后台管理系统中非常常见的写法。

---

## 十八、路由导航守卫 {#kaj-h-bedfb3ab-209c-4a1d-a719-e64f6acd9290}

导航守卫可以在路由跳转过程中进行拦截。

最常见的是：

```js
router.beforeEach((to, from, next) => {
  // ...
})
```

其中：

```text
to
↓
准备去哪里

from
↓
当前来自哪里
```

例如：

```js
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (!token) {
    next('/login')
  } else {
    next()
  }
})
```

可以实现：

```text
访问页面
   ↓
beforeEach
   ↓
检查 token
   ↓
没有 token
   ↓
/login

有 token
   ↓
允许进入目标页面
```

---

## 十九、白名单路由 {#kaj-h-4418d68d-3cf5-4f83-8e80-145fa40ffa27}

登录页通常不需要登录，因此可以定义：

```js
const whiteList = ['/login']
```

然后：

```js
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (whiteList.includes(to.path)) {
    next()
    return
  }

  if (!token) {
    next('/login')
  } else {
    next()
  }
})
```

常见白名单：

```text
/login
/register
/404
```

---

## 二十、结合实际项目理解路由守卫 {#kaj-h-0ae960cd-78bf-4a88-919f-16464fee104d}

例如用户访问：

```text
/
```

首先经过：

```text
beforeEach
```

检查：

```text
localStorage.getItem('token')
```

如果存在 token：

```text
允许进入 /
    ↓
匹配 /
    ↓
MainLayout
    ↓
children中的默认路由
    ↓
redirect /home
    ↓
Home
```

所以这里要注意：

> **“有 token 后进入首页”与“**`/` **重定向到** `/home`**”其实是两个不同的过程。**

---

## 二十一、Vue Router 的完整运行流程 {#kaj-h-d70b5abd-18ae-4828-8321-8f76be27ab3e}

把前面的知识全部串起来：

```text
浏览器输入 URL
        ↓
Vue Router 获取当前 URL
        ↓
触发导航
        ↓
beforeEach 路由守卫
        ↓
是否允许进入？
    ↙           ↘
  否             是
  ↓               ↓
/login          路由匹配
                  ↓
          得到匹配的路由层级
                  ↓
          确定对应的组件
                  ↓
            router-view
                  ↓
          渲染路由组件
                  ↓
        子组件中的 router-view
                  ↓
          渲染更深层组件
                  ↓
            形成组件树
                  ↓
              Vue 渲染
```

---

## 二十二、一个完整例子 {#kaj-h-5d4b7e6e-97b4-4a40-9b57-341b40b9599b}

路由：

```js
const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('./views/Home.vue')
      },
      {
        path: 'user',
        component: UserLayout,
        children: [
          {
            path: 'profile',
            name: 'Profile',
            component: () => import('./views/Profile.vue')
          }
        ]
      }
    ]
  }
]
```

访问：

```text
/user/profile
```

Router 匹配：

```text
/
└── MainLayout
    └── /user
        └── UserLayout
            └── /profile
                └── Profile
```

最终：

```text
MainLayout
    │
    └── router-view
            ↓
        UserLayout
            │
            └── router-view
                    ↓
                 Profile
```

---

## 二十三、Vue Router 中最重要的几个概念 {#kaj-h-461c7123-e0f7-4837-9e99-d6d9c2700501}

学习 Vue Router 时，可以重点掌握下面这些：

```js
1. routes
   ↓
   路由配置

2. path
   ↓
   URL路径

3. component
   ↓
   路由对应的组件

4. children
   ↓
   嵌套路由

5. router-view
   ↓
   路由组件渲染出口

6. router.push
   ↓
   路由跳转

7. useRouter
   ↓
   操作路由

8. useRoute
   ↓
   获取当前路由

9. params
   ↓
   动态路由参数

10. query
    ↓
    查询参数

11. redirect
    ↓
    路由重定向

12. beforeEach
    ↓
    导航守卫

13. createWebHashHistory
    ↓
    Hash路由

14. createWebHistory
    ↓
    History路由

15. 路由懒加载
    ↓
    () => import(...)
```

---

## 二十四、最终理解：Vue Router 到底做了什么？ {#kaj-h-12276a5d-cc5c-45ad-8169-2bffaea187b6}

可以把 Vue Router 总结成下面这张图：

```text
                    Vue Router
                         │
                         ↓
                  当前浏览器 URL
                         │
                         ↓
                    路由匹配
                         │
             ┌───────────┴───────────┐
             ↓                       ↓
          路由守卫                 路由配置
             │                       │
             ↓                       ↓
          是否允许                找到组件
             │                       │
             └───────────┬───────────┘
                         ↓
                    router-view
                         ↓
                    渲染组件
                         ↓
                 嵌套路由继续渲染
                         ↓
                    最终组件树
```

最核心的理解可以浓缩成四句话：

> **① 路由配置建立 URL 和组件之间的映射关系。**

> **② Vue Router 根据当前 URL 匹配路由，并确定需要渲染哪些组件。**

> **③** `router.push()` **等 API 负责改变路由，**`useRoute()` **负责读取当前路由信息。**

> **④** `<router-view>` **是路由组件的渲染出口，嵌套路由通过父子组件中的多个** `router-view` **逐层渲染。**

如果把 Vue Router 比作一个导航系统：

```text
router
    ↓
导航控制器
“我要去哪里？”

route
    ↓
当前状态
“我现在在哪里？”

routes
    ↓
地图
“每个地址对应什么页面？”

router-view
    ↓
页面显示区域
“把当前匹配到的页面显示在这里。”

beforeEach
    ↓
门卫
“你有没有权限进去？”
```

掌握这几个核心概念，基本就建立起 Vue Router 的整体框架了。
