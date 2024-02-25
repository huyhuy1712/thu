#include<iostream>
#include<math.h>
using namespace std;
int UCLN(int a, int b){ // ham tim UCLN (a,b)
	if(a == 0 || b == 0) {
	return a + b;
	}
	while (a!=b){
		if (a>b) a-=b;
		else { b-=a;}
	}
			return a;			
}
 void BCNN(int a, int b){ // ham tim BCNN (a,b)
	if( a != 0 && b != 0){
	cout << (a*b)/UCLN(a,b) << "\n";
}
else {cout << "khong co BCNN \n";
}}

	void  toigianphanso (int a, int b){ // ham toi gian phan so a/b
	if (b == 0){ cout << "loi! \n";
	}
	else{int tu = a / UCLN(a,b);
		int mau = b / UCLN(a,b);
	cout << tu << "/"<< mau << "\n";	
	}}
	
 void tong(int a, int b, int c, int d){ // ham tinh tong phan so
 	int tu = (a*d) + (b*c);
 	int mau = b*d;
 	if (mau == 0){ cout << "loi!";
	 }
	 else{
 	cout << "tong 2 phan so a/b + c/d = " << tu / UCLN(tu,mau) << "/" << mau / UCLN(tu,mau);
 }}

int main(){
	int a,b,c,d;
	cout <<"a= "; cin >> a;
	cout <<"b= "; cin >> b;
	cout <<"c= "; cin >> c;
	cout <<"d= "; cin >> d;
	
	cout <<"Cau a: \n";
	cout <<"UCLN cua "<<a<<" "<<"va"<<" "<<b<<" "<<"la: "<<	UCLN(a,b) <<"\n";

	cout << " Cau b: \n" <<"BCNN cua "<<a<<" "<<"va"<<" "<<b<<" "<<"la: ";
	 BCNN(a,b) ;
	cout << "Cau c: \n";
	 toigianphanso(a,b);
	 cout << "Cau d: \n";
	 tong(a,b,c,d);
		return 0;	
}
