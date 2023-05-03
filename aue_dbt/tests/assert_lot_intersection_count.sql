-- Lot intersections are pairs of tax lots, so the number of intersection records
-- should always be a function of the number of tax lots
-- intersections_count = tax_lots_count * (tax_lots_count - 1).
-- Therefore return records where this isn't true to make the test fail

with tax_lots_count as (
    select
        count(*) as lots_count,
        (lots_count * lots_count)
        - lots_count as calc_count_intersections
    from {{ ref('tax_lot_geometries' ) }}
),


intersections_count as (
    select count(*) as record_count_intersections
    from {{ ref('buffered_lot_intersections' ) }}
)

select
    tax_lots_count.*,
    intersections_count.*
from tax_lots_count
full outer join intersections_count
    on
        tax_lots_count.calc_count_intersections
        = intersections_count.record_count_intersections
where
    tax_lots_count.calc_count_intersections is null
    or intersections_count.record_count_intersections is null
