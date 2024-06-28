#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

void solve(ifstream &cin, ofstream &cout){
    int n; cin>>n;
    vector<int> a(n);
    for(int i=0; i<n; i++) cin>>a[i];
    set<int> s;
    for(int i=0;i<n;i++){
        s.insert(a[i]);
    }
    if(s.size() == n){
        cout<<"NO"<<"\n";
    }
    else{
        cout<<"YES"<<"\n";
    }
}

int main() {
    ifstream inputFile("input5.txt");
    if (!inputFile) {
        cerr << "Unable to open file input2.txt" << endl;
        return 1; 
    }
    ofstream outputFile("output5.txt");
    if (!outputFile) {
        cerr << "Unable to open file output2.txt" << endl;
        return 1; 
    }
    int t ; inputFile>>t;
    while(t--) {
        solve(inputFile, outputFile);
    }
}