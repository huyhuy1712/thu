#include <bits/stdc++.h>
using namespace std;
int main(){
	int m, n, p;
	cout << "m= "; cin >> m;
	cout << "n= "; cin >> n;
	cout << "p= "; cin >> p;
	int a[m][n], b[n][p];
	for (int i = 0; i < m; i++ ){
	for (int j = 0; j < n; j++){
	cout << "a[" << i << "][" << j << "]= "; cin >> a[i][j]; 
	}
	}
	for (int i = 0; i < n; i++ ){
	for (int j = 0; j < p; j++){
	cout << "b[" << i << "][" << j << "]= "; cin >> b[i][j]; 
	}
	}  
	cout << "ma tran A: \n";
	for (int i = 0; i < m; i++ ){
	for (int j = 0; j < n; j++){
	cout << a[i][j] << "\t";
} cout << endl;
}
	cout << "ma tran B: \n";
	for (int i = 0; i < n; i++ ){
	for (int j = 0; j < p; j++){
	cout << b[i][j] << "\t";
} cout << endl;
}
	int k = 0, s = 0, t;
cout << "tich 2 ma tran la: \n";
for (int i = 0; i < m; i++){
for (int j = 0; j < p; j++){
	while (k < n){  // toa do thu i, j cua c dc tinh theo cong thuc xichma(k=1->n)(a[i][k]*b[k][j])
		t = a[i][k] * b[k][j];
		s += t;
		k++;}
	cout << s << "\t";
	k = 0;
	s = 0;
} cout << endl;
}	
}
