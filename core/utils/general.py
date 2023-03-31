from rest_framework import parsers, renderers, permissions, authentication, views, status


class CSRFExemptSessionAuth(authentication.SessionAuthentication):

    def enforce_csrf(self, request):
        pass


class JSONApi(views.APIView):
    authentication_classes = (authentication.TokenAuthentication, CSRFExemptSessionAuth,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (renderers.JSONRenderer,)
    parser_classes = (parsers.JSONParser,)


