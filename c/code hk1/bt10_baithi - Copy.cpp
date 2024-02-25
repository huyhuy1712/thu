#include <bits/stdc++.h>
using namespace std;
long long int demso(int n){
	long long int count = 0;
	while (n != 0){
	n /= 10;
	count++;
 } return count;
}
int main(){
	int n, i;
	cout << "n= "; cin >> n;
	int a[n];
	for (i = 0 ; i < n; i++){
		cout << "a[" << i << "]= ";
		cin >> a[i];
		cout << "phan tu a[" << i << "] co " << demso(a[i]) << " chu so \n";
	}
	return 0;	
}
