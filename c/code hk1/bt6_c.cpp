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
	for (int i = 0; i < n; i++){
	for (int j = 0; j < m - 1; j++){
	for(int t = j+1; t < m; t++){
	if(x[j][i] > x[t][i]){
		int k = x[j][i];
		x[j][i] = x[t][i];
		x[t][i] = k;
	}}
	}}
	cout << "ma tran A sap xep tang dan theo tung cot: \n";
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

