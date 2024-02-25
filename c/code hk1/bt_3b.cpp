#include <iostream>
#include <math.h>
using namespace std;
int main() {
	int n = 4;
	int a[n];
	for (int i = 0; i < n; i++) {
		cout << "so : "; cin >> a[i];
	}
	for (int i = 0; i < n - 1; i++) {
		for (int j = i + 1; j < n; j++) {
			if (a[i] > a[j]) {
				int t = a[i];
				a[i] = a[j];
				a[j] = t;
			}
		}
	}
	for (int i = 0; i < n; i++) {
		cout << a[i] << " ";
	}
	return 0;
}


