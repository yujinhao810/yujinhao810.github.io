---
title: "对requestAnimationFrame（rAF）的理解"
description: "requestAnimationFrame（简称 rAF）可以把它理解成："
date: "2026-08-18"
publishedAt: "2026-08-18T16:43:49.227404+08:00"
source: "https://kajspace.cn/articles/01M0A0MXZBQRRD57W8E5G9SSTC/"
tags: ["前端"]
---

# 对requestAnimationFrame（rAF）的理解

`requestAnimationFrame`（简称 `rAF`）可以把它理解成：

“告诉浏览器：我这段 JavaScript 动画代码，最好在下一次浏览器准备绘制画面之前执行。”

它主要用于做**动画、拖拽、滚动位置跟随、Canvas 绘制**等需要频繁更新页面的场景。

## requestAnimationFrame 的核心思想 {#kaj-h-335f2e5b-7dfe-4940-a895-82c9cd7231c6}

requestAnimationFrame是把回调交给浏览器：

requestAnimationFrame(callback)

意思类似于：

“浏览器，你下一次准备绘制画面之前，调用一下callback”

`function animate() {`

`  box.style.transform = 'translateX(100px)'`

`  requestAnimationFrame(animate)`

`}`

`requestAnimationFrame(animate)`

执行过程可以理解成：

浏览器准备绘制第 1 帧

↓

执行 animate()

↓

修改页面

↓

浏览器绘制

浏览器准备绘制第 2 帧

↓

执行 animate()

↓

修改页面

↓

浏览器绘制

……

requestAnimationFrame会根据浏览器的刷新率来绘制，每一帧的刷新时间由浏览器的屏幕刷新率决定。

## requestAnimationFrame 有什么特点？ {#kaj-h-c00b6e79-caca-4c15-8e5b-ce763110d79c}

浏览器不可见时通常会降频，比如页面切到后台：

用户切换标签页

↓

浏览器降低甚至暂停 rAF

返回一个 ID，可以取消

const id = requestAnimationFrame(fn)

cancelAnimationFrame(id)

## requestAnimationFrame 不会自动重复 {#kaj-h-272e699d-bad3-4eef-8249-2380b494508a}

`requestAnimationFrame(fn)`

只会执行一次。

如果需要持续动画：

`function animate() {`

`  // 修改位置`

`  requestAnimationFrame(animate)`

`}`

`requestAnimationFrame(animate)`

相当于自己形成递归循环：

rAF

↓

animate

↓

rAF

↓

animate

↓

rAF

↓

……

## 最适合面试背的版本 {#kaj-h-1668c138-d71d-4328-b1c0-f520e74ce764}

requestAnimationFrame 是浏览器提供的动画调度 API，用于告诉浏览器在下一次重绘之前执行回调。它会根据浏览器当前的刷新节奏进行调度，相比 setTimeout 和 setInterval 更适合做动画、拖拽和高频视觉更新。它本身只执行一次，如果需要连续动画，需要在回调中再次调用 requestAnimationFrame。另外它通常会在页面不可见时降低调用频率，从而减少资源消耗。

如果动画需要保持与真实时间一致，不能简单依赖“每帧移动多少像素”，而应该利用 rAF 回调提供的 timestamp 根据时间差计算动画进度。

## setTimeout 和 setInterval 有什么区别 {#kaj-h-3def3dc4-8cea-405d-9191-8ad8462cced0}

`setTimeout` 是延迟**执行一次**，`setInterval` 是按照指定时间间隔**重复执行**，都属于定时器机制；而 `requestAnimationFrame` 是面向浏览器渲染帧的调度 API，会在下一次重绘前执行回调，所以更适合动画和高频视觉更新。

**setTimeout执行动画的缺点**：它通过设定间隔时间来不断改变图像位置，达到动画效果。但是容易出现卡顿、抖动的现象；原因是：

- settimeout任务被放入异步队列，只有当主线程任务执行完后才会执行队列中的任务，因此实际执行时间总是比设定时间要晚；
- settimeout的固定时间间隔不一定与屏幕刷新间隔时间相同，会引起丢帧。
