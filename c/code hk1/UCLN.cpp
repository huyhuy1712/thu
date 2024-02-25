#include<iostream>
#include<math.h>
using namespace std;
	float UCLN( int a, int b){
	if ( a==0 || b==0)
	return a+b;
	while (a!=b){ 
	if (a>b) a-=b;
else{b-=a;}}
	return a;}
int main(){int a,b;
	cin>> a;
	cin>>b;
 cout <<UCLN(a,b);
 return 0;
}
