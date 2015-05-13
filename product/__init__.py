SHOPS = {
    "pk1": {
        "name": "Game",
        "url": "http:\\www.game.es",
        "brand": "game.png",
        "active": True,

    },
    "pk2": {
        "name": 'Xtralife',
        "url": 'http://www.xtralife.es',
        "brand": None,
        "active": True,
    }
    ,
    "pk99": {
        "name": None,
        "url": None,
        "brand": None,
        "active": False,
    }
}

PEGI_CHOICE = {
    (18, 100),
}

CONSOLE_CHOICE = (
    (1, u'ps4'),
    (2, u'ps3'),
    (3, u'ps2'),
    (4, u'ps1'),
    (5, u'xbox360'),
    (6, u'xbox one'),
    (7, u'wii'),
    (8, u'pc'),
    (9, u'ps vita'),
    (10, u'psp'),
    (11, u'wiiu'),
    (12, u'nitendo ds'),
)

CATEGORY_CHOICE = (
    (1, u'accion'),
    (2, u'arcade'),
    (3, u'aventura'),
    (4, u'conducion'),
    (5, u'deporte'),
    (6, u'estrategia'),
    (7, u'plataforma'),
    (8, u'rol'),
    (9, u'terror'),
    (10, u'shooter'),
    (11, u'infantil'),
    (12, u'otros'),
)

STOCK_CHOICE = (
    (1, u'reserva'),
    (2, u'agotado'),
    (3, u'disponible')
)