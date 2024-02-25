#include <stdio.h>
#include <stdlib.h>

int main(){
	int a[100][100];
	int m,n;
	printf("m= ");
	scanf("%d",&m); 
	printf("n= ");
	scanf("%d",&n); 
	for(int i = 0; i < m;i++){
		for(int j =0;j<n;j++){
	scanf("%d",&a[i][j]);		
		} 
	}
	for(int i = 0; i < m;i++){
		for(int j =0;j<n;j++){	
		printf("%d ",a[i][j]);} 
		printf("\n");}
		printf("%d",a[5/4][5%4]);
}
