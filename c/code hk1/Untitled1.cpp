#include <stdio.h>
using namespace std;
long cau(int n) {
	if (n == 1) return 1;
	else return n + cau(n - 1);
}
int main() {
	int n;
	printf("nhap n: ");
	scanf("%d", &n);
	printf("cau a :");
	printf("%d\n", cau(n));
}
