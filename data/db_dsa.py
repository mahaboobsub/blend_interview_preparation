# db_dsa.py - COMPREHENSIVE Data Structures & Algorithms
# Covers: Array problems, String problems, Linked Lists, Trees, Sorting, Searching
# Each has Java + Python implementations

DSA_QUESTIONS = []

def add(sub, q, a, code_java="", code_python=""):
    DSA_QUESTIONS.append({
        "category": "dsa",
        "subcategory": sub,
        "question": q,
        "answer": a.strip(),
        "is_coding": True,
        "code_sql": "",
        "code_java": code_java.strip(),
        "code_python": code_python.strip()
    })

# ═══════════════════════════════════════════════════════════════
# ARRAY PROBLEMS (25)
# ═══════════════════════════════════════════════════════════════

add("Arrays", "Two Sum: Find two numbers that add up to a target.", """
Given an array of integers and a target, return indices of two numbers that add up to the target.
* **Approach**: Use a HashMap to store each number's complement (target - num) as you iterate. O(n) time, O(n) space.
""",
code_java="""
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement))
            return new int[]{map.get(complement), i};
        map.put(nums[i], i);
    }
    return new int[]{};
}
""",
code_python="""
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
""")

add("Arrays", "Best Time to Buy and Sell Stock: Maximum profit from one transaction.", """
Track the minimum price seen so far and calculate profit at each step.
* **Approach**: Single pass, O(n) time, O(1) space. Keep running min_price and max_profit.
""",
code_java="""
public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE, maxProfit = 0;
    for (int price : prices) {
        minPrice = Math.min(minPrice, price);
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    return maxProfit;
}
""",
code_python="""
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit
""")

add("Arrays", "Contains Duplicate: Check if any value appears at least twice.", """
Use a HashSet to track seen values. If a number is already in the set, return true.
* **Time**: O(n), **Space**: O(n).
""",
code_java="""
public boolean containsDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int num : nums) {
        if (!seen.add(num)) return true;
    }
    return false;
}
""",
code_python="""
def contains_duplicate(nums):
    return len(nums) != len(set(nums))
""")

add("Arrays", "Product of Array Except Self: Return array where each element is the product of all others.", """
Use prefix and suffix products without division.
* **Approach**: Two passes — first pass computes prefix products, second pass multiplies by suffix products. O(n) time, O(1) extra space (output array doesn't count).
""",
code_java="""
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] result = new int[n];
    result[0] = 1;
    for (int i = 1; i < n; i++)
        result[i] = result[i-1] * nums[i-1];  // prefix
    int suffix = 1;
    for (int i = n-1; i >= 0; i--) {
        result[i] *= suffix;
        suffix *= nums[i];
    }
    return result;
}
""",
code_python="""
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n-1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result
""")

add("Arrays", "Maximum Subarray (Kadane's Algorithm): Find contiguous subarray with the largest sum.", """
Kadane's Algorithm: Track current_sum and max_sum. Reset current_sum to current element if it drops below.
* **Time**: O(n), **Space**: O(1).
""",
code_java="""
public int maxSubArray(int[] nums) {
    int maxSum = nums[0], curSum = nums[0];
    for (int i = 1; i < nums.length; i++) {
        curSum = Math.max(nums[i], curSum + nums[i]);
        maxSum = Math.max(maxSum, curSum);
    }
    return maxSum;
}
""",
code_python="""
def max_sub_array(nums):
    max_sum = cur_sum = nums[0]
    for num in nums[1:]:
        cur_sum = max(num, cur_sum + num)
        max_sum = max(max_sum, cur_sum)
    return max_sum
""")

add("Arrays", "Merge Two Sorted Arrays in-place.", """
Start from the end of both arrays and fill the larger array from the back.
* **Time**: O(m+n), **Space**: O(1).
""",
code_java="""
public void merge(int[] nums1, int m, int[] nums2, int n) {
    int i = m - 1, j = n - 1, k = m + n - 1;
    while (j >= 0) {
        if (i >= 0 && nums1[i] > nums2[j])
            nums1[k--] = nums1[i--];
        else
            nums1[k--] = nums2[j--];
    }
}
""",
code_python="""
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]; i -= 1
        else:
            nums1[k] = nums2[j]; j -= 1
        k -= 1
""")

add("Arrays", "Move Zeroes: Move all 0s to end while maintaining order of non-zero elements.", """
Two-pointer approach: slow pointer tracks position for next non-zero, fast pointer scans array.
* **Time**: O(n), **Space**: O(1).
""",
code_java="""
public void moveZeroes(int[] nums) {
    int slow = 0;
    for (int fast = 0; fast < nums.length; fast++) {
        if (nums[fast] != 0) {
            int temp = nums[slow];
            nums[slow] = nums[fast];
            nums[fast] = temp;
            slow++;
        }
    }
}
""",
code_python="""
def move_zeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
""")

add("Arrays", "Find the missing number in array of 0 to n.", """
Use XOR or math (expected sum - actual sum). XOR cancels out pairs.
* **Time**: O(n), **Space**: O(1).
""",
code_java="""
public int missingNumber(int[] nums) {
    int n = nums.length;
    int expected = n * (n + 1) / 2;
    int actual = 0;
    for (int num : nums) actual += num;
    return expected - actual;
}
""",
code_python="""
def missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
""")

add("Arrays", "Rotate Array: Rotate array to the right by k steps.", """
Reverse the entire array, then reverse first k elements, then reverse the rest.
* **Time**: O(n), **Space**: O(1).
""",
code_java="""
public void rotate(int[] nums, int k) {
    k %= nums.length;
    reverse(nums, 0, nums.length - 1);
    reverse(nums, 0, k - 1);
    reverse(nums, k, nums.length - 1);
}
private void reverse(int[] nums, int l, int r) {
    while (l < r) {
        int tmp = nums[l]; nums[l] = nums[r]; nums[r] = tmp;
        l++; r--;
    }
}
""",
code_python="""
def rotate(nums, k):
    k %= len(nums)
    nums.reverse()
    nums[:k] = reversed(nums[:k])
    nums[k:] = reversed(nums[k:])
""")

add("Arrays", "Container With Most Water: Find two lines that hold the most water.", """
Two-pointer approach: start from both ends, move the shorter line inward.
* **Time**: O(n), **Space**: O(1). Greedy — moving the shorter line is the only way to potentially find a larger area.
""",
code_java="""
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1, maxWater = 0;
    while (left < right) {
        int area = Math.min(height[left], height[right]) * (right - left);
        maxWater = Math.max(maxWater, area);
        if (height[left] < height[right]) left++;
        else right--;
    }
    return maxWater;
}
""",
code_python="""
def max_area(height):
    left, right, max_water = 0, len(height) - 1, 0
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, area)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water
""")

add("Arrays", "Three Sum: Find all unique triplets that sum to zero.", """
Sort the array, fix one element, use two pointers for the remaining two. Skip duplicates.
* **Time**: O(n²), **Space**: O(1) extra.
""",
code_java="""
public List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i-1]) continue;
        int lo = i + 1, hi = nums.length - 1;
        while (lo < hi) {
            int sum = nums[i] + nums[lo] + nums[hi];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[lo], nums[hi]));
                while (lo < hi && nums[lo] == nums[lo+1]) lo++;
                while (lo < hi && nums[hi] == nums[hi-1]) hi--;
                lo++; hi--;
            } else if (sum < 0) lo++;
            else hi--;
        }
    }
    return result;
}
""",
code_python="""
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]: continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                result.append([nums[i], nums[lo], nums[hi]])
                while lo < hi and nums[lo] == nums[lo+1]: lo += 1
                while lo < hi and nums[hi] == nums[hi-1]: hi -= 1
                lo += 1; hi -= 1
            elif s < 0: lo += 1
            else: hi -= 1
    return result
""")

add("Arrays", "Majority Element: Find the element that appears more than n/2 times.", """
Boyer-Moore Voting Algorithm: maintain a candidate and count. O(n) time, O(1) space.
""",
code_java="""
public int majorityElement(int[] nums) {
    int candidate = nums[0], count = 1;
    for (int i = 1; i < nums.length; i++) {
        if (count == 0) { candidate = nums[i]; count = 1; }
        else if (nums[i] == candidate) count++;
        else count--;
    }
    return candidate;
}
""",
code_python="""
def majority_element(nums):
    candidate, count = nums[0], 1
    for num in nums[1:]:
        if count == 0:
            candidate, count = num, 1
        elif num == candidate:
            count += 1
        else:
            count -= 1
    return candidate
""")

# ═══════════════════════════════════════════════════════════════
# STRING PROBLEMS (15)
# ═══════════════════════════════════════════════════════════════

add("Strings", "Reverse a String in-place.", """
Two-pointer swap from both ends. O(n) time, O(1) space.
""",
code_java="""
public void reverseString(char[] s) {
    int l = 0, r = s.length - 1;
    while (l < r) {
        char tmp = s[l]; s[l] = s[r]; s[r] = tmp;
        l++; r--;
    }
}
""",
code_python="""
def reverse_string(s):
    s.reverse()  # in-place
    # or: s[:] = s[::-1]
""")

add("Strings", "Valid Anagram: Check if two strings are anagrams.", """
Count character frequencies. If both strings have identical frequency counts, they are anagrams.
* **Time**: O(n), **Space**: O(1) since the character set is fixed (26 letters).
""",
code_java="""
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] counts = new int[26];
    for (char c : s.toCharArray()) counts[c - 'a']++;
    for (char c : t.toCharArray()) counts[c - 'a']--;
    for (int c : counts) if (c != 0) return false;
    return true;
}
""",
code_python="""
from collections import Counter
def is_anagram(s, t):
    return Counter(s) == Counter(t)
""")

add("Strings", "Valid Palindrome: Check if a string reads the same forwards and backwards.", """
Two-pointer approach: compare characters from both ends, skipping non-alphanumeric characters.
* **Time**: O(n), **Space**: O(1).
""",
code_java="""
public boolean isPalindrome(String s) {
    int l = 0, r = s.length() - 1;
    while (l < r) {
        while (l < r && !Character.isLetterOrDigit(s.charAt(l))) l++;
        while (l < r && !Character.isLetterOrDigit(s.charAt(r))) r--;
        if (Character.toLowerCase(s.charAt(l)) != Character.toLowerCase(s.charAt(r)))
            return false;
        l++; r--;
    }
    return true;
}
""",
code_python="""
def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
""")

add("Strings", "Longest Substring Without Repeating Characters (Sliding Window).", """
Use a sliding window with a HashSet. Expand right pointer, shrink left when duplicate found.
* **Time**: O(n), **Space**: O(min(n, alphabet_size)).
""",
code_java="""
public int lengthOfLongestSubstring(String s) {
    Set<Character> set = new HashSet<>();
    int left = 0, maxLen = 0;
    for (int right = 0; right < s.length(); right++) {
        while (set.contains(s.charAt(right)))
            set.remove(s.charAt(left++));
        set.add(s.charAt(right));
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
""",
code_python="""
def length_of_longest_substring(s):
    seen = set()
    left = max_len = 0
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len
""")

add("Strings", "Longest Palindromic Substring: Find the longest palindrome in a string.", """
Expand around center approach: for each character (and each pair), expand outward while characters match.
* **Time**: O(n²), **Space**: O(1).
""",
code_java="""
public String longestPalindrome(String s) {
    int start = 0, maxLen = 0;
    for (int i = 0; i < s.length(); i++) {
        int len1 = expand(s, i, i);     // odd length
        int len2 = expand(s, i, i + 1); // even length
        int len = Math.max(len1, len2);
        if (len > maxLen) {
            maxLen = len;
            start = i - (len - 1) / 2;
        }
    }
    return s.substring(start, start + maxLen);
}
private int expand(String s, int l, int r) {
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
    return r - l - 1;
}
""",
code_python="""
def longest_palindrome(s):
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return s[l+1:r]
    result = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1)
        result = max(result, odd, even, key=len)
    return result
""")

add("Strings", "Group Anagrams: Group strings that are anagrams of each other.", """
Sort each string to create a canonical key. Group by that key using a HashMap.
* **Time**: O(n × k log k) where k is max string length. **Space**: O(n × k).
""",
code_java="""
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for (String s : strs) {
        char[] arr = s.toCharArray();
        Arrays.sort(arr);
        String key = new String(arr);
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(map.values());
}
""",
code_python="""
from collections import defaultdict
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())
""")

add("Strings", "String to Integer (atoi): Implement string to integer conversion.", """
Handle whitespace, sign, digits, and overflow. Process character by character.
* **Edge cases**: Leading whitespace, +/- sign, non-digit characters, INT_MIN/INT_MAX overflow.
""",
code_java="""
public int myAtoi(String s) {
    int i = 0, sign = 1, result = 0;
    while (i < s.length() && s.charAt(i) == ' ') i++;
    if (i < s.length() && (s.charAt(i) == '+' || s.charAt(i) == '-'))
        sign = s.charAt(i++) == '-' ? -1 : 1;
    while (i < s.length() && Character.isDigit(s.charAt(i))) {
        int digit = s.charAt(i++) - '0';
        if (result > (Integer.MAX_VALUE - digit) / 10)
            return sign == 1 ? Integer.MAX_VALUE : Integer.MIN_VALUE;
        result = result * 10 + digit;
    }
    return result * sign;
}
""",
code_python="""
def my_atoi(s):
    s = s.lstrip()
    if not s: return 0
    sign = -1 if s[0] == '-' else 1
    i = 1 if s[0] in '+-' else 0
    result = 0
    while i < len(s) and s[i].isdigit():
        result = result * 10 + int(s[i])
        i += 1
    result *= sign
    return max(-(2**31), min(2**31 - 1, result))
""")

add("Strings", "Count and Say: Generate the nth term of the count-and-say sequence.", """
Iteratively build each term by reading off digits of the previous term.
* 1 → '1', 2 → '11' (one 1), 3 → '21' (two 1s), 4 → '1211' (one 2, one 1).
""",
code_java="""
public String countAndSay(int n) {
    String s = "1";
    for (int i = 2; i <= n; i++) {
        StringBuilder sb = new StringBuilder();
        int count = 1;
        for (int j = 1; j < s.length(); j++) {
            if (s.charAt(j) == s.charAt(j-1)) count++;
            else { sb.append(count).append(s.charAt(j-1)); count = 1; }
        }
        sb.append(count).append(s.charAt(s.length()-1));
        s = sb.toString();
    }
    return s;
}
""",
code_python="""
def count_and_say(n):
    s = "1"
    for _ in range(n - 1):
        result, i = "", 0
        while i < len(s):
            count = 1
            while i + count < len(s) and s[i + count] == s[i]:
                count += 1
            result += str(count) + s[i]
            i += count
        s = result
    return s
""")

# ═══════════════════════════════════════════════════════════════
# LINKED LIST / TREE / SORTING PROBLEMS (13)
# ═══════════════════════════════════════════════════════════════

add("Linked Lists", "Reverse a Linked List iteratively and recursively.", """
Iterative: Use three pointers (prev, curr, next). Recursive: Reverse the rest, then fix pointers.
* **Time**: O(n), **Space**: O(1) iterative, O(n) recursive.
""",
code_java="""
// Iterative
public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
""",
code_python="""
# Iterative
def reverse_list(head):
    prev, curr = None, head
    while curr:
        curr.next, prev, curr = prev, curr, curr.next
    return prev
""")

add("Linked Lists", "Detect a cycle in a linked list (Floyd's Algorithm).", """
Use slow (1 step) and fast (2 steps) pointers. If they meet, there's a cycle.
* **Time**: O(n), **Space**: O(1).
""",
code_java="""
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
""",
code_python="""
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
""")

add("Linked Lists", "Merge Two Sorted Linked Lists.", """
Use a dummy node and compare heads of both lists, linking the smaller one.
* **Time**: O(n+m), **Space**: O(1).
""",
code_java="""
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0), curr = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) { curr.next = l1; l1 = l1.next; }
        else { curr.next = l2; l2 = l2.next; }
        curr = curr.next;
    }
    curr.next = (l1 != null) ? l1 : l2;
    return dummy.next;
}
""",
code_python="""
def merge_two_lists(l1, l2):
    dummy = curr = ListNode(0)
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next, l1 = l1, l1.next
        else:
            curr.next, l2 = l2, l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
""")

add("Binary Trees", "Inorder, Preorder, Postorder Traversals of a Binary Tree.", """
* **Inorder** (Left, Root, Right): Gives sorted order for BST.
* **Preorder** (Root, Left, Right): Used for tree serialization.
* **Postorder** (Left, Right, Root): Used for deletion, expression evaluation.
""",
code_java="""
// Inorder traversal (iterative)
public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> result = new ArrayList<>();
    Stack<TreeNode> stack = new Stack<>();
    TreeNode curr = root;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) { stack.push(curr); curr = curr.left; }
        curr = stack.pop();
        result.add(curr.val);
        curr = curr.right;
    }
    return result;
}
""",
code_python="""
# All three traversals (recursive)
def inorder(root):
    return inorder(root.left) + [root.val] + inorder(root.right) if root else []

def preorder(root):
    return [root.val] + preorder(root.left) + preorder(root.right) if root else []

def postorder(root):
    return postorder(root.left) + postorder(root.right) + [root.val] if root else []
""")

add("Binary Trees", "Maximum Depth of a Binary Tree.", """
Recursively find max depth of left and right subtrees, return the larger + 1.
* **Time**: O(n), **Space**: O(h) where h is height.
""",
code_java="""
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
""",
code_python="""
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
""")

add("Binary Trees", "Validate Binary Search Tree (BST).", """
Use inorder traversal (should produce sorted sequence) or pass valid range recursively.
* **Time**: O(n), **Space**: O(h).
""",
code_java="""
public boolean isValidBST(TreeNode root) {
    return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
}
private boolean validate(TreeNode node, long min, long max) {
    if (node == null) return true;
    if (node.val <= min || node.val >= max) return false;
    return validate(node.left, min, node.val) &&
           validate(node.right, node.val, max);
}
""",
code_python="""
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root: return True
    if root.val <= lo or root.val >= hi: return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))
""")

add("Sorting", "Implement Merge Sort.", """
Divide array in half, recursively sort each half, merge the two sorted halves.
* **Time**: O(n log n) always, **Space**: O(n). Stable sort.
""",
code_java="""
public void mergeSort(int[] arr, int l, int r) {
    if (l < r) {
        int m = (l + r) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}
private void merge(int[] arr, int l, int m, int r) {
    int[] left = Arrays.copyOfRange(arr, l, m + 1);
    int[] right = Arrays.copyOfRange(arr, m + 1, r + 1);
    int i = 0, j = 0, k = l;
    while (i < left.length && j < right.length)
        arr[k++] = left[i] <= right[j] ? left[i++] : right[j++];
    while (i < left.length) arr[k++] = left[i++];
    while (j < right.length) arr[k++] = right[j++];
}
""",
code_python="""
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
""")

add("Sorting", "Implement Binary Search.", """
Divide search space in half each iteration. Array must be sorted.
* **Time**: O(log n), **Space**: O(1) iterative.
""",
code_java="""
public int binarySearch(int[] arr, int target) {
    int lo = 0, hi = arr.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
""",
code_python="""
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1
""")
