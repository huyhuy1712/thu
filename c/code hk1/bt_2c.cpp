#include <iostream>
#include <math.h>
using namespace std;
double dinhthuc(float a, float b, float c, float d) {
	return a * d - b * c;
}
 int main() {
	float a1, b1, c1, a2, b2, c2;
	cout << " Giai he phuong trinh bac nhat hai an x va y" << endl;
	cout << "a1.x + b1.y = c1" << endl;
	cout << "a2.x + b2.y = c2" << endl;
	cout << "Nhap he so a1: "; cin >> a1;
	cout << "Nhap he so a2: "; cin >> a2;
	cout << "Nhap he so b1: "; cin >> b1;
	cout << "Nhap he so b2: "; cin >> b2;
	cout << "Nhap he so c1: "; cin >>c1 ;
	cout << "Nhap he so c2: "; cin >> c2;
	double d, dx, dy;
	d = dinhthuc(a1, b1, a2, b2);
	dx = dinhthuc(c1, b1, c2, b2);
	dy = dinhthuc(a1, c1, a2, c2);
	if (d == 0) {
		if (dx == 0 and dy == 0) { cout << "phuong trinh vo so nghiem"; }
		else { cout << "phuong trinh vo nghiem"; }
	}
	else {
		cout << "phuong trinh co mot ngiem duy nhat:" << endl;
		cout << "x = " << dx / d << endl;
		cout << "y = " << dy / d << endl;
	}
	return 0;}

