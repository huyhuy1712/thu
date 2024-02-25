#include<bits/stdc++.h>
using namespace std;
 bool checkshc(long long int n){ // ham check so hoan chinh
 int s = 0;
 	for (int i = 1 ; i < n ; i++){
  	if (n % i == 0){ s += i;
	 }
	 } if (s == n ) return true; 
 		return false;
 }
 
 int tong(int n){ // ham tinh tong phan tu 1 so
 	int s = 0, so;
 	while(n != 0){
 	 so = n % 10;
	  s += so;
	  n /= 10; 
	 } return s; 
 }
 	int timsocotongmax (int n){ // ham tim so co tong phan tu max
 		int max = 1, i;
 	for(int i = 1; i <= n; i++){
 	if (tong(i) > max) {max = tong(i);}}
 		for(int j = 1; j <= n; j++){
	 if (tong(j) == max) { cout << "so nguyen duong nho hon bang n co tong chu so max la: " << j << "\n";
	 cout << "max= " << max << endl;
	 } 
	 }
	 }
 
bool checkarm(long long int n){ // ham check so armstrong
  	int count = 0, t = n, so1, so2, s = 0;
  	while ( n != 0){
  		so1 = n % 10;
  		count ++;
  		n /= 10;
	  } n = t;
  	while ( n != 0){
	so2 = n % 10;
	s += pow(so2,count);	
	n /= 10;
	  } n = t;
	  if ( s == n) return true;
	  return false;
  }
  
  bool checksnt(long long int n){ // ham check so nguyen to
  	int count = 0;
  	for (int i = 2; i < n; i++ ){ 
  		if (n % i == 0) count++;
	  }
	  if (count == 0 || n == 2) return true;
	  return false;
  }
  
  int songuoc(long long int n){ // ham dao so
  	int so, sodao = 0;
  	while ( n != 0){
  		so = n % 10;
  		sodao = (sodao * 10) + so;
  		n /= 10;
	  } return sodao;
  }
  
  void demsntk(long long int n){ // ham dem so nguyen to kep
  	int count = 0;
  	for (int i = 11; i <= n; i++){
  	if (checksnt(i) == true && checksnt(songuoc(i) == true) )count ++;
  } cout << " tu 10 -> " << n << " co " << count << " so nguyen to kep \n";
  }  
  
 void demso(long long int n){ // ham dem so
  int count1 = 0, count2 = 0;
  	for ( int i = 1; i <= n; i++){
	if (checkshc(i) == true) count1++;
	if (checkarm(i) == true) count2++;
	  }
	cout << "tu 1 -> " << n << " co " << count1 << " so hoan chinh va " << count2 << " so armstrong \n";  
}
  
   int demsntdx(int n){ 
   int count = 0, i, j;
	for (int f = 2; f <= n; f++ ){ // vong dem so
	for (i = f; i >= 2; i-- ){ 
	if (checksnt(i) == true) break;
  } 
	 for (j = f + 1; j <= pow(10,4); j++ ){
  	if (checksnt(j) == true) break;
  } 
  int sntdx = (i + j)/2;
	  if (checksnt(f) == true && f == sntdx ) count++;
  } cout << "tu 1 -> "<< n <<" co " << count << " so nguyen to doi xung \n";
  }
  
    int sntlientiep(int n){ // ham tim snt lien tiep cua n
  	int j = n+1;
	while( checksnt(j) != true){
	j++;
}  return j;
  }
  
  	timkcxy(int n){ // cau 5
  	int max = 1;
  	for(int i = 2; i <= n; i++){
  		if(checksnt(i) == true){
  	int k = abs(i - sntlientiep(i));
  	if (k > max) {
  		max = k;
	  } 
	  }
	  } 
	  int h;
 	for(int i = 2; i <= n; i++){
 		if (checksnt(i) == true){
 	int h = abs(i - sntlientiep(i));
 	if (h == max){ cout << i << " " << sntlientiep(i) << "\n";
	 }
	 }}
	  cout << "max= " << max << "\n";}
	 
  void tongxyz(int n){ // cau 6
 	int count1 = 0, count2 = 0;
 	for(int i = 1; i < n; i++){
 	for (int j = 2; j < n; j++){
 	if(i+j == n){ count1 ++;
	 }
	 } 
	 } 
	 cout << "co " << count1 << " cap so nguyen duong co tong bang n \n";
 	for(int i = 1; i < n - 2; i++){
 	for (int j = 2 ; j < n - 1; j++){
	for (int k = 3; k < n; k++)	{
	if (i + j + k == n ){ count2 ++;}
	}
 }} cout << "co " << count2 << " bo ba so nguyen duong co tong bang n \n";
}
  int main(){
  	long long int n;
  	cout << "n= "; cin >> n;
  	cout << "cau 1: \n";
	timsocotongmax(n);
  	cout << " cau 2: \n";
  	demso(n);
  	cout << "cau 3 \n";
  	demsntk(n);
  	cout << "cau 4: \n";
  	demsntdx(n);
  	cout << "cau 5: \n";
  	timkcxy(n);
  	cout << "cau 6: \n";
  	tongxyz(n);
  	return 0;
  }
