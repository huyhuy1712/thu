#include<iostream>
#include <math.h>
using namespace std;
bool checksnt(int n){
	int dem = 0 ; 
	for (int i = n-1; i>=2; i--){
		if (n % i == 0) dem++ ; 	
	} 
	if (dem == 0 && n != 0 && n!= 1){ return true;;
	} 
  else { return false;}
}
 
int sodoi(int n){
	int so, sodoi = 0;
	while(n != 0){
		so = n % 10;
		sodoi = (sodoi*10) + so;
		n /= 10; 
	} return sodoi;
}

int main (){
	for (int k = 10000; k <= 99999; k++ ){
	if((sodoi(k) == k) && (checksnt(k) == true)) {
		cout << k << " ";
	}
} return 0;
}

