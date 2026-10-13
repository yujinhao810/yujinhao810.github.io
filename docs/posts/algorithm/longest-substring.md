---
title: "3. 无重复字符的最长子串"
description: 用双指针和哈希集合在线性时间内求解最长无重复子串
date: 2026-02-10
tags:
  - 算法
  - 双指针
  - 哈希
---

# 3. 无重复字符的最长子串

给定字符串 `s`，返回不含重复字符的最长子串长度。窗口 `[left, right]` 始终表示当前满足条件的区间。

```js
export function lengthOfLongestSubstring(s) {
  const seen = new Set()
  let left = 0
  let answer = 0

  for (let right = 0; right < s.length; right += 1) {
    while (seen.has(s[right])) {
      seen.delete(s[left])
      left += 1
    }
    seen.add(s[right])
    answer = Math.max(answer, right - left + 1)
  }

  return answer
}
```

## 正确性

当右指针加入重复字符时，持续移动左指针直到窗口重新满足“无重复”。因此每一步计算的窗口都是以 `right` 结尾的最长合法窗口，所有右端点的最大值就是全局答案。

## 复杂度

每个字符最多被左右指针各访问一次，时间复杂度为 `O(n)`；集合最多存放 `n` 个字符，空间复杂度为 `O(n)`。
