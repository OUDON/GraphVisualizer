# coding: utf-8

# Verified http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_1_A
class UnionFind:
    def __init__(self, node_num):
        self._rank = [0] * node_num
        self._par  = [i for i in range(node_num)]
        self.N    =  node_num

    def _find(self, x):
        if self._par[x] == x:
            return x
        else:
            self._par[x] = self._find(self._par[x])
            return self._par[x]

    def merge(self, x, y):
        x = self._find(x)
        y = self._find(y)
        if x == y: return

        if self._rank[x] < self._rank[y]:
            self._par[x] = y
        else:
            self._par[y] = x
            if self._rank[x] == self._rank[y]:
                self._rank[y] += 1

    def is_same(self, x, y):
        return self._find(x) == self._find(y)
