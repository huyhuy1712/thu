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
void sapxep(int x[100][100],int m ,int n){
	int t = m*n;
	for (int i = 0; i < t - 1; i++){
	for (int j = i+1; j < t; j++){
	if(x[i/n][i%n] >= x[j/n][j%n]){
		int k = x[i/n][i%n];
		x[i/n][i%n] = x[j/n][j%n];
		x[j/n][j%n] = k;
	}}}
	cout << "ma tran A sap xep tang dan theo dong: \n";
	for (int i = 0; i < m; i++){
	for (int j = 0; j < n; j++){
	cout << x[i][j] << "\t";}
	cout << endl;}
}

int main(){
	int m, n;
	cout << "m= "; cin >> m;
	cout << "n= "; cin >> n;
	int a[100][100];
	nhap(a, m, n);
	cout << "ma tra A: \n";
	xuat(a, m, n);
	sapxep(a, m, n);
}			

