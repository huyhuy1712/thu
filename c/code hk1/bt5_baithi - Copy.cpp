#include <bits/stdc++.h>
using namespace std;
 void bin(int n){
 	int t1, t2 = 0, i = 0, u = n;
	while (n != 0){
	 t1 = (n % 2) * pow(10,i);
	t2 += t1;
	n /= 2;
 i++;} 
 cout << "he nhi phan cua " << u << " la: " << t2;
}

int main (){
	int n;
	cout << "n= "; cin >> n;
	bin(n);
	return 0;
}
