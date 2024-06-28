#include <iostream>
#include <fstream>
#include <cstdlib>  // For srand() and rand()
#include <ctime>    // For time()
using namespace std;
int rd(int max, int min){
    int val = rand() % (max - min + 1);
    if(val == 0) return max;
    else return val;
}

int main() {
    int min, max;
    // std::ifstream input_file("input.txt");
    ofstream outputFile("input5.txt");
    cout.rdbuf(outputFile.rdbuf());

    srand(time(0)); 
    int t = rd(1,500);
    cout<<t<<"\n";
    for(int i=0;i<t;i++){
        int n = rd(1, 10000);
        for(int i=0;i<n;i++){
            cout<<rd(1, 1e9)<<" ";
        }
    }
    outputFile.close();
    return 0;
}
