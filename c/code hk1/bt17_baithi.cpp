#include <bits/stdc++.h>
using namespace std;
int main(){
	int r,c;
	cout <<"so dong: "; cin >> r;
	cout << "so cot: "; cin >> c;
	int a[r][c], e[r][c];
	for (int i = 0 ; i < r; i++){
	for (int j = 0; j < c; j++){
		cout << "a[" << i << "][" << j << "]= "; cin >> a[i][j];}}
	for (int i = 0 ; i < r; i++){
	for (int j = 0; j < c; j++){
		cout << "e[" << i << "][" << j << "]= "; cin >> e[i][j];
	}
	}
	cout << "Ma tran A: \n";
	for (int i = 0 ; i < r; i++){
	for (int j = 0; j < c; j++){
		cout << a[i][j] << "\t";
} cout << endl;
}
cout << "Ma tran B: \n";
	for (int i = 0 ; i < r; i++){
	for (int j = 0; j < c; j++){
		cout  << e[i][j] << "\t";
} cout << endl;
}
cout << "Tong 2 ma tran A va B la: \n";
	for (int i = 0 ; i < r; i++){
	for (int j = 0; j < c; j++){
	cout << a[i][j] + e[i][j] << "\t";
} cout << endl;
}
}
