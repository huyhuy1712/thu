#include<iostream>
#include<math.h>
using namespace std;
float UCLN(int e, int f) {
	if (e == 0 || f == 0) e + f;
	while (e != f) {
		if (e > f) e -= f;
		else { f -= e; }
	}
	return e;
}

int main() {
	int a, b, c, d;
chaylai:
	cout << "a= "; cin >> a;
	cout << "b= "; cin >> b;
	cout << "c= "; cin >> c;
	cout << "d= "; cin >> d;
	cout << "phan so " << a / UCLN(a, b) << "/" << b / UCLN(a, b) << endl;
	cout << "phan so " << c / UCLN(c, d) << "/" << d / UCLN(c, d) << endl;
	if (b == 0 || d == 0) {
		cout << "du lieu khong hop le! \n";
		goto chaylai;
	}
	else {
		int tongtu = (a * d) + (c * b);
		int hieutu = (a * d) - (c * b);
		int thuongtu = a * d;
		int m = b * d;
		int mauthuong = b * c;
		int tichtu = a * c;
		cout << "tong hai phan so= " << tongtu / UCLN(tongtu, m) << "/" << m / UCLN(tongtu, m) << endl;
		cout << "hieu hai phan so= " << hieutu / UCLN(hieutu, m) << "/" << m / UCLN(hieutu, m) << endl;
		cout << "tich hai phan so= " << tichtu / UCLN(tichtu, m) << "/" << m / UCLN(tichtu, m) << endl;
		cout << "thuong hai phan so= " << thuongtu / UCLN(thuongtu, mauthuong) << "/" << mauthuong / UCLN(thuongtu, mauthuong) << endl;
	}
	return 0;
}
