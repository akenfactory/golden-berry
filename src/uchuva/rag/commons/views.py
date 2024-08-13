#--------------------------------------
# Imports.
#--------------------------------------

import json
from rest_framework import status
from wiki.views import search_ipm
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from commons.runtime.program3 import update_know_domain
from commons.serializers import KUpdateSerializer, QuerySerializer
from rest_framework.decorators import api_view, permission_classes

#--------------------------------------
# REST API Methos.
#--------------------------------------

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def query(request):
    try:
        if request.method == 'POST':
            serializer = QuerySerializer(data=request.data)
            if serializer.is_valid():
                data = request.data        
                dto = {
                    "prompt": data['prompt'],
                    "serviceID": 1,
                    "area": 100
                }
                rtn = search_ipm(request, dto)
                if rtn.status_code == 200 and rtn.data['external_source']:
                    resp = {
                        "statusCode": 200,
                        "body": json.dumps({
                            "message": "success",
                            "response": rtn.data['data']['completion']
                        })
                    }
                    return Response(resp, status=status.HTTP_200_OK)
                elif rtn.status_code == 403:
                    resp = {
                        "statusCode": 403,
                        "body": json.dumps({
                            "message": "You have exceeded the limit of requests"
                        })
                    }
                    return Response(resp, status=status.HTTP_403_FORBIDDEN)
                elif rtn.status_code == 500:
                    resp = {
                        "statusCode": 500,
                        "body": json.dumps({
                            "message": "Internal Server Error"
                        })
                    }
                    return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            resp = {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Bad Request",
                    "erros": serializer.errors
                })
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'PUT':
            serializer = KUpdateSerializer(data=request.data)
            if serializer.is_valid():
                data = request.data
                path = "model_%d_%d" % (request.user.id, 1)
                dto = {
                    "path": path,
                    "documento": data['document'],
                    "user": 100
                }
                rtn = update_know_domain(dto)
                if rtn:
                    resp = {
                        "statusCode": 200,
                        "body": json.dumps({
                            "message": "Updated robot knowledge"
                        })
                    }
                    return Response(resp, status=status.HTTP_200_OK)
                else:
                    resp = {
                        "statusCode": 500,
                        "body": json.dumps({
                            "message": "Internal Server Error"
                        })
                    }
                    return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            resp = {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Bad Request",
                    "erros": serializer.errors
                })
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
        resp = {
            "statusCode": 405,
            "body": json.dumps({
                "message": "Method Not Allowed"
            })
        }    
        return Response(resp, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        resp = {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal Server Error"
            })
        }
        return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)