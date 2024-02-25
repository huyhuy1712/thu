#include <stdio.h>
#include <string.h>
#include <stdlib.h> 
#define MAX 100
struct HoTen{
	char HoSV[MAX];
	char TenSV[MAX];
};
struct sv{
	char MSV[MAX];
	HoTen hoten;
	char gt[MAX];
	float DTB;
};
struct dssv{
	int n;
	sv a[MAX];
};
	
	void tachhoten(char *str, sv &a) {
    char *last_word = strrchr(str, ' ');
    if (last_word != NULL) {
        *last_word = '\0';  // ngat chuoi tai khoang trang cuoi cùng
        strcpy(a.hoten.TenSV, last_word + 1);  // copy tên vào bi?n tên c?a struct HoTen
        strcpy(a.hoten.HoSV, str);  // copy h? vào bi?n h? c?a struct HoTen
    }
}

	void input2(sv &a){
	char s[MAX] = "10063#Le Khai Minh#M#8.5";
	char *token = strtok(s,"#");
	int i = 0;
	while(token != NULL){
		switch(i){
			case 0:
				strcpy(a.MSV, token); break;
			case 1:
				tachhoten(token,a); break;
			case 2:
			strcpy(a.gt,token); break;
			case 3:
				a.DTB = atof(token); break;
			default: break;
		}
	i++;
	token = strtok(NULL,"#");	
	} 
	} 
int main(){
	sv a;
	input2(a);
	puts(a.gt);
	puts(a.hoten.TenSV);
	puts(a.hoten.HoSV);
	printf("%f\n",a.DTB);
	puts(a.MSV);
 
}
