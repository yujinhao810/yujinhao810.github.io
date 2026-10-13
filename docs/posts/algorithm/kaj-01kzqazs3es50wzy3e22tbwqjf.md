---
title: "3. 无重复字符的最长子串"
description: "方法：滑动窗口，创建一个哈希表记录每个字符的出现次数，遍历字符串，如果当前字符的出现次数大于1说明有重复，删除left下标的元素，右移一位，并更新最大的字串数量。主要用到了Map的get/set方法。"
date: "2026-08-11"
publishedAt: "2026-08-11T10:39:09.432272+08:00"
source: "https://kajspace.cn/articles/01KZQAZS3ES50WZY3E22TBWQJF/"
tags: ["算法"]
---

# 3. 无重复字符的最长子串

**方法：**滑动窗口，创建一个哈希表记录每个字符的出现次数，遍历字符串，如果当前字符的出现次数大于1说明有重复，删除left下标的元素，右移一位，并更新最大的字串数量。  
主要用到了Map的**get/set**方法。

![](/images/kajspace/4a7989a283eab4bb.png)
