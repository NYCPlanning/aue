-- Buffer tax lots and determine which ones intersect

with lot_pair_intersections as (
    select
        t1.bbl as t1,
        t2.bbl as t2,
        (
            case
                when
                    ST_INTERSECTS(
                        ST_BUFFER(t1.wkb_geometry, 500), t2.wkb_geometry
                    )
                    then
                        0
                else
                    1
            end
        ) as intersection
    from
        {{ ref('stg_dcp__restricted_lots') }} as t1
    inner join {{ ref('stg_dcp__restricted_lots') }} as t2 on (t1.bbl != t2.bbl)
)

select *
from lot_pair_intersections
