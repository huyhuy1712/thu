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
};
typedef node* NODE;

NODE create_node(student x){
	NODE p = new node;
	strcpy(p->data.name,x.name);
	p->data.ID = x.ID;
	p->data.grade = x.grade;
	p->next = NULL;
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
	for(NODE p = I; p; p=p->next){
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
	
	void xoa(NODE &I,int x){
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
		}
	}
	void insert_last(NODE &I, NODE x){
		NODE p = I;
		if(I == NULL){
			I = x;
		}
		else{
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
			for(int i = 0; i < pos; i++){
				pre = p;
				p = p->next;
			}
			pre->next = x;
			x->next = p;
			n++;
		}
	} 
	
	int main(){
		NODE I;
		int n;
		printf("n: ");
		scanf("%d",&n);
		create_list(I);
		input(I,n);
		int x;
		printf("x: ");
		scanf("%d",&x);
		insert(I,create_node()) 
	}
