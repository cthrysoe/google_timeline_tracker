class GoogleRequestBuilder(object):
    def __init__(self):
        self.base_google_request_url = \
            'https://www.google.com/maps/timeline/kml?authuser=0&pb=!1m8!1m3!1i{0}!2i{1}!3i{2}!2m3!1i{0}!2i{1}!3i{2}'

    def build_google_request(self, day, month, year):
        return self.base_google_request_url.format(year, month, day)
