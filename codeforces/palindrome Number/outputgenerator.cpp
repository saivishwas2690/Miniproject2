#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

void solve(ifstream &cin, ofstream &cout){
    int n;
    cin>>n;
    int temp = n;
    int rev = 0;
    while(temp){
        int rem = temp%10;
        rev = rev*10 + rem;
        temp = temp/10;
    }
    if(n == rev){
        cout<<"YES\n";
    }else{
        cout<<"NO\n";
    }
}

int main() {
    ifstream inputFile("input3.txt");
    if (!inputFile) {
        cerr << "Unable to open file input2.txt" << endl;
        return 1; 
    }
    ofstream outputFile("output3.txt");
    if (!outputFile) {
        cerr << "Unable to open file output2.txt" << endl;
        return 1; 
    }
    int t ; inputFile>>t;
    while(t--) {
        solve(inputFile, outputFile);
    }
}