#include<bits/stdc++.h>  
using namespace std;
int random(int min, int max){
    int val = rand()%(max-min);
    return val + min;
}

int palin(){
    int n = random(1, 8);
    vector<int> b;
    for(int i=0;i<n;i++){
        b.push_back(random(0, 9));
    }
    for(int i=0;i<b.size()/2;i++){
        b[n-i-1] = b[i];
    }
    int num = 0;
    for(int i=0;i<b.size();i++){
        num = num * 10 + b[i];
    }
    return num;
}

int main() {
    int min, max;
    ofstream outputFile("input2.txt");
    cout.rdbuf(outputFile.rdbuf());

    srand(time(0)); 
    int t = 1e5;
    cout<<t<<"\n";
    for(int i=0;i<t;i++){
        cout<<palin()<<" ";
        cout<<"\n";
    }

    
    outputFile.close();
    return 0;
}
