#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
#define mod 1000000007
#define pb push_back
#define X first
#define Y second

int main() {
    // Open the input file
    ifstream inputFile("input3.txt");
    if (!inputFile) {
        cerr << "Unable to open file input2.txt" << endl;
        return 1; // Exit with error code
    }

    // Open the output file
    ofstream outputFile("output3.txt");
    if (!outputFile) {
        cerr << "Unable to open file output2.txt" << endl;
        return 1; // Exit with error code
    }

    // Redirect input and output to files
    int t;
    inputFile >> t;
    while (t--) {
        int n, a, b;
        inputFile >> n >> a >> b;

        if (2 * a <= b) {
            outputFile << n * a << "\n";
        } else {
            if (n % 2) {
                int r = n - 1;
                outputFile << (r / 2) * b + a << "\n";
            } else {
                outputFile << (n / 2) * b << "\n";
            }
        }
    }

    // Close the files
    inputFile.close();
    outputFile.close();

    return 0;
}
