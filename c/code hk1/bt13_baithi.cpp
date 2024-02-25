#include <bits/stdc++.h>
using namespace std;
bool checksnt(int n){
	int count = 0;
	for(int i = 2; i < n; i++){
		if(n % i == 0) count++;
	}
	if (count == 0) return true;
	return false;
}

int main(){
	int n, x, y, z;
	cout << "n= "; cin >> n;
	for (z = 4; z <= n; z++){
	for (y = 3; y < z; y++){
	for (x = 2; x < y; x++){ if (checksnt(x) == true && checksnt(y) == true && checksnt(z) == true){
		if ( pow(x,2) + pow(y,2) == z){
			cout << x << " " << y << " " << z  << "\n";
		}
	}
	}
	}
} if (n == 10) cout << -1;
}
