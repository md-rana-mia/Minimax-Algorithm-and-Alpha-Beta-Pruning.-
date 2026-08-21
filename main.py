import math


class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None
        self.is_leaf = False


def build_tree(values, depth, idx):
    if depth == 0:
        node = Node(values[idx[0]])
        node.is_leaf = True
        idx[0] += 1
        return node

    node = Node()
    node.left = build_tree(values, depth - 1, idx)
    node.right = build_tree(values, depth - 1, idx)
    return node


def minimax(node, depth, is_max, count):
    count[0] += 1
    if node.is_leaf:
        return node.value

    if is_max:
        left = minimax(node.left, depth - 1, False, count)
        right = minimax(node.right, depth - 1, False, count)
        return max(left, right)
    else:
        left = minimax(node.left, depth - 1, True, count)
        right = minimax(node.right, depth - 1, True, count)
        return min(left, right)


def alpha_beta(node, depth, alpha, beta, is_max, count, prune):
    if node.is_leaf:
        count[0] += 1
        return node.value

    count[0] += 1

    if is_max:
        v = -math.inf

        v = alpha_beta(node.left, depth - 1, alpha, beta, False, count, prune)
        alpha = max(alpha, v)

        if alpha >= beta:
            prune[0] += count_subtree(node.right)
            return v

        v = max(v, alpha_beta(node.right, depth - 1, alpha, beta, False, count, prune))
        return v

    else:
        v = math.inf

        v = alpha_beta(node.left, depth - 1, alpha, beta, True, count, prune)
        beta = min(beta, v)

        if alpha >= beta:
            prune[0] += count_subtree(node.right)
            return v

        v = min(v, alpha_beta(node.right, depth - 1, alpha, beta, True, count, prune))
        return v


def count_subtree(node):
    if node is None:
        return 0
    if node.is_leaf:
        return 1
    return 1 + count_subtree(node.left) + count_subtree(node.right)


def run_case(values, case_num):
    print(f"Case #{case_num}:")
    print(f"Generated Leaf Nodes: {values}")

    depth = 3
    idx = [0]
    root = build_tree(values, depth, idx)

    minimax_count = [0]
    optimal = minimax(root, depth, True, minimax_count)

    print("Minimax:")
    print(f"    Nodes Evaluated: {minimax_count[0]}")
    print(f"    Optimal Value: {optimal}")

    ab_count = [0]
    prune_count = [0]
    ab_optimal = alpha_beta(root, depth, -math.inf, math.inf, True, ab_count, prune_count)

    print("Alpha-Beta Pruning:")
    print(f"    Nodes Evaluated: {ab_count[0]}")
    print(f"    Nodes Pruned: {prune_count[0]}")

    improvement = ((minimax_count[0] - ab_count[0]) / minimax_count[0]) * 100
    print(f"Efficiency Improvement: {improvement:.2f}%")
    print()


def main():
    run_case([3, 5, 2, 9, 12, 5, 23, 23], 1)
    run_case([8, 6, 7, 4, 15, 10, 9, 11], 2)


if __name__ == "__main__":
    main()