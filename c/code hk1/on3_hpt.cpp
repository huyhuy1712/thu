#include <bits/stdc++.h>
using namespace std;
	float D(float a, float b, float c, float d){
	return a*c - b*d;
	}
	int main(){
	float a, b, c, a1, b1, c1;
	cout << "a= "; cin >> a;
	cout << "b= "; cin >> b;
	cout << "c= "; cin >> c;
	cout << "a1= "; cin >> a1;
	cout << "b1= "; cin >> b1;
	cout << "c1= "; cin >> c1;
	float d = D(a, a1, b1, b);
	float Dy = D(a, a1, c1, c);
	float Dx = D(b1, b, c, c1);
	if ( d != 0){
	cout << "he phuong trinh co nghiem la: \n";
	cout << "x= " << Dx / d << "\n";
	cout << "y= " << Dy / d;
	}
	else { 
	if ( Dx + Dy == 0){
		cout << "he phuong trinh vo so nghiem!";
	}
	if( (Dx == 0 || Dy == 0) && Dx != Dy ){
		cout << "he phuong trinh vo nghiem!";
	}
	}
}
