#include <bits/stdc++.h>
using namespace std;
bool checksnt(int n){
	int count = 0;
	for (int i = 2; i < n; i++){
		if(n % i == 0) count++;
	}
	if(count == 0) {
	return true;}
	return false; 
}
int main(){
int a[100];
for(int i = 0; i < 10; i++){
for (int j = 2; j < 10; j++){
	if(checksnt(j) == true){
a[i] = j; 
}
}}
for(int i = 0; i < 10 ; i++){
	cout << a[i] << " "; 
} 
}
