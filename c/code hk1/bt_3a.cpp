#include <iostream>
#include <math.h>
using namespace std;
int main() {
	int a, b, c, d, max, min;
	cout << "a= "; cin >> a;
	cout << "b= "; cin >> b;
	cout << "c= "; cin >> c;
	cout << "d= "; cin >> d;
	max = a;
	if (b > max) max = b;
		if (c > max) max = c;
		if (d > max) max = d;
		cout << "max cua bon so nguyen" <<" " << a << "," << b << "," << c << "," << d << " " << "la: " << max << endl;
		min = a;
		if (b < min) min = b;
		if (c < min) min = c;
		if (d < min) min = d;
		cout << "min cua bon so nguyen " << a << "," << b << "," << c << "," << d << " "<<" la: " << min << endl;

	return 0;
}
