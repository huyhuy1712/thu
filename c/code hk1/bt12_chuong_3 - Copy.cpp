#include <string.h>
#include <math.h>
#include <stdio.h>
#include <iostream>
using namespace std;

double Round(double n){ // ham lam tron
 double b = n;
 while (n>1) {n -= 1;} // lay phan thap phan
 if(n>=0 && n<0.25) {
 b = b - n;}
 if(n>=0.25 && n<0.75) {
 b = b - n + 0.5;}
 if(n >= 0.75 && n <= 1) {
 b = b - n + 1;}
 return b;
}
int main(){
	char HoTen[30];
	char sbd[30];
	float Toan, Ly, Hoa;
	puts("Nhap ho ten: ");
	gets(HoTen);
	puts("nhap so bao danh: ");
	gets(sbd);
	cout << "toan la \n";
	cin >> Toan;
	cout << "Ly la: \n";
	cin >> Ly;
	cout <<"Hoa la: \n";
	cin >> Hoa;
	cout << " Ho va ten la: " << HoTen << "\n";
	cout << "so bao danh la: " << sbd << "\n";
	cout << "diem toan = " << Round(Toan) << "\n";
	cout << " diem ly = " << Round(Ly) << "\n";
	cout << "diem hoa = " << Round(Hoa)<< "\n";
	return 0;
}

