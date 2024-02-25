#include <bits/stdc++.h>
using namespace std;
int main(){
	int n;
	cout << "n= "; cin >> n;
	int a[n][n];
	for (int i = 0; i < n; i++){
	for (int j = 0; j < n; j++){
	cout << "a[" << i << "][" << j << "]= "; cin >> a[i][j];
	}
	}
	cout << "ma tran A: \n";
	for (int i = 0; i < n; i++){
	for (int j = 0; j < n; j++){
		cout << a[i][j] << "\t";
} cout << endl;
}
	int s = 0;
	for (int k = 0; k < n; k++){
	s += a[k][k];
	}
	cout << "tong phan tu tren duong cheo chinh la: " << s;
}
