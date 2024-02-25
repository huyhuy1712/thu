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

int main(){
	char s[MAX] = "10063#Le Khai Minh#M#8.5";
	sv a;
	
//	printf("Nhap thong tin theo dang MSV#HoTen#DTB: ");
//	fflush(stdin);
//	gets(s);
// tach ma SV
	char *token = strtok(s,"#");
	for(int i = 0; i < strlen(token); i++){
	a.MSV[i] = token[i];
}
// tach ho va ten
	token = strtok(NULL,"#");
	char k[MAX];
	strcpy(k,token);
		char *temp = strtok(k," ");
		char *last_word;
		while(temp != NULL){
			last_word = temp;
			temp = strtok(NULL," ");
		}
	strcpy(a.hoten.TenSV,last_word);
	a.hoten.HoSV == (char*)malloc((strlen(token) - strlen(last_word))*sizeof(char));
		for(int i = 0; i < (strlen(token) - strlen(last_word)); i++){
			a.hoten.HoSV[i] = token[i];
		}
	a.hoten.HoSV[strlen(token) - strlen(last_word)] = '\0';
	puts(a.hoten.HoSV);
// tach gioi tinh 
	token = strtok(NULL,"#");
	strcpy(a.gt,token);
// tach DTB
	token = strtok(NULL,"#");
	a.DTB = atof(token); 
	printf("%f",a.DTB);
}
