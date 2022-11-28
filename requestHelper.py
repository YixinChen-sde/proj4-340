from requests import Response, Session

def parse_header(request_response):
    redirect_to_https, hsts, http_server = False, False, None
    error_range = [i for i in range(300, 311)]
    if request_response in error_range:
        if "https" in request_response.url:
            redirect_to_https = True
        if "Strict-Transport-Security" in request_response.headers:
            hsts = True
        if "Server" in request_response.headers:
            http_server = request_response.headers["Server"]
        return redirect_to_https, http_server, hsts
    else:
        return False, False, None

def get_server_info(hostname):
    curr_session = Session()
    curr_session.max_redirects = 10
    insecure_http, redirect_https, hsts, http_server = True, False, False, None
    try:
        url = "http://" + hostname
        request_response = curr_session.get(url, timeout=3)
        redirect_https, http_server, hsts = parse_header(request_response)
    except Exception as exception:
        try:
            url = "https://" + hostname
            insecure_http = False  # we switch to https connection
            request_response_https = curr_session.get(url, timeout=3)
            redirect_https, http_server, hsts = parse_header(request_response)
        except:
            pass
    return redirect_https, insecure_http, http_server, hsts