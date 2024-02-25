#include <iostream>
using namespace std;
struct phanso{
	int tu;
	int mau;
};
struct list{
	int n;
	phanso l[100];
};

int UCLN(int a,int b){
	if(a == b) return a;
	while(a != b){
		if(a>b) a-=b;
		else b-=a;
	} return a;
}
int BCNN(int a, int b){
	return (a*b)/UCLN(a,b);
}

//void quidong(phanso &a, phanso &b){
//	int bcnn = BCNN(a.mau,b.mau);
//	a.mau = bcnn;
//	b.mau = bcnn;
//	a.tu = a.tu*(bcnn/a.mau);
//	b.tu = b.tu*(bcnn/b.mau);
//} 
void timmax(list L){
	float max = (float)L.l[1].tu / (float)L.l[1].mau;  
	 for(int i = 1; i <= L.n; i++){
	float gt = (float)L.l[i].tu / (float)L.l[i].mau;  
	 	if(max <= gt ) max = gt; 
	 } 
	 for(int i = 1; i <= L.n; i++){
	float gt = (float)L.l[i].tu / (float)L.l[i].mau; 
	 	if(max == gt){
	 		cout << "phan so lon nhat la: \n";
	 		cout << L.l[i].tu << "/" << L.l[i].mau << "\n";
		 }
}
} 
void nhap1phanso(phanso &p) {
	nhaplai:
	cout << "nhap tu: ";
	cin >> p.tu;
	cout << "nhap mau: ";
	cin >> p.mau;
	if(p.mau == 0) goto nhaplai;
}
void nhapdsps(list &ps){
	cout << "nhap so luong ps: ";
	cin >> ps.n;
	for(int i = 1; i <= ps.n; i++){
	cout << "phan so " << i << ": \n"; 
		nhap1phanso(ps.l[i]);
	}
}
	void rutron(phanso &a){
		int ucln = UCLN(a.mau,a.tu);
		a.mau /= ucln;
		a.tu /= ucln; 
	} 
void xuat(list ps){ 
	for(int i = 1; i <= ps.n; i++){
		if(ps.l[i].mau == 1){
			cout << ps.l[i].tu << endl;
		}
		else{
	cout <<  ps.l[i].tu << "/" << ps.l[i].mau;
	cout << endl;
	}
}
}

float Sum(list L){
	float sum = 0;
	for(int i = 1; i <= L.n; i++){
		float gt = (float)L.l[i].tu / (float)L.l[i].mau;
		sum += gt;
	}
	return sum;
}

int main(){
	int n;
	list ps;
	nhapdsps(ps);
	for(int i =1; i <= ps.n; i++){
		rutron(ps.l[i]); 
		}
	xuat(ps); 
	timmax(ps);
	cout << "tong cua cac phan so la: " << Sum(ps);
} 
