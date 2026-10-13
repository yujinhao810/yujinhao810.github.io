---
title: "CSS八股-1"
description: "none：元素不显示，并且会从文档流中移除"
date: "2026-08-17"
publishedAt: "2026-08-17T16:23:07.017904+08:00"
source: "https://kajspace.cn/articles/01M07C0SHGHMMB6B6NHB37G681/"
tags: ["前端"]
---

# CSS八股-1

## **display的属性值及其作用** {#kaj-h-6ab333a7-cf76-4190-b602-a6deceee745c}

none：元素不显示，并且会从文档流中移除

block：块类型。默认宽度为父元素宽度，可设置宽高，换行显示。

inline：行内元素类型。默认宽度为内容宽度，不可设置宽高，同行显示。

inline-block：默认宽度为内容宽度，可以设置宽高，同行显示。

list-item：像块类型元素一样显示，并添加样式列表标记。

table：此元素会作为块级表格来显示。

inherit：规定应该从父元素继承display属性的值。

## display的block、inline和inline-block的区别 {#kaj-h-54a3b5c6-8e35-40c9-8e2d-3804a0f19e31}

(1) block：会独占一行，多个元素会另起一行，可以设置width、height、margin和padding属性；

(2) inline：元素不会独占一行，设置width、height属性无效。但可以设置水平方向的margin和padding属性，不能设置垂直方向的padding和margin；

(3) inline-block：将对象设置为inline对象，但对象的内容作为block对象呈现，之后的内联对象会被排列在同一行内；

对于行内元素和块级元素，其特点如下：

**(1) 行内元素**

- 宽高设置无效；
- 可以设置水平方向的margin和padding属性，不能设置垂直方向的padding和margin；
- 不会自动换行；

**(2) 块级元素**

- 可以设置宽高；
- 设置margin和padding都有效；
- 可以自动换行；
- 多个块状，默认排列都从上到下

## 隐藏元素的方法有哪些 {#kaj-h-bbb05737-515b-428f-8f0c-b6def99f6b8d}

- **display;：none：**渲染树不会包含该渲染对象，因此该元素不会在页面中占据位置，也不会响应绑定的监听事件。
- **visibility：hidden：**元素在页面中仍占据空间，但是不会响应绑定的监听事件。
- **opacity：0：**将元素的透明度设置为0，以此来实现元素的隐藏。元素在页面中仍然占据空间，并且能够响应元素绑定的监听事件。
- **position：absolute：**通过使用绝对定位将元素移除可视区域内。以此来实现元素的隐藏。

`注：absolute会寻找最近的能够作为定位参考的祖先元素作为定位包含块。`

- **z-index：**负值：来使其他元素遮盖住该元素，以此来实现隐藏。
- **clip/clip-path：**使用元素裁剪的方法来实现元素的隐藏，这种方法下，元素仍在页面中占据位置，但不会响应绑定的监听事件。
- **transform：scale（0，0）：**将元素缩放为0，来实现元素的隐藏。这种方法下，元素仍在页面中占据位置，但是不会响应绑定的监听事件。

注：`fixed` 默认以 viewport 作为 containing block，但如果它的祖先元素设置了 `transform` 等会建立 containing block 的属性，那么这个祖先会成为 fixed 元素的定位参考。因为 transform 会建立新的坐标系，CSS 规范规定后代 fixed 元素可以基于这个新的 containing block 计算位置。

## display:none与visibility:hidden的区别 {#kaj-h-dd5c1235-a8bb-487a-a129-db6b5271deef}

（1）**在渲染树中**

- `display:none`会让元素完全从渲染树中消失，渲染时不会占据任何空间；
- `visibility:hidden`不会让元素从渲染树中消失，渲染的元素还会占据相应的空间，只是内容不可见。

（2）**是否是继承属性**

- `display:none` 本身不是继承属性，设置父元素 `display:none` 后，父元素及整个后代子树都不会参与渲染和布局，因此子元素即使设置 `display:block` 也无法单独显示。
- `visibility:hidden` 是继承属性，子元素默认会继承 `hidden`，但可以通过给子元素设置 `visibility:visible` 覆盖继承值，从而让子元素重新显示。它和 `display:none` 的区别之一是 `visibility:hidden` 仍然占据原来的布局空间。

（3）修改常规文档流中元素的 `display` 通常会造成文档的重排，但是修改`visibility`属性只会造成本元素的重绘；

（4）如果使用读屏器，设置为`display:none`的内容不会被读取，设置为`visibility:hidden`的内容会被读取。
