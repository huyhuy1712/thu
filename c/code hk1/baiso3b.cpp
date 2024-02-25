#include <bits/stdc++.h>
using namespace std;
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
	for (int i=0;i<n;i++) {
		sum=sum+a[i];
	}
	cout<<"Tong cua mang la: "<<sum;
}
