# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/health/v1/health.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1cproto/health/v1/health.proto\x12\x0b\x61uthservice"%\n\x12HealthCheckRequest\x12\x0f\n\x07service\x18\x01 \x01(\t"\xe3\x01\n\x13HealthCheckResponse\x12>\n\x06status\x18\x01 \x01(\x0e\x32..authservice.HealthCheckResponse.ServingStatus"\x8b\x01\n\rServingStatus\x12\x1a\n\x16SERVING_STATUS_UNKNOWN\x10\x00\x12\x1a\n\x16SERVING_STATUS_SERVING\x10\x01\x12\x1e\n\x1aSERVING_STATUS_NOT_SERVING\x10\x02\x12"\n\x1eSERVING_STATUS_SERVICE_UNKNOWN\x10\x03\x32\xa6\x01\n\x06Health\x12L\n\x05\x43heck\x12\x1f.authservice.HealthCheckRequest\x1a .authservice.HealthCheckResponse"\x00\x12N\n\x05Watch\x12\x1f.authservice.HealthCheckRequest\x1a .authservice.HealthCheckResponse"\x00\x30\x01\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "proto.health.v1.health_pb2", _globals
)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_HEALTHCHECKREQUEST"]._serialized_start = 45
    _globals["_HEALTHCHECKREQUEST"]._serialized_end = 82
    _globals["_HEALTHCHECKRESPONSE"]._serialized_start = 85
    _globals["_HEALTHCHECKRESPONSE"]._serialized_end = 312
    _globals["_HEALTHCHECKRESPONSE_SERVINGSTATUS"]._serialized_start = 173
    _globals["_HEALTHCHECKRESPONSE_SERVINGSTATUS"]._serialized_end = 312
    _globals["_HEALTH"]._serialized_start = 315
    _globals["_HEALTH"]._serialized_end = 481
# @@protoc_insertion_point(module_scope)
