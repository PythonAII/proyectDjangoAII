__author__ = 'ismael'


def upload_image_game(console, category, name):
    return u'games/%s/%s/%s' % (console, category, name)


def upload_image_brand(brand):
    return u'shops/%s' % brand