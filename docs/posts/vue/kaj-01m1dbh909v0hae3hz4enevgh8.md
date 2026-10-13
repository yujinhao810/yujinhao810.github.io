---
title: "面试官：你封装过组件吗？"
description: "面试官问：“你封装过组件吗？举两个例子。”"
date: "2026-09-01"
publishedAt: "2026-09-01T10:07:53.288265+08:00"
source: "https://kajspace.cn/articles/01M1DBH909V0HAE3HZ4ENEVGH8/"
tags: ["前端"]
---

# 面试官：你封装过组件吗？

## 一、面试时的简短回答 {#kaj-h-325ba4a8-f416-412e-a559-7e579b99e362}

面试官问：“你封装过组件吗？举两个例子。”

可以这样回答：

> 封装过两个偏业务的复用组件。
> 
> 
> 
> 第一个是 `DisasterResultImage`，用于展示各类灾害成果图。不同页面原本都需要自己处理接口请求、Blob 图片转换、加载状态、错误状态、图片预览和 Blob URL 释放。我把这些逻辑集中到组件内部，父组件只需要传入灾害文件类型和煤层 ID，就可以完成图片加载和预览。
> 
> 
> 
> 第二个是 `RiskAssessment`，用于展示不同灾害类型的风险评价。瓦斯、火灾、水害、采空区等页面使用的是相同的展示结构，区别只是灾害类型不同，所以我通过 `type` 和 `descriptionOnly` 两个 Props 抽取成公共业务组件，组件内部负责请求风险评价接口并展示结果。
> 
> 
> 
> 这两个组件的区别是：`DisasterResultImage` 更偏资源加载和生命周期管理，`RiskAssessment` 更偏业务数据和展示逻辑复用。

## 二、什么才叫“封装组件” {#kaj-h-e7f0e2db-746b-4959-a2c7-2b2dc9f8eea2}

封装组件不只是把一段 HTML 拆到一个 `.vue` 文件中，至少包含四个方面：

1. **定义清晰的输入**

   

   通过 `props` 接收外部参数，例如：

   

   ```html
   <DisasterResultImage
     :type="DISASTER_FILE_TYPES.GAS_RESULT"
     height="258px"
   />
   ```
2. **隐藏内部实现**

   

   父组件不需要知道：

   

   - 请求地址是什么
   - 请求返回的是 Blob 还是 JSON
   - 如何生成图片 URL
   - 如何处理加载失败
   - 如何销毁 Blob URL
3. **提供稳定的交互接口**

   

   常见方式有：

   

   - `emit`：子组件通知父组件
   - `slot`：父组件传入可变内容
   - `defineExpose`：父组件调用子组件的命令式方法
4. **解决重复问题**

   

   如果三个、五个甚至八个页面都要写同样的逻辑，就适合抽成组件。

所以面试时不要只说“我把代码抽成了组件”，而要说清楚：

> 重复逻辑是什么，组件对外暴露了什么，内部隐藏了什么，复用后减少了什么成本。

## 三、组件案例一：`DisasterResultImage` {#kaj-h-2c1f9104-1d1d-4d43-9d12-5d9b6a40dd60}

文件位置：

`DisasterResultImage.vue`

## 3.1 为什么需要这个组件 {#kaj-h-09d39210-b2a7-4f44-8775-275c97ab2557}

项目中很多灾害模块都需要展示成果图，例如：

- 瓦斯成果图
- 火灾成果图
- 水害成果图
- 冲击地压成果图
- 地质构造成果图
- 采空区成果图
- 封闭不良钻孔成果图

如果每个页面都自己处理，就会重复出现：

```js
const loading = ref(false)
const imageUrl = ref('')
const error = ref('')

const loadImage = async () => {
  const blob = await getViewByType(...)
  imageUrl.value = URL.createObjectURL(blob)
}
```

同时还要处理：

- 接口返回二进制文件
- `Blob.type` 为空
- 图片预览
- 图片加载失败
- 请求切换时的数据竞争
- 旧 Blob URL 释放
- 组件销毁后的清理

因此，这个组件不是单纯的图片标签，而是一个“灾害成果图加载与预览业务组件”。

---

## 3.2 组件对外提供了什么 {#kaj-h-55a74857-9f2d-4b1f-8238-30adc94a77e0}

### Props {#kaj-h-659d12e6-5883-488a-ac16-35c86ad49cdd}

代码位于 `DisasterResultImage.vue`。

| 参数 | 类型 | 作用 |
| --- | --- | --- |
| `type` | `Number/String` | 成果图类型，必填 |
| `coalLayerId` | `Number/String` | 可选的煤层 ID |
| `alt` | `String` | 图片替代文本 |
| `height` | `String` | 图片容器高度 |

父组件不需要传入：

- 图片 URL
- `loading`
- `error`
- `previewVisible`
- Blob 对象

这些都由子组件内部管理。

### 对外暴露的方法 {#kaj-h-3b4f1ef3-606d-4949-ab87-1bd66b4c9d4b}

```js
const openPreview = () => {
  if (!src.value || loading.value) return
  previewVisible.value = true
}

defineExpose({ openPreview })
```

这表示父组件可以通过模板 ref 调用：

```text
gasResultImage.value?.openPreview()
```

这个方法不是普通的事件，而是子组件主动暴露出来的命令式 API。

---

## 3.3 父组件如何使用 {#kaj-h-30b38631-7fcb-42b1-9a1d-02813a11dbe8}

以瓦斯页面为例：

`Gas.vue`

```html
<ZhCard
  titleText="瓦斯普查成果图"
  :height="'330px'"
  previewable
  @preview="gasResultImage?.openPreview()"
>
  <DisasterResultImage
    ref="gasResultImage"
    :type="DISASTER_FILE_TYPES.GAS_RESULT"
    alt="瓦斯普查成果图"
    height="258px"
  />
</ZhCard>
```

页面脚本中只需要保存组件引用：

```js
const gasResultImage = ref(null)
```

父组件做的事情很少：

1. 传入成果图类型；
2. 设置显示高度；
3. 监听卡片的预览按钮；
4. 调用子组件暴露的 `openPreview`。

父组件不需要关心图片请求的具体细节。

---

## 3.4 完整实现流程 {#kaj-h-d961772c-351b-43a6-99e8-4e0f61b1a78c}

整体流程可以概括为：

```text
父组件传入 type
        ↓
watch 监听 type 和 coalLayerId
        ↓
调用 getViewByType
        ↓
Axios 返回 Blob
        ↓
检测图片 MIME 类型
        ↓
生成 blob URL
        ↓
绑定到 el-image
        ↓
用户点击预览
        ↓
打开 el-image-viewer
        ↓
组件销毁时释放 URL
```

---

## 3.5 接口请求部分 {#kaj-h-abb348e8-fa6a-44d4-b941-31980048560f}

接口定义在：

`common.js`

```js
export const getViewByType = (params) => {
  return request({
    url: '/colliery-disaster/system/disasterFile/viewByType',
    method: 'get',
    params,
    responseType: 'blob'
  })
}
```

这里有几个关键点。

### 参数如何传递 {#kaj-h-f4561b38-04bd-43f5-827c-b0c519ca70d0}

```js
const params = { type: props.type }

if (props.coalLayerId !== null && props.coalLayerId !== '') {
  params.coalLayerId = props.coalLayerId
}
```

最终请求类似：

```text
GET /colliery-disaster/system/disasterFile/viewByType
    ?type=5
    &coalLayerId=12
```

### 为什么使用 `responseType: 'blob'` {#kaj-h-48ef0bc4-b01c-4ca4-8c03-5a14af59781c}

因为后端返回的不是普通 JSON，而是图片二进制数据。

如果不写：

```text
responseType: 'blob'
```

Axios 可能会尝试把响应解析为 JSON，前端就无法直接作为图片展示。

`request.js` 中的响应拦截器最终返回 `response.data`，所以对于这个接口来说，组件拿到的就是 Blob：

```js
const blob = await getViewByType(params)
```

---

## 3.6 Blob 到图片的转换 {#kaj-h-6f72b038-056c-4b27-8995-7b54360a4e96}

浏览器的 `<img>` 或 `el-image` 需要一个 URL，而不是直接接受任意二进制对象。

因此代码使用：

```js
const imageBlob = blob.type === mimeType
  ? blob
  : new Blob([blob], { type: mimeType })

src.value = URL.createObjectURL(imageBlob)
```

结果可能类似：

```text
blob:http://localhost:5173/6d3e...
```

然后模板绑定：

```html
<el-image :src="src" fit="contain" />
```

### 为什么不用 Base64 {#kaj-h-602ebba6-6768-4ddd-a151-46cebafc12c0}

也可以将 Blob 转成 Base64，但通常不优先选择：

```js
const reader = new FileReader()
reader.readAsDataURL(blob)
```

原因是：

- Base64 会增加大约三分之一的数据体积；
- 需要额外进行编码；
- 大图片会占用更多字符串内存；
- Blob URL 更适合临时预览。

因此这个场景使用 `URL.createObjectURL` 更合适。

---

## 3.7 为什么要检测图片 MIME 类型 {#kaj-h-d9a97d87-e16d-487b-9010-bdb27953c31e}

部分后端接口虽然返回的是图片，但响应头的 `Content-Type` 可能为空或不准确。

代码先读取：

```js
if (blob.type?.startsWith('image/')) return blob.type
```

如果 Blob 类型为空，则读取文件头，也就是所谓的“魔数”：

```js
const bytes = new Uint8Array(
  await blob.slice(0, 12).arrayBuffer()
)
```

例如：

- PNG 文件头：`89 50 4E 47`
- JPEG 文件头：`FF D8 FF`
- GIF 文件头：`47 49 46`
- BMP 文件头：`42 4D`
- WebP 文件头：`RIFF ... WEBP`

这样可以避免把错误响应或非图片文件当成图片渲染。

面试时可以这样说：

> 后端返回的是 Blob，部分情况下 Blob 的 MIME 类型不可靠，所以组件先通过 `Blob.type` 判断，判断不到时再读取文件头进行兜底识别。识别失败就认为接口没有返回有效图片。

---

## 3.8 为什么要做请求竞争处理 {#kaj-h-3b904222-c2d5-4f17-a57a-70565010ad2d}

代码中有：

```js
let loadId = 0

const loadImage = async () => {
  const currentLoadId = ++loadId
  ...
  if (currentLoadId !== loadId) return
}
```

举个例子：

```text
第一次请求：type = A，响应较慢
第二次请求：type = B，响应较快
```

如果没有保护，可能出现：

```text
B 先返回并显示
A 后返回又把页面覆盖成 A
```

但此时页面当前需要的是 B。

`loadId` 的作用是：

1. 每次请求生成一个递增编号；
2. 请求完成后检查自己是不是最新请求；
3. 只有最新请求才能更新 `src`、`error` 和 `loading`。

需要注意：

> `loadId` 只能忽略旧响应，不能真正取消网络请求。

如果要进一步优化，可以使用：

- `AbortController`
- Axios 的 `signal`
- 请求取消机制

---

## 3.9 为什么要释放 Blob URL {#kaj-h-838c5dc9-363e-4ad3-887b-ae856d19c657}

代码中：

```js
const revokeSource = () => {
  previewVisible.value = false

  if (src.value?.startsWith('blob:')) {
    URL.revokeObjectURL(src.value)
  }

  src.value = ''
}
```

`URL.createObjectURL` 创建的是浏览器内部资源引用。如果不断创建新 URL，却不释放旧 URL，页面长期运行可能产生内存占用。

组件在两个时机释放：

1. 图片切换前；
2. 组件销毁时。

```js
onBeforeUnmount(() => {
  loadId += 1
  revokeSource()
})
```

面试回答：

> Blob URL 不会因为变量被覆盖就立即释放，所以在替换图片和组件销毁时调用 `URL.revokeObjectURL`，避免临时资源长期占用内存。

---

## 3.10 为什么有无 `coalLayerId` 两次请求 {#kaj-h-f0d1bff0-f662-448e-b783-580e427919b3}

代码逻辑是：

```js
try {
  imageData = await getImageBlob(params)
} catch (primaryError) {
  if (!params.coalLayerId) throw primaryError
  imageData = await getImageBlob({ type: props.type })
}
```

也就是：

1. 优先使用 `type + coalLayerId` 查询；
2. 如果失败，再只使用 `type` 查询。

这属于业务兼容逻辑，可能是因为部分成果图与煤层关联，部分成果图是全局成果图。

面试时不要说成“自动重试机制”，更准确的说法是：

> 这里不是通用的无限重试，而是根据业务参数做一次有条件的降级查询。

---

## 3.11 三种显示状态 {#kaj-h-8d63d577-5681-4d5e-b69f-975ba1577a74}

模板中主要有三种状态：

```html
<div v-if="loading">正在加载</div>

<el-image v-else-if="src" :src="src" />

<div v-else>{{ error || '暂无成果图' }}</div>
```

分别对应：

1. 请求中；
2. 请求成功并有图片；
3. 没有图片或请求失败。

此外，图片预览由：

```html
<el-image-viewer
  v-if="previewVisible && src"
  :url-list="[src]"
  teleported
/>
```

负责。

`teleported` 表示预览层被挂载到更高层级，避免被父级的 `overflow: hidden` 或层叠上下文遮挡。

---

## 3.12 面试标准回答 {#kaj-h-d148014c-b0fe-47ff-a9bb-eac772fc2b30}

### 问题：你为什么封装这个组件？ {#kaj-h-1dbbdaf6-cf6b-4542-9fa7-37b0f5c80605}

> 项目中多个灾害页面都要展示成果图，重复处理了接口请求、Blob 转 URL、图片预览、加载失败和资源释放。我把这些逻辑集中到 `DisasterResultImage` 中，父组件只传入成果图类型和可选的煤层 ID。组件内部通过 `watch` 监听参数变化，调用 Blob 接口生成临时 URL，并在组件销毁或图片切换时释放旧 URL，从而减少了各页面的重复代码。

### 问题：为什么使用 `defineExpose`？ {#kaj-h-213a109e-282d-4451-a94f-d5b743119bfd}

> 图片预览按钮实际位于外层的 `ZhCard` 中，点击事件发生在父组件。这个动作属于“父组件命令子组件打开预览”，所以我通过模板 ref 和 `defineExpose` 暴露 `openPreview`。如果是子组件通知父组件，则更适合使用 `emit`。这两个方向不一样。

### 问题：如何处理快速切换图片？ {#kaj-h-232e5673-c2c4-4ec2-88d2-d8789e555a30}

> 每次加载都会生成一个递增的 `loadId`，请求完成后检查当前请求是不是最新请求。旧请求即使返回，也不会覆盖最新结果。当前实现主要是忽略旧响应，如果需要进一步节省网络资源，可以使用 AbortController 取消旧请求。

---

## 3.13 这个组件的危险点 {#kaj-h-8b918f0b-42aa-4a8e-ae4d-934a2d9242e8}

### 危险点一：它不是纯通用图片组件 {#kaj-h-e1dcf912-5f1e-42f1-bdae-744a46199bc7}

它内部直接调用：

```text
getViewByType(params)
```

因此它依赖具体业务接口，不适合描述成“通用图片组件库”。

更准确的说法是：

> 这是一个面向灾害成果图场景的可复用业务组件。

如果面试官问：“为什么不把请求放父组件？”

可以回答：

> 如果多个页面都需要完全相同的请求和 Blob 处理逻辑，放在组件内部可以减少重复。但它确实和业务接口耦合。如果以后要做更通用的设计，可以把请求逻辑抽成 `useDisasterImage` composable，图片展示组件只接收最终的 URL。

### 危险点二：图片加载错误处理还有改进空间 {#kaj-h-111a601e-0e54-462a-ac51-2e877493d615}

当前代码：

```text
@error="error = '成果图加载失败'"
```

只修改了 `error`，但 `src` 仍然存在，因此模板可能仍然满足：

```text
v-else-if="src"
```

这意味着错误文字不一定会替换掉损坏的图片。

如果被问到，可以主动承认：

> 当前版本已经记录了错误状态，但如果要让错误占位层稳定显示，还应该在图片错误时清空 `src`，或者额外增加 `imageLoadError` 状态并在模板中优先判断。

### 危险点三：没有取消真实请求 {#kaj-h-af03b91b-de06-4f75-9c16-ed8baf696296}

`loadId` 只是防止旧响应覆盖新响应，并没有停止网络请求。

不要说：

> 我取消了之前的请求。

应该说：

> 我做了旧响应隔离；如果需要取消请求，还可以接入 AbortController。

### 危险点四：不要主动扩展成缓存系统 {#kaj-h-31b60c92-02c0-46ce-89db-aa732fd250d4}

当前代码没有体现：

- 图片缓存
- IndexedDB
- 全局状态
- 自动重试次数控制
- WebSocket 实时更新

面试时不要主动说这些。

## 四、组件案例二：`RiskAssessment` {#kaj-h-7982905b-79d7-47e9-aec4-0d0750114d7d}

文件位置：

`RiskAssessment.vue`

## 4.1 为什么需要这个组件 {#kaj-h-4138d38f-68ed-40ba-ab2f-abf147f556ea}

项目中多个页面都有“风险评价”区域：

- 瓦斯
- 火灾
- 水害
- 地质构造
- 采空区
- 冲击地压
- 其他灾害
- 封闭不良钻孔

这些页面的展示结构基本相同：

```text
危险评价：某个评价结果
评价描述：一段详细文字
```

区别只是查询参数不同。

所以没有必要在每个页面中重复：

```js
const assessment = ref('--')
const describe = ref('--')

const loadData = async () => {
  const response = await getRiskAssessmentByType(type)
  ...
}
```

这个组件将“风险评价接口请求 + 数据转换 + 展示结构”统一起来。

---

## 4.2 组件对外 API {#kaj-h-5ded3d9e-83d3-4b72-92e3-7a056c0ae151}

### Props {#kaj-h-b1154735-94d8-4361-bee9-2c9f6d792343}

代码位于：

`RiskAssessment.vue`

| 参数 | 类型 | 作用 |
| --- | --- | --- |
| `type` | `Number` | 风险评价类型，必填 |
| `descriptionOnly` | `Boolean` | 是否只展示描述，不展示评价等级 |

类型常量定义在：

`riskAssessmentTypes.js`

```js
export const RISK_ASSESSMENT_TYPES = Object.freeze({
  SEALED_BOREHOLE: 1,
  GOAF: 2,
  GEOLOGICAL_STRUCTURE: 3,
  WATER: 4,
  GAS: 5,
  ROCK_BURST: 6,
  FIRE: 7,
  OTHER: 8,
})
```

使用常量而不是直接写数字：

```html
<RiskAssessment :type="RISK_ASSESSMENT_TYPES.GAS" />
```

比下面这样更容易维护：

```html
<RiskAssessment :type="5" />
```

因为看到常量名称，就能知道 `5` 代表瓦斯风险评价。

---

## 4.3 父组件如何使用 {#kaj-h-eec2ffc7-6cbc-444a-9106-d048d958870f}

瓦斯页面：

`Gas.vue`

```html
<ZhCard titleText="瓦斯风险评价" height="330px">
  <RiskAssessment :type="RISK_ASSESSMENT_TYPES.GAS" />
</ZhCard>
```

封闭不良钻孔页面还可以只展示描述：

```html
<RiskAssessment
  description-only
  :type="RISK_ASSESSMENT_TYPES.SEALED_BOREHOLE"
/>
```

这里的：

```text
description-only
```

会自动对应到组件中的：

```text
descriptionOnly
```

---

## 4.4 内部请求流程 {#kaj-h-7c320c19-5b2c-4ef4-8bdc-186e60a611be}

组件初始化时：

```js
watch(
  () => props.type,
  loadRiskAssessment,
  { immediate: true }
)
```

这意味着：

1. 组件首次加载时执行一次；
2. `type` 变化时重新执行；
3. 不需要额外写 `onMounted`。

请求函数：

```js
const loadRiskAssessment = async () => {
  assessment.value = '--'
  describe.value = '--'

  try {
    const response = await getRiskAssessmentByType(props.type)

    const data = response?.data && typeof response.data === 'object'
      ? response.data
      : response

    assessment.value = data?.assessment || '--'
    describe.value = data?.describe || '--'
  } catch (error) {
    console.error(`获取类型 ${props.type} 风险评价失败`, error)
  }
}
```

---

## 4.5 为什么请求前先重置为 `--` {#kaj-h-2a9abb5d-4f11-43a2-b105-33edd500af61}

假设组件原来显示瓦斯风险评价，后来 `type` 改成火灾：

```text
旧内容：瓦斯评价
开始请求：火灾评价
```

如果不重置，接口请求期间页面会继续显示旧的瓦斯内容，用户可能误以为它是火灾评价。

所以请求开始时先设置：

```text
assessment.value = '--'
describe.value = '--'
```

这是一种简单的过渡状态处理。

不过要注意：

> 当前代码没有单独的 `loading` 状态，因此页面显示的是 `--`，不是“正在加载”。

---

## 4.6 为什么要兼容两种响应结构 {#kaj-h-5b7c4078-2ad9-4a7a-a708-e1857231ddb1}

代码中：

```js
const data = response?.data && typeof response.data === 'object'
  ? response.data
  : response
```

它兼容两种可能的数据结构。

### 结构一 {#kaj-h-51f39e2d-ead2-4c99-99e7-9ff97179af76}

```text
{
  "code": 200,
  "data": {
    "assessment": "中等风险",
    "describe": "需要加强监测"
  }
}
```

### 结构二 {#kaj-h-cb89c6a3-3895-4e24-8161-fc3998396ff4}

```text
{
  "assessment": "中等风险",
  "describe": "需要加强监测"
}
```

项目的 Axios 响应拦截器会返回 `response.data`，因此不同接口实际拿到的数据层级可能不完全一样。这里做了一层归一化。

面试时可以说：

> 因为项目请求封装会对响应做一次解包，而后端不同接口的数据包装层又不完全一致，所以组件在拿到结果后统一取出真正的业务对象，再读取 `assessment` 和 `describe` 字段。

---

## 4.7 模板渲染逻辑 {#kaj-h-614f6db3-4802-433c-aeeb-ad61f81c1a77}

```html
<div v-if="!descriptionOnly" class="pingjia-box">
  <div class="pingjia-box-title">危险评价</div>
  <div class="pingjia-box-value">{{ assessment }}</div>
</div>

<div class="pingjia-box-text">
  {{ describe }}
</div>
```

当：

```js
descriptionOnly === false
```

显示：

- 危险评价
- 评价描述

当：

```js
descriptionOnly === true
```

只显示：

- 评价描述

这说明组件不仅抽取了请求逻辑，也把不同页面的展示差异抽象成了一个可配置参数。

---

## 4.8 CSS 为什么使用 `flex` 和 `overflow-y` {#kaj-h-e14f7e22-5ec3-4406-8ee5-407d1b517ce6}

代码中：

```text
.risk-assessment {
  display: flex;
  flex-direction: column;
  height: calc(100% - 16px);
  min-height: 0;
}

.pingjia-box-text {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  white-space: pre-wrap;
}
```

含义是：

- 整个组件纵向排列；
- 评价描述区域占据剩余空间；
- 描述文字过长时可以滚动；
- `white-space: pre-wrap` 保留后端返回文本中的换行。

`min-height: 0` 也比较关键。在 Flex 布局中，如果不设置它，子元素可能因为默认最小高度而无法正常收缩，滚动区域可能失效。

---

## 4.9 面试标准回答 {#kaj-h-e2c0351a-c4b0-40de-acbf-d27928d9b292}

### 问题：为什么封装 `RiskAssessment`？ {#kaj-h-d3e50de4-3c81-4eb0-94ca-9873da2f588a}

> 多个灾害页面都有风险评价模块，接口调用和展示结构基本一致，区别只是风险类型不同。我把接口请求、字段处理、默认值和展示结构抽成 `RiskAssessment`，通过 `type` 区分灾害类型，通过 `descriptionOnly` 兼容只展示描述的场景。这样父页面只需要传入业务类型，不需要重复写请求和模板。

### 问题：为什么使用 `watch`，而不是只在 `onMounted` 请求？ {#kaj-h-24d12f15-41b3-4492-a2f0-a316b4838bb2}

> 因为这个组件的 `type` 可能发生变化。只在 `onMounted` 中请求只能覆盖首次加载，后续切换类型不会更新。监听 `type` 可以在初始化和参数变化时都重新请求，`immediate: true` 可以避免再单独写一份 `onMounted` 初始化逻辑。

### 问题：为什么不把数据放 Pinia？ {#kaj-h-ae6f1d00-ffcf-4a2b-b606-3528a7da57ea}

> 当前风险评价数据只属于当前组件实例，不需要多个页面共享，也不需要跨页面持久化，所以放在组件内部更简单。如果后续多个页面需要共享同一份评价数据，或者需要缓存和统一刷新，再考虑 composable 或 Pinia。

---

## 4.10 这个组件的危险点 {#kaj-h-d9be2f6b-bbed-4dd3-af99-d2dae25ab55d}

### 危险点一：当前没有 loading 和明确错误状态 {#kaj-h-94c5143b-f96f-47c1-ae38-2364266e5cf2}

请求失败时只是：

```js
console.error(...)
```

页面仍然显示默认的：

```text
--
```

面试官可能会问：“用户怎么知道是加载中还是没有数据？”

应该诚实回答：

> 当前版本用 `--` 做了默认占位，错误主要记录在控制台，没有单独区分 loading、空数据和错误状态。更完善的版本可以增加 `loading`、`error` 和 `empty` 三种状态，分别展示加载中、请求失败和确实没有数据。

### 危险点二：没有处理快速切换导致的旧响应覆盖 {#kaj-h-fb0496ea-4c90-4ead-9d4d-8a8d1b3b2110}

当前组件没有像图片组件那样使用 `loadId`。

如果：

```text
type = 5 的请求很慢
type = 7 的请求很快
```

可能出现 7 先显示，5 后返回又覆盖页面。

如果面试官继续追问：

> 当前实现默认 `type` 不会高频变化。如果需要支持快速切换，我会增加请求序号，或者使用 AbortController 取消旧请求，只允许最后一次请求更新状态。

### 危险点三：不要说成“通用数据组件” {#kaj-h-531c7044-e5f6-486f-9dcb-4467cd7b88bb}

它直接依赖：

```text
getRiskAssessmentByType
```

所以准确说法是：

> 风险评价业务组件。

而不是：

> 我封装了一个完全通用的数据展示组件。

### 危险点四：`|| '--'` 对数字 0 不友好 {#kaj-h-9683d890-ee27-4377-b050-5a3a6aff2f5b}

```text
assessment.value = data?.assessment || '--'
```

如果后端合法返回数字 `0`，它会被当成空值。

当前评价字段一般是文本，所以问题不大。但更严谨的写法是：

```text
assessment.value = data?.assessment ?? '--'
```

`??` 只在 `null` 或 `undefined` 时使用默认值，不会把 `0`、`false` 当成空值。

## 五、两个组件的区别 {#kaj-h-a96ba512-52a4-41ff-97e3-460724bce9fc}

| 组件 | 封装重点 | 对外接口 | 主要技术点 |
| --- | --- | --- | --- |
| `DisasterResultImage` | 图片资源加载、预览和生命周期 | Props + `defineExpose` | Blob、Object URL、MIME 检测、竞态处理 |
| `RiskAssessment` | 风险评价请求和展示逻辑 | Props | `watch`、接口数据归一化、默认值、条件渲染 |

可以这样总结：

> `DisasterResultImage` 解决的是“如何加载和管理一张业务图片”；`RiskAssessment` 解决的是“不同灾害类型如何复用同一套风险评价逻辑”。

## 六、模拟连续追问 {#kaj-h-1b078f47-fae8-46ad-8f55-82a80eecc80b}

## 追问链一：图片组件 {#kaj-h-be46b773-4314-4045-a49d-6ab5f333e1ee}

### 面试官：你说减少了重复代码，具体减少了哪些？ {#kaj-h-6311bae1-1e80-43dc-8354-368ab63cb00d}

> 主要减少了成果图接口请求、Blob 转换、加载状态、错误显示、预览打开以及 URL 释放等重复逻辑。各个灾害页面只需要传入文件类型，父页面不再直接处理二进制图片。

### 面试官：为什么接口返回 Blob？ {#kaj-h-7c2f47af-1478-4328-b45d-cadfaf87e892}

> 因为接口返回的是图片文件本身，不是图片地址。前端拿到 Blob 后，通过 `URL.createObjectURL` 生成临时 URL，再交给 `el-image` 渲染。

### 面试官：Blob URL 和普通 URL 有什么区别？ {#kaj-h-65cd8c3c-b653-4256-8bbd-95db2f67b0b3}

> 普通 URL 通常指向服务器资源，而 Blob URL 是浏览器为本地内存中的 Blob 创建的临时地址。它不需要把文件重新上传到服务器，但使用完需要主动调用 `URL.revokeObjectURL` 释放。

### 面试官：你处理并发了吗？ {#kaj-h-6cec9e7a-0dc3-464c-b4a7-3bdb623e7a21}

> 处理了旧响应覆盖新响应的问题。每次请求生成一个 `loadId`，只有最新请求可以更新组件状态。但它没有取消底层网络请求，如果需要进一步优化，可以使用 AbortController。

### 面试官：为什么用 `defineExpose`，不用事件？ {#kaj-h-ffb9f611-2a9a-4e92-964c-ecb1e31d8c19}

> 事件更适合子组件通知父组件，例如“图片加载完成”。这里是父组件点击外层卡片按钮后，命令子组件打开预览，所以使用 `defineExpose` 暴露 `openPreview` 更符合交互方向。

---

## 追问链二：风险评价组件 {#kaj-h-e8863d3f-6f97-49a4-bb03-ea5b3cf2bc92}

### 面试官：为什么不让父组件请求接口，再把结果传给子组件？ {#kaj-h-3e5cc609-6f73-49ea-8294-47027a5f156c}

> 也可以这样做，但项目中多个页面都使用同一接口和同一展示结构。如果每个父页面都请求并处理字段，就会产生重复代码。当前场景下，组件内部封装请求能让父页面只关心风险类型。

### 面试官：这会不会导致组件和接口耦合？ {#kaj-h-5955fde7-ae70-4cd9-97a3-82723ce9f7cf}

> 会，所以它属于业务组件，不是完全通用组件。对于当前项目，这种耦合换来了较好的复用性。如果未来需要更通用，可以把请求逻辑抽成 composable，组件只负责展示传入的数据。

### 面试官：为什么不用 Pinia？ {#kaj-h-182626b0-2805-47ef-92d7-7aab83dd718d}

> 风险评价只在当前页面使用，组件实例之间也不需要共享，放在 Pinia 会增加全局状态复杂度。只有在需要跨页面共享、缓存或统一刷新时，才更适合放到 Pinia 或 composable 中。

### 面试官：如果接口很慢怎么办？ {#kaj-h-006d3d41-2a33-4325-9c28-6df5b8b307dc}

> 当前实现会先重置为 `--`，避免显示旧类型数据。更完善的处理是增加 loading 状态，展示加载提示；同时可以增加请求取消、超时提示，必要时做缓存。
> 
> 
> 
> ## 七、回答边界 {#kaj-h-1993cb03-d44e-4233-9c64-f4b493043956}
> 
> 
> 
> 面试时建议明确使用以下表达：
> 
> 
> 
> > 这两个组件我主要负责的是组件内部实现和业务页面接入，接口字段和后端接口由前后端共同约定。
> 
> 
> 
> 如果整体方案不是你一个人决定的：
> 
> 
> 
> > 组件抽取的方向是团队共同确定的，我负责其中的请求处理、状态展示和页面接入部分。
> 
> 
> 
> 如果被问到当前代码的不足：
> 
> 
> 
> > 当前版本已经满足项目使用，但还可以继续完善，例如风险评价增加 loading/error 状态，图片加载失败时清空旧 src，以及对旧请求进行真正取消。
> 
> 
> 
> 不要主动声称：
> 
> 
> 
> - 我设计了整个前端组件体系；
> - 我实现了全局图片缓存；
> - 我做了高并发优化；
> - 我使用 WebSocket 实现了实时图片更新；
> - 我给组件补充了完整单元测试；
> - 我独立设计了整个项目架构。
> 
> 
> 
> 这些内容当前代码没有证据支撑，容易被继续追问。
> 
> 
> 
> ## 八、最终知识卡片 {#kaj-h-f970d19d-6641-4837-83d8-884aba11e6e6}
> 
> 
> 
> ## 知识卡片一：`DisasterResultImage` {#kaj-h-59706da7-6fa6-4246-9d14-92e09284b885}
> 
> 
> 
> **一句话介绍**
> 
> 
> 
> > 面向灾害成果图场景的图片加载、展示和预览组件。
> 
> 
> 
> **项目背景**
> 
> 
> 
> > 多个灾害页面都需要展示后端返回的成果图。
> 
> 
> 
> **原来的问题**
> 
> 
> 
> > 各页面重复处理接口请求、Blob 转换、加载状态、预览和资源释放。
> 
> 
> 
> **我的职责**
> 
> 
> 
> > 封装组件内部请求和图片处理逻辑，并在多个灾害页面接入。
> 
> 
> 
> **输入参数**
> 
> 
> 
> > `type`、`coalLayerId`、`alt`、`height`。
> 
> 
> 
> **核心实现**
> 
> 
> 
> > 监听 Props，调用 Blob 接口，识别 MIME 类型，生成 Blob URL，绑定到 `el-image`，通过 `defineExpose` 提供预览方法。
> 
> 
> 
> **为什么这样做**
> 
> 
> 
> > 让父页面只负责传入业务参数，隐藏图片加载细节。
> 
> 
> 
> **难点**
> 
> 
> 
> > Blob 处理、MIME 兜底、旧请求覆盖新请求、Blob URL 释放。
> 
> 
> 
> **优化点**
> 
> 
> 
> > `loadId` 隔离旧响应；组件销毁时释放 URL；查询失败时无煤层 ID 兜底请求。
> 
> 
> 
> **当前不足**
> 
> 
> 
> > 没有真正取消旧请求，图片 `error` 状态还可以进一步完善。
> 
> 
> 
> ---
> 
> 
> 
> ## 知识卡片二：`RiskAssessment` {#kaj-h-5e2ceec8-7e7d-44f6-8292-ac0e601962f8}
> 
> 
> 
> **一句话介绍**
> 
> 
> 
> > 用于展示不同灾害类型风险评价和描述信息的业务组件。
> 
> 
> 
> **项目背景**
> 
> 
> 
> > 多个灾害模块有相同的风险评价区域。
> 
> 
> 
> **原来的问题**
> 
> 
> 
> > 各页面重复请求风险评价接口并编写相同模板。
> 
> 
> 
> **我的职责**
> 
> 
> 
> > 抽取公共组件，统一请求、字段处理和展示逻辑。
> 
> 
> 
> **输入参数**
> 
> 
> 
> > `type` 表示灾害类型，`descriptionOnly` 控制是否只展示描述。
> 
> 
> 
> **核心实现**
> 
> 
> 
> > 使用 `watch` 监听 `type`，通过 `immediate` 首次加载，调用接口后统一读取 `assessment` 和 `describe`。
> 
> 
> 
> **为什么这样做**
> 
> 
> 
> > 各页面只传入类型常量即可复用，不需要关心接口细节。
> 
> 
> 
> **难点**
> 
> 
> 
> > 不同接口响应包装层级兼容，以及参数变化后的重新请求。
> 
> 
> 
> **优化点**
> 
> 
> 
> > 请求前重置旧数据，避免新旧灾害类型混淆；描述区域支持滚动和换行。
> 
> 
> 
> **当前不足**
> 
> 
> 
> > 没有单独的 loading/error 状态，也没有请求竞态保护。
> 
> 
> 
> ## 九、如果面试官问到 `baseEchart` {#kaj-h-fafe0019-170e-42fe-b457-6998ba79b1d7}
> 
> 
> 
> 可以这样说：
> 
> 
> 
> > 项目中还有 `baseEchart` 通用图表组件，我参与过它的使用和维护。它通过 `option`、宽高和自动 resize 等 Props 接收配置，在 mounted 时初始化 ECharts，在卸载时销毁实例，并监听配置变化重新调用 `setOption`。不过这个组件的初始封装是团队其他同学完成的，所以我不会把它说成完全由我独立设计。
> 
> 
> 
> 文件：
> 
> 
> 
> `baseEchart.vue`
> 
> 
> 
> 另外，这个组件当前代码中存在一个值得注意的问题：
> 
> 
> 
> ```js
> watch(
>   () => [props.option, props.xData, props.seriesData, props.type],
>   ...
> )
> ```
> 
> 
> 
> `seriesData` 没有在 Props 中声明。如果面试官读代码发现这一点，应该诚实说：
> 
> 
> 
> > 这是当前组件实现中的遗留问题，应该要么补充 `seriesData` Props，要么从监听项中删除。它不影响我对组件封装思想的理解，但说明这个组件还可以继续规范化。
> 
> 
> 
> 最终，最稳妥的两个面试案例仍然是：
> 
> 
> 
> 1. `DisasterResultImage`：资源加载和生命周期封装；
> 2. `RiskAssessment`：业务请求和展示逻辑封装。
