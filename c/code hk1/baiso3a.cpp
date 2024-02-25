#include <bits/stdc++.h>
using namespace std;
bool ktrsnt(int n) {
	if (n<2) return false;
	for (int i=2; i<=sqrt(n); i++) {
		if(n%i==0) {
			return false;
		}
	} return true;
}
void nhapmang(int a[], int n) {
	cout<<"Nhap mang:"<<endl;
	for (int i=0;i<n;i++) {
		cin>>a[i];
	}
}
int main () {
	int a[100];
	int n;
	int sum;
	do {
		cout<<"Nhap n:"; cin>>n;
	} while (n<2||n>99);
	nhapmang(a,n);
	for (int i=0; i<n;i++) {
		if (ktrsnt(a[i])==true) 
		cout<<a[i]<<" ";
	}
}
