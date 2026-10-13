---
title: "LeetCode 5. 最长回文子串"
description: "不用暴力枚举，能不能O（1）判断一个字串是不是回文的？"
date: "2026-08-25"
publishedAt: "2026-08-25T15:55:03.583959+08:00"
source: "https://kajspace.cn/articles/01M0VYJED9WJ7ZSYVNWQG6Q1RJ/"
tags: ["算法"]
---

# LeetCode 5. 最长回文子串

![正文图片](/images/kajspace/f43fa7161a3679ff.png)

不用暴力枚举，能不能O（1）判断一个字串是不是回文的？

比如子串 abcba，最左边和最右边的字母都是 a，如果中间的 bcb 是回文串，那么我们就能 O(1) 地知道 abcba 是回文串。对于子串 bcb 来说，最左边和最右边的字母都是 b，如果中间的 c 是回文串，那么我们就能 O(1) 地知道 bcb 是回文串。显然 c 是回文串，所以 bcb 是回文串，所以 abcba 是回文串。

既然如此，为什么不直接从 c 开始向外扩展呢？

c 是回文串。

看看 c 左右两边的字母是不是一样的，一样，那么 bcb 是回文串。

继续，看看 bcb 左右两边的字母是不是一样的，一样，那么 abcba 是回文串。我们 O(1) 地判断出了一个子串是不是回文串！

这些子串的长度都是奇数，我们称其为奇回文串。

回文串还可以是偶数长度，我们称其为偶回文串。

![正文图片](/images/kajspace/a764ae85352c2eb2.png)
