#include <bits/stdc++.h>
using namespace std;
int main(){
	int n;
	cout << "n= "; cin >> n;
	int a[n], i, j, min;
	for (int i = 0; i < n; i++){
		cout << " a[" << i << "]= ";
		cin >> a[i];
	}
	min = a[i];
	for (int i = 0; i < n-1; i++){
	for (int j = i+1; j < n; j++){
	if (min > a[j]) min = a[j]; 		
		}
	} cout << "phan tu nho nhat trong mang la: " << min;
	return 0;
}
