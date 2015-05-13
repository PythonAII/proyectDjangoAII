from urlparse import urlparse


def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.hostname
    return domain.split('.')[1] if domain.startswith('www') else domain.split('.')[0]


def get_filename(image):
    return image.split('/')[-1].split['.'][0]