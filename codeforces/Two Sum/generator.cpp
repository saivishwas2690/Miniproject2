#include<bits/stdc++.h>  
using namespace std;
int random(int min, int max){
    int val = rand()%(max-min);
    return val + min;
}

int main() {
    int min, max;
    ofstream outputFile("input4.txt");
    cout.rdbuf(outputFile.rdbuf());

    srand(time(0)); 
    

    outputFile.close();
    return 0;
}
