---
title: "LeetCode 112. 路径总和"
description: "从根节点开始，不断减去路径上节点的值，如果走到叶子节点且targetSum = 0，那么就找到了一条符合题目要求的路径，再看总问题和子问题，总问题是从当前节点往下找路径，子问题是从子节点往下找路径，因此我们可以直接递归调用hasPathSu"
date: "2026-08-18"
publishedAt: "2026-08-18T16:11:46.076077+08:00"
source: "https://kajspace.cn/articles/01M09YT916BV765TF7C6TGFC67/"
tags: ["算法"]
---

# LeetCode 112. 路径总和

![正文图片](/images/kajspace/76c64bab0d48cf69.png)

从根节点开始，不断减去路径上节点的值，如果走到叶子节点且targetSum = 0，那么就找到了一条符合题目要求的路径，再看总问题和子问题，总问题是从当前节点往下找路径，子问题是从子节点往下找路径，因此我们可以直接递归调用hasPathSum：

1. 如果root为空就返回false。
2. 把targetSum减少root.val。
3. 如果root是叶子节点：如果targetSum = 0，返回true，否则返回false。
4. 递归左子树，如果左子树返回true，那么当前子树就返回true，否则返回递归右子树的结果。

![正文图片](/images/kajspace/c9e99e868836bb81.png)
