tileTypeProperties = {
    0:
    {
        'name': 'Air',          # Names to be used in editor
        'alpha': False,          # Since Surface.convert() is faster than Surface.convert_alpha(), we can tell the code whetever the image we made has any alpha pixels
        'render': False         # Air Tile is Empty and shouldn't be rendered
    },
    1:
    {
        'name': 'Wood V1',
        'alpha': False,
        'render': True
    },
    2:
    {
        'name': 'Wood V2',
        'alpha': False,
        'render': True
    },
    3:
    {
        'name': 'Dark Wood',
        'alpha': False,
        'render': True
    },
    4:
    {
        'name': 'Table Left',
        'alpha': True,
        'render': True
    },
    5:
    {
        'name': 'Table Right',
        'alpha': True,
        'render': True
    },
    6:
    {
        'name': 'Table Full',
        'alpha': True,
        'render': True
    },
    7:
    {
        'name': 'Table Mid',
        'alpha': True,
        'render': True
    }
}

def get(tile, property):
    return tileTypeProperties[tile][property]