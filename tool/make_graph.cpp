const int MAX_N = 10000;
    
class UnionFind {
private:
    vector<int> union_size, rank;

public:
    vector<int> par;
    
    void init(int n)
    {
        union_size.resize(n);
        rank.resize(n);
        par.resize(n);

        for (int i=0; i<n; i++) {
            par[i]=i;
            rank[i]=0;
            union_size[i] = 1;
        }
    }
    
    // 木の根を求める
    int find(int x)
    {
        if (par[x] == x) {
            return x;
        } else {
            return par[x] = find(par[x]);
        }
    }
    
    // xとyの属する集合を併合する
    void merge(int x, int y)
    {
        x = find(x);
        y = find(y);
        if (x == y) return;

        union_size[x] += union_size[y];
        union_size[y] = union_size[x];

        if (rank[x] < rank[y]) {
            par[x] = y;
        } else {
            par[y] = x;
            if (rank[x] == rank[y]) rank[x]++;
        }
    }
    
    // xとyが同じ集合に属するか判定する
    bool same(int x, int y)
    {
        return find(x) == find(y);
    }
    
    // x が含まれる集合の要素数を返す
    int getUnionSize(int x)
    {
        return union_size[find(x)];
    }
};

int main()
{
}
