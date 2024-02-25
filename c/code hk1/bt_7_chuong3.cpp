#include <iostream>
#include <math.h>
using namespace std;
	void solve(int n){
 	int s = 0, m = 1;
 	for (int i = 1; i <= n; i++){
 		m *= i;
		s += m;
	 } cout << "S(" << n << ")= " << s;  
 } 
 int main(){ 
 	int n;
 	cout <<"n "; cin >> n;
 	cout << "S(n)= 1 + 1*2 +1*2*3 +1*2*3*4*....*n \n";
 	solve (n);
 	return 0;
 }
