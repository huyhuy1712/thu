#include <bits/stdc++.h>
using namespace std;
int gt(int n){
int k = n; 
for (int i = k - 1; i >= 1; i--){
 n *= i;
} return n;
}
int main(){
	int n, k;
	cout << "k= "; cin >> k;
	cout << "n= "; cin >> n;
	if (k > n) {cout << "error!";
	}
	else{
	int C = gt(n) / (gt(n-k)*gt(k));
	int A = gt(n) / gt(n-k);
	cout << n << "C" << k << "= " << C << "\n";
	cout << n << "A" << k << "= " << A << "\n";
	}
}
