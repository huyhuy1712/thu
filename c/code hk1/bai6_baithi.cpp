#include <bits/stdc++.h>
using namespace std;
int V(int a, int b, int c){
	return a*b*c;
 }
 
 int main(){
 	cout << "Tinh the tich hinh hop chu nhat \n";
 	int a, b, c;
 	cout << " nhap chieu dai: "; cin >> a;
 	cout << " nhap chieu rong: "; cin >> b;
 	cout << " nhap chieu cao: "; cin >> c;
	cout << " The tich hinh hop chu nhat: " << V(a,b,c);
 	return 0;
	 }
