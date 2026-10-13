---
title: "1143. 最长公共子序列"
description: "动态规划，dp[i][j] 表示 text1 的前 i 个字符 与 text2 的前 j 个字符 的最长公共子序列的长度。dp[0][0], dp[0][*] 和 dp[*][0]，递归的初始边界，多出的一行表示空串"
date: "2026-08-07"
publishedAt: "2026-08-07T09:47:56.522789+08:00"
source: "https://kajspace.cn/articles/01KZCYF70BJGK6RSKYFHPSS7F5/"
tags: ["算法"]
---

# 1143. 最长公共子序列

动态规划，dp[i][j] 表示 text1 的前 i 个字符 与 text2 的前 j 个字符 的最长公共子序列的长度。  
dp[0][0], dp[0][\*] 和 dp[\*][0]，递归的初始边界，多出的一行表示空串

![](/images/kajspace/3218d89d1427b9a3.png)
