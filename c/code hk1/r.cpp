#include <bits/stdc++.h>
using namespace std;
int main(){
	int n;
cout << "n= "; cin >> n;
int a[n], e[n];
for (int i = 0; i < n; i++){
	cout << "a[" << i << "]= "; cin >> a[i];
}
cout << "day so: ";
for (int i = 0; i < n; i++){
	cout << a[i] << " ";
}
int i, count = 1, j = 0, k = 0;;
	dk :
	for (i = j; i < n; i++){
		if (a[i] < a[i+1]) {
	count++; }
	else break;}
	e[k] = count;
	k++;
	j = i + 1;
	count = 1;
	if (i < n){goto dk;}
	int max = e[0];
	for (int v = 0; v < 100; v++){
	if (max < e[v]) max = e[v];
	} cout << max;
}
