#include <bits/stdc++.h>
using namespace std;
bool checksnt(int n){
	int count = 0;
	for (int i = 2; i < n; i++){
	if(n % i == 0) count++;
	}
	if(count == 0) {return true;}
	if (count != 0 || n <= 1) { return false;}	
	}
void phantichsnt(int n){ int i = 2;
	do{
	if(n % i == 0 && checksnt(i) == true){
	cout << i << " ";
	n /= i;	
} else i++;  
} while( i <= n);
}

	int main(){
	cout << "cau 1: \n";
	int n, count = 0;
	cout << "n= "; cin >> n;
	for(int i = 2; i <= n; i++){
	if(checksnt(i) == true) { count++; }
	} cout << "tu 1 -> n co " << count << " so nguyen to \n";
	cout << "cau 2: \n";
	phantichsnt(n);
	}

