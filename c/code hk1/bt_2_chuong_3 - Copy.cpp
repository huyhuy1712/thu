#include <iostream>
#include <math.h>
using namespace std;
void keobuabao(char nguoichoi1,char nguoichoi2) // b: bua, k: keo, a: bao
{ char b,k,a;
	if ('b' == nguoichoi1 && 'k' == nguoichoi2){
			cout << " Nguoi choi 1 win \n" << "Nguoi choi 2 lose \n";
}
if ('b' == nguoichoi1 && 'a'== nguoichoi2){	cout << " Nguoi choi 1 lose \n" << "Nguoi choi 2 win";
}
if ('k' == nguoichoi1 && 'b' == nguoichoi2){ 
	cout << " Nguoi choi 1 lose \n" << "Nguoi choi 2 win";}
if ('a' == nguoichoi1 && 'b' == nguoichoi2){cout << " Nguoi choi 1 win \n" << "Nguoi choi 2 lose";}
if ('a' == nguoichoi1 && 'k' == nguoichoi2){cout << " Nguoi choi 1 lose \n" << "Nguoi choi 2 win";}
	if (nguoichoi1 == nguoichoi2){ cout << "hai nguoi choi hoa nhau";
	}
}

	int main (){
	 char b,k,a, nguoichoi1, nguoichoi2;
	 cout << "Nguoi choi 1: "; cin >> nguoichoi1;
	  cout << "Nguoi choi 2: "; cin >> nguoichoi2;
	 keobuabao (nguoichoi1, nguoichoi2);
	 return 0;
}

