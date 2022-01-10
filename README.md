# LP simplex
A implementation for simplex algorithm solving LP

Implementation of simplex algorithm

 maximize z = c'[x, 1]
 subject to 
        Ax <= b
        x >= 0
 return 'unbounded' if unbounded, 'infeasible' if infeasible, 'optimal',z* and x* if feasible.
 
 INPUT: 
 ```
    c: a n + 1 array, where the last term is constance.
    A: a m x n matrix 
    b: a m x 1 matrix 
```

OUTPUT:

```
    INFO, z*, x*. 
```
In practice, I have extendde A with 1, like

```
maximize c1 * N1 + ... + cn * Nn + cn+1 * 1
----------------------------
|       N1   N2 ...  Nn   1|
|B1 =  a11  a12 ... a1n  b1|
|B2 =  a21  a22 ... a2n  b2|
|...                       |
|Bm =  am1  am2 ... amn  bm|
----------------------------
```
