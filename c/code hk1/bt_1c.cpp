#include <iostream>
#include<math.h>
using namespace std;
int main() {
	float xA, yA, xB, yB, xC, yC, xG, yG, h;
nhaplaidulieu:
	cout << "toa do A: \n";
	cout << "xA= "; cin >> xA;
	cout << "yA= "; cin >> yA;
	cout << "toa do B: \n";
	cout << "xB= "; cin >> xB;
	cout << "yB= "; cin >> yB;
	cout << "toa do C: \n";
	cout << "xC= "; cin >> xC;
	cout << "yC= "; cin >> yC;
	float xAB = xB - xA;
	float yAB = yB - yA;
	float yAC = yC - yA;
	float xAC = xC - xA;
	if (xAB * yAC == xAC * yAB) {
		cout << " 3 diem thang hang! \n";
		goto nhaplaidulieu;
	}
	else {
		float	AB = sqrt(((xB - xA) * (xB - xA)) + ((yB - yA) * (yB - yA)));
		float 	AC = sqrt(((xC - xA) * (xC - xA)) + ((yC - yA) * (yC - yA)));
		float 	BC = sqrt(((xC - xB) * (xC - xB)) + ((yC - yB) * (yC - yB)));
		float q = (AB + AC + BC) / 2;
		float dt = sqrt(q * (q - AB) * (q - AC) * (q - BC));
		xG = (xA + xB + xC) / 3;
		yG = (yA + yB + yC) / 3;
		float  r = dt / q ;
		float R = ( AB * AC * BC) / ( 4 * dt ) ;
		cout << " trong tam tam giac ABC la: G(" << xG << ";" << yG << ")" << endl;
		cout << " dien tich duong tron noi tiep tam giac ABC la: " << r * r * 3.14 << endl;
		cout << " dien tich duong tron ngoai tiep tam giac ABC la: " << R * R * 3.14 << endl;	
	}
	return 0;
}

