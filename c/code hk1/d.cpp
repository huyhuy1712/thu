#include <bits/stdc++.h>
using namespace std;
 void tongxy(int n){
 	int count = 0;
 	for(int i = 1; i < n; i++){
 	for (int j = 1; j < n; j++){
 	if(i+j == n){ count ++;
	 }
	 } 
	 } cout << "co " << count << " cap so nguyen duong co tong bang n \n";
 }
int main(){
	int n; 
	cout <<" n= "; cin >> n;
	tongxy(n);
} 
