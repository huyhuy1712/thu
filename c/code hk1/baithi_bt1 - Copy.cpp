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
 
int main (){
	int n, count = 0;
	cout << "n= "; cin >> n;
	for (int j = 2; j <= n; j++){
		if (checksnt(j) == true) {
			count ++;
		}}
			cout << "tu 1 -> " << n << " co " << count << " so nguyen to \n";
}
