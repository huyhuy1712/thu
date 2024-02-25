#include <iostream>
#include <math.h>
using namespace std;
int main() {
	float a, b;
	cout << "giai phuong trinh bac giat ax+b=0" << endl;
	cout << "nhap he so a: "; cin >> a;
	cout << "nhap he so b: "; cin >> b;
	if (a == 0 && b == 0) {
		cout << "phuong trinh vo so nghiem!";
	}
	else if (a == 0 && b != 0) { cout << "phuong trinh vo nghiem!"; }
	else { cout << "phuong trinh ax+b=0 co nghiem la: " << -b / a; }
	return 0;
}
