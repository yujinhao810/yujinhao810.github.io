---
title: "LeetCode 15. 三数之和"
description: "枚举nums[i],问题变成 nums[j]+nums[k]=−nums[i]，这和两数之和是一样的。题目要求答案中不能有重复的三元组，如何避免重复？"
date: "2026-08-18"
publishedAt: "2026-08-18T11:38:14.832023+08:00"
source: "https://kajspace.cn/articles/01M09F4STGN1CCVEFJVD9J8QN4/"
tags: ["算法"]
---

# LeetCode 15. 三数之和

![正文图片](/images/kajspace/42db569c7d2df91e.png)

枚举nums[i],问题变成 nums[j]+nums[k]=−nums[i]，这和两数之和是一样的。题目要求答案中不能有重复的三元组，如何避免重复？

在外层循环中，如果发现 nums[i]=nums[i−1]，那么 nums[i] 与后面两个数组成的和为 0 的三元组，nums[i−1] 也能组成一模一样的三元组，这就重复了，所以遇到 nums[i]=nums[i−1] 的情况，直接 continue。

在内层循环中，当三数之和等于 0 时，为避免把相同的三元组计入答案，跳过后续相同的 nums[j] 和 nums[k]（也可以只跳过相同的 nums[j]）。

除了排除重复元素外，我们还能进行优化，如果当前遍历到的元素nums[i] &gt; 0，由于数组是升序排列的了，那么三数之和必然大于0，直接break结束遍历。

![正文图片](/images/kajspace/f9841024de5990b2.png)
