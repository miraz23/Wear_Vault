
class LoggerConstants:
    METHOD = "method"
    """Key representing the method of the HTTP request."""

    URL = "url"
    """Key representing the URL of the HTTP request."""

    QUERY_PARAMETER = "query_parameter"
    """Key representing the query parameters of the HTTP request."""

    HEADERS = "headers"
    """Key representing the headers of the HTTP request or response."""

    BODY = "body"
    """Key representing the body of the HTTP request or response."""

    STATUS_CODE = "status_code"
    """Key representing the status code of the HTTP response."""

    CONTENT_LENGTH = "content_length"
    """Key representing the content length of the HTTP response."""

    CONTENT_TYPE = "content_type"
    """Key representing the content type of the HTTP response."""

    CONTENT_LENGTH_HEADER = "content-length"
    """Key representing the content length header."""

    CONTENT_TYPE_HEADER = "content-type"
    """Key representing the content type header."""

    NON_SENSITIVE_HEADERS = tuple(map(lambda x: x.lower(), [
        "Accept", "Accept-Charset", "Accept-Encoding", "Accept-Language",
        "Access-Control-Allow-Origin", "Cache-Control", "Connection",
        "Content-Encoding", "Content-Language", "Content-Length", "Content-Location",
        "Content-MD5", "Content-Range", "Content-Type", "Date", "ETag", "Expect",
        "Expires", "From", "Host", "If-Match", "If-Modified-Since", "If-None-Match",
        "If-Range", "If-Unmodified-Since", "Keep-Alive", "Last-Modified", "Location",
        "Max-Forwards", "Pragma", "Range", "Referer", "Retry-After", "Server",
        "Trailer", "Transfer-Encoding", "Upgrade", "User-Agent", "Vary", "Via",
        "Warning", "X-Forwarded-For", "X-Requested-With", "X-Powered-By"
    ]))
    """List of sensitive headers that need to be filtered."""
