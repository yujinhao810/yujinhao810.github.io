---
title: Vue 2 与 Vue 3 响应式原理详解
category: vue
description: 从 Observer、Dep、Watcher 到 Proxy、track、trigger 和 ReactiveEffect，系统对比 Vue 2 与 Vue 3 的响应式机制及 computed、watch 的使用边界。
date: "2026-10-28"
publishedAt: "2026-10-28T10:49:27+08:00"
tags:
  - Vue 2
  - Vue 3
  - 响应式原理
  - Proxy
  - 前端八股
---

# Vue 2 与 Vue 3 响应式原理详解

## 一、什么是响应式？

响应式是 Vue 的核心特性之一。它能够在数据发生变化时，自动更新依赖这些数据的计算结果或视图，从而减少开发者手动操作 DOM 的工作。

例如：

```js
const state = {
  count: 0
};
```

当 `count` 发生变化时，如果页面使用了这个属性，Vue 就会在适当的时机更新视图。

要实现这种能力，框架需要解决三个问题：

1. **如何检测数据变化？**
2. **如何知道哪些代码依赖了这个数据？**
3. **数据变化后，如何执行相应的更新任务？**

Vue 2 和 Vue 3 都围绕这三个问题构建响应式系统，但底层实现存在明显区别。

- Vue 2：基于 `Object.defineProperty()`，使用 `Observer`、`Dep` 和 `Watcher` 等机制。
- Vue 3：基于 `Proxy`，通过依赖追踪、依赖触发和 `ReactiveEffect` 等机制实现响应式。

## 二、Vue 2 的响应式原理

Vue 2 主要使用 `Object.defineProperty()` 劫持对象已有属性的读取和修改，并通过依赖收集机制追踪属性与相关任务之间的关系。

### 2.1 Observer：将普通对象转换为响应式对象

`Observer` 是 Vue 2 响应式系统中的一个核心实现。

当 Vue 初始化数据时，会对对象进行观测。对于普通对象，Vue 会遍历其属性，并通过 `Object.defineProperty()` 为属性定义 getter 和 setter。

例如，原始数据如下：

```js
const data = {
  name: 'Tom',
  age: 18
};
```

Vue 2 会将相关属性转换为具有 getter 和 setter 的响应式属性。

可以将其简化理解为：

```js
let value = 'Tom';

Object.defineProperty(data, 'name', {
  enumerable: true,
  configurable: true,

  get() {
    return value;
  },

  set(newValue) {
    value = newValue;
  }
});
```

以上代码仅用于解释原理，省略了 Vue 2 实际实现中的依赖收集、变化判断以及嵌套对象处理等逻辑。

Observer 的主要职责是建立响应式观测机制，而不是直接负责执行组件更新。

需要注意，Vue 2 对数组采用了特殊处理，例如通过改写 `push()`、`pop()`、`splice()` 等变异方法来侦测数组变化。

### 2.2 getter 和 setter：依赖收集与更新通知

Vue 2 使用 getter 和 setter 拦截属性访问与修改。

- getter：属性被读取时，尝试收集当前任务的依赖。
- setter：属性被修改且检测到有效变化时，通知相关依赖更新。

例如：

```js
this.count;
```

当组件渲染过程中读取 `count` 时，getter 可以收集当前渲染任务。

当执行：

```js
this.count++;
```

setter 会检测变化，并通知相关依赖。

因此，可以将 getter 和 setter 分别理解为依赖收集与更新通知的重要入口。

### 2.3 Dep：依赖管理器

`Dep` 是 Vue 2 中用于管理响应式依赖的内部实现。

每个响应式属性通常关联一个 Dep 实例，用于记录依赖该属性的 Watcher。

Dep 主要承担两个职责：

1. 收集依赖。
2. 在数据变化时通知相关依赖。

例如，一个组件只读取了 `count`，却没有读取 `name`，那么 `name` 变化时，不需要仅仅因为该组件存在，就触发这个组件的渲染更新。

Dep 负责维护属性与相关 Watcher 之间的联系，使 Vue 能够针对变化更新必要的任务。

### 2.4 Watcher：执行响应式任务

`Watcher` 是 Vue 2 响应式系统中的另一个核心内部类。

它可以执行某个表达式或函数，并在执行过程中收集所依赖的数据。当相关数据变化时，Watcher 会执行相应的处理逻辑。

按照用途，可以将其理解为以下几类：

- **渲染 Watcher**：负责组件的渲染更新。
- **计算属性 Watcher**：支撑计算属性的惰性求值和缓存。
- **用户 Watcher**：支撑开发者通过 `watch` 选项声明的侦听逻辑。

这些是不同用途的 Watcher，并不意味着它们分别对应一个同名的公开 API。

### 2.5 Vue 2 的完整响应式流程

Vue 2 的响应式流程可以简化为：

```text
初始化数据
    ↓
Observer
    ↓
Object.defineProperty()
    ↓
为属性定义 getter / setter
    ↓
组件渲染或其他任务读取属性
    ↓
getter 收集 Watcher 到 Dep
    ↓
数据发生变化
    ↓
setter 通知 Dep
    ↓
Dep 通知相关 Watcher
    ↓
执行相应任务或安排更新
```

其中，组件渲染更新通常还涉及异步更新队列，因此数据变化并不意味着 DOM 一定会在同一行代码执行后立即完成更新。

## 三、Vue 3 的响应式原理

Vue 3 重构了底层响应式系统，核心机制从 `Object.defineProperty()` 转向 `Proxy`。

Vue 3 的响应式系统不再依赖 Vue 2 那套 `Observer`、`Dep`、`Watcher` 组合来实现全部功能，而是通过代理拦截、依赖追踪、依赖触发以及响应式任务调度等机制完成更新。

### 3.1 Proxy：代理整个对象

`Proxy` 是 JavaScript 提供的代理机制，可以拦截对象的属性读取、修改、删除等操作。

例如：

```js
const data = {
  name: 'Tom',
  age: 18
};

const proxy = new Proxy(data, {
  get(target, key, receiver) {
    console.log('读取属性：', key);

    return Reflect.get(target, key, receiver);
  },

  set(target, key, value, receiver) {
    const result = Reflect.set(
      target,
      key,
      value,
      receiver
    );

    console.log('修改属性：', key);

    return result;
  }
});

proxy.name;
proxy.age = 20;
proxy.gender = '男';
```

这段代码展示了 JavaScript 原生 Proxy 的基本用法，并非 Vue 3 的完整响应式实现。

Vue 3 通过 `reactive()` 等 API 封装代理机制，让对象具备响应式能力。

与 Vue 2 相比，Proxy 的重要优势在于可以拦截对象的新增属性、删除属性等操作，而不需要像 Vue 2 那样针对新增属性使用 `Vue.set()` 等特殊处理方式。

### 3.2 track()：收集依赖

Proxy 负责拦截对象操作，但仅仅知道属性被读取还不够。

Vue 还需要知道：究竟是哪个响应式任务读取了这个属性？

这就是 `track()` 的作用。

例如：

```js
const state = reactive({
  count: 0
});
```

当组件渲染过程中读取：

```js
state.count;
```

Proxy 的 `get` 拦截器会进入 Vue 的依赖追踪逻辑。

Vue 记录当前正在执行的响应式任务，并建立该任务与 `count` 属性之间的依赖关系。

可以将依赖关系概念性地理解为：

```text
target 对象
  └── count 属性
       ├── 组件渲染任务
       ├── watchEffect 对应的任务
       └── 其他依赖 count 的响应式任务
```

这里的结构只是帮助理解的示意，并不是 Vue 内部数据结构的完整表示。

### 3.3 trigger()：触发依赖

当响应式属性发生变化时，Vue 需要找到依赖该属性的任务，并触发相应的处理机制。

这就是 `trigger()` 的作用。

例如：

```js
state.count++;
```

Proxy 的 `set` 拦截器会处理这次修改，并进入相关的依赖触发逻辑。

Vue 根据目标对象、属性和操作类型等信息，找到受到影响的依赖，并触发相关任务。

因此，可以将 Vue 3 的依赖追踪过程概括为：

- `track()`：建立属性与响应式任务之间的依赖关系。
- `trigger()`：在相关数据变化时，触发受到影响的响应式任务。

需要注意，`track()` 和 `trigger()` 不是直接挂载在每个 Proxy 对象上的方法，而是 Vue 内部响应式系统使用的机制。

### 3.4 ReactiveEffect：响应式任务的底层机制

`ReactiveEffect` 是理解 Vue 3 响应式系统的重要概念。

可以将它理解为一种能够追踪依赖、并在相关依赖发生变化时重新执行或触发相应处理的底层任务机制。

例如，下面是用于理解原理的示意代码：

```js
import { reactive, effect } from '@vue/reactivity';

const state = reactive({
  count: 0
});

effect(() => {
  console.log('当前 count：', state.count);
});

state.count++;
```

概念上，输出为：

```text
当前 count：0
当前 count：1
```

执行过程如下：

1. 首次执行函数。
2. 函数读取 `state.count`。
3. Vue 追踪这次读取，建立依赖关系。
4. 修改 `state.count`。
5. Vue 触发相关依赖，使对应任务再次执行。

这里需要区分：`ReactiveEffect` 是底层机制，而 `effect()` 是用于创建和运行响应式副作用的接口。它们都不应与 `watch()` 直接画等号。

在普通 Vue 3 业务代码中，开发者更常使用 `computed()`、`watch()` 和 `watchEffect()` 等公开 API，而不是直接调用底层 `effect()`。

### 3.5 Vue 3 的完整响应式流程

```text
reactive()
    ↓
Proxy 代理对象
    ↓
读取属性
    ↓
get 拦截器调用 track()
    ↓
建立依赖关系
    ↓
修改属性
    ↓
set 等拦截器进入 trigger() 逻辑
    ↓
找到受到影响的响应式任务
    ↓
ReactiveEffect 及相关调度机制
    ↓
执行相应任务或安排更新
```

这里的流程是简化模型。实际 Vue 3 实现还包含依赖失效处理、任务调度、组件更新队列以及不同类型响应式任务的特殊逻辑。

## 四、Vue 2 与 Vue 3 响应式原理的区别

| 对比项 | Vue 2 | Vue 3 |
| --- | --- | --- |
| 核心机制 | `Object.defineProperty()` | `Proxy` |
| 响应式初始化 | `Observer` | `reactive()` 等 API |
| 属性读取 | getter | Proxy 的 `get` |
| 属性修改 | setter | Proxy 的 `set` 等操作 |
| 依赖收集 | `Dep` 收集 Watcher | `track()` 等依赖追踪机制 |
| 更新通知 | `Dep.notify()` 等机制 | `trigger()` 等触发机制 |
| 响应式任务 | `Watcher` | `ReactiveEffect` 及相关调度机制 |
| 新增属性 | 需要 `Vue.set()` 等特殊处理 | 可以通过代理追踪新增属性 |
| 删除属性 | 需要 `Vue.delete()` 等特殊处理 | 可以通过代理追踪删除操作 |
| 数组响应式 | 对数组变异方法进行特殊处理 | 通过代理机制追踪相关操作 |
| 嵌套对象 | 初始化时递归观测 | 访问嵌套对象时按需建立代理 |
| 上层 API | 支持 `computed`、`watch` 等 | 保留相应功能，并提供 Composition API |

需要特别说明：表中的对应关系是概念层面的对比，并非内部实现的一对一替换。

例如，Vue 2 的 `Dep` 与 Vue 3 的依赖追踪机制在职责上具有相似性，但不能认为二者内部实现完全相同。同样，Vue 2 的 `Watcher` 与 Vue 3 的 `ReactiveEffect` 也不是完全等价的类。

## 五、Vue 2 和 Vue 3 都有 computed 和 watch 吗？

有。`computed` 和 `watch` 并不是 Vue 3 才出现的功能。

需要区分的是：它们作为开发者使用的功能 API，与框架内部用于实现这些功能的类和机制并不是一回事。

### 5.1 Vue 2 的 computed

Vue 2 常见的写法是 Options API：

```js
export default {
  data() {
    return {
      count: 1
    };
  },

  computed: {
    doubleCount() {
      return this.count * 2;
    }
  }
};
```

`doubleCount` 是计算属性。

Vue 2 内部使用 Computed Watcher 等机制实现计算属性的惰性求值与缓存。

当依赖发生变化时，计算属性的缓存会失效；在下一次读取时，Vue 才会根据最新数据重新计算。

### 5.2 Vue 3 的 computed()

Vue 3 Composition API 常见写法：

```js
import { ref, computed } from 'vue';

const count = ref(1);

const doubleCount = computed(() => {
  return count.value * 2;
});
```

`computed()` 返回一个计算属性引用。

计算属性会自动追踪 getter 中读取的响应式依赖，并缓存计算结果。依赖没有变化时，重复读取不会导致 getter 重新计算。

需要注意，计算属性适合派生数据，而不是承担异步请求等副作用管理。

### 5.3 Vue 2 的 watch

Vue 2 常见写法：

```js
export default {
  data() {
    return {
      count: 0
    };
  },

  watch: {
    count(newValue, oldValue) {
      console.log(oldValue, '->', newValue);
    }
  }
};
```

这里：

- `count` 是监听的数据属性名。
- `newValue` 是变化后的值。
- `oldValue` 是变化前的值。

Vue 会在符合触发条件时自动调用回调函数，不需要开发者手动传入新旧值。

Vue 2 内部通过 User Watcher 等机制实现这类侦听行为。

### 5.4 Vue 3 的 watch()

Vue 3 Composition API 常见写法：

```js
import { ref, watch } from 'vue';

const count = ref(0);

watch(count, (newValue, oldValue) => {
  console.log(oldValue, '->', newValue);
});
```

`watch()` 监听指定的数据源，当数据变化且满足触发条件时，执行回调。

它支持 `immediate`、`deep`、`flush` 等选项，可用于异步请求、数据持久化和其他副作用。

Vue 3 还提供 `watchEffect()`，它会立即执行传入的函数，并自动追踪函数同步执行过程中读取的响应式数据。

### 5.5 Watcher 和 watch() 的区别

这是一个容易混淆的知识点。

- `Watcher`：Vue 2 的内部实现类。
- `watch`：Vue 2 Options API 中的组件选项。
- `watch()`：Vue 3 Composition API 中的公开侦听函数。
- `ReactiveEffect`：Vue 3 底层响应式任务机制之一。

因此，不能简单地说 Vue 2 的 `Watcher` 在 Vue 3 中直接变成了 `watch()`。

更准确的理解是：Vue 2 中由 Watcher 等内部机制支撑的不同任务，在 Vue 3 中由重构后的响应式机制及相应 API 实现。

## 六、computed 和 watch 的区别

`computed` 和 `watch` 在 Vue 2 与 Vue 3 中具有一致的核心用途，但具体使用形式取决于所采用的 API 风格。

| 对比项 | computed | watch |
| --- | --- | --- |
| 核心用途 | 计算派生数据 | 监听数据变化并执行副作用 |
| 依赖声明 | 自动收集 | 通常显式指定监听源 |
| 缓存 | 有缓存 | 不具有计算属性式的缓存机制 |
| 新旧值参数 | 不以回调参数为主要用途 | 回调可以接收新值和旧值 |
| 异步操作 | 不适合管理异步副作用 | 适合异步请求和后续处理 |
| 常见场景 | 筛选、统计、格式化数据 | 请求接口、保存数据、执行业务操作 |

### 6.1 computed：计算派生数据

例如：

```js
const price = ref(100);
const quantity = ref(2);

const totalPrice = computed(() => {
  return price.value * quantity.value;
});
```

`totalPrice` 是从 `price` 和 `quantity` 计算得到的派生数据。

当依赖发生变化时，计算属性缓存失效，并在下一次读取时重新计算。

计算属性的 getter 可以返回 Promise，但这并不意味着 Vue 会自动等待异步操作完成并管理加载状态。因此，通常不推荐使用 computed 管理异步请求。

计算属性也支持 getter/setter 形式的可写计算属性。setter 在计算属性被赋值时调用，而不是在其依赖变化时自动调用。

### 6.2 watch：监听变化并执行副作用

例如：

```js
const keyword = ref('');

watch(keyword, async (newValue, oldValue) => {
  console.log(oldValue, '->', newValue);

  // 根据关键词请求接口
  // const result = await fetchProducts(newValue);
});
```

这里的目标不是计算一个派生值，而是在关键词变化时执行接口请求。

`watch()` 可以使用 `immediate: true` 立即执行回调，也可以使用 `deep: true` 追踪嵌套对象或数组的变化。

需要注意，深度监听对象内部属性变化时，`newValue` 和 `oldValue` 可能指向同一个对象，因为对象引用本身没有发生变化。

## 七、为什么 Vue 3 不再沿用 Vue 2 的响应式实现？

Vue 3 使用 Proxy，不只是为了替换 getter 和 setter，而是为了让响应式系统能够更自然地处理对象操作，并重新组织依赖追踪机制。

主要区别包括：

1. **能够拦截更多对象操作。** Proxy 可以处理属性新增、删除等操作，而 Vue 2 对这些情况需要额外处理。
2. **不需要为每个已有属性逐一定义 getter/setter。** Proxy 从对象操作层面进行拦截。
3. **重构依赖追踪与更新机制。** Vue 3 通过依赖追踪、Reactive Effect 和调度机制组织不同响应式任务。
4. **保留开发者熟悉的功能。** 计算属性、侦听器、组件自动更新等功能继续存在，同时提供 Composition API 等使用方式。

但 Proxy 并不意味着所有 JavaScript 数据都自动具备响应式能力。普通局部变量的赋值无法被 Vue 自动拦截，Vue 也需要通过 `ref()` 等机制来处理基本类型数据。

## 八、总结

理解 Vue 2 与 Vue 3 的响应式原理，最重要的是区分底层机制与上层 API。

### Vue 2

```text
Observer
   ↓
Object.defineProperty()
   ↓
getter / setter
   ↓
Dep
   ↓
Watcher
   ↓
执行任务或更新视图
```

### Vue 3

```text
reactive() + Proxy
   ↓
get / set 等拦截操作
   ↓
track() / trigger()
   ↓
ReactiveEffect + 调度机制
   ↓
执行任务或更新视图
```

记忆要点：

- **Observer / Proxy**：建立响应式观测机制。
- **getter / track**：收集依赖。
- **setter / trigger**：触发相关依赖。
- **Dep / 依赖关系管理**：记录属性与任务之间的联系。
- **Watcher / ReactiveEffect**：理解响应式任务的执行机制。
- **computed**：计算并缓存派生数据。
- **watch**：监听数据变化并执行回调。

最后要强调：这些对应关系主要用于帮助理解原理，并不是 Vue 2 和 Vue 3 内部实现的一对一替换。Vue 3 的核心变化是底层响应式机制的重构，而不是简单地将几个旧类替换成新名字。

面试时，如果能够讲清楚数据变化如何被检测、依赖如何收集、任务如何触发，以及 computed 和 watch 的用途区别，就已经掌握了这部分知识的核心。
