#include <iostream>
#include <math.h>
using namespace std;
float lamtron (float num, int n) {
	double base = pow(10, n);
	double result = round(num * base) / base;
	return result;
}
int main() {
	float a, b, c, q, h;
	cout << "do dai BC la: "; cin >> a;
	cout << "do dai AC la: "; cin >> b;
	cout << "do dai AB la: "; cin >> c;
	float cv = a + b + c;
	q = (a + b + c) / 2;
	float S = sqrt(q * (q - a) * (q - b) * (q - c));
	 h = (2 * S) / a;
	if (a > 0 && b > 0 && c > 0 && a + b > c && b + c > a && a + c > b) {
		cout << "chu vi tam giac ABC la: " << cv <<endl;
		cout << "chieu cao AH tam giac ABC la: " << lamtron (h,2) << endl;
	 	cout << "dien tich  tam giac ABC la: " << lamtron (S,2) << endl;
	}
	else { cout << "khong phai la tam giac!"; }
	return 0;
}

