---
title: "JS 操作 DOM"
description: "根据 id 获取一个元素。"
date: "2026-09-03"
publishedAt: "2026-09-03T16:26:56.757301+08:00"
source: "https://kajspace.cn/articles/01M1K61G6ZBJF0CA01ENZT9WY6/"
tags: ["前端"]
---

# JS 操作 DOM

## 一、查找 DOM 元素 {#kaj-h-d940e170-5403-4bed-ba75-34bd3cd2b3c0}

## 1. `getElementById` {#kaj-h-9f3c8930-6196-46af-adb4-3c86307de395}

根据 `id` 获取一个元素。

```js
const box = document.getElementById('box');

console.log(box);
```

HTML：

```html
<div id="box">Hello</div>
```

---

## 2. `getElementsByClassName` {#kaj-h-927b6666-d174-48cb-8e8a-430cdb597781}

根据 class 获取元素集合。

```js
const items = document.getElementsByClassName('item');

console.log(items);
console.log(items[0]);
```

返回的是 **HTMLCollection**。

---

## 3. `getElementsByTagName` {#kaj-h-b1597dcd-3046-497d-a49f-2a0d1e73fb00}

根据标签名获取元素集合。

```js
const divs = document.getElementsByTagName('div');

console.log(divs);
```

---

## 4. `querySelector` {#kaj-h-85930cb9-aff2-4511-93e7-a55e30945706}

**非常重要，面试最常用。**

获取第一个匹配的元素。

```js
const box = document.querySelector('#box');

const item = document.querySelector('.item');

const div = document.querySelector('div');
```

也可以使用复杂 CSS 选择器：

```js
const item = document.querySelector('.list .item');

const input = document.querySelector('input[type="text"]');
```

---

## 5. `querySelectorAll` {#kaj-h-433e8f91-5ebb-4f11-9d2d-289a2c96fdd5}

获取所有匹配的元素。

```js
const items = document.querySelectorAll('.item');

console.log(items);
```

返回 **NodeList**。

可以直接使用 `forEach`：

```js
items.forEach(item => {
    console.log(item);
});
```

---

## 二、创建 DOM 元素 {#kaj-h-c61572f5-ae46-41d2-9e0a-7e4db13ff6d6}

## `createElement` {#kaj-h-1c747405-b8a3-48e6-9ebf-e41317e68fd1}

```js
const div = document.createElement('div');
```

此时只是创建了元素：

```html
JavaScript
   ↓
createElement
   ↓
<div></div>
```

还没有放到页面中。

例如：

```js
const li = document.createElement('li');

li.textContent = '苹果';

document.body.appendChild(li);
```

页面：

```html
<li>苹果</li>
```

---

## 三、修改元素内容 {#kaj-h-e5517c3d-5dec-456e-9a94-2e08cd932245}

## 1. `textContent` {#kaj-h-3803bfd6-adb0-40b5-ab36-2ec9c6a5560d}

修改文本内容。

```js
const box = document.querySelector('.box');

box.textContent = 'Hello World';
```

原来：

```html
<div class="box">
    Hello
</div>
```

变成：

```html
<div class="box">
    Hello World
</div>
```

### 注意 {#kaj-h-e10f2704-7c1b-4c5b-9163-191585ceb4ce}

`textContent` 会把内容当成普通文本。

```html
box.textContent = '<span>Hello</span>';
```

页面会显示：

```html
<span>Hello</span>
```

而不是创建 `span`。

---

## 2. `innerHTML` {#kaj-h-57ac839b-af2b-44d2-800a-b34cb7532eb4}

修改 HTML 内容。

```html
box.innerHTML = '<span>Hello</span>';
```

此时会真正解析 HTML：

```html
<div class="box">
    <span>Hello</span>
</div>
```

### 面试区别 {#kaj-h-45ab9949-6d9a-4d8e-adbf-9fe7c19c3284}

```text
textContent
    ↓
纯文本

innerHTML
    ↓
HTML字符串
    ↓
浏览器解析成DOM
```

---

## 四、操作属性 {#kaj-h-17c2792a-a20f-4733-b5c1-f2bdf8764b5b}

## 1. 直接修改属性 {#kaj-h-d3e1af1b-993a-4277-a0a7-266ca43eb15a}

```js
const img = document.querySelector('img');

img.src = 'a.jpg';

img.alt = '图片';
```

例如：

```js
const input = document.querySelector('input');

input.value = 'hello';
input.disabled = true;
```

---

## 2. `setAttribute` {#kaj-h-e3f1fe08-7952-4411-961d-93a505dbb0ec}

设置 HTML 属性。

```js
const box = document.querySelector('.box');

box.setAttribute('id', 'container');

box.setAttribute('data-id', '100');
```

HTML：

```html
<div class="box" id="container" data-id="100"></div>
```

---

## 3. `getAttribute` {#kaj-h-08da16aa-44fc-4742-b8dd-01ea27b9a149}

获取属性。

```js
const id = box.getAttribute('id');

console.log(id);
```

---

## 4. `removeAttribute` {#kaj-h-bf6486ab-bfc7-4e2a-85fd-9b99de19a03b}

删除属性。

```text
box.removeAttribute('id');
```

---

## 5. 判断属性是否存在 {#kaj-h-9dcdda59-0686-4b14-8394-0a1a5ed2d884}

```text
box.hasAttribute('id');
```

返回：

```text
true
```

或者：

```text
false
```

---

## 五、操作 class {#kaj-h-05a1d9c1-710f-44ea-a975-fde53343b8c1}

这是前端开发非常常用的。

## `className` {#kaj-h-3102d6d4-61b7-4a27-9255-ca0ea6e8702c}

直接修改整个 class。

```text
box.className = 'box active';
```

相当于：

```html
<div class="box active"></div>
```

但注意：

```text
box.className = 'active';
```

会把原来的 class 全部覆盖掉。

---

## 六、`classList` {#kaj-h-aef19748-a3a0-4f47-9c11-6e461e96cbdf}

实际开发中更推荐。

## 1. 添加 class {#kaj-h-e11fd200-838a-4ae9-ab4b-b5a381b79589}

```text
box.classList.add('active');
```

---

## 2. 删除 class {#kaj-h-ed84d8e4-751c-482e-b0a5-e25a2d103b10}

```text
box.classList.remove('active');
```

---

## 3. 切换 class {#kaj-h-869abce3-5d0a-4e2f-928c-ed94e2227f45}

```text
box.classList.toggle('active');
```

如果没有：

```text
box
```

变成：

```text
box active
```

如果已经有：

```text
box active
```

变成：

```text
box
```

---

## 4. 判断是否存在 {#kaj-h-cb2ad476-3c88-4222-ab53-fa89906bb7f3}

```text
box.classList.contains('active');
```

---

## 七、操作 CSS 样式 {#kaj-h-177e8183-652d-4768-b20d-b6bb4edcdee8}

## 1. `style` {#kaj-h-0d996804-8b96-4746-8c2f-2031ca0c42b2}

直接修改行内样式。

```js
const box = document.querySelector('.box');

box.style.width = '100px';
box.style.height = '100px';
box.style.backgroundColor = 'red';
```

注意 CSS 属性：

```text
background-color
```

在 JS 中写成：

```text
backgroundColor
```

因为使用的是 **驼峰命名**。

---

## 2. 获取计算后的 CSS {#kaj-h-11c306fd-efa9-45bf-a61e-8e4d4f81b882}

```js
const style = getComputedStyle(box);

console.log(style.width);
console.log(style.height);
console.log(style.color);
```

这个非常容易面试问。

### 区别 {#kaj-h-88b8a45a-406d-4ca5-beaf-1112a009f8a1}

```text
box.style.width
```

主要获取**行内样式**。

而：

```text
getComputedStyle(box).width
```

获取浏览器计算后的最终样式。

例如：

```text
.box {
    width: 200px;
}
```

此时：

```text
box.style.width
```

可能是：

```text
''
```

但是：

```text
getComputedStyle(box).width
```

是：

```text
200px
```

---

## 八、添加 DOM {#kaj-h-6a9c68df-0601-4038-a309-c4be7aae184c}

## 1. `appendChild` {#kaj-h-e22ddd8c-ea26-4c07-9bc8-7fc6705cde38}

添加到最后。

```js
const ul = document.querySelector('ul');

const li = document.createElement('li');

li.textContent = '苹果';

ul.appendChild(li);
```

结构：

```text
ul
├── li
├── li
└── li（新添加）
```

---

## 2. `append` {#kaj-h-22135f5b-ae8e-4465-be82-c91b8c558cda}

也可以添加：

```text
ul.append(li);
```

甚至可以直接添加字符串：

```text
ul.append('Hello');
```

---

## 3. `prepend` {#kaj-h-38f1f9d0-4d55-45e1-b38c-466131cc0a8d}

添加到最前面。

```text
ul.prepend(li);
```

结构：

```text
ul
├── li（新添加）
├── li
└── li
```

---

## 九、插入元素 {#kaj-h-27e0d0d2-1bc3-4955-a121-130ba2538c66}

## `insertBefore` {#kaj-h-1f3be6fe-dbc0-45c6-94e0-a1fa2f49b746}

```text
parent.insertBefore(newNode, referenceNode);
```

例如：

```js
const ul = document.querySelector('ul');

const newLi = document.createElement('li');
newLi.textContent = '新元素';

const firstLi = ul.children[0];

ul.insertBefore(newLi, firstLi);
```

---

## `before / after` {#kaj-h-519dda60-3058-456e-9290-6fce56caf55c}

现代 DOM API：

```text
firstLi.before(newLi);
```

或者：

```text
firstLi.after(newLi);
```

---

## 十、删除 DOM {#kaj-h-e1e0d53d-f38d-40f3-be8a-a13df7ff2af4}

## 1. `remove` {#kaj-h-e685e8ed-ab62-4f12-bc0b-0ad8866ac23b}

现代写法：

```js
const box = document.querySelector('.box');

box.remove();
```

---

## 2. `removeChild` {#kaj-h-2063aee7-2f80-4019-8651-68d102021274}

```text
parent.removeChild(child);
```

例如：

```js
const ul = document.querySelector('ul');
const li = ul.children[0];

ul.removeChild(li);
```

---

## 十一、替换 DOM {#kaj-h-0058804a-9536-4a99-bbb2-4579c6739c6d}

## `replaceWith` {#kaj-h-7986a5d4-42a4-4549-b066-70fb5431be91}

```js
const oldBox = document.querySelector('.box');

const newBox = document.createElement('div');

newBox.textContent = '新的盒子';

oldBox.replaceWith(newBox);
```

---

## 十二、DOM 节点关系 {#kaj-h-80fa7837-5962-497c-bb87-a22ccd75b14b}

这是面试非常重要的一块。

假设：

```html
<div id="parent">
    <p id="child">Hello</p>
</div>
```

---

## 1. 父节点 {#kaj-h-3c1f9a05-9eb3-4bba-8db8-a17714a39590}

```text
child.parentNode
```

或者：

```text
child.parentElement
```

得到：

```html
<div id="parent">
```

---

## 2. 子节点 {#kaj-h-cdba4ad6-72d0-48f9-87b4-dfb743f523a8}

```text
parent.childNodes
```

获取所有子节点，包括文本节点。

---

## 3. 子元素 {#kaj-h-6bc33a44-72ba-459a-b540-dfd20dd91ebc}

```text
parent.children
```

只获取元素节点。

这个区别很重要：

```text
childNodes
    ↓
所有节点

children
    ↓
只有元素节点
```

---

## 4. 第一个子元素 {#kaj-h-62492b9c-bd88-49f3-b385-5aa67ee3e75f}

```text
parent.firstElementChild
```

---

## 5. 最后一个子元素 {#kaj-h-df0d8731-7d21-45fd-aa61-604f1bec5654}

```text
parent.lastElementChild
```

---

## 6. 下一个兄弟元素 {#kaj-h-3c32ab22-3e46-49e1-9e08-3c3bcc8e3d73}

```text
child.nextElementSibling
```

---

## 7. 上一个兄弟元素 {#kaj-h-f2c8767a-82d4-47d2-ac18-60457dafc0b6}

```text
child.previousElementSibling
```

---

## 十三、判断 DOM 关系 {#kaj-h-366e028b-eb62-43fd-8bb6-6100024e21ef}

## `contains` {#kaj-h-4892c951-6b6c-442c-819e-10d1e7be5dbd}

判断一个元素是否包含另一个元素。

```text
parent.contains(child);
```

返回：

```text
true
```

---

## `matches` {#kaj-h-14f6b488-4ed1-410e-a3d9-90d65934ca01}

判断元素是否匹配 CSS 选择器。

```js
const item = document.querySelector('.item');

item.matches('.item');
```

返回：

```text
true
```

这个在**事件委托**里面很常见。

---

## 十四、事件操作 {#kaj-h-8ba45c2d-5ebf-4fe1-8d6d-6503fcf20834}

DOM 操作一定要掌握事件。

## `addEventListener` {#kaj-h-551c7865-0fed-4331-b4ca-8a71da7db208}

```js
const button = document.querySelector('button');

button.addEventListener('click', function () {
    console.log('点击了按钮');
});
```

箭头函数：

```js
button.addEventListener('click', () => {
    console.log('点击了按钮');
});
```

---

## 常见事件 {#kaj-h-75e86e3a-8c97-4746-ac42-6d5a00169db0}

```text
click
dblclick

mousedown
mouseup
mousemove

mouseenter
mouseleave

keydown
keyup

input
change

focus
blur

submit
```

---

## 十五、事件对象 {#kaj-h-148ac4ea-6398-4ec9-830f-5345ba58ed3e}

```js
button.addEventListener('click', function (event) {
    console.log(event);
});
```

常见：

```text
event.target
event.currentTarget
event.type
```

其中最重要的是：

```text
event.target
```

表示：

> **真正触发事件的元素**

而：

```text
event.currentTarget
```

表示：

> **当前绑定事件监听器的元素**

---

## 十六、事件委托 {#kaj-h-951ff784-9bc3-4162-bc64-ea73c8af557b}

面试非常重要。

HTML：

```html
<ul id="list">
    <li>苹果</li>
    <li>香蕉</li>
    <li>西瓜</li>
</ul>
```

不要给每个 `li` 都绑定：

```js
const items = document.querySelectorAll('li');

items.forEach(item => {
    item.addEventListener('click', () => {
        console.log(item.textContent);
    });
});
```

可以利用**事件冒泡 + 事件委托**：

```js
const list = document.querySelector('#list');

list.addEventListener('click', function (event) {
    if (event.target.matches('li')) {
        console.log(event.target.textContent);
    }
});
```

核心：

```text
li 点击
 ↓
事件冒泡
 ↓
ul
 ↓
ul 统一处理
```

优点：

- 减少事件监听器数量
- 动态添加的元素也可以处理
- 性能更好

---

## 十七、阻止默认行为 {#kaj-h-0db858ce-5b55-4147-9a7d-7ec1cbc2cbfc}

```text
event.preventDefault();
```

例如阻止 `<a>` 跳转：

```js
const link = document.querySelector('a');

link.addEventListener('click', function (event) {
    event.preventDefault();

    console.log('不跳转');
});
```

---

## 十八、阻止冒泡 {#kaj-h-b2b48e5d-2548-460a-89f2-a07f357c2700}

```text
event.stopPropagation();
```

例如：

```js
child.addEventListener('click', function (event) {
    event.stopPropagation();
});
```

点击 child 后，就不会继续向父元素冒泡。

---

## 十九、获取 DOM 尺寸 {#kaj-h-f6f23f98-a172-4bfb-a498-a6cd1ad1698b}

## `offsetWidth / offsetHeight` {#kaj-h-eeb0dec2-f126-4b62-b74f-1e33be135bb7}

```js
console.log(box.offsetWidth);
console.log(box.offsetHeight);
```

通常表示元素：

> **布局尺寸，包含 padding + border**

---

## `clientWidth / clientHeight` {#kaj-h-3809acc4-b422-4a67-b6cb-170add9fb21c}

```js
console.log(box.clientWidth);
console.log(box.clientHeight);
```

通常：

> **内容 + padding，不包含 border**

---

## `scrollWidth / scrollHeight` {#kaj-h-6d66a177-ecd5-4508-8afc-dc381647bba3}

```js
console.log(box.scrollWidth);
console.log(box.scrollHeight);
```

表示：

> **元素实际内容所需要的完整尺寸，包括被滚动隐藏的部分**

---

## 二十、获取元素位置 {#kaj-h-1fd74d58-37b6-4e3f-ba99-8a8630cc2fbe}

## `getBoundingClientRect` {#kaj-h-681c61be-f535-421f-929d-0b797adcb118}

非常重要。

```js
const rect = box.getBoundingClientRect();

console.log(rect);
```

可以得到：

```text
rect.top
rect.left
rect.right
rect.bottom
rect.width
rect.height
```

例如：

```js
console.log(rect.top);
```

表示元素距离**视口顶部**的距离。

---

## 二十一、滚动 DOM {#kaj-h-10c621ff-436f-4a7a-9a13-90ddd5a78bee}

## 获取滚动距离 {#kaj-h-ee043c59-dfe6-4f1c-8b59-aed7f015c9ab}

```js
console.log(document.documentElement.scrollTop);
```

---

## 滚动到指定位置 {#kaj-h-e4e32875-2ec2-4b7b-83e1-ebbbada95186}

```text
window.scrollTo(0, 500);
```

---

## 平滑滚动 {#kaj-h-a22b0e61-ef33-4d0a-afbe-855eca43c08e}

```text
window.scrollTo({
    top: 500,
    behavior: 'smooth'
});
```

---

## 滚动元素 {#kaj-h-5184c383-1575-4283-82b3-d33cf4ddafa5}

```text
box.scrollTop = 100;
```

---

## 二十二、一个完整 DOM 操作例子 {#kaj-h-a014c950-cd6c-4fe5-94cc-432c27f3e275}

假设 HTML：

```html
<div id="app">
    <ul id="list"></ul>

    <button id="add">添加</button>
</div>
```

JS：

```js
const list = document.querySelector('#list');
const button = document.querySelector('#add');

button.addEventListener('click', () => {

    // 1. 创建元素
    const li = document.createElement('li');

    // 2. 设置文本
    li.textContent = '新的商品';

    // 3. 添加 class
    li.classList.add('item');

    // 4. 添加到 DOM
    list.appendChild(li);
});
```

整个过程就是：

```text
获取 DOM
  ↓
createElement
  ↓
修改内容
  ↓
修改属性 / class / style
  ↓
appendChild
  ↓
页面更新
```

---

## 二十三、面试最应该记住的 API {#kaj-h-9205e5cb-39d1-4fc3-9ea0-68b6beffd711}

如果你现在是为了**前端秋招面试**，不需要把所有 DOM API 都背下来，优先掌握这一张：

| 类型 | API |
| --- | --- |
| 查找 | `getElementById` |
| 查找 | `querySelector` |
| 查找 | `querySelectorAll` |
| 创建 | `createElement` |
| 内容 | `textContent` |
| 内容 | `innerHTML` |
| 属性 | `getAttribute` |
| 属性 | `setAttribute` |
| 属性 | `removeAttribute` |
| class | `classList.add` |
| class | `classList.remove` |
| class | `classList.toggle` |
| class | `classList.contains` |
| 样式 | `element.style.xxx` |
| 样式 | `getComputedStyle` |
| 添加 | `appendChild` |
| 添加 | `append` |
| 添加 | `prepend` |
| 插入 | `insertBefore` |
| 删除 | `remove` |
| 替换 | `replaceWith` |
| 父元素 | `parentElement` |
| 子元素 | `children` |
| 兄弟 | `nextElementSibling` |
| 兄弟 | `previousElementSibling` |
| 事件 | `addEventListener` |
| 事件目标 | `event.target` |
| 阻止默认 | `preventDefault` |
| 阻止冒泡 | `stopPropagation` |
| 尺寸 | `offsetWidth` |
| 尺寸 | `clientWidth` |
| 滚动尺寸 | `scrollWidth` |
| 位置 | `getBoundingClientRect` |

### 最核心的一句话 {#kaj-h-c38460e5-3499-4860-82f6-530bf1b14973}

你可以把 **JS 操作 DOM** 记成下面这个框架：

```text
① 找
querySelector

② 建
createElement

③ 改
textContent
innerHTML
style
classList
setAttribute

④ 加
append
appendChild
prepend
insertBefore

⑤ 删
remove
removeChild

⑥ 查关系
parentElement
children
nextElementSibling

⑦ 事件
addEventListener
event.target
preventDefault
stopPropagation

⑧ 尺寸位置
offsetWidth
clientWidth
scrollWidth
getBoundingClientRect
```

这套基本覆盖了**手写原生 JS DOM 题 + 前端面试 DOM 基础题**。
