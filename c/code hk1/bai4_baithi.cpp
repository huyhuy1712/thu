#include <bits/stdc++.h>
using namespace std;
void sodao( int n) {
	int ndao=0; int t;
	while (n != 0) {
		t = n%10;
		ndao = (ndao*10)+t;
		n /= 10;
	}  cout << ndao << endl;
}
int main () {
	 int n;
	cout << " nhap n: " ;
	cin >> n;
	sodao(n);
}
