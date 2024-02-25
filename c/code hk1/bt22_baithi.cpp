#include <bits/stdc++.h>
using namespace std;
void nhapMT(int x[100][100], int row, int columm){
	for(int i = 0; i < row; i++ ){
	for (int j = 0; j < columm; j++){
	cout << "x[" << i << "][" << j << "]= ";
	cin >> x[i][j];
	}
	}
}
void xuatMT(int x[100][100], int row, int columm){
	for(int i = 0; i < row; i++ ){
	for (int j = 0; j < columm; j++){
	cout << x[i][j] << "\t";} cout << endl;	
}}

void sapxep(int x[100][100], int row, int columm){
	int k = row*columm; 
	for (int i = 0; i < k-1; i++ ){
	for (int j = i+1; j < k; j++){
		if (x[i % row][i / row] > x[j % row][j / row] ){
		int t = x[i % row][i / row];
		x[i % row][i / row] = x[j % row][j / row];
		x[j % row][j / row] = t;}
		
	}
	}
	for(int i = 0; i < row; i++ ){
	for (int j = 0; j < columm; j++){
	cout << x[i][j] << "\t";} cout << endl;	
}}
int main(){
	int row, columm;
	cout << "row= "; cin >> row;
	cout << "columm= "; cin >> columm;
	int a[row][columm];
	nhapMT(a, row, columm);
	cout << "ma tran A la: \n";
	xuatMT(a, row, columm);
	cout << "ma tran A tang dan: \n";
	sapxep(a, row, columm); 
}
