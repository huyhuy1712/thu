#include <iostream>
#include <math.h>
using namespace std;
int main(){
	int n = 4, k = -1;
	int a[n];
	for (int i = 0; i<n ; i++){
		cout << "a["<<i<<"]= "; cin >> a[i];}
		for	(int i=0; i<n; i++){
	{
			if ( a[i] != a[i+1] ) k++;
		}
		}
		 cout << "so gia tri khac nhau la: "<< k <<endl;
		 return 0;}
	
