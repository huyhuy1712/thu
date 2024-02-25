#include <bits/stdc++.h>
using namespace std;
int nhap(int a[100], int n){
	for(int i = 0; i < n; i++){
	cout << "a[" << i << "]= "; cin >> a[i]; 
	}
}
int xuat(int a[100], int n){
	for(int i = 0; i < n; i++){
	cout << a[i] << " ";} cout << endl;
}
int Max(int a[100], int n){
	int max = a[0];
	for(int i = 1; i < n; i++){
	if(a[i] >= max)  {
	max = a[i];}
	} return max;  
} 
int main(){
int n;
cout << "n= "; cin >> n;
int a[n];
nhap(a,n);
xuat(a,n); 
	cout << "max= " << Max(a,n); 
}
