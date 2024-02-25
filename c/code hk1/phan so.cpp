#include <bits/stdc++.h>
using namespace std;
	int UCLN(int a, int b){
		if (a == 0 || b == 0) return a+b;
		while (a != b){
		if (a > b) a -= b;
		else {
		b -= a;}
		} return a;
	}
int main(){
	cout << "tinh tong hieu thuong tich phan so a/b + c/d \n";
	int a, b, c, d;
	cout << " a= "; cin >> a;
	cout << " b= "; cin >> b;
	cout << " c= "; cin >> c;
	cout << " d= "; cin >> d;
		if( b == 0 || d == 0){
		cout << "Error!";}
	else{
	cout << "phan so : " << a / UCLN(a,b) << "/" << b / UCLN(a,b)<< "\n";
	cout << "phan so : " << c / UCLN(c,d) << "/" << d / UCLN(c,d) << "\n";
	int tongtu = a*d + b*c;
	int hieutu = a*d - b*c;
	int tichtu = a*c;
	int thuongtu = a*d;
	int thuongmau = b*c; 
	int mau = b*d;
	cout << "tong= " << tongtu / UCLN(tongtu, mau) << "/" << mau / UCLN(tongtu, mau) << "\n";
	cout << "hieu= " << hieutu / UCLN(hieutu, mau) << "/" << mau / UCLN(hieutu, mau) << "\n";
	cout << "tich= " << tichtu / UCLN(tichtu, mau)  << "/" << mau / UCLN(tichtu, mau)  << "\n";  	
	cout << "thuong= " << thuongtu / UCLN(thuongtu, thuongmau)  << "/" << thuongmau / UCLN(thuongtu, thuongmau)  << "\n";
}
}
