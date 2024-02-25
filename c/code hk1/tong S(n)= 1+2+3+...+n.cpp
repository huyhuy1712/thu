#include <iostream>
#include <math.h>
using namespace std;
int main() {
	int n,s;
	cout << "n= "; cin >> n;
	cout << "tong S(n) = 1 + 2 + 3 ..... + n \n";
	for (int i=1; i<=n; i++ ){
		s = s + i;
}
	cout << " S(n)= "<<s;
	return 0;
}
