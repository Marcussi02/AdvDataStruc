"""Generalised suffix tree built with Ukkonen's online algorithm, in O(total length).

Several strings are joined, each followed by its own unique terminator, and one
suffix tree is built over the result. Ukkonen's tricks make it linear:

- global end: every leaf's edge ends at a shared counter, so extending all leaves
  (rule 1) in a phase is a single increment ("once a leaf, always a leaf")
- active point (node, edge, length) plus skip/count: walk down by edge lengths
  instead of character by character
- suffix links: after an extension at a node for suffix x+alpha, jump to alpha
- showstopper (rule 3): once a character is already on the path, the rest of the
  phase is implicit, so stop and carry the remainder into the next phase

Queries: substring search, all occurrences with (string, offset), and the longest
common substring of all strings.

    python generalised_suffix_tree.py banana ananas   # longest common substring
"""

import sys
from bisect import bisect_right


class _End:
    """Shared, mutable end index for all leaves (the global end)."""

    __slots__ = ("value",)

    def __init__(self, value: int) -> None:
        self.value = value


class Node:
    __slots__ = ("start", "end", "children", "link", "suffix_start")

    def __init__(self, start: int, end) -> None:
        self.start = start  # edge label into this node is text[start : end + 1]
        self.end = end  # int for internal nodes, the shared _End for leaves
        self.children: dict[str, Node] = {}
        self.link: Node | None = None
        self.suffix_start = -1  # leaves only: where their suffix starts in text

    @property
    def is_leaf(self) -> bool:
        return not self.children

    def edge_length(self) -> int:
        end = self.end.value if isinstance(self.end, _End) else self.end
        return end - self.start + 1


class GeneralisedSuffixTree:
    def __init__(self, strings: list[str]) -> None:
        if not strings:
            raise ValueError("need at least one string")
        # Private-use code points as terminators: unique and never in normal input.
        terminators = [chr(0xE000 + i) for i in range(len(strings))]
        if any(t in s for s in strings for t in terminators):
            raise ValueError("input contains reserved terminator characters")
        self.strings = strings
        self.starts: list[int] = []  # offset of each string in the joined text
        pieces, offset = [], 0
        for s, t in zip(strings, terminators, strict=True):
            self.starts.append(offset)
            pieces.append(s + t)
            offset += len(s) + 1
        self.text = "".join(pieces)
        self.root = Node(-1, -1)
        self.root.link = self.root
        self._build()
        self._label_leaves()

    # ---------- construction ----------

    def _build(self) -> None:
        text = self.text
        leaf_end = _End(-1)
        active_node, active_edge, active_length = self.root, 0, 0
        remaining = 0  # suffixes still to be inserted explicitly
        for i, c in enumerate(text):
            leaf_end.value = i  # rule 1 for every existing leaf, in O(1)
            remaining += 1
            pending_link: Node | None = None  # internal node waiting for its suffix link
            while remaining:
                if active_length == 0:
                    active_edge = i
                edge_char = text[active_edge]
                child = active_node.children.get(edge_char)
                if child is None:
                    # Rule 2 at a node: hang a new leaf directly off active_node.
                    active_node.children[edge_char] = Node(i, leaf_end)
                    if pending_link is not None:
                        pending_link.link = active_node
                        pending_link = None
                else:
                    length = child.edge_length()
                    if active_length >= length:  # skip/count down the edge
                        active_edge += length
                        active_length -= length
                        active_node = child
                        continue
                    if text[child.start + active_length] == c:
                        # Rule 3 (showstopper): already present, finish the phase.
                        if pending_link is not None and active_node is not self.root:
                            pending_link.link = active_node
                        active_length += 1
                        break
                    # Rule 2 mid-edge: split the edge with a new internal node.
                    split = Node(child.start, child.start + active_length - 1)
                    split.link = self.root
                    active_node.children[edge_char] = split
                    split.children[c] = Node(i, leaf_end)
                    child.start += active_length
                    split.children[text[child.start]] = child
                    if pending_link is not None:
                        pending_link.link = split
                    pending_link = split
                remaining -= 1
                if active_node is self.root and active_length > 0:
                    active_length -= 1
                    active_edge = i - remaining + 1
                elif active_node is not self.root:
                    active_node = active_node.link

    def _label_leaves(self) -> None:
        """Record each leaf's suffix start (iterative DFS: no recursion limit)."""
        n = len(self.text)
        stack = [(self.root, 0)]
        while stack:
            node, depth = stack.pop()
            if node is not self.root:
                depth += node.edge_length()
            if node.is_leaf:
                node.suffix_start = n - depth
            else:
                stack.extend((child, depth) for child in node.children.values())

    # ---------- queries ----------

    def _locate(self, suffix_start: int) -> tuple[int, int]:
        idx = bisect_right(self.starts, suffix_start) - 1
        return idx, suffix_start - self.starts[idx]

    def _walk(self, pattern: str) -> Node | None:
        """Node at or just below the end of pattern's path, or None if absent."""
        node, i = self.root, 0
        while i < len(pattern):
            child = node.children.get(pattern[i])
            if child is None:
                return None
            label_end = child.start + child.edge_length()
            j = child.start
            while j < label_end and i < len(pattern):
                if self.text[j] != pattern[i]:
                    return None
                i, j = i + 1, j + 1
            node = child
        return node

    def contains(self, pattern: str) -> bool:
        return pattern == "" or self._walk(pattern) is not None

    def occurrences(self, pattern: str) -> list[tuple[int, int]]:
        """Sorted (string index, offset) pairs where pattern occurs."""
        if not pattern:
            return []
        node = self._walk(pattern)
        if node is None:
            return []
        found, stack = [], [node]
        while stack:
            current = stack.pop()
            if current.is_leaf:
                found.append(self._locate(current.suffix_start))
            else:
                stack.extend(current.children.values())
        # Terminators are unique, so a match can never run across two strings.
        return sorted(found)

    def longest_common_substring(self) -> str:
        """Longest string occurring in every input: the deepest node whose subtree
        has a leaf from each string."""
        k = len(self.strings)
        full = (1 << k) - 1
        best_depth, best_end = 0, 0
        # Post-order: children's string sets must be known before their parent's.
        order, stack = [], [(self.root, 0)]
        while stack:
            node, depth = stack.pop()
            if node is not self.root:
                depth += node.edge_length()
            order.append((node, depth))
            stack.extend((child, depth) for child in node.children.values())
        mask: dict[int, int] = {}
        for node, depth in reversed(order):
            if node.is_leaf:
                mask[id(node)] = 1 << self._locate(node.suffix_start)[0]
                continue
            m = 0
            for child in node.children.values():
                m |= mask[id(child)]
            mask[id(node)] = m
            if m == full and node is not self.root and depth > best_depth:
                best_depth, best_end = depth, node.end
        return self.text[best_end - best_depth + 1 : best_end + 1] if best_depth else ""


def build_suffix_tree(text: str) -> GeneralisedSuffixTree:
    """Ordinary suffix tree of a single string."""
    return GeneralisedSuffixTree([text])


if __name__ == "__main__":
    print(GeneralisedSuffixTree(sys.argv[1:] or ["banana", "ananas"]).longest_common_substring())
