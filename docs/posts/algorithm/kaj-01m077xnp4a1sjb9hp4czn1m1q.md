---
title: "LeetCode 121. 买卖股票的最佳时机"
description: "维护变量 minPrice 表示遍历到当前天之前的最低股价，初始化为 prices[0]；从第二天起依次遍历价格 p，先用 p - minPrice 计算若在当天卖出所能获得的最大利润（因为买入价是此前最低价，保证买入日早于卖出日且非同一日"
date: "2026-08-17"
publishedAt: "2026-08-17T14:53:17.143027+08:00"
source: "https://kajspace.cn/articles/01M077XNP4A1SJB9HP4CZN1M1Q/"
tags: ["算法"]
---

# LeetCode 121. 买卖股票的最佳时机

![正文图片](/images/kajspace/9a235489d1df6bcf.png)

维护变量 `minPrice` 表示遍历到当前天之前的最低股价，初始化为 `prices[0]`；从第二天起依次遍历价格 `p`，先用 `p - minPrice` 计算若在当天卖出所能获得的最大利润（因为买入价是此前最低价，保证买入日早于卖出日且非同一日），并用该值更新全局最大利润 `ans`；随后再将 `minPrice` 更新为 `min(minPrice, p)`，以便后续天数使用。这一先计算利润、后更新最低价的顺序，确保了不会出现当天买入卖出的情况，最终返回的 `ans` 即为最大利润。
