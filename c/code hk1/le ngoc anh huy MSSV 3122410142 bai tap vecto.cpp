#include <bits/stdc++.h>
using namespace std;
struct Oxy{
 float A, B, C, D ,a1 , a2, b1, b2,c1 , c2 ,d1, d2, AB, CD;
 void diem(){
 	cout << "a1= "; cin >> a1;
 	cin.ignore();
 	cout << "a2= "; cin >> a2;
 	cout << "diem A(" << a1 << ";" << a2 << ") \n";
 	cin.ignore();
 	cout << "b1= "; cin >> b1;
 	cin.ignore();
 	cout << "b2= "; cin >> b2;
 	cin.ignore(); 	
 	cout << "diem B(" << b1 << ";" << b2 << ") \n";
 	cout << "c1= "; cin >> c1;
 	cin.ignore();
 	cout << "c2= "; cin >> c2;
 	cin.ignore(); 	
 	cout << "diem C(" << c1 << ";" << c2 << ") \n";
  	cout << "d1= "; cin >> d1;
 	cin.ignore();
 	cout << "d2= "; cin >> d2;
 	cin.ignore(); 	
 		cout << "diem D(" << d1 << ";" << d2 << ") \n";
 }
 void vecto (){
 	float xAB = b1 - a1;
	float yAB = b2 - a2;
	float xCD = d1 - c1;
	float yCD = d2 - c2;
 	cout << "vecto AB(" << xAB << ";" << yAB << ") \n";
 	cout << "vecto CD(" << xCD << ";" << yCD << ") \n";	  
 }
 void tong(){
 	float xAB = b1 - a1;
	float yAB = b2 - a2;
	float xCD = d1 - c1;
	float yCD = d2 - c2;
	cout << "AB + CD = " << "(" << xAB + xCD << ";" << yAB + yCD << ") \n"; 
 }
 void hieu(){
 	float xAB = b1 - a1;
	float yAB = b2 - a2;
	float xCD = d1 - c1;
	float yCD = d2 - c2;
	cout << "AB - CD = " << "(" << xAB - xCD << ";" << yAB - yCD << ") \n";  	
 }
 void tich(){
 	float xAB = b1 - a1;
	float yAB = b2 - a2;
	float xCD = d1 - c1;
	float yCD = d2 - c2;
 	float tichvohuong = (xAB*xCD) + (yAB*yCD);
 	cout << "tich vo huong cua vecto AB va CD la: " << tichvohuong << "\n";
 	if(tichvohuong == 0) {
 	cout << " vecto AB va CD vuong goc nhau \n";
	 }
	 else { cout << "2 vecto AB va CD khong vuong goc nhau \n";
	 }
 }
 void checkvitri(){
 	float d = a1 + a2 - 4;
 	float d1 = b1 + b2 - 4;
 	float d2 = c1 + c2 - 4;
 	float d3 = d1 + d2 - 4;
 	cout << "d: x + y = 4 \n";
	 if (d > 0) cout << " diem A nam phia tren d \n";
	 if (d == 0) cout << "diem A thuoc d \n";
	 if (d < 0) cout << "diem A nam phia duoi d \n";
	
	 if (d1 > 0)  cout << " diem B nam phia tren d \n";
	 if (d1 == 0) cout << "diem B thuoc d \n";
	 if (d1 < 0) cout << "diem B nam phia duoi d \n";

	 if (d2 > 0)  cout << " diem C nam phia tren d \n";
	 if (d2 == 0) cout << "diem C thuoc d \n";
	 if (d2 < 0) cout << "diem C nam phia duoi d \n";

	
	 if (d3 > 0)  cout << " diem D nam phia tren d \n";
	 if (d3 == 0) cout << "diem D thuoc d \n";
	if (d3 < 0) cout << "diem D nam phia duoi d \n";
	}
};

int main (){
	Oxy k;
	k.diem();
	k.vecto();
	k.tong();
	k.hieu();
	k.tich();
	k.checkvitri(); 
} 
