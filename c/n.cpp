#include <stdio.h>
#include <string.h>
#include <ctype.h>
#define MAX 100
void push(char stack[], int *top, int value){
	if(*top == MAX - 1){
		printf("stack full !!");
	}
		else{
			stack[++(*top)] == value;
		}
}

int pop(char stack[],int *top){
	if(*top == -1){
		printf("stack overflow !!");
		return -1;
	}
	else{
		return stack[(*top)--];
	}
}

bool is_operator(char o){
	if(o == '+' || o == '-' || o == '*' || o == '/' || o == '^') return true;
	else return false; 
}

int uutien(char o){
	if(o == '^') return 3;
	else if(o == '*' || o == '/') return 2;
	else if(o == '+' || o == '-') return 1;
	else return 0;
}

void infix_to_postfix(char infix[]){
	int topi;
	int topp;
	topi = -1;
	topp = -1;
	char postfix[MAX];
	for(int i = 0; i < strlen(infix); i++){
	if(infix[i] == ' ') continue;
	else if(isdigit(infix[i]) || isalpha(infix[i])){
	push(postfix,&topp,infix[i]);
		}
	else if(is_operator(infix[i]) == true){
		while(topi != -1 && infix[topi] != '(' && uutien(infix[i]) <= uutien(infix[topi])){
		push(postfix,&topp,pop(infix,&topi));
		}
	push(infix,&topi,infix[i]);
	}
	else if(infix[i] == '('){
		push(infix,&topi,infix[i]);
	}
	else if(infix[i] == ')'){
	while(infix[topi] != '(' && topi != -1){
	push(postfix,&topp,pop(infix,&topi));	
		}
	pop(infix,&topi);
	}
	else{
		printf("co gia tri khong hop le !!");
		break;
	}
	}
	while(topi != -1){
	push(postfix,&topp,pop(infix,&topi));
	}
	postfix[topp+1] = '\0';
	strcpy(infix,postfix);
}

int main(){
	char infix[MAX];
	printf("nhap pheps tinh: ");
	gets(infix);
	infix_to_postfix(infix);
	for(int i = 0; i < strlen(infix); i++){
		printf("%c",infix[i]);
	}
} 
