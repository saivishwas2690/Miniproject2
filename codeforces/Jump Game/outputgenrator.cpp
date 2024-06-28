
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
#define mod 1000000007
#define pb push_back
#define X first
#define Y second
 
void solve(istream &cin, ostream &cout){
    int n; cin>>n;
    vector<int>a(n);
    for(int i=0;i<n;i++) cin>>a[i];
    int pos = 0;
    for(int i=0;i<n;i++){
        if(i > pos) {
            cout<<"FALSE\n";
            return ;
        }
        pos = max(pos, a[i] + i);
    }
    if(pos >= a.size()-1){
        cout<<"TRUE\n";
    }
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
    int t; inputFile >> t;
    while(t--) {
        solve(inputFile, outputFile);
    }
}