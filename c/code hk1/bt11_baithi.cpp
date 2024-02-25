#include <bits/stdc++.h>
using namespace std;
int main (){
	int n, i;
	float m = 1;
	cout << "n= "; cin >> n;
	int a[n];
	for (i = 0; i < n; i++){
	cout << "a[" << i << "]= ";
	cin >> a[i];
	}
	for (i = 0; i < n; i++){
	m *= a[i];
	} float s = m / n; 
	cout << "trung binh nhan cua tat ca phan tu la: " << s;
}
