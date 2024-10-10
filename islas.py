import numpy as np
matriz=np.matrix([[0,0,0,0,0],
                  [0,0,0,1,1],
                  [0,0,0,1,1],
                  [0,1,0,0,0],
                  [0,1,0,0,0]])
print(matriz)

NM=0

F,C=np.shape(matriz)
#print(F)
om=[]
visitas=np.zeros((F,C),dtype=bool)
print(f"tamaño de la matriz:filas:{F} Y COLUMNAS:{C}")
posicion=[(-1,0),(1,0),(0,-1),(0,1)]
def dfs(i,j):
   visitas[i,j]=True
   om.append([i,j])
   for d in posicion:
      ni,nj= i + d[0],j+d[1]
      if 0<=ni<F and 0<=nj<C and matriz[ni,nj]==1 and not visitas[ni,nj]:
         dfs(ni,nj)
         


for i in range(F):
    for j in range(C):
         if matriz[i, j] == 1 and not visitas[i, j]:
            NM+= 1     
            dfs(i, j)          


print(f'Número de islas de 1s: {NM}')
