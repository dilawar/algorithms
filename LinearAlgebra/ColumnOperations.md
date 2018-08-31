---
title: Inverse by using column operations
author: Dilawar Singh
institute: NCBS Bangalore
---

# Elementary column operation and permutation matrix

If we tranform $A=\begin{bmatrix} a & b \\ c & d \end{bmatrix}$ to $A_1=\begin{bmatrix} a & b-a \\ c
& d-c \end{bmatrix}$ by elementary column operation $O: C_2 \leftarrow C_1 - C_2$.
We can write $A=A_1P_1$ where $P_1$ is a permutation matrix.  For example:

   Elementary column operation  |  Matrix 
   -----------------------------+---------------------------------------------
   $C_1 \leftarrow C_1 - C_2$   |  $\begin{bmatrix} 1&0\\-1&1\end{bmatrix}$
   $C_2 \leftarrow C_2 + 2C_1$  |  $\begin{bmatrix} 1&2\\0&1\end{bmatrix}$
