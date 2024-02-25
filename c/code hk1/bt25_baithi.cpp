#include <bits/stdc++.h>
using namespace std;
struct toado{
	int x;
	int y;	
void nhapPdem(int n){ 
int i = 1, c1 = 0, c2 = 0, c3 = 0;
	while ( i <= n){
	cout << "x" << i << "= ";
	cin >> x;
	cin.ignore();
	cout << "y" << i << "= ";
	cin >> y;
	cin.ignore();
	int k = (3*x) + (4*y) + 1;
	if ( k > 0) { c1++;}
	if (k == 0){ c2++;}
	if (k < 0){ c3++;}
	i++;
	} 
	cout << "so diem nam tren y la: " << c1 << "\n";
	cout << "so diem thuoc y la: " << c2 << "\n";
	cout << "so diem nam duoi y la: " << c3 << "\n";
}
};

int main(){
	cout <<"duong thang y: 3x+4y+1=0 \n";
	toado k;
	int n;
	cout << "n= "; cin >> n ;
	k.nhapPdem(n);
}

