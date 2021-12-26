import json
from rest_framework import renderers


# class UserRenderer(renderers.JSONRenderer):
#     def render(self, data,accepted_media_type=None, renderer_context=None):
#         response=''
#         import pdb
#         pdb.set_trace()
#         return super().render(data,accepted_media_type=accepted_media_type, renderer_context=renderer_context)




class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data,accepted_media_type=None, renderer_context=None):
        response=''
        if 'ErrorDetail' in str(data):
            response=json.dumps({'errors': data})
            print(data)
        else:
            response=json.dumps({'data': data})
            print(data)
            
        return response
        # return super().render(data,accepted_media_type=accepted_media_type, renderer_context=renderer_context)