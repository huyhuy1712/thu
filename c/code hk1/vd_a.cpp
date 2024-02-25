#include <iostream>
#include <math.h>
using namespace std;
int main() {
	float a,b,c;
	int t;
	cout << "t(s)= "; cin >> t;
	if (t < 0) { cout << "nhap lai dieu kien"; }
	else {
		a = t / 3600;
		b = (t % 3600) / 60;
		c = (t % 3600) % 60;
		cout << t << "s" << " " << "doi ra la: " << a << "h" << " " << b << "m" << " " << c << "s" << endl ;
	}
	return 0;
}
