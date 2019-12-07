from flask import has_request_context, request
from urllib.parse import urlparse, urljoin


def is_safe_url(target_url):
    if has_request_context():
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target_url))
        return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
    else:
        return False
