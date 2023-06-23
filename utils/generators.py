import datetime
import re

def create_content_metadata_v2(variant):
    if len(variant) < 1:
        raise ValueError("Variant must contain at least one character.")
    return {"variant": variant}


def create_content_response_v2(content, effective_reference, documentation):
    return {
        "content": content,
        "effectiveReference": effective_reference,
        "documentation": documentation
    }


def validate_hash(hash):
    pattern = re.compile("^([0-9a-fA-F]{8,64})?((?:([~*^])([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[.][0-9]{1,9}Z|([0-9]+)))*)$")
    if not pattern.match(hash):
        raise ValueError("Hash is not valid.")
    return hash


# def create_commit_meta_v2(hash, committer, authors, all_signed_off_by, message, commit_time, author_time, all_properties, parent_commit_hashes, expected_hash=None):
#     validate_hash(hash)
#     return {
#         "hash": hash,
#         "committer": committer,
#         "authors": authors,
#         "allSignedOffBy": all_signed_off_by,
#         "message": message,
#         "commitTime": commit_time,
#         "authorTime": author_time,
#         "allProperties": all_properties,
#         "parentCommitHashes": parent_commit_hashes,
#         "expectedHash": expected_hash
#     }


def create_reference_metadata_v2(num_commits_ahead, num_commits_behind, commit_meta_of_head, common_ancestor_hash, num_total_commits):
    validate_hash(common_ancestor_hash)
    return {
        "numCommitsAhead": num_commits_ahead,
        "numCommitsBehind": num_commits_behind,
        "commitMetaOfHEAD": commit_meta_of_head,
        "commonAncestorHash": common_ancestor_hash,
        "numTotalCommits": num_total_commits
    }


def create_reference_v2(name, hash, metadata, type):
    validate_hash(hash)
    pattern = re.compile("^(?:[A-Za-z](?:(?:(?![.][.])[A-Za-z0-9./_-])*[A-Za-z0-9_-])?)|-$")
    if not pattern.match(name):
        raise ValueError("Name is not valid.")
    return {
        "name": name,
        "hash": hash,
        "metadata": metadata,
        "type": type
    }


def create_detached_v2(hash, metadata):
    validate_hash(hash)
    return {
        "hash": hash,
        "metadata": metadata
    }


def create_tag_v2(name, hash, metadata):
    validate_hash(hash)
    pattern = re.compile("^(?:[A-Za-z](?:(?:(?![.][.])[A-Za-z0-9./_-])*[A-Za-z0-9_-])?)|-$")
    if not pattern.match(name):
        raise ValueError("Name is not valid.")
    return {
        "name": name,
        "hash": hash,
        "metadata": metadata
    }

## Create a Commit Meta Object
def create_commit_meta_v2(hash, parent_commit_hashes, committer="committer", authors=["committer"], signed_off_by=["author"], message="a commit was made", properties={}, commit_time=None, author_time=None):
    
    if authors is None:
        Exception ("authors must be provided")
    if signed_off_by is None:
        Exception ("signed_off_by must be provided")
    if message is None:
        Exception ("message must be provided")
    if properties is None:
        Exception ("properties must be provided")
    if parent_commit_hashes is None:
        Exception ("parent_commit_hashes must be provided")
        
    commit_meta_v2 = {
        "hash": hash,
        "committer": committer,
        "authors": authors,
        "allSignedOffBy": signed_off_by,
        "message": message,
        "allProperties": properties,
        "parentCommitHashes": parent_commit_hashes,
    }

    # If commitTime and authorTime are not provided, use current UTC time
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    commit_meta_v2["commitTime"] = commit_time if commit_time else now
    commit_meta_v2["authorTime"] = author_time if author_time else now

    return commit_meta_v2

def create_content_key_v2(elements):
    if not elements:
        raise ValueError("Elements for ContentKey_V2 cannot be empty")
    return {
        "elements": elements
    }

def create_content_v2(content_type, **kwargs):
    if content_type == "ICEBERG_TABLE":
        return create_iceberg_table_v2(**kwargs)
    elif content_type == "DELTA_LAKE_TABLE":
        return create_delta_lake_table_v2(**kwargs)
    elif content_type == "ICEBERG_VIEW":
        return create_iceberg_view_v2(**kwargs)
    elif content_type == "NAMESPACE":
        return create_namespace_v2(**kwargs)
    elif content_type == "UDF":
        return create_udf_v2(**kwargs)
    else:
        return {}

def create_delta_lake_table_v2(id, metadata_location_history, checkpoint_location_history, last_checkpoint):
    return {
        "id": id,
        "type": "DELTA_LAKE_TABLE", # TODO: remove this once we have a better way to identify content type
        "metadataLocationHistory": metadata_location_history,
        "checkpointLocationHistory": checkpoint_location_history,
        "lastCheckpoint": last_checkpoint
    }

def create_udf_v2(id, sql_text, dialect):
    return {
        "id": id,
        "type": "UDF", # TODO: remove this once we have a better way to identify content type
        "sqlText": sql_text,
        "dialect": dialect
    }

def create_iceberg_table_v2(id, metadata_location, snapshot_id, schema_id, spec_id, sort_order_id):
    return {
        "id": id,
        "type": "ICEBERG_TABLE", # TODO: remove this once we have a better way to identify content type
        "metadataLocation": metadata_location,
        "snapshotId": snapshot_id,
        "schemaId": schema_id,
        "specId": spec_id,
        "sortOrderId": sort_order_id
    }

def create_iceberg_view_v2(id, metadata_location, version_id, schema_id, sql_text, dialect):
    return {
        "id": id,
        "type": "ICEBERG_VIEW", # TODO: remove this once we have a better way to identify content type
        "metadataLocation": metadata_location,
        "versionId": version_id,
        "schemaId": schema_id,
        "sqlText": sql_text,
        "dialect": dialect
    }

def create_namespace_v2(id, elements, properties):
    return {
        "id": id,
        "type": "NAMESPACE", # TODO: remove this once we have a better way to identify content type
        "elements": elements,
        "properties": properties
    }

def create_content_metadata_v2(variant):
    if not variant:
        raise ValueError("Variant for ContentMetadata_V2 cannot be empty")
    return {
        "variant": variant
    }

def create_documentation_v2(mime_type, text):
    if not mime_type or not text:
        raise ValueError("MimeType and Text for Documentation_V2 cannot be empty")
    return {
        "mimeType": mime_type,
        "text": text
    }

def create_put_v2(key_elements, content_kwargs, metadata_variant, documentation_kwargs=None):
    return {
        "type": "PUT",
        "key": create_content_key_v2(key_elements),
        "content": create_content_v2(**content_kwargs),
        "metadata": [create_content_metadata_v2(metadata_variant)],
        "documentation": create_documentation_v2(**documentation_kwargs) if documentation_kwargs else None
    }

def create_unchanged_v2(key_elements):
    return {
        "type": "UNCHANGED",
        "key": create_content_key_v2(key_elements)
    }

def create_delete_v2(key_elements):
    return {
        "type": "DELETE",
        "key": create_content_key_v2(key_elements)
    }

def create_operation_v2(key_elements, operation_type, **kwargs):
    operation_v2 = {
        "key": create_content_key_v2(key_elements)
    }
    
    if operation_type.lower() == "put":
        operation_v2.update(create_put_v2(key_elements, **kwargs))
    elif operation_type.lower() == "unchanged":
        operation_v2.update(create_unchanged_v2(key_elements, **kwargs))
    elif operation_type.lower() == "delete":
        operation_v2.update(create_delete_v2(key_elements, **kwargs))
    else:
        raise ValueError(f"Unsupported operation type: {operation_type}")
    
    return operation_v2

def create_operations(commit_meta, operations):
    return {
        "commitMeta": commit_meta,
        "operations": operations
    }