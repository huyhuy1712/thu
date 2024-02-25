#include <bits/stdc++.h>
#include <cstdlib>
using namespace std;
int GetRandom(int min,int max){
    return min + (int)(rand()*(max-min+1.0)/(1.0+RAND_MAX));}
    
int main(){
	long int c1 = 0, c2 = 0, c3 = 0, c4 = 0, c5 = 0, c6 = 0;
	srand((unsigned int) time(NULL));
	for (long int i = 1; i <= 6*pow(10,6); i++){
	int t = GetRandom(1, 6);
	if (t == 1) c1++;
	if (t == 2) c2++;
	if (t == 3) c3++;
	if (t == 4) c4++;
	if (t == 5) c5++;
	if (t == 6) c6++;
} cout << "so lan xuat hien nut 1: " << c1 << "\n";
	cout << "so lan xuat hien nut 2: " << c2 << "\n";
	cout << "so lan xuat hien nut 3: " << c3 << "\n";
	cout << "so lan xuat hien nut 4: " << c4 << "\n";
	cout << "so lan xuat hien nut 5: " << c5 << "\n";
	cout << "so lan xuat hien nut 6: " << c6 << "\n";	
}
