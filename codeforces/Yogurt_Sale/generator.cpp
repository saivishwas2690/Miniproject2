#include <iostream>
#include <fstream>
#include <cstdlib>  // For srand() and rand()
#include <ctime>    // For time()
using namespace std;
int rd(int max, int min){
    return rand() % (max - min + 1);
}

int main() {
    int min, max;
    // std::ifstream input_file("input.txt");
    ofstream outputFile("input3.txt");
    cout.rdbuf(outputFile.rdbuf());

    srand(time(0)); 
    int t = rd(1,1000);
    cout<<t<<"\n";
    for(int i=0;i<t;i++){
        int n = rd(1, 101);
        int a = rd(1, 30);
        int b = rd(1, 30);
        if(n == 0) n = 7;
        if(a == 0) a = 7;
        if(b == 0) b = 7;
        cout<<n<<" "<<a<<" "<<b<<"\n";
    }
    outputFile.close();
    return 0;
}
