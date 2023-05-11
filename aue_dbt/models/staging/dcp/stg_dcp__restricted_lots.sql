with source as (
    select * from {{ source('source_data', var('input_version')) }}
),

tax_lot_geometries as (
    select
        bbl,
        borocode,
        cast(wkb_geometry as geometry) as wkb_geometry
    from source
)

select * from tax_lot_geometries
