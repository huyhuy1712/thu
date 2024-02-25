#include <bits/stdc++.h>
using namespace std;
int main(){
	int n; 
	cout << "n= "; cin >> n;
	int a[n][n];
	for (int i = 0 ; i < n; i++){
	for (int j = 0; j < n; j++){
	cout << "a[" << i <<"][" << j << "]= "; cin >> a[i][j];
	}
	}
	cout << "ma tran A la: \n";
	for (int i = 0 ; i < n; i++){
	for (int j = 0; j < n; j++){
	cout << a[i][j] << "\t";
	} cout << endl;
	}
	int s = 0;
	for(int i = 0; i < n; i++){
	s += a[i][n - 1 - i];
	} 
	cout << "tong phan tu tren duong cheo phu la: " << s;	
}
