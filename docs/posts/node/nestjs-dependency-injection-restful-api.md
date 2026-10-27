---
title: NestJS 核心知识：依赖注入、装饰器与 RESTful API
category: node
description: 从 Controller、Service 和 Module 出发，梳理 NestJS 的依赖注入、装饰器、请求处理流程、RESTful API 与 DTO 参数验证。
date: "2026-10-27"
publishedAt: "2026-10-27T19:03:13+08:00"
tags:
  - NestJS
  - Node.js
  - 依赖注入
  - RESTful API
  - TypeScript
---

# NestJS 核心知识：依赖注入、装饰器与 RESTful API

## 一、什么是 NestJS？

NestJS 是一个基于 Node.js 的后端开发框架，主要使用 TypeScript 构建服务端应用。它借鉴了 Angular 的模块化、装饰器和依赖注入等设计思想，能够帮助开发者构建结构清晰、易于维护的后端应用。

与直接使用 Express 编写接口相比，NestJS 提供了更明确的代码组织方式。我们可以把不同职责的代码拆分为 Controller、Service 和 Module。

一个典型的 NestJS 项目可以分为以下几个部分：

- **Controller：** 接收 HTTP 请求，解析请求参数，并返回响应。
- **Service：** 负责业务逻辑，例如查询用户、创建订单等。
- **Module：** 组织和注册 Controller、Service 等组件。
- **DTO：** 定义请求数据的结构，通常配合验证管道使用。
- **Provider：** NestJS 依赖注入系统管理的对象或服务，Service 是常见的一种 Provider。

例如，开发一个用户管理接口时，可以让 Controller 负责接收请求，让 Service 负责查询用户数据，而 Module 负责将两者组织起来。

这种职责分离能够降低代码耦合度，便于后续测试和维护。

## 二、NestJS 的三个核心装饰器

NestJS 大量使用 TypeScript 装饰器来声明类的用途，以及框架应该如何管理这些类。

### 1. @Controller()：声明 HTTP 控制器

`@Controller()` 用于标记一个类是 HTTP 控制器。

```ts
@Controller('users')
export class UserController {
  @Get()
  findAll() {
    return ['张三', '李四'];
  }

  @Get(':id')
  findOne() {
    return '用户详情';
  }
}
```

这里的 `'users'` 是**路由前缀**，不是类名，也不是必须与类名保持一致的标识符。

控制器上的路由前缀会与方法上的路由路径组合，形成完整的接口路径。

| 代码 | HTTP 方法 | 接口路径 |
|---|---|---|
| `@Get()` | GET | `/users` |
| `@Get(':id')` | GET | `/users/:id` |
| `@Post()` | POST | `/users` |
| `@Patch(':id')` | PATCH | `/users/:id` |
| `@Delete(':id')` | DELETE | `/users/:id` |

例如，访问 `GET /users/123` 时，NestJS 会将请求分发到对应的路由处理方法。

需要注意：`@Controller()` 负责声明控制器及其路由前缀，真正定义具体 HTTP 接口的是方法上的 `@Get()`、`@Post()` 等装饰器。

### 2. @Injectable()：声明可参与依赖注入的类

`@Injectable()` 用于标记一个类可以参与 NestJS 的依赖注入机制。

例如，创建一个用户服务：

```ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class UserService {
  findAll() {
    return ['张三', '李四'];
  }
}
```

这里的 `UserService` 负责提供用户相关的业务逻辑。

不过，需要注意：`@Injectable()` 本身并不会自动完成所有依赖注入工作。通常还需要将该类注册到模块的 `providers` 中，并通过构造函数声明依赖关系，让 NestJS 的容器负责解析和管理实例。

### 3. @Module()：组织和注册组件

`@Module()` 用于定义模块，告诉 NestJS 当前模块包含哪些控制器、提供哪些服务，以及依赖哪些其他模块。

```ts
import { Module } from '@nestjs/common';

@Module({
  controllers: [UserController],
  providers: [UserService],
})
export class UserModule {}
```

其中：

- `controllers`：注册当前模块的控制器。
- `providers`：注册当前模块提供的服务或其他 Provider。
- `imports`：引入其他模块。
- `exports`：将当前模块中的 Provider 导出，供导入该模块的其他模块使用。

一个模块可以把某个业务领域的相关功能组织在一起。例如，用户管理功能可以放在 `UserModule` 中，订单管理功能可以放在 `OrderModule` 中。

这样，随着项目规模扩大，代码依然能够保持相对清晰的结构。

## 三、什么是依赖注入（DI）？

依赖注入是 NestJS 的核心机制之一，也是面试中的高频考点。

### 1. 先理解什么是依赖

假设 `UserController` 需要调用 `UserService` 的方法，那么 `UserController` 就依赖于 `UserService`。

如果直接在 Controller 中创建 Service 实例：

```ts
export class UserController {
  private readonly userService = new UserService();

  findAll() {
    return this.userService.findAll();
  }
}
```

这种写法将对象的创建和使用耦合在了一起。如果后续需要替换 Service 的实现，或者在测试中使用模拟对象，就不够灵活。

### 2. 使用依赖注入

NestJS 通常通过构造函数注入依赖：

```ts
@Controller('users')
export class UserController {
  constructor(
    private readonly userService: UserService,
  ) {}

  @Get()
  findAll() {
    return this.userService.findAll();
  }
}
```

这里最重要的是：

```ts
constructor(
  private readonly userService: UserService,
) {}
```

这段代码声明 `UserController` 需要一个 `UserService` 实例。

NestJS 会根据依赖注入配置解析这个依赖，并将相应实例传给 Controller，而不需要 Controller 自己调用 `new UserService()`。

因此，**是 Controller 依赖 Service，由 NestJS 将 Service 注入 Controller，而不是 Controller 注入 Service。**

### 3. IoC 与 DI 有什么区别？

IoC（Inversion of Control，控制反转）是一种设计思想：对象的创建和依赖管理不再完全由业务类自己控制，而是交给外部容器管理。

DI（Dependency Injection，依赖注入）是实现控制反转的一种常见方式。

可以简单理解为：

- **IoC：** 一种设计思想，强调控制权的转移。
- **DI：** 一种实现方式，通过外部提供对象依赖。
- **NestJS 容器：** 负责解析依赖关系，并按照 Provider 的作用域管理实例。

依赖注入的优势包括降低耦合度、提高代码复用性，以及方便单元测试和替换实现。

## 四、整合 Controller、Service 与 Module

下面通过一个完整的简单示例，理解这三个核心组件如何协作。

### 1. UserService：处理业务逻辑

```ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class UserService {
  private readonly users = [
    { id: 1, name: '张三' },
    { id: 2, name: '李四' },
  ];

  findAll() {
    return this.users;
  }

  findOne(id: number) {
    return this.users.find(user => user.id === id);
  }

  create(name: string) {
    const user = {
      id: this.users.length + 1,
      name,
    };

    this.users.push(user);
    return user;
  }
}
```

这里为了便于理解，使用数组模拟数据存储。实际项目通常会通过数据库访问层查询和修改数据。

### 2. UserController：处理 HTTP 请求

```ts
import {
  Body,
  Controller,
  Get,
  Param,
  ParseIntPipe,
  Post,
} from '@nestjs/common';

@Controller('users')
export class UserController {
  constructor(
    private readonly userService: UserService,
  ) {}

  @Get()
  findAll() {
    return this.userService.findAll();
  }

  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.userService.findOne(id);
  }

  @Post()
  create(@Body('name') name: string) {
    return this.userService.create(name);
  }
}
```

这里用到了几个常见装饰器：

- `@Get()`：处理 GET 请求。
- `@Post()`：处理 POST 请求。
- `@Param()`：获取 URL 路径参数。
- `@Body()`：获取请求体中的数据。
- `ParseIntPipe`：将参数转换为整数；转换失败时会抛出请求错误。

例如，请求 `GET /users/1` 时，NestJS 会从路径中提取 `id`，经过管道转换后调用 `findOne()`。

### 3. UserModule：注册组件

```ts
import { Module } from '@nestjs/common';

@Module({
  controllers: [UserController],
  providers: [UserService],
})
export class UserModule {}
```

实际项目还需要将 `UserModule` 引入应用的根模块，才能纳入整个应用的模块体系。

这个例子展示了三个组件之间的关系：

1. Module 注册 Controller 和 Service。
2. Controller 通过构造函数声明对 Service 的依赖。
3. NestJS 容器解析依赖并提供 Service 实例。
4. Controller 接收 HTTP 请求，调用 Service 执行业务逻辑，再返回结果。

## 五、NestJS 的请求处理流程

在 NestJS 中，一个典型的 HTTP 请求会经过多个处理阶段。理解这些阶段有助于理解中间件、权限校验、参数验证和异常处理应该放在哪里。

```text
客户端发起 HTTP 请求
        ↓
     Middleware
        ↓
       Guards
        ↓
Interceptors（前置处理）
        ↓
       Pipes
        ↓
    Controller
        ↓
      Service
        ↓
Interceptors（后置处理）
        ↓
    返回 HTTP 响应
```

异常发生时，异常过滤器可以负责处理异常并生成相应的 HTTP 响应。

各部分的主要职责如下：

| 组件 | 主要职责 | 常见场景 |
|---|---|---|
| Middleware | 在请求进入路由处理流程前执行通用逻辑 | 日志、请求预处理 |
| Guards | 判断当前请求是否允许继续执行 | 登录认证、权限检查 |
| Interceptors | 在处理前后执行逻辑，转换响应或控制执行流程 | 响应格式统一、耗时统计 |
| Pipes | 转换和验证输入数据 | 类型转换、参数校验 |
| Controller | 接收请求并调用相应业务逻辑 | 接口入口 |
| Service | 实现业务逻辑 | 查询用户、创建订单 |
| Exception Filters | 捕获并处理异常 | 统一异常响应 |

需要注意，这是一种典型的理解模型。具体执行细节会受到全局、控制器级和方法级绑定方式，以及异常发生位置等因素影响。

## 六、什么是 RESTful API？

RESTful API 是一种围绕资源组织 Web 接口的设计风格。它通常使用资源路径标识操作对象，并通过 HTTP 方法表达操作意图。

例如，用户资源可以统一使用 `/users` 表示，而不是为每种操作都设计不同的动词路径。

### 1. 常见 HTTP 方法

| 操作 | HTTP 方法 | 示例路径 | 说明 |
|---|---|---|---|
| 查询用户列表 | GET | `/users` | 获取多个用户 |
| 查询单个用户 | GET | `/users/123` | 获取指定用户 |
| 创建用户 | POST | `/users` | 新建用户 |
| 更新部分信息 | PATCH | `/users/123` | 修改指定字段 |
| 整体替换资源 | PUT | `/users/123` | 提交完整资源表示 |
| 删除用户 | DELETE | `/users/123` | 删除指定用户 |

RESTful 风格强调资源导向和 HTTP 语义，而不是单纯要求所有接口都必须使用某种固定路径。

### 2. Path、Query 和 Body 的区别

HTTP 请求中的数据通常通过不同位置传递。

**Path 参数：** 用于标识具体资源。

```http
GET /users/123
```

这里的 `123` 表示用户 ID。

**Query 参数：** 通常用于筛选、搜索、分页或排序。

```http
GET /users?page=1&size=10
```

这里的 `page` 和 `size` 用于指定分页条件。

**Body 请求体：** 通常用于提交创建或更新资源的数据。

```http
POST /users
Content-Type: application/json

{
  "name": "王五"
}
```

在 NestJS 中，可以分别使用 `@Param()`、`@Query()` 和 `@Body()` 获取这些数据。

### 3. 常见 HTTP 状态码

| 状态码 | 含义 | 常见使用场景 |
|---|---|---|
| 200 OK | 请求成功 | 查询成功、更新成功并返回内容 |
| 201 Created | 资源创建成功 | 创建用户成功 |
| 204 No Content | 请求成功但无响应正文 | 删除成功且不返回内容 |
| 400 Bad Request | 请求数据不符合要求 | 参数格式错误、验证失败 |
| 401 Unauthorized | 未通过身份认证 | 未登录或认证凭证无效 |
| 403 Forbidden | 不允许访问该资源 | 已登录但没有操作权限 |
| 404 Not Found | 资源不存在 | 用户 ID 不存在 |
| 409 Conflict | 请求与当前资源状态冲突 | 用户名重复等冲突 |
| 500 Internal Server Error | 服务端发生未预期错误 | 未处理的服务端异常 |

`401` 和 `403` 的区别尤其值得记忆：前者通常表示身份认证未通过，后者通常表示已认证但无权执行操作。

## 七、参数验证与 DTO

在真实项目中，不能完全信任客户端提交的数据。后端需要验证参数是否存在、类型是否正确，以及是否满足业务约束。

NestJS 通常使用 DTO（Data Transfer Object，数据传输对象）描述请求数据结构，并配合 `class-validator`、`class-transformer` 和 `ValidationPipe` 进行验证与转换。

例如，定义创建用户的 DTO：

```ts
import {
  IsInt,
  IsString,
  Min,
  MinLength,
} from 'class-validator';

export class CreateUserDto {
  @IsString()
  @MinLength(2)
  name: string;

  @IsInt()
  @Min(1)
  age: number;
}
```

Controller 中可以这样使用：

```ts
@Post()
create(@Body() dto: CreateUserDto) {
  return this.userService.create(dto.name);
}
```

要让 DTO 验证生效，需要启用 `ValidationPipe`。例如，在 `main.ts` 中配置全局管道：

```ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    transform: true,
  }),
);
```

其中：

- `whitelist: true`：移除 DTO 中没有声明验证规则的属性。
- `transform: true`：根据配置尝试将输入转换为 DTO 声明的类型。

实际使用时，DTO 的字段、验证规则和 Service 的业务逻辑应当保持一致。仅声明 DTO 类并不会自动启用验证。

## 八、前端如何调用 NestJS 接口？

对于前端开发者而言，NestJS Controller 提供的 HTTP 接口通常通过 Axios 或 Fetch 调用。

例如：

```ts
import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 5000,
});

export async function getUsers() {
  const response = await api.get('/users');
  return response.data;
}

export async function getUserById(id: number) {
  const response = await api.get(`/users/${id}`);
  return response.data;
}

export async function createUser(name: string) {
  const response = await api.post('/users', { name });
  return response.data;
}
```

这段代码假设前端开发服务器或部署环境已将 `/api` 正确代理到 NestJS 后端。

从前后端协作角度看，双方需要约定：

- 接口路径和 HTTP 方法。
- 请求参数及数据格式。
- 响应数据结构。
- HTTP 状态码和错误响应格式。
- 身份认证方式，例如 Cookie 或 Token。
- 跨域、代理和超时处理策略。

Controller 负责接收请求并返回响应，前端则负责发起请求、展示数据和处理交互状态。

## 九、面试高频问题总结

### 1. 什么是 NestJS 的依赖注入？

依赖注入是指对象不需要自己创建依赖对象，而是通过外部容器获得依赖。NestJS 通常通过构造函数注入依赖，由 IoC 容器解析和管理 Provider。

### 2. `@Controller()`、`@Injectable()` 和 `@Module()` 有什么区别？

- `@Controller()`：声明 HTTP 控制器，并可设置路由前缀。
- `@Injectable()`：标记类可以参与 NestJS 的依赖注入机制。
- `@Module()`：组织模块中的 Controller、Provider 及模块之间的依赖关系。

### 3. `@Controller('users')` 中的 `users` 是什么？

它是路由前缀，会与方法上的路由路径组合。例如，`@Controller('users')` 配合 `@Get(':id')`，对应 GET `/users/:id`。

### 4. Controller 和 Service 有什么区别？

Controller 负责接收和处理 HTTP 请求入口相关的逻辑，Service 负责业务逻辑。将两者分离可以减少控制器中的业务代码，提高复用性和可测试性。

### 5. IoC 和 DI 有什么区别？

IoC 是控制反转的设计思想，DI 是实现控制反转的一种常见方式。NestJS 的依赖注入容器负责解析并提供组件依赖。

### 6. RESTful API 的设计原则是什么？

以资源为中心设计路径，使用 HTTP 方法表达操作意图，合理使用 Path、Query 和 Body 传递数据，并通过适当的 HTTP 状态码表达请求结果。

### 7. 为什么要使用 DTO 和 ValidationPipe？

DTO 用于描述请求数据结构，验证装饰器定义字段约束，ValidationPipe 负责在请求处理过程中执行验证和转换，减少不合法数据进入业务逻辑。

## 十、总结

学习 NestJS 时，建议先掌握以下核心知识：

1. **Controller：** 接收 HTTP 请求，定义接口路由。
2. **Service：** 编写可复用的业务逻辑。
3. **Module：** 注册和组织组件。
4. **DI：** 通过依赖注入降低组件之间的耦合。
5. **请求处理流程：** 理解 Middleware、Guards、Interceptors、Pipes 和 Exception Filters 的职责。
6. **RESTful API：** 掌握 HTTP 方法、参数传递方式和状态码。
7. **DTO 与参数验证：** 确保客户端提交的数据满足约束。

对于前端开发者而言，学习 NestJS 不必一开始就深入复杂的后端架构。可以先尝试独立实现一个简单的用户管理 API，串联路由定义、参数获取、Service 业务逻辑、依赖注入和前端 Axios 调用，再逐步学习数据库、认证授权和测试。

当能够清楚解释一个 HTTP 请求从进入 Controller 到调用 Service，再到返回响应的完整过程时，就已经建立了比较扎实的 NestJS 入门基础。
