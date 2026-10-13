---
title: "LeetCode 141. 环形链表"
description: "想象兔子和乌龟在同一跑道上，一个速度快、另一个速度慢。如果跑道有环，兔子必然在一段时间后追上乌龟。对于链表来说，如果在链表中引入两个以不同速度（一个比另一个快一倍）前进的指针，在链表存在环的情况下，这两个指针必定会相遇。注意这里的while"
date: "2026-08-18"
publishedAt: "2026-08-18T15:47:08.907993+08:00"
source: "https://kajspace.cn/articles/01M09XD6JSATEDZTH03Y50R357/"
tags: ["算法"]
---

# LeetCode 141. 环形链表

![正文图片](/images/kajspace/8be9874267fb7253.png)

想象兔子和乌龟在同一跑道上，一个速度快、另一个速度慢。如果跑道有环，兔子必然在一段时间后追上乌龟。对于链表来说，如果在链表中引入两个以不同速度（一个比另一个快一倍）前进的指针，在链表存在环的情况下，这两个指针必定会相遇。  
注意这里的while循环的停止条件，判断fast是否为空，需要同时判断fast和fast.next，缺一不可，因为fast不能为空，fast.next也不能为空，如果只写了fast.next，就会出现当fast为null时，null.next这样的错误表达式。

![正文图片](/images/kajspace/402cb08bff15dafb.png)
