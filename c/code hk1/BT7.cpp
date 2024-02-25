#include <bits/stdc++.h>
using namespace std;
int main(){
	int n;
	int a[100];
	cout << "n= "; cin >> n;
	for(int i = 0; i < n; i++){
		cout << "a[" << i << "]= "; cin >> a[i];
	}
	for (int i = 0; i < n; i++){
		cout << a[i] << " ";
	} cout << "\n";
int sum1 = 0, sum2 = 0;
for(int i = 0; i < n; i++){
	sum1 += a[i];
	if( sum1 >= sum2){ sum2 = sum1;
	}
} 
 cout << sum2;}


