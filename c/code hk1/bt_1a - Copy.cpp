#include <iostream>
#include <math.h>
using namespace std;
int main() {
	float r;
	cout << "ban kinh cua hinh tron la: "<<endl;
	cout << "r= ";  cin >> r;
	if (r < 0) { cout << "khong phai hinh tron!"; }
	else {
	float cv = 2 * 3.14 * r;
		float dt = r * r * 3.14;
		cout << "chu vi hinh tron la: " << cv << endl;
		cout << "dien tich hinh tron la: " << dt << endl;
	}
	return 0;
}
