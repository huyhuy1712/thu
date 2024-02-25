#include <iostream>
#include <math.h>
using namespace std;
int main(){
	int n = 3 , k;
	int a[n];
	for(int i=0; i<n ; i++){
	cout<< "so= "; cin>> a[i] ;}
	k= a[0];
	for (int i=0 ; i<n-1 ; i++ ){
		for(int j=i+1 ; j<n ; j++){
			if( a[j] < a[i] ) { k = a[i];
			a[i] = a[j];
			a[j]= k;
			}
		}
	}
	for(int i=0 ; i<n ; i++){
	cout << a[i]<<" ";}
	return 0;
}
