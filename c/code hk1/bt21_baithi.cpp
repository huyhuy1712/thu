#include <bits/stdc++.h>
using namespace std;

void doicot(int a[100][100], int n, int cot1, int cot2){
	for (int i = 0; i < n; i++){
	int k = a[i][cot1];
		a[i][cot1] =  a[i][cot2];
		a[i][cot2] = k;	
	}
	for (int i = 0; i < n; i++){
	for (int j = 0; j < n; j++){
	cout << a[i][j] << "\t";
} cout << endl;
}}

int main(){
	int n, cot1, cot2; 
	cout <<" n= "; cin >> n;
	int a[100][100];	
	for (int i = 0; i < n; i++){
	for (int j = 0; j < n; j++){
	cout << "a[" << i << "][" << j << "]= ";
	cin >> a[i][j];
	}
	}
	cout << "ma tran A: \n";
	for (int i = 0; i < n; i++){
	for (int j = 0; j < n; j++){
	cout << a[i][j] << "\t";
	} cout << endl;
	}
	cout << "vi tri cot can doi cho: "; cin >> cot1;
	cout << "vi tri cot can doi cho: "; cin >> cot2;
	doicot(a, n, cot1, cot2);
} 
