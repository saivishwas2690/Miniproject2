#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

void solve(ifstream &cin, ofstream &cout){
    int n, t; cin>>n>>t;
    vector<int> a(n);
    for(int i=0; i<n; i++) cin>>a[i];
    set<int> s;
    for(int i=0;i<n;i++){
        if(s.find(t-a[i])!=s.end()){
            cout<<"YES\n";
            return;
        }
        s.insert(a[i]);
    }
    cout<<"NO\n";
}

int main() {
    ifstream inputFile("input4.txt");
    if (!inputFile) {
        cerr << "Unable to open file input2.txt" << endl;
        return 1; 
    }
    ofstream outputFile("output4.txt");
    if (!outputFile) {
        cerr << "Unable to open file output2.txt" << endl;
        return 1; 
    }
    int t ; inputFile>>t;
    while(t--) {
        solve(inputFile, outputFile);
    }
}