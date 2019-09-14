/* 2º PROJETO DA PRIMEIRA UNIDADE DE STR - UFRN
 * GERENCIADOR DE PROCESSOS
 * DANIELLY COSTA E DANIEL ARAÚJO
 * 
 * Implemente um programa com as seguintes funcionalidades
 * - Mostre numa interface gráfica os processos em execução (com filtro).
 * - Pause/continue e mata um determinado processo.
 * - Muda a prioridade de um determinado processo.
 * - Escolhe a CPU que um determinado processo irá executar.
 */

#include <time.h>
#include <iostream> // para: cout
#include <stdio.h>
#include <unistd.h> // para: sleep()
#include <stdlib.h>
#include <math.h>

#include <sys/time.h> // getpriority(int which, int who)  setpriority(int which, int who, int prio);
#include <sys/resource.h>

using namespace std;

int main()
{
  system("ps -af -U $USER | grep fork ");

}
