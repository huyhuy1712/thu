#include <iostream>
#include <math.h>
using namespace std;
int sodao(long long int n){ // ham xep nguoc so
 int ndao = 0;
 	 while ( n != 0)  { int socuoi = n % 10; // lay so cuoi 
	  ndao = (ndao * 10) + socuoi; // them so cuoi vao ndao 
	  n /= 10; // xoa so cuoi  
	 } return ndao; 
	 } 
	
void kiemtrasodoixung (long long int n){ // ham kiem tra so doi xung 
	 	if  (n == sodao(n)){ cout << n << " la so doi xung \n";  
		 }
		 else { cout << n << " khong phai la so doi xung"; 
		 } 
	 } 
int main (){
	long long int n; 
	cout << "n= "; cin >> n;
	cout << "cau a: \n"; 
	cout << sodao(n) << "\n"; 
	cout  << "cau b: \n";
	kiemtrasodoixung(n); 
	return 0;
}
