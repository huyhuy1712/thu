#include <bits/stdc++.h>
using namespace std;
int min(int x[100][100], int m, int n, int row){
	int min = x[row][0];
	for (int i = 0; i < n; i++){
	if (min > x[row][i]) min = x[row][i];
	} return min;
}
int max(int x[100][100], int m, int n, int columm){
	int max = x[0][columm];
	for (int i = 0; i < m; i++){
	if (max < x[i][columm]) max = x[i][columm];
	} return max;
}

int main(){
	int row, columm , i, j ;
	cout << "row= "; cin >> row;
	cout << "columm= "; cin >> columm;
	int a[100][100];
	for( i = 0; i < row; i++){
	for( j = 0; j < columm; j++){
	cout << "a[" << i << "][" << j << "]= ";
	cin >> a[i][j];
	}
	}
	cout << "ma tran A la: \n";
	for( i = 0; i < row; i++){
	for( j = 0; j < columm; j++){
	cout << a[i][j] << "\t";
} cout << endl;
}
int t, h;
cout << "dong can tim min: "; cin >> t;
cout << "min= " << min(a, row, columm, t) << "\n";
cout << "cot can tim max: "; cin >> h;
cout << "max= " << max(a, row, columm, h) << "\n";
}
