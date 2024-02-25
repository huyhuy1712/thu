#include <iostream>
#include<math.h>
using namespace std;
int main() {
	float n, s;
	s = 0;
	cout << "n= "; cin >> n;
	for (int i = 1; i <= n; i++) {
		 s = s + (1.0 / i);
	}
	cout << "tong 1+1/2+1/3+...+1/n la: " << s << endl;
	return 0;
}
