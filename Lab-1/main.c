#include <stdio.h>
#include <stdlib.h>

struct StateGraph{
  int *arr;
  struct StateGraph *next;
};

struct StateGraph *newState(int m, int n){
  struct StateGraph *tmp = (struct StateGraph *)malloc(sizeof(struct StateGraph));
  tmp->arr = (int *)malloc((m*n)*sizeof(int));
  tmp->next = NULL;
  return tmp;
}

struct Search{
  struct StateGraph *head;

  int statesExploredLength;


  // 8465853942
  int pathLength;

  struct StateGraph *tail;
};

void BFS_Search(struct Search *s){

}


void MoveGen(struct Search *s, struct StateGraph *sg){}


void GoalTest(struct Search *s, struct StateGraph *sg){}

void printEndState(struct Search *s){}

int main(int argc,char *argv[]){
/*
    Take Input and process
*/
for(int i = 0; i <= argc; i++ ){
  printf("\n%s\n", argv[i] );
}



//  Search Algorithm

/*
    Print output
*/
}
