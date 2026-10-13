---
title: "Vue生命周期"
description: "Vue 生命周期"
date: "2026-09-18"
publishedAt: "2026-09-18T14:49:55.351462+08:00"
source: "https://kajspace.cn/articles/01M2SKR11S5QG6E93Q5D0ZNGXX/"
tags: ["前端"]
---

# Vue生命周期

## 整个首次加载过程 {#kaj-h-02f85d47-696a-49b3-8082-843f86fe2064}

Vue 生命周期

│

↓

创建组件实例

│

↓

beforeCreate

│

初始化组件相关数据

│

↓

created

│

开始首次渲染

│

↓

render

│

↓

VNode

│

↓

beforeMount

│

创建真实 DOM

│

↓

插入页面 DOM 树

│

↓

mounted

│

↓

───── Vue 工作结束 ─────

│

↓

浏览器渲染管线

│

↓

Style

↓

Layout

↓

Paint

↓

Composite

↓

屏幕

## 数据发生变化以后 {#kaj-h-cf5cf9c2-a621-4dad-96b7-8fe047530a36}

count.value++

↓

响应式系统检测到变化

↓

beforeUpdate

↓

重新 render

↓

生成新的 VNode

↓

Diff

↓

修改真实 DOM

↓

updated

↓

浏览器重新进行必要的

Style / Layout / Paint / Composite

↓

屏幕显示新结果

## 销毁/卸载 {#kaj-h-b04cdceb-5e26-4174-8b20-b4a4d601d53d}

beforeUnmount

↓

组件还存在

↓

执行卸载

↓

DOM 移除

↓

响应式副作用等清理

↓

unmounted
