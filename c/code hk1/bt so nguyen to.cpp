#include <iostream>
#include <math.h>
using namespace std;
	int kiemtrasonguyento(int n){
		int d=0;
	for ( int i = 2; i <= n-1; i++){
		if ( n % i == 0) {
			d++;
		}
		if (d==0){
	return true;
		}
		else{
			return false;
		}
		}
	return true;
	}
int main (){
	int i, n;
	cout<<"n= "; cin>> n;
for(i=2;i<n;i++){
	if(	kiemtrasonguyento(i) == true){
		cout << i <<" ";
	}
}
	return 0;
}
