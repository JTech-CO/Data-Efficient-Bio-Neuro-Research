"""Public query domains, nominal costs and a fixed audit schedule."""
from __future__ import annotations
from .contracts import Query

def candidate_queries(observational_only: bool = False) -> tuple[Query,...]:
    return tuple(Query(x,t,r,u) for x in (0.4,0.9,1.4) for t in (0.4,1.2,2.4)
                 for r in (("aggregate",) if observational_only else ("aggregate","pathway_a","pathway_b"))
                 for u in ((0.,) if observational_only else (0.,1.)))

def initial_queries() -> tuple[Query,...]:
    return (Query(.4,.4,'aggregate'),Query(1.4,.4,'aggregate'),
            Query(.4,2.4,'aggregate'),Query(1.4,2.4,'aggregate'))

def audit_query(index: int, observational_only: bool) -> Query:
    # Audit values never enter posterior fitting. They *do* affect the diagnostic gate.
    if observational_only:
        return Query((.9,1.4,.4)[index%3],(1.2,2.4,.4)[index%3],'aggregate',0.,replicate=1000+index)
    return Query((1.4,1.4,.9)[index%3],(2.4,.4,1.2)[index%3],
                 ('pathway_b','pathway_b','aggregate')[index%3],1.,replicate=1000+index)

def evaluation_queries(ood: bool=False, observational_only: bool=False) -> tuple[Query,...]:
    # Held-out conditions and times, never supplied to the acquisition module.
    return tuple(Query(x,t,r,u) for x in ((1.9,2.2) if ood else (.55,.75,1.1,1.25))
                 for t in (.7,1.7,2.1) for r in (("aggregate",) if observational_only else ('aggregate','pathway_b'))
                 for u in ((0.,) if observational_only else (0.,1.)))
