---
title: "704. 二分查找"
description: "这是一道比较基础的二分查找题。维护 left 和 right 两个指针，每次取两者的中间位置 mid，将 nums[mid] 与 target 比较：如果相等则直接返回 mid；如果 nums[mid] < target，说明目标值在右半部"
date: "2026-08-30"
publishedAt: "2026-08-30T10:10:32.251637+08:00"
source: "https://kajspace.cn/articles/01M185EDDAYE0PXR8TN7H8V8VR/"
tags: ["算法"]
---

# 704. 二分查找

![正文图片](/images/kajspace/448bec46fb493e4f.png)

这是一道比较基础的二分查找题。维护 `left` 和 `right` 两个指针，每次取两者的中间位置 `mid`，将 `nums[mid]` 与 `target` 比较：如果相等则直接返回 `mid`；如果 `nums[mid] < target`，说明目标值在右半部分，将 `left` 移动到 `mid + 1`；否则说明目标值在左半部分，将 `right` 移动到 `mid - 1`。不断缩小搜索区间，直到找到目标值，或者 `left > right` 时说明不存在，返回 `-1`。

![正文图片](/images/kajspace/f2285add426e5e99.png)
