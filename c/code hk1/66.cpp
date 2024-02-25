#include <stdio.h>
#include <stdlib.h>

struct node{
	int data;
	node* next;
}; 

typedef node* NODE;

NODE maxlist(NODE I){
 	NODE p = I;
 	NODE max = p;
 	while(p != NULL){
 		if(p->data > max->data){
 			max = p;
		 }
	 p = p->next;
	 }
	 return max;
 }

NODE taonode(int data){
 	NODE p = (node*)malloc(sizeof(node));
	p->data = data;
	p->next = NULL;
	return p; 
}

void chendau(NODE &I, NODE p){
 	if(I == NULL){
 		I = p;
	 }
	 else{
	 	p->next = I;
	 	I = p;
	 }
}

void input(NODE &I){
 	int n;
 	printf("Nhap so luong phan tu: ");
 	scanf("%d",&n);
 	for(int i = 0; i < n; i++){
 		int data;
 		printf("\nnhap phan tu %d: ",i);
 		scanf("%d",&data);
 		chendau(I, taonode(data));
	 }
}

void output(NODE I){
 	printf("\n");
 	for(NODE p = I; p != NULL; p=p->next){
 		printf("%d ",p->data);
	 }
}

int main(){
	NODE I = NULL;
	input(I);
	output(I);
	
	NODE max_node = maxlist(I);
	if (max_node != NULL) {
		printf("\nMax cua DSLK la: %d", max_node->data);
	} else {
		printf("\nDSLK rong.");
	}
	
	return 0;
}

