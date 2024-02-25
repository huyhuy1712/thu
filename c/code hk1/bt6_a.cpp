#include <bits/stdc++.h>
using namespace std;
void nhap(int x[100][100], int m, int n ){
	for (int i = 0; i < m; i++){
	for (int j = 0; j < n; j++){
	cout << "x[" << i << "][" << j << "]= "; cin >> x[i][j];
	}
}
}
void xuat(int x[100][100], int m, int n ){
	for (int i = 0; i < m; i++){
	for (int j = 0; j < n; j++){
	cout << x[i][j] << "\t";
	}
	cout << endl;}
}
int min(int x[100][100], int m, int n, int i){
	int min = x[i][0];
	for(int k = 0; k < n; k++){
	if (min > x[i][k]) min = x[i][k];
	} return min;
	}
int main(){
	int m, n;
	cout << "m= "; cin >> m;
	cout << "n= "; cin >> n;
	int a[100][100], b[100][100];
	nhap(a, m, n);
	xuat(a, m, n);
	cout << "mang B: \n";
	for (int i = 0; i < m; i++){
	for (int j = 0; j < n; j++){
	b[i][j] = a[i][j] * min(a, m, n, i);
	cout << b[i][j] << "\t";} 
	cout << endl;
}
}
