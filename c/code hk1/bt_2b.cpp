# include <math.h>
#include <iostream>
using namespace std;
int main() {
	float a, b, c;
	float delta, x, x1, x2;
	cout << "giai phuong trinh dang ax^2+bx+c=0" << endl;
	cout << "nhap he so a: "; cin >> a;
	cout << "nhap he so b: "; cin >> b;
	cout << "nhap he so c: "; cin >> c;
	if (a == 0 && b == 0 && c == 0) {
		cout << "phuong trinh vo so nghiem";
	}
	else if (a == 0 && b == 0 && c != 0) { cout << "phuong trinh vo nghiem"; }
	else if (a == 0 && b != 0) { cout << "phuong trinh co nghiem: " << round(-b / 2 * a * 100) / 100 << endl; }
	else {
		delta = b * b - 4 * a * c;
		x = -b / 2 * a;
		x1 = (-b + sqrt(delta)) / 2 * a;
		x2 = (-b - sqrt(delta)) / 2 * a;
		if (delta < 0) { cout << "phuong trinh vo nghiem!"; }
		else if (delta == 0) {
			cout << "phuong trinh co mot nghiem duy nhat: " << round(x * 100) / 100;
		}
		else {
			cout << "phuong trinh co hai nghiem phan biet la: \n";
			cout << "x1= " << x1 << endl;
			cout << " x2= " << x2;
		}
	}
	return 0;
}
