#include <bits/stdc++.h>
using namespace std;
 bool checksnt(int n){
 	int count = 0;
 	for ( int i = 2 ; i < n; i++){
	if (n % i == 0) count ++;  		
	 }
	 if ( count == 0 ) return true;
	 return false;
 } 
 
 	tach(int n){ 
 	int t = n;
 	if( n == 1 ) cout << 1; 
 	for ( int i = 2; i <= n; i++){
 	if (checksnt(i) == true){
 	while ( n % i == 0 ) {
	 cout << i << " "; 
	n /= i;
	} n = t;
} 
}
}
 
 int main (){
 	int n;
 	cout << "n= "; cin >> n;
	tach(n);		
 }

