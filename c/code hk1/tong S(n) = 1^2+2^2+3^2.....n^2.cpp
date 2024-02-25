#include <iostream>
#include <math.h>
using namespace std;
int main() {
	int n,s;
	cout << "S(n)= 1^2 + 2^2 + 3^2 + .... + n^2 \n";	
	cout << "n= "; cin >> n;
	for (int i = 1 ; i <= n ; i++){
		s += pow(i,2);
	}
	cout <<"S(n)= "<< s;
	return 0;
}
