#include <bits/stdc++.h>
using namespace std;
int ucln(int a, int b) {
	if (a == 0 || b == 0) return a+b;
	while (a != b){
		if (a > b) a -= b;
	else b -= a;} return a;
	}
int bcnn(int a, int b) {
	if ( a== 0 || b == 0) {
		cout << " khong co bcnn \n";
	} if (a != b){
		cout << " BCNN cua a va b la: " << (a*b) / ucln(a, b);
	}
}
int main () {
	int a; int b;
	cout << " nhap he so a, b: " << endl;
	cin >> a >> b;
	 cout << " UCLN cua a va b la: " << ucln(a,b) << "\n";
	bcnn(a,b);
	return 0;
}
