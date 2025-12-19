#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>

using namespace std;

const int INF = 1e9; // inf: vô cùng

struct Graph { // graph: đồ thị
    int n;
    map<string, int> mapTen;
    map<int, string> mapSo;
    vector<vector<int>> matrix;

    Graph() { n = 0; }

    // thêm đỉnh
    void ThemDinh(string ten) {
        if (mapTen.find(ten) == mapTen.end()) {
            mapTen[ten] = n;
            mapSo[n] = ten;
            n++;
            for (auto& hang : matrix) hang.resize(n, INF);
            matrix.push_back(vector<int>(n, INF));
            matrix[n - 1][n - 1] = 0;
        }
    }

    // nối đỉnh
    void NoiDinh(string tu, string den, int w) {
        if (mapTen.count(tu) && mapTen.count(den)) {
            int u = mapTen[tu];
            int v = mapTen[den];
            matrix[u][v] = w;
        }
    }
};

// đọc file dữ liệu
Graph DocFile(string tenFile) {
    Graph g;
    ifstream f(tenFile);
    if (!f.is_open()) return g;
    string temp;
    if (f >> temp && temp == "Vertex") {
        while (f >> temp) {
            if (temp == "Edge") break;
            string ten = temp;
            double x, y; f >> x >> y;
            g.ThemDinh(ten);
        }
    }
    string u, v; int w;
    while (f >> u >> v >> w) g.NoiDinh(u, v, w);
    return g;
}

// tìm đường ngắn nhất(dijkstra)
void Dijkstra(Graph& g, string p1, string p2, string fileGhi) {
    ofstream out(fileGhi);
    if (g.mapTen.find(p1) == g.mapTen.end() || g.mapTen.find(p2) == g.mapTen.end()) {
        out << "Loi: Sai ten dinh"; return;
    }
    int Start = g.mapTen[p1];
    int End = g.mapTen[p2];
    vector<int> Dist(g.n, INF); // dist: khoảng cách
    vector<int> Trace(g.n, -1); // trace: dấu vết đường đi
    vector<bool> Done(g.n, false); // done: đã xét xong

    Dist[Start] = 0;
    for (int i = 0; i < g.n; i++) {
        int u = -1;
        for (int j = 0; j < g.n; j++)
            if (!Done[j] && (u == -1 || Dist[j] < Dist[u])) u = j;
        if (u == -1 || Dist[u] == INF) break;
        Done[u] = true;
        for (int v = 0; v < g.n; v++) {
            if (g.matrix[u][v] != INF && Dist[u] + g.matrix[u][v] < Dist[v]) {
                Dist[v] = Dist[u] + g.matrix[u][v];
                Trace[v] = u;
            }
        }
    }
    if (Dist[End] == INF) out << "Khong Thay Duong";
    else {
        out << Dist[End] << endl;
        vector<string> Path; // path: đường đi
        int curr = End;
        while (curr != -1) {
            Path.push_back(g.mapSo[curr]);
            curr = Trace[curr];
        }
        reverse(Path.begin(), Path.end());
        for (size_t i = 0; i < Path.size(); i++) out << Path[i] << (i == Path.size() - 1 ? "" : " ");
    }
    out.close();
}

int MinCP = INF;
vector<int> BestPath; // bestPath: đường tốt nhất
vector<int> TmpPath;  // tmpPath: đường tạm thời
vector<bool> Visited; // visited: đã đi qua

// thuật toán tsp
void TryTSP(int u, int dem, int cp, int Start, Graph& g) {
    if (cp >= MinCP) return;
    if (dem == g.n) {
        if (g.matrix[u][Start] != INF) {
            int tong = cp + g.matrix[u][Start];
            if (tong < MinCP) {
                MinCP = tong;
                BestPath = TmpPath;
                BestPath.push_back(Start);
            }
        }
        return;
    }
    for (int v = 0; v < g.n; v++) {
        if (!Visited[v] && g.matrix[u][v] != INF) {
            Visited[v] = true;
            TmpPath.push_back(v);
            TryTSP(v, dem + 1, cp + g.matrix[u][v], Start, g);
            Visited[v] = false;
            TmpPath.pop_back();
        }
    }
}

// chạy tsp
void RunTSP(Graph& g, string p1, string fileGhi) {
    ofstream out(fileGhi);
    if (g.mapTen.find(p1) == g.mapTen.end()) {
        out << "Loi: Sai ten dinh"; return;
    }
    int Start = g.mapTen[p1];
    MinCP = INF;
    BestPath.clear();
    TmpPath.clear();
    Visited.assign(g.n, false);
    Visited[Start] = true;
    TmpPath.push_back(Start);
    TryTSP(Start, 1, 0, Start, g);
    if (MinCP == INF) out << "KhongTheDiVongQuanh";
    else {
        out << MinCP << endl;
        for (size_t i = 0; i < BestPath.size(); i++) out << g.mapSo[BestPath[i]] << (i == BestPath.size() - 1 ? "" : " ");
    }
    out.close();
}

int main() {

    ofstream reset("result.txt"); reset.close();

    Graph g = DocFile("data_dothi.txt");
    ifstream lenh("request.txt");
    string cmd, p1, p2;
    if (lenh >> cmd) {
        if (cmd == "DIJKSTRA") {
            lenh >> p1 >> p2;
            Dijkstra(g, p1, p2, "result.txt");
        }
        else if (cmd == "TSP") {
            lenh >> p1;
            RunTSP(g, p1, "result.txt");
        }
    }
    return 0;
}