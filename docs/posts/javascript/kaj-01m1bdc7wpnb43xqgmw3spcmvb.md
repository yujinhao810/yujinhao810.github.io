---
title: "请求拦截器和响应拦截器"
description: "这是 HTTP 请求头（Request Header）中的一个字段，用来告诉后端："
date: "2026-08-31"
publishedAt: "2026-08-31T16:01:23.907398+08:00"
source: "https://kajspace.cn/articles/01M1BDC7WPNB43XQGMW3SPCMVB/"
tags: ["前端"]
---

# 请求拦截器和响应拦截器

## 1. `Authorization: Bearer xxx` 是什么？ {#kaj-h-034d65f4-809a-46a1-91af-58c093040c97}

这是 HTTP 请求头（Request Header）中的一个字段，用来告诉后端：

> **“我是哪个已经登录的用户，我有这个 Token，可以让我访问接口。”**

例如：

```text
GET /api/user/info

Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

这里分成两部分：

```text
Authorization
     ↓
字段名

Bearer
     ↓
认证方式，表示使用 Bearer Token

xxx
     ↓
真正的 Token
```

所以：

```text
Authorization: Bearer xxx
```

可以理解成：

> **Authorization 是“我要进行身份认证”，Bearer 表示“我拿 Token 来证明身份”，xxx 就是具体的 Token。**

---

## 2. 为什么要加这个东西？ {#kaj-h-9ac53440-f581-4959-814d-9b64f8c613c9}

比如用户登录：

```text
用户输入账号密码
        ↓
POST /login
        ↓
后端验证成功
        ↓
后端返回 Token
        ↓
前端保存 Token
```

例如：

```text
localStorage.setItem('token', 'abc123')
```

以后用户请求：

```text
GET /user/info
GET /user/order
POST /user/update
```

后端需要知道：

> “这个请求是谁发来的？”

所以前端把 Token 放到请求头：

```text
Authorization: Bearer abc123
```

后端拿到 Token 后进行验证。

---

## 3. 为什么要用请求拦截器？ {#kaj-h-82f87c8d-77c3-4a67-85fc-12ecb7a61fc3}

假设你的项目有 100 个接口。

如果没有请求拦截器，你可能需要每个接口都写：

```js
const token = localStorage.getItem('token')

axios.get('/user/info', {
    headers: {
        Authorization: `Bearer ${token}`
    }
})
```

然后：

```text
axios.get('/user/order', {
    headers: {
        Authorization: `Bearer ${token}`
    }
})
```

又要写一遍。

这样非常麻烦。

所以可以使用**请求拦截器**统一处理。

例如 Axios：

```js
axios.interceptors.request.use(config => {
    const token = localStorage.getItem('token')

    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
})
```

以后：

```text
axios.get('/user/info')
```

请求真正发送之前，会自动经过：

```text
axios.get()
    ↓
请求拦截器
    ↓
读取 Token
    ↓
添加 Authorization
    ↓
真正发送 HTTP 请求
```

所以你可以把：

> **请求拦截器理解成“请求发送之前的统一加工站”。**

---

## 4. 请求拦截器一般做什么？ {#kaj-h-124a9ab9-64e5-4610-b17d-15a6c5746d9a}

最常见的就是：

### ① 添加 Token {#kaj-h-12a11e12-0197-46d9-9a8d-df7b13d14aec}

```text
config.headers.Authorization = `Bearer ${token}`
```

### ② 添加公共请求参数 {#kaj-h-3bd54cfe-1456-488a-9cf7-795dd21fac1b}

例如：

```text
config.headers['X-Platform'] = 'web'
```

### ③ 统一设置请求配置 {#kaj-h-3ecdc5e5-982a-4ccb-ada1-ae8240369e40}

例如：

```text
config.timeout = 5000
```

### ④ 请求加载状态 {#kaj-h-98d757fa-0663-4fe5-9559-e52e1744278d}

比如发送请求之前：

```text
loading = true
```

然后请求结束：

```text
loading = false
```

不过实际项目中 loading 通常会结合响应拦截器一起处理。

---

## 5. 那响应拦截器是什么？ {#kaj-h-f803f46f-9592-4a14-9924-2bb82ba689d7}

请求发送之后：

```text
前端
 ↓
请求拦截器
 ↓
HTTP 请求
 ↓
后端
 ↓
HTTP 响应
 ↓
响应拦截器
 ↓
前端拿到最终数据
```

所以：

> **响应拦截器就是“服务器返回结果之后的统一处理站”。**

例如后端返回：

```text
{
    "code": 200,
    "data": {
        "name": "Tom"
    },
    "message": "success"
}
```

响应拦截器可以统一处理：

```js
axios.interceptors.response.use(
    response => {
        return response.data
    },
    error => {
        // 处理错误
        return Promise.reject(error)
    }
)
```

这样业务代码里：

```js
const res = await axios.get('/user/info')
```

拿到的可能直接就是：

```text
{
    name: 'Tom'
}
```

而不需要每个接口都写：

```text
res.data.data
```

---

## 6. 响应拦截器最重要的作用：统一处理错误 {#kaj-h-0835e1d7-b82e-4118-b47d-164a6d222a62}

比如后端规定：

```text
200 → 成功
401 → Token 失效
403 → 没有权限
500 → 服务器错误
```

如果没有响应拦截器，每个接口都要自己判断：

```js
if (res.status === 401) {
    // Token失效
}
```

有了响应拦截器：

```js
axios.interceptors.response.use(
    response => {
        return response
    },

    error => {
        if (error.response?.status === 401) {
            // 清除 Token
            // 跳转登录页
        }

        return Promise.reject(error)
    }
)
```

就可以统一处理。

---

## 7. 两个拦截器放在一起理解 {#kaj-h-a43e93ba-00ac-440b-a99e-0ef1ad6cf581}

这是你面试最应该记住的：

```text
                    请求
                     ↓
              ┌──────────────┐
              │ 请求拦截器    │
              │              │
              │ 读取 Token    │
              │ 添加请求头    │
              │ 公共参数处理  │
              └──────┬───────┘
                     ↓
                  后端服务器
                     ↓
              ┌──────┴───────┐
              │ 响应拦截器    │
              │              │
              │ 统一处理数据  │
              │ 401 登录失效  │
              │ 500 服务器错误│
              │ 错误提示      │
              └──────┬───────┘
                     ↓
                  业务代码
```

因此可以非常简单地记：

> **请求拦截器：请求发出去之前统一处理。**

> **响应拦截器：服务器返回之后统一处理。**

---

## 8. 面试的时候可以这样回答 {#kaj-h-fb49a18b-06ac-4609-9ca4-dd728703fb62}

如果面试官问：

**“你们项目为什么使用请求拦截器和响应拦截器？”**

你可以回答：

> 我们主要是为了统一处理 HTTP 请求和响应。请求拦截器是在请求发送之前执行，可以统一从本地获取 Token，并通过 `Authorization: Bearer xxx` 添加到请求头中，同时也可以处理公共请求参数等。响应拦截器是在后端返回响应之后执行，可以统一处理响应数据以及异常状态，比如遇到 401 说明登录凭证可能失效，可以清除 Token 并跳转登录页，这样就不需要在每个业务接口中重复处理这些逻辑。
