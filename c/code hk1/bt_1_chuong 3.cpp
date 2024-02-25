#include <iostream>
#include <math.h>
using namespace std;
 int dieukientamgiac (int a, int b, int c){
	if (a+b>c && b+c>a && a+c>b) {
	cout <<  "a,b,c la so do 3 canh cua tam giac ABC \n";
	return 1;}
	 else { cout << "khong phai tam giac!";
	 } 
}
void kiemtratamgiac (int a, int b, int c){ 

		 if (a == b && b == c){ cout << "ABC la tam giac deu \n"; 
		} 
	 else if ((a == b && b!=c) || (a == c && b!=c) || (b == c && b!=a)) {
			cout << "ABC la tam giac can \n"; 
		}
	else if (((a*a) + (b*b) == (c*c)) || ((a*a)+ (c*c) == (b*b)) || ((b*b)+(c*c) == (a*a))){
			cout << "ABC la tam giac vuong \n"; 
		} 
	else { cout << "ABC la tam giac thuong \n"; 
		} 
}
int main(){
	int a,b,c;
	cout << "a= "; cin >> a; 
	cout << "b= "; cin >> b;
	cout << "c= "; cin >> c;
	if(dieukientamgiac(a,b,c) == 1){
	 kiemtratamgiac(a,b,c);}
	return 0;
}

