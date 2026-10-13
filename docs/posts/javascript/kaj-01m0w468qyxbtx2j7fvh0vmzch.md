---
title: "跨域问题及其解决方法"
description: "跨域（Cross-Origin）问题是在前后端分离开发中最常见、也最基础的一个概念。"
date: "2026-08-25"
publishedAt: "2026-08-25T17:32:07.550738+08:00"
source: "https://kajspace.cn/articles/01M0W468QYXBTX2J7FVH0VMZCH/"
tags: ["前端"]
---

# 跨域问题及其解决方法

## 开发时经常会遇到跨域问题，什么是跨域问题 {#kaj-h-fc76e785-87db-43e2-af25-b34553e66211}

跨域（Cross-Origin）问题是在前后端分离开发中**最常见、也最基础**的一个概念。

简单来说，跨域是**浏览器**出于安全考虑，强制执行的一种限制策略（同源策略）。当你的前端页面想要向一个**不同源**的后端接口发送请求时，浏览器就会拦截这个请求。

### 1. 什么是“同源”？ {#kaj-h-e8bb2bfe-0501-4fce-9fdf-069d7fe2b89a}

要理解跨域，首先要知道什么是“同源”。一个完整的 URL 由以下三部分组成：

`协议` + `域名` + `端口`

只有当这三个部分**完全相同**时，才叫“同源”。只要其中**任何一个**不同，就是“跨域”。

**假设你的前端页面地址是：**`http://localhost:5173`

- ✅ **同源**：`http://localhost:5173/api/books` （完全一样）
- ❌ **跨域（端口不同）**：`http://localhost:8080/api/books` （后端 Spring Boot 默认端口）
- ❌ **跨域（协议不同）**：`https://localhost:5173/api/books` （http 与 https）
- ❌ **跨域（域名不同）**：`http://192.168.1.100:5173/api/books` （IP 与 localhost）

### 2. 为什么浏览器要搞这种限制？ {#kaj-h-f4b89329-bf49-462e-864d-fcfff3f69cdf}

这是浏览器的**同源策略（Same-Origin Policy）**，它的核心目的是**安全**。

想象一下，如果没有这个限制：你一边在浏览器里登录了银行网站（`bank.com`），一边打开了一个恶意网站（`hack.com`）。恶意网站的代码就可以偷偷向 `bank.com` 发送转账请求，甚至读取你在银行页面的数据。有了同源策略，浏览器就会死死捂住你的数据，不让其他网站偷看或篡改。

### 3. 跨域报错长什么样？ {#kaj-h-175a94c7-5056-4006-b070-a78466d5d38b}

当发生跨域时，虽然你的后端可能已经成功处理了请求并返回了数据，但浏览器会在控制台抛出类似这样的红色错误：

> `Access to XMLHttpRequest at 'http://localhost:8080/api/books' from origin 'http://localhost:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.`

### 4. 实际开发中怎么解决跨域？ {#kaj-h-5166e87f-cc0f-451a-990e-77f8a5cc465b}

既然前后端分离必然跨域，我们就必须解决它。业界有以下几种主流方案：

#### 方案一：后端配置 CORS（最常用） {#kaj-h-5d940cca-faa0-431f-bfa4-51d61b1ad790}

让后端在响应头中加上 `Access-Control-Allow-Origin`，告诉浏览器：“我允许这个前端网站访问我”。

- **Spring Boot 极简写法**：直接在 Controller 或接口方法上加一个注解 `@CrossOrigin`。
- **全局配置**：在 Spring Boot 中写一个配置类，统一放行所有跨域请求。

#### 方案二：前端开发服务器代理（Vite/Webpack Proxy） {#kaj-h-9afb8608-24fd-4939-b01b-2f17ccbc77e9}

这是前端开发时最推荐的做法。

- **原理**：前端请求依然发给 `localhost:5173/api/books`，由 Vite 开发服务器在后台偷偷把请求转发给后端的 `localhost:8080/api/books`。
- **优势**：对浏览器来说，前端和接口是“同源”的，根本不存在跨域问题。而且部署到生产环境时，通常也会用 Nginx 做反向代理，所以这种方案和线上环境完全一致。

#### 方案三：Nginx 反向代理（生产环境标配） {#kaj-h-ec9e4b00-566c-4db7-bd66-1c5cdc5b8e2d}

Nginx 本身是运行在服务器上的 Web 服务器和反向代理软件。生产环境中通常由 Nginx 作为统一入口，对外暴露一个域名。用户访问前端页面时，Nginx 可以直接返回前端打包后的静态资源；当前端请求 `/api` 等接口时，Nginx 根据路径将请求反向代理到后端服务。这样从浏览器的角度看，前端和 API 都属于同一个域名，因此可以避免浏览器的跨域问题。

### 💡 总结 {#kaj-h-7a771550-5f27-47a1-9c2d-b2df823968ba}

跨域是浏览器的安全机制，不是后端的 Bug。在实际开发中，**前端用 Vite Proxy 代理，后端加** `@CrossOrigin` **注解**，双管齐下，基本可以解决 99% 的跨域烦恼。
