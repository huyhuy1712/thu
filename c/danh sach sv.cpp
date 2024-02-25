#include <stdio.h>
#include <string.h>
#define MAX 10000
struct student{
	char name[MAX];
	int ID;
	float grade;
};

struct node{
	student data;
	node *next;
	node *pre; 
};
typedef node* NODE;

NODE create_node(student x){
	NODE p = new node;
	strcpy(p->data.name,x.name);
	p->data.ID = x.ID;
	p->data.grade = x.grade;
	p->next = NULL;
	p->pre = NULL; 
	return p; 
}

void create_list(NODE &I){
	I = NULL; 
}

void insert_first(NODE &I, NODE x){
	if(I == NULL){
		I = x; 
	}
	else{
	x->next = I;
	I = x; 
	} 
}
    void swap(student &a, student &b){
    	student temp;
		strcpy(temp.name,a.name);
		strcpy(a.name,b.name);
		strcpy(b.name,temp.name);
		
		temp.ID = a.ID;
		a.ID = b.ID;
		b.ID = temp.ID;
		
		temp.grade = a.grade;
		a.grade = b.grade;
		b.grade = temp.grade; 
	} 
	
	void SelectionSort(NODE &I,int n){
		NODE min;
		for(NODE i = I; i->next; i = i->next){
			min = i;
			for(NODE j = i; j ; j = j->next){
				if(j->data.ID < min->data.ID){
					min = j;
				}
			}
			swap(i->data,min->data);
		}
	} 

void input(NODE &I,int n){
	for(int i = 0; i < n; i++){
		student a;
		printf("student %d: \n",i);
		printf("Enter your name: ");
		fflush(stdin);
		gets(a.name);
		printf("Enter your ID: ");
		scanf("%d",&a.ID);
		printf("Enter your grade: ");
		scanf("%f",&a.grade);
		printf("\n");
		insert_first(I,create_node(a));
	} 
} 

void output(NODE I){
	int i = 0;
	for(NODE p = I; p; p=p->pre){
		printf("\nStudent %d: \n",i);
		i++;
		printf("Full Name: ");
		puts(p->data.name);
		printf("ID: %d\n",p->data.ID);
		printf("Grade: %f",p->data.grade);
		printf("\n");
	}
}



	void tim(NODE I, int x){
		NODE p = I;
		while(p && p->data.ID != x){
			p = p->next;
		}
		if(p == NULL){
			printf("khong tim thay hoc sinh !!\n");
			return;
		}
		else{
			printf("Full Name: ");
			puts(p->data.name);
			printf("ID: %d\n",p->data.ID);
			printf("Grade: %f\n",p->data.grade);
		}
	}
	
	void xoa(NODE &I,int x,int &n){
		NODE p = I;
		NODE pre = NULL;
		while(p && p->data.ID != x){
			pre = p;
			p = p->next;
		}
		if(p == NULL) return;
		else{
			printf("Da xoa student co ID la %d\n",p->data.ID);
			pre->next = p->next;
			delete p;
			n--; 
		}
	}
	void insert_last(NODE &I, NODE x){
		if(I == NULL){
			I = x;
		}
		else{
		NODE p = I;
			while(p->next){
				p = p->next;
			}
			p->next = x;
		}
	}
	void insert(NODE &I, NODE x,int pos, int &n){
		NODE p = I;
		NODE pre = NULL;
		if(pos == 0){
			insert_first(I,x);
			n++;
		}
		else if(pos < 0 || pos > n){
			printf("Vi tri them vao khong hop le !!\n");
		}
		else if(pos == n){
			insert_last(I,x);
		n++;
		}
		else{
			for(int i = 0; i < pos-1; i++){
				pre = p;
				p = p->next;
			}
			pre->next = x;
			x->next = p;
			n++;
		}
	} 
	
void menu(NODE &I){
	int n;
	while(1){
		int i;
	printf("\t\t MENU \t\t\n");
	printf("1.Nhap danh sach\n");
	printf("2.Sap xep danh theo ID\n");
	printf("3.Tim hoc sinh theo ID\n");
	printf("4.Xoa hoc sinh theo ID\n");
	printf("5.Them hoc sinh\n");
	printf("6.Hien thi danh sach hoc sinh\n");
	printf("7.Hien thi so luong hoc sinh hien tai\n");
	printf("8.Hien cac hoc sinh co diem TB > 8\n");
	printf("So bat ki.Thoat chuong trinh\n");
	printf("\nNhap yeu cau: ");
	scanf("%d",&i);
	switch(i){
		case 1:
	printf("Enter the number of list: ");
	scanf("%d",&n);
		input(I,n);
		break;
		case 2:
			SelectionSort(I,n);
		break;
		case 3:
		int x;
		printf("Nhap ID hs can tim: ");
		scanf("%d",&x);
			tim(I,x);
		break;
		case 4:
			int x1;
			printf("Nhap ID hs can xoa: ");
			scanf("%d",&x1);
			xoa(I,x1,n);
		break;
		case 5:
			student x2;
			printf("Nhap hoc sinh can them: \n");
			printf("Full Name: ");
			fflush(stdin);
			gets(x2.name);
			printf("Nhap ID: ");
			scanf("%d",&x2.ID);
			printf("Nhap grade: ");
			scanf("%f",&x2.grade);
			int pos;
			printf("Nhap vi tri can them: ");
			scanf("%d",&pos);
			insert(I,create_node(x2),pos,n);
		break;
		case 6:
		printf("\t\t Danh sach \t\t\n");
			output(I);
		break;
		case 7:
			printf("So hs hien tai la: %d\n",n);
		break;
		case 8:
			for(NODE p = I; p ; p = p->next){
				if(p->data.grade > 8){
					printf("Full Name: %s",p->data.name);
					printf("\nID: %d",p->data.ID);
					printf("\nGrade: %f",p->data.grade); 
				}
			}
		default: break;
	} 
	}
}
int main(){
	NODE I;
	create_list(I);
	menu(I);
}
