---
title: "LeetCode 912. 排序数组"
description: "这道题和 215 题一样，都可以想到使用快速排序。不过 215 题只需要通过分区找到第 k 大的元素，而这道题需要把整个数组排好序，所以我还是采用快速排序的思路，通过递归不断划分子数组。"
date: "2026-08-24"
publishedAt: "2026-08-24T11:22:21.837814+08:00"
source: "https://kajspace.cn/articles/01M0RWMJZQ0TSV0131FXSX3QYJ/"
tags: ["算法"]
---

# LeetCode 912. 排序数组

![正文图片](/images/kajspace/9772528eafaa0f7f.png)

这道题和 215 题一样，都可以想到使用快速排序。不过 215 题只需要通过分区找到第 `k` 大的元素，而这道题需要把整个数组排好序，所以我还是采用快速排序的思路，通过递归不断划分子数组。

接下来需要考虑递归的停止条件。我想到可以用一个 `ordered` 的布尔变量判断当前子数组是否已经有序。遍历当前子数组`[left, right]`，如果发现 `nums[i] > nums[i + 1]`，就说明它还没有排好序，需要继续进行 partition；如果整个子数组遍历结束都没有发现逆序，那么说明它已经有序，就可以直接返回，不需要再进行排序。

![正文图片](/images/kajspace/ddc4266fdaf1f7c8.png)![正文图片](/images/kajspace/3ded05f5c46af49a.png)
