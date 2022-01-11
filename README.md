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

- Step 1: check if any `bi < 0`. if true, solve the auxiliary linear program:
```
    maximize z = -x0
    subject to
            Ax - 1 * x0 <= b
            x0, x1, ..., xn >= 0

```
check if its optimal value is 0. If true, eliminate x0,
and forward the revised `(B, N, A)` to pivot iteration. Otherwise, we claim its infeasible since the domain is empty set.


If it's reaily prepared, we do nothing and directly forward to next step.

- Step 2: pivot slackness 
  
    We first convert original target function to expression incorporates only the variables in N.

    Next we find any constance `ci` in target function that is positive. Try to increment the `xi` before the tightest constraint discovered. If no constraints apply, we claim problem unbounded since `xi` can increase infinitely. 

    Replace the left-hand-side variable by `Ni`, substitute for all equations as well as target function. Repeat the step 2 until no `ci` is positive.
