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
int main () {
	int n,dem=0;
	cout<<"Nhap n= "; cin>>n;
	for (int j=2; j<=n; j++) {
		if (ktrsnt(j)==true) {
			dem++;
		}
	}
	cout<<"Tu 1 den "<<n<<" co "<<dem<<" so nguyen to";
}
