---
title: "React Fiber 实现原理详解"
description: "Reconciliation、Render 与 Commit 阶段"
date: "2026-10-11"
publishedAt: "2026-10-11T10:36:41.844069+08:00"
source: "https://kajspace.cn/articles/01M4MD3H6S1VSRKH0EXHTMX95X/"
tags: ["前端"]
---

# React Fiber 实现原理详解

<span id="kaj-h-ae057673-50d3-4b66-939a-e0b5e2253fa0"></span>

Reconciliation、Render 与 Commit 阶段

## 一、Fiber 的实现原理 {#kaj-h-b299f86b-ab77-42dd-889b-d95a51c0d5d8}

### 1.1 什么是 Fiber？ {#kaj-h-c6d00cf0-aa38-444d-844a-ed0370b479f5}

Fiber 是 React 16 引入的一套核心架构。它既指 React 内部用于描述组件和工作单元的数据结构，也指基于这种数据结构实现的可中断、可恢复、可调度的更新机制。

在 Fiber 架构出现之前，React 的协调过程主要采用递归方式遍历组件树。一旦开始执行较大的更新任务，就可能长时间占用 JavaScript 主线程，导致浏览器无法及时响应用户输入和动画。

Fiber 的核心思想是：**将原本连续执行的组件更新任务拆分成多个工作单元，使 React 能够根据任务优先级灵活安排执行时机。**

需要注意，Fiber 并不等同于虚拟 DOM，也不等同于调度器。它们之间的关系可以概括为：

- **React Element：** 描述希望渲染什么 UI。
- **Fiber：** 保存组件对应的内部工作信息和更新状态。
- **Reconciliation（协调）：** 比较新旧 UI 描述，确定需要进行哪些更新。
- **Scheduler（调度器）：** 协助安排不同优先级任务的执行时机。
- **Render 阶段：** 执行协调、计算更新结果，构建新的 Fiber 工作树。
- **Commit 阶段：** 将需要提交的变更应用到真实 DOM，并执行相关提交逻辑。

### 1.2 为什么需要 Fiber？ {#kaj-h-b0294679-386a-4a97-a648-becb71348804}

假设页面有一个包含大量节点的组件树。当某个状态发生变化时，React 需要重新执行相关组件的渲染逻辑，并协调新旧 UI。

传统的同步递归更新可能存在以下问题：

1. **任务执行时间过长：** 大量组件需要依次处理。
2. **主线程被持续占用：** 浏览器难以及时处理输入、滚动和动画等任务。
3. **无法灵活调整优先级：** 一旦进入长时间的同步工作，就很难让更紧急的更新优先执行。

Fiber 通过将工作拆分成一个个 Fiber 节点对应的处理单元，让 React 可以在合适的时机暂停当前的 Render 工作，将主线程让给其他任务，之后再恢复或重新开始相关工作。

例如，用户正在输入搜索关键词时，输入框内容需要尽快更新，而庞大的搜索结果列表可以稍后更新。Fiber 架构为这种优先级调度提供了基础。

需要注意，Fiber 不会让所有更新自动变成异步任务。具体任务是否可以中断、何时让出主线程，取决于 React 使用的更新模式、优先级和调度逻辑。

### 1.3 Fiber 节点的数据结构 {#kaj-h-63ab99b3-cdcd-4a59-ba38-7ae611589a1b}

Fiber 节点是 React 内部表示组件、DOM 节点或其他工作单元的数据结构。每个 Fiber 节点都保存着处理当前组件所需的信息。

常见字段包括：

| 字段 | 作用 |
| --- | --- |
| `type` | 表示组件类型或对应的宿主元素类型 |
| `key` | 帮助 React 在同级节点之间匹配元素身份 |
| `stateNode` | 保存关联的实例或宿主节点，例如真实 DOM |
| `child` | 指向第一个子 Fiber 节点 |
| `sibling` | 指向下一个兄弟 Fiber 节点 |
| `return` | 指向父 Fiber 节点 |
| `alternate` | 指向同一个逻辑节点在另一棵 Fiber 树中的对应节点 |

其中，`child`、`sibling` 和 `return` 构成了 Fiber 树的主要遍历关系。

例如，下面的组件结构：

```js
function App() {
  return (
    <div>
      <Header />
      <Main />
    </div>
  );
}
```

可以用简化的 Fiber 关系表示：

```text
App
 └── div
      ├── Header
      └── Main
```

这里的 `div` 的 `child` 指向 `Header`，`Header` 的 `sibling` 指向 `Main`，它们的 `return` 都指向 `div`。

借助这些指针，React 可以按照工作循环逐步遍历节点，而不必完全依赖普通 JavaScript 函数调用栈进行递归。

### 1.4 Fiber 的双缓冲机制 {#kaj-h-cb23bb04-82b4-4329-a973-472bcb011bfe}

React 通常通过两棵 Fiber 树管理更新：

- **current 树：** 对应当前已经提交到界面的状态。
- **workInProgress 树：** 用于计算下一次更新结果的工作树。

当状态发生变化时，React 会基于当前树及其更新信息构建或复用 `workInProgress` 节点，执行协调工作。

当 Render 阶段完成，并且更新符合提交条件时，React 进入 Commit 阶段，将需要的变更应用到真实 DOM。提交完成后，新的 Fiber 树成为当前树。

简化流程如下：

```text
状态发生变化
    ↓
基于 current 树准备 workInProgress 树
    ↓
Render 阶段：计算新的 UI
    ↓
Commit 阶段：提交变更到真实 DOM
    ↓
workInProgress 树成为新的 current 树
```

这种机制可以理解为双缓冲：一棵树代表当前已提交的状态，另一棵树用于准备下一次状态。

需要注意，React 不一定每次都重新创建整棵树。它可以通过 `alternate` 关联并复用 Fiber 节点，具体实现会根据更新路径和节点情况决定。

### 1.5 Fiber 如何支持可中断更新？ {#kaj-h-782c4764-a2c5-48d9-a8a8-153cc4ffded9}

Fiber 将组件树更新拆解成多个工作单元，并通过工作循环依次处理。

以下代码只用于理解基本思想，并非 React 源码：

```js
let nextUnitOfWork = null;

function workLoop() {
  while (nextUnitOfWork !== null) {
    nextUnitOfWork = performUnitOfWork(nextUnitOfWork);
  }
}
```

`performUnitOfWork` 代表处理一个工作单元，并返回下一个需要处理的 Fiber 节点。

在支持可中断调度的更新中，React 不必一次性处理完整棵树。当调度机制判断需要让出主线程时，可以暂停当前工作，稍后再继续。

不过，以上代码省略了优先级判断、时间片控制、更新队列、异常处理等实际实现细节。React 的真实工作循环比这个示例复杂得多。

**总结：Fiber 的核心价值，是将组件更新组织成可管理的工作单元，并结合优先级调度，让 React 更灵活地安排 UI 更新。**

---

## 二、Reconciliation（协调）过程 {#kaj-h-02ad42d5-e356-49d9-93b1-5224876ce346}

### 2.1 什么是 Reconciliation？ {#kaj-h-b7673137-cb0c-4562-ac30-216edcef6db8}

Reconciliation，中文通常称为协调，是 React 在更新过程中比较新旧 UI 描述、确定需要进行哪些变更的过程。

例如：

```js
function App() {
  const [count, setCount] = useState(0);

  return <div>{count}</div>;
}
```

当 `count` 从 `0` 变为 `1` 时，React 会重新执行相关组件的渲染逻辑，得到新的 React Element 描述，然后协调新旧结果。

协调过程需要判断：

- 哪些节点可以继续复用？
- 哪些节点需要更新？
- 哪些节点需要新增？
- 哪些节点需要删除？

React 不会简单地把整个页面全部删除后重新创建，而是尽可能复用已有节点，只处理必要的变更。

### 2.2 Reconciliation 的基本流程 {#kaj-h-16435875-f6b3-429d-83be-2301b18a10ae}

一次典型的更新可以简化为以下过程：

```text
状态或属性发生变化
        ↓
重新执行相关组件，得到新的 React Element
        ↓
根据新旧结果协调 Fiber 节点
        ↓
标记需要新增、更新或删除的节点
        ↓
完成 Render 阶段
        ↓
Commit 阶段应用变更
```

需要注意，Reconciliation 是更新过程中的协调工作，并不是一个完全独立于 Render 阶段的阶段。React 通常在 Render 阶段执行协调，并构建新的 Fiber 工作树。

### 2.3 React 如何比较新旧节点？ {#kaj-h-a1323c79-847e-4a8d-8c93-88db9c59c779}

React 会根据节点的类型、位置以及 `key` 等信息决定是否复用节点。

#### 1. 类型相同：尽可能复用 {#kaj-h-9fde353b-a246-428a-add5-ece542b7f704}

例如：

```html
// 更新前
<div className="old">Hello</div>

// 更新后
<div className="new">Hello</div>
```

新旧元素的类型都是 `div`，React 通常可以复用原有 DOM 节点，只更新变化的属性。

这里的 `className` 从 `old` 变成了 `new`，不需要重新创建整个 `div`。

对于组件，如果对应位置上的组件类型相同，React 通常也会复用相应的 Fiber，并根据新的 props 和状态处理更新。

#### 2. 类型不同：通常替换节点 {#kaj-h-cc262d36-90b8-4db2-aec6-dabf05c31892}

例如：

```html
// 更新前
<div>Hello</div>

// 更新后
<span>Hello</span>
```

由于元素类型从 `div` 变成了 `span`，React 通常会删除原来的 DOM 节点并创建新的节点。

对于组件类型发生变化的情况，React 通常也会卸载原组件，并挂载新组件，因此原组件的局部状态通常不会保留。

#### 3. 同级列表：通过 key 匹配节点 {#kaj-h-50fff34e-675a-40f4-978c-e9e96bb8c328}

例如：

```js
const list = [
  { id: 1, name: "张三" },
  { id: 2, name: "李四" },
  { id: 3, name: "王五" },
];

function UserList() {
  return (
    <ul>
      {list.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

`key` 用于帮助 React 在同级节点之间识别元素身份。当列表发生插入、删除或排序时，稳定且唯一的 `key` 能帮助 React 更准确地匹配新旧节点。

例如，原列表为：

```text
A → B → C
```

更新后变成：

```text
C → A → B
```

如果使用稳定的 `key`，React 就可以根据节点身份识别出这些元素，而不是只根据数组下标判断它们是否相同。

需要注意：

- `key` 应当在同级列表中唯一。
- `key` 不会作为普通 prop 自动传给子组件。
- 不推荐在可能发生插入、删除或排序的列表中使用数组下标作为 `key`，因为这可能造成节点与数据错配。
- `key` 不是直接操作 DOM 的指令，而是协调过程中用于匹配节点的重要信息。

### 2.4 Reconciliation 与 Diff 算法 {#kaj-h-3f059500-c178-4cfc-a46a-f4feeca968a7}

在理想情况下，对任意两棵树进行完整比较可能产生较高的计算成本。React 利用一些启发式规则降低比较复杂度。

常见原则包括：

1. **不同类型的元素通常生成不同的树。** 当元素类型变化时，React 通常会替换对应子树。
2. **同级节点通过 key 识别身份。** 稳定的 key 有助于复用对应节点。
3. **优先比较同级节点。** React 不会对新旧树中的任意节点进行全面的跨层级搜索。

React 的协调并不等于对整棵树执行一个完全通用的最优树编辑算法，而是采用针对 UI 场景设计的比较策略。

对于列表，React 会根据新旧子节点的类型和 key 进行匹配，并结合节点位置等信息决定复用、插入、移动或删除等操作。具体算法比简单的逐项比较更复杂。

### 2.5 Reconciliation 的结果是什么？ {#kaj-h-504ba53d-d93c-4fb1-849a-21048b85ae5d}

协调的结果不是立即完成所有 DOM 操作，而是计算出下一次 UI 应当如何变化。

在 Fiber 架构中，React 会构建或更新 `workInProgress` Fiber 树，并记录后续提交需要处理的工作，例如：

- 插入新的 DOM 节点。
- 更新已有 DOM 节点的属性。
- 删除不再需要的 DOM 节点。
- 执行与组件生命周期、引用或副作用相关的提交工作。

这些工作会在 Commit 阶段按照 React 的提交逻辑执行。

### 2.6 Reconciliation 的几个重要特点 {#kaj-h-5b2a3547-3379-40fa-8921-d9d8f6baf082}

**第一，协调不一定意味着 DOM 变化。**

组件重新执行后，即使产生了新的 React Element，最终也可能没有需要提交的 DOM 变更。

**第二，Render 阶段的工作可能被重新执行。**

在支持可中断调度的更新中，Render 工作可能被暂停、恢复或重新开始。因此，不应该在组件渲染过程中执行不可重复的副作用，例如直接发送不受控的请求或修改外部变量。

**第三，协调并不保证所有节点都复用。**

React 会根据元素类型、key 和节点结构决定是否复用。类型变化、key 变化等情况可能导致原组件卸载并重新挂载。

**总结：Reconciliation 的核心是比较新旧 UI 描述，决定 Fiber 节点如何复用和变化，并为后续提交准备更新结果。**

---

## 三、Render 和 Commit 阶段 {#kaj-h-6428f5ed-5e1b-4d95-99b5-26adfc4066ec}

React 的一次典型更新可以划分为两个主要阶段：Render 阶段和 Commit 阶段。

它们的核心区别是：

- **Render 阶段：计算 UI 应当如何变化。**
- **Commit 阶段：将计算得到的变更提交到宿主环境，例如真实 DOM。**

### 3.1 Render 阶段 {#kaj-h-373d1b2f-9d4f-4709-9dc0-f968c6621859}

Render 阶段负责计算下一次 UI 的结果。它包括组件渲染、Reconciliation、Fiber 工作树的构建或更新，以及相关副作用标记等工作。

#### Render 阶段的执行流程 {#kaj-h-5a682c94-3359-46e4-816b-1777983b64ff}

```text
状态更新被触发
      ↓
React 根据更新信息安排工作
      ↓
执行相关组件的渲染逻辑
      ↓
生成新的 React Element
      ↓
协调新旧节点，处理 Fiber 工作单元
      ↓
形成新的 workInProgress 树
      ↓
Render 工作完成，等待提交
```

例如：

```js
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      {count}
    </button>
  );
}
```

当用户点击按钮后，`setCount` 触发状态更新。React 会根据新的状态重新执行相关组件，得到新的 UI 描述，并协调新旧结果。

如果原来按钮显示 `0`，现在应该显示 `1`，React 就会在协调过程中识别文本内容的变化，为后续提交准备对应工作。

#### Render 阶段的特点 {#kaj-h-fe5c8332-b0cf-4bd6-b63f-893c9f65109b}

**1. 主要负责计算，不直接完成最终 DOM 提交。**

Render 阶段会计算出需要发生的变化，但通常不会在这个阶段把这些变化应用到真实 DOM。

**2. 在支持可中断调度的更新中，可以让出主线程。**

React 可以将 Render 工作分段处理，让浏览器有机会执行其他任务。之后，React 可以恢复工作，也可能因为新的更新而重新计算。

**3. 组件渲染逻辑可能执行多次。**

例如，开发环境开启 `StrictMode` 时，React 可能额外执行某些渲染逻辑，以帮助发现不纯的渲染代码。因此，组件函数应该保持纯粹：相同的输入应产生相同的 UI 描述，不应在渲染过程中直接产生不可重复的副作用。

**4. Render 阶段不保证一定进入 Commit 阶段。**

如果某次计算被更高优先级的更新取代，或者遇到其他需要放弃当前工作的情况，React 可能不会提交那次计算结果。

### 3.2 Commit 阶段 {#kaj-h-5c4571a2-cddc-48a6-971a-77beb0f15289}

Commit 阶段负责将 Render 阶段计算出的变更应用到真实 DOM，并执行与提交相关的操作。

在客户端 DOM 渲染中，这通常包括 DOM 的插入、更新和删除，以及相关引用和副作用的处理。

#### Commit 阶段的执行流程 {#kaj-h-4dfb5d88-afd6-4fc3-9410-c8555063581e}

```text
Render 阶段完成
      ↓
进入 Commit 阶段
      ↓
执行必要的 DOM 插入、更新和删除
      ↓
处理相关的引用及提交阶段副作用
      ↓
执行布局相关的生命周期和 Effects 处理
      ↓
浏览器在适当时机绘制更新后的界面
```

以上是便于理解的简化流程。React 内部会进一步区分提交前、DOM mutation、布局相关工作和被安排在提交后的 Effects 等处理，不同类型的 Effect 并不都在同一个时机执行。

例如，组件中使用：

```js
function Counter() {
  const [count, setCount] = useState(0);

  useLayoutEffect(() => {
    console.log("layout effect");
  }, [count]);

  useEffect(() => {
    console.log("passive effect");
  }, [count]);

  return <div>{count}</div>;
}
```

当 `count` 更新后：

- React 在 Render 阶段计算新的 UI。
- Commit 阶段将相应变化应用到 DOM。
- `useLayoutEffect` 在 DOM 变更之后、浏览器绘制前的布局相关时机执行。
- `useEffect` 属于被动 Effect，通常在提交后安排执行；具体是否在浏览器绘制前执行，取决于更新来源和调度时机，不能简单地认为它一定在绘制后执行。

如果需要在更新后读取布局信息，或者在用户看到画面之前同步调整布局，通常应关注 `useLayoutEffect`；一般的数据订阅和副作用更适合使用 `useEffect`。

#### Commit 阶段的特点 {#kaj-h-a1fc9258-183d-4e97-965b-230f3ee688cb}

**1. 负责应用变更。**

Render 阶段只是计算更新结果，Commit 阶段才会将相应变更应用到真实 DOM。

**2. 不会像可中断的 Render 工作那样任意暂停。**

Commit 阶段需要保持提交操作的一致性。React 不会把一个正在执行的 Commit 阶段随意切成多个可让出主线程的工作片段。

因此，即使 Render 阶段可以被中断，如果 Commit 阶段本身需要执行大量工作，仍然可能造成主线程阻塞。

**3. 不一定每次更新都产生 DOM 变更。**

即使组件重新执行并完成协调，如果没有需要应用的 DOM 变更，提交过程也不意味着必须插入、删除或修改 DOM 节点。

### 3.3 Render 与 Commit 的对比 {#kaj-h-487e7c41-2d4f-4699-b5d9-b0bb90259c4b}

| 对比维度 | Render 阶段 | Commit 阶段 |
| --- | --- | --- |
| 核心任务 | 计算下一次 UI | 应用计算结果 |
| 主要工作 | 组件渲染、协调、构建或更新 Fiber 树 | DOM 变更、引用处理、提交相关副作用 |
| 是否直接修改最终 DOM | 通常不负责应用最终 DOM 变更 | 负责应用相应 DOM 变更 |
| 是否可以中断 | 在支持可中断调度的更新中可以 | 不会像 Render 一样任意中断 |
| 是否可能重新执行 | 可能 | 提交逻辑按 React 的提交流程执行 |
| 是否一定导致 DOM 变化 | 不一定 | 也不一定存在实际 DOM 变更 |

### 3.4 从状态更新到页面显示的完整流程 {#kaj-h-c95613d8-ce2a-44de-b01c-7eb3249fed62}

结合 Fiber、Reconciliation、Render 和 Commit，可以将 React 更新流程串联起来：

```text
用户点击按钮
      ↓
调用 setState
      ↓
React 记录更新并安排调度
      ↓
Render 阶段
  ├─ 重新执行相关组件
  ├─ 生成新的 React Element
  ├─ Reconciliation 协调新旧节点
  ├─ 构建或更新 workInProgress Fiber 树
  └─ 标记需要提交的变更
      ↓
Commit 阶段
  ├─ 应用 DOM 变更
  ├─ 处理相关引用
  └─ 执行相应提交阶段工作
      ↓
浏览器在适当时机绘制界面
```

这里有几个容易混淆的概念：

1. `setState` 并不意味着立即同步修改 DOM，它会触发 React 的更新流程。
2. React 组件重新执行，并不意味着所有真实 DOM 节点都会重新创建。
3. Render 阶段完成，不代表用户已经看到更新后的界面。
4. Commit 阶段完成 DOM 变更，也不代表浏览器已经完成像素绘制。
5. 浏览器绘制时机还受到主线程任务、样式计算、布局、合成及浏览器调度等因素影响。

---

## 四、总结 {#kaj-h-3fbb0f32-9b05-4d6e-a089-cbac1e691dda}

理解 React Fiber，重点是区分三个层次：

**第一，Fiber 是基础架构。** 它通过 Fiber 节点和工作循环组织组件树更新，为可中断、可恢复和优先级调度提供基础。

**第二，Reconciliation 是协调过程。** 它比较新旧 UI 描述，结合元素类型、key 和节点结构决定哪些节点可以复用，哪些需要新增、更新或删除。

**第三，Render 和 Commit 是更新的两个主要阶段。** Render 负责计算新的 UI 和协调结果；Commit 负责将相应变更应用到真实 DOM，并执行提交相关操作。

面试时可以这样回答：

React Fiber 是 React 16 引入的核心架构。它把组件树的更新拆分为多个工作单元，通过 Fiber 节点之间的 `child`、`sibling` 和 `return` 等关系遍历组件树，并结合调度机制实现更新工作的灵活安排。

当状态发生变化时，React 首先进入 Render 阶段，重新执行相关组件，通过 Reconciliation 比较新旧 UI 描述，构建或更新 `workInProgress` Fiber 树，并确定需要进行哪些变更。在支持可中断调度的更新中，这个阶段可以暂停、恢复或重新开始。Render 完成后，React 进入 Commit 阶段，将需要的变更应用到真实 DOM，并处理相关引用和副作用。最后，浏览器在适当时机完成绘制。

**一句话记忆：Fiber 解决更新任务如何组织和调度的问题，Reconciliation 解决新旧 UI 如何比较的问题，Render 负责计算，Commit 负责提交。**
