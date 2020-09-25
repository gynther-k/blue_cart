# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import Info_pb2 as Info__pb2


class InfoStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetInfo = channel.unary_unary(
                '/Info/GetInfo',
                request_serializer=Info__pb2.Request.SerializeToString,
                response_deserializer=Info__pb2.Reply.FromString,
                )


class InfoServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_InfoServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetInfo,
                    request_deserializer=Info__pb2.Request.FromString,
                    response_serializer=Info__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Info', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Info(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Info/GetInfo',
            Info__pb2.Request.SerializeToString,
            Info__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
