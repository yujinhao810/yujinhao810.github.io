---
title: "CSS八股-2"
description: "CSS3中的盒模型分为两种：标准盒模型和IE盒模型"
date: "2026-08-23"
publishedAt: "2026-08-23T15:45:03.372230+08:00"
source: "https://kajspace.cn/articles/01M0PS8K6THGJHPX0FSBWWH0X7/"
tags: ["前端"]
---

# CSS八股-2

## 1、对盒模型的理解 {#kaj-h-873a9ed4-cde1-4f61-9ea8-e3944c31783b}

CSS3中的盒模型分为两种：标准盒模型和IE盒模型

盒模型都是由四个部分组成的，分别是margin、border、padding和content

- 标准盒模型的width和height属性的范围只包含了content
- IE盒模型的width和height属性的范围包含了border、padding和content

可以通过修改元素的 **box-sizing** 属性来改变元素的盒模型

- `box-sizing: content-box`表示标准盒模型（默认值）

- `box-sizing: border-box`表示IE盒模型（怪异盒模型）

## 2、为什么有时候用translate来改变位置而不是定位 {#kaj-h-d6f8bef8-6e66-4323-a7a6-9da04c91436f}

translate是transform属性的一个值。改变transform或opacity不会触发浏览器的重排或重绘，只会触发复合。而改变绝对定位会触发重新布局，进而触发重绘和复合。transform使浏览器为元素创建一个GPU图层，但改变绝对定位会使用到CPU。因此translate更高效，可以缩短平滑动画的绘制时间。⽽translate改变位置时，元素依然会占据其原始空间，绝对定位就不会发⽣这种情况。

## 3、媒体查询 {#kaj-h-9e65f232-44c0-423a-aae2-c8473f6c942d}

@media (条件) {

/\* 条件满足时生效的 CSS \*/

}

## 4、BFC（块级格式化上下文） {#kaj-h-548779ae-3cc1-478e-8fb3-719ddd676899}

BFC是页面上一个独立的渲染区域，内部元素的布局不会影响外部元素。

创建方式：

/\* 以下任一属性均可创建 BFC \*/

.container {

overflow: hidden | auto | scroll;

display: inline-block | flex | grid | table-cell;

position: absolute | fixed;

float: left | right;

contain: layout | content | strict;

}

作用：

清除浮动：包含浮动子元素，防止高度塌陷

阻止margin重叠：BFC内部与外部margin不合并

阻止元素被浮动覆盖：自适应两栏布局

### clearfix： {#kaj-h-2cb4c2c5-0e04-438e-a337-34500232e12c}

.clearfix::after {

content: '';

display: block;

clear: both;

}

content

↓

创建一个伪元素

display: block

↓

让它成为块级清除点

clear: both

↓

让它排到所有浮动元素下面

## 5、CSS 优化和提高性能的方法有哪些？ {#kaj-h-3893b0b0-b3b9-4a3c-afd0-9c0e74937739}

1、将写好的CSS进行打包压缩

2、减少使用@import，建议使用link，因为后者在页面加载时一起加载，前者是等待页面加载完成之后再进行加载

3、避免使用通配规则，尽量少的去对标签进行选择，而是使用class

4、尽量少的去使用后代选择器，降低选择器的权重值。后代选择器的开销是最高的，尽量将选择器的深度降到最低，最高不要超过三层，更多的使用类来关联每一个标签元素。

5、慎重使用高性能属性：浮动、定位。尽量减少页面重排、重绘。

6、将具有相同属性的样式抽离出来，整合并通过class在页面中进行使用，提高css的可维护性。

## 6、CSS预处理器 {#kaj-h-f0e41975-4b05-45d7-8be1-296ec888d381}

**预处理器，**如：`less`，`sass`，`stylus`，用来预编译`sass`或者`less`，增加了`css`代码的复用性。层级，`mixin`， 变量，循环， 函数等对编写以及开发UI组件都极为方便。

**为什么要使用它们？**

- 结构清晰，便于扩展。 可以方便地屏蔽浏览器私有语法差异。封装对浏览器语法差异的重复处理， 减少无意义的机械劳动。
- 可以轻松实现多重继承。 完全兼容 CSS 代码，可以方便地应用到老项目中。LESS 只是在 CSS 语法上做了扩展，所以老的 CSS 代码也可以与 LESS 代码一同编译。
