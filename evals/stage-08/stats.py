from __future__ import annotations
import math

def proportion(k:int,n:int)->float:
    return k/n if n else float("nan")

def wilson_interval(k:int,n:int,z:float=1.959963984540054):
    if n == 0:
        return (float("nan"),float("nan"))
    p=k/n
    den=1+z*z/n
    center=(p+z*z/(2*n))/den
    half=(z*math.sqrt((p*(1-p)+z*z/(4*n))/n))/den
    return (max(0.0,center-half),min(1.0,center+half))

def zero_failure_upper_bound(n:int,alpha:float=0.05)->float:
    if n <= 0:
        return float("nan")
    return 1 - alpha**(1/n)

def zero_failure_required_n(target_upper:float,alpha:float=0.05)->int:
    if not (0 < target_upper < 1):
        raise ValueError("target_upper must be between 0 and 1")
    return math.ceil(math.log(alpha)/math.log(1-target_upper))

def cohens_kappa(labels_a,labels_b):
    if len(labels_a) != len(labels_b) or not labels_a:
        raise ValueError("labels must have equal non-zero length")
    cats=sorted(set(labels_a)|set(labels_b))
    n=len(labels_a)
    po=sum(a==b for a,b in zip(labels_a,labels_b))/n
    pa={c:labels_a.count(c)/n for c in cats}
    pb={c:labels_b.count(c)/n for c in cats}
    pe=sum(pa[c]*pb[c] for c in cats)
    if pe == 1:
        return 1.0
    return (po-pe)/(1-pe)
