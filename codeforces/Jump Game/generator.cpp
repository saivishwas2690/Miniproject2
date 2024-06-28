#include<bits/stdc++.h>  
using namespace std;
int random(int min, int max){
    int val = rand()%(max-min);
    return val + min;
}

int main() {
    int min, max;
    ofstream outputFile("input2.txt");
    cout.rdbuf(outputFile.rdbuf());

   int t = 1;
   cout<<t<<"\n";
   for(int i=0;i<3;i++){
        int n = 1e5;
        cout<<n<<"\n";
        for(int i=0;i<n;i++){
            cout<<random(0, 7)<<" ";
        }
        cout<<"\n";
   }
   


    outputFile.close();
    return 0;
}
