# NessieV2Client

`NessieV2Client` is a class to interact with the Nessie V2 API. It includes methods to retrieve, create, and manipulate references (branches and tags), and their associated contents and commits.

---

## Class Initialization
`NessieV2Client(config: Dict)`

This initializes the class with a configuration dictionary. The configuration should include an endpoint, authentication details, SSL verification preference, and a default branch.

**Parameters:**
- `config`: A dictionary containing the configurations. 

```python

from nessiev2_unofficial.client import NessieV2Client

config = { 
          "endpoint": "http://0.0.0.0:19120/api/v2",
          "verify": False,
          "default_branch": "main",
          "auth": {
              "type": "none",
              "timeout": 10
          }
        }

client = NessieV2Client(config)
```

---

## Class Methods

---

### setup_auth()

This method sets up the authentication based on the provided authentication type in the configuration. Supported types are 'none', 'bearer', 'aws', and 'basic'. 

**Returns:** 
- An authentication object for the requests.

**This Method is used in all the other methods automatically**

---

### get_config()

This method sends a GET request to the `/config` endpoint to retrieve the configuration details.

**Returns:**
- A JSON object containing the configuration details.

```python
{
'defaultBranch': 'main', 
'minSupportedApiVersion': 1, 
'maxSupportedApiVersion': 2, 
'actualApiVersion': 2, 
'specVersion': '2.1.0', 
'noAncestorHash': '2e1cfa82b035c26cbbbdae632cea070514eb8b773f616aaeaf668e2f0be8f10d', 
'repositoryCreationTimestamp': '2023-06-30T02:03:05.387435066Z',
 'oldestPossibleCommitTimestamp': '2023-06-30T02:03:05.387435066Z'
}
```

---

### get_all_references(fetch=None, filter=None, max_records=None, page_token=None)

This method retrieves information about all the branches and tags from the `/trees` endpoint. 

**Parameters:**
- `fetch`: Specifies how much extra information is to be retrieved from the server.
- `filter`: A Common Expression Language (CEL) expression to filter the results.
- `max_records`: Maximum number of entries to return.
- `page_token`: Paging continuation token.

**Returns:**
- A JSON object containing information about all the branches and tags.

```python
{'token': None, 
'references': [
    {'type': 'BRANCH', 'name': 'main', 'hash': '2e1cfa82b035c26cbbbdae632cea070514eb8b773f616aaeaf668e2f0be8f10d'},
    {'type': 'BRANCH', 'name': 'test-branch', 'hash': 'fd97cf49f40ea092abe8f9b1ebccf2c14de8702c2c07f5d84da5898b7c49b28b'},
    {'type': 'BRANCH', 'name': 'test-branch3', 'hash': '3f52a463534cd31d312a65d61a35308b3124f9494e52892a16d1f6faa2543754'},
    {'type': 'BRANCH', 'name': 'test-branch4', 'hash': '2e1cfa82b035c26cbbbdae632cea070514eb8b773f616aaeaf668e2f0be8f10d'}
    ], 
    'hasMore': False
}
```

---

### get_hash(name)

This method retrieves the hash of a given branch or tag.

**Parameters:**
- `name`: The name of the branch or tag.

**Returns:**
- The hash of the branch or tag.

**Usage**
```python
client.get_hash("test-branch3")
```

**Response**
```python
be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c
```

---

### create_reference(name, ref_type="BRANCH", source_reference={"name":"main"})

This method creates a new branch or tag in the repository. 

**Parameters:**
- `name`: Name of the new branch or tag.
- `ref_type`: Type of the new reference ('BRANCH' or 'TAG').
- `source_reference`: Source reference data (should be a dictionary representing the reference object). By Default will use latest commit on the main branch.

**Returns:**
- A JSON object representing the created reference.

**Creating a Branch off the main branch**
```python
client.create_reference("test-branch4")
```

**Creating a tag off a commit on another branch**
```python
client.create_reference(name="test-tag",ref_type="TAG", source_reference={'type': 'BRANCH', 'name': 'test-branch3', 'hash': 'be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c'})
```

**Response**
```python
{'reference': {'type': 'TAG', 'name': 'test-tag', 'hash': 'be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c'}}
```

---

### create_commit(operations, branch="main")

This method creates a new commit on a branch. 

**Parameters:**
- `operations`: The operations to be committed.
- `branch`: The branch on which to commit. Defaults to "main".
- `hash`: hash to create commit from, will auto get latest hash if unspecified

*note: If a new table, then it should not have a hash or content id in the operation, but if an existing table it must have a content id that matches the existing entry.*

Example Operations for New Table
```python
operations = {
  "commitMeta": {
    "author": "authorName <authorName@example.com>",
    "authorTime": "2021-04-07T14:42:25.534748Z",
    "message": "Example Commit Message",
    "properties": {
      "additionalProp1": "xxx",
      "additionalProp2": "yyy",
      "additionalProp3": "zzz"
    },
    "signedOffBy": "signedOffByName <signedOffBy@example.com>"
  },
  "operations": [
    {
      "type": "PUT",
      "key": {
        "elements": [
          "table1"
        ]
      },
      "content": {
        "type": "ICEBERG_TABLE",
        "metadataLocation": "/path/to/metadata/",
        "snapshotId": 1,
        "schemaId": 2,
        "specId": 3,
        "sortOrderId": 4
      }
    }
  ]
}
```

For an Existing Table
```python
operations = {
  "commitMeta": {
    "author": "authorName <authorName@example.com>",
    "authorTime": "2021-04-07T14:42:25.534748Z",
    "message": "Example Commit Message",
    "properties": {
      "additionalProp1": "xxx",
      "additionalProp2": "yyy",
      "additionalProp3": "zzz"
    },
    "signedOffBy": "signedOffByName <signedOffBy@example.com>"
  },
  "operations": [
    {
      "type": "PUT",
      "key": {
        "elements": [
          "table1"
        ]
      },
      "content": {
        "type": "ICEBERG_TABLE",
        "id": "10df6e9b-890f-491e-821f-02dfeed3a847",
        "metadataLocation": "/path/to/metadata/",
        "snapshotId": 1,
        "schemaId": 2,
        "specId": 3,
        "sortOrderId": 4
      }
    }
  ]
}
```

*Refer to API Documentation for shape of other events like NAMESPACE, ICEBERG_VIEW, DELTA_TABLE, and more*

**Returns:**
- A JSON object representing the commit.

```python
{'targetBranch': 
    {
        'type': 'BRANCH',
        'name': 'test-branch3',
        'hash': 'bbef45ace9c7a32b47da0e1ad2f6a42003651250406beb9b156af71c58c0c657'
    }, 
    'addedContents': None
}
```

---

### create_merge(merge, branch="main")

This method merges changes into a branch.

**Parameters:**
- `merge`: The merge operation details.
- `branch`: The target branch. Defaults to "main".
- `hash`: hash to create commit from, will auto get latest hash if unspecified

**Returns:**
- A JSON object representing the merge.

**Sample Merge Operation**
```python
merge = {
  "fromHash": "be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c",
  "fromRefName": "test-branch3",
  "defaultKeyMergeMode": "NORMAL",
  "keyMergeModes": [
    {
      "key": {
        "elements": [
          "table1"
        ], 
      },
      "mergeBehavior": "FORCE"
    }
  ],
  "dryRun": False,
  "fetchAdditionalInfo": False,
  "returnConflictAsResult": True
}
```

**Usage**
```python
client.create_merge(branch="main", merge=merge)
```

---

### create_transplant(transplant, branch="main")

This method transplants changes onto a branch.

**Parameters:**
- `transplant`: The transplant operation details.
- `branch`: The target branch. Defaults to "main".
- `hash`: hash to create commit from, will auto get latest hash if unspecified

**Returns:**
- A JSON object representing the transplant.

---

### get_diff(from_ref: str, to_ref: str, filter: Optional[str]=None, key: list=None, max_key:str=None, max_records:int=None, min_key:str=None, page_token:str=None, prefix_key:str=None)

This method retrieves the differences between two references.

**Parameters:**
- `from_ref`: The reference from which to start.
- `to_ref`: The reference to compare.
- `filter`: A CEL expression to filter the results.
- `key`: A specific key to retrieve.
- `max_key`: The maximum key to include in the results.
- `max_records`: The maximum number of records to return.
- `min_key`: The minimum key to include in the results.
- `page_token`: Paging continuation token.
- `prefix_key`: The prefix key to include in the results.

**Returns:**
- A JSON object containing the differences between two references.


**Usage**
```python
client.get_diff(from_ref="test-branch3", to_ref="main")
```

**Response**
```python
{
  'token': None, 
  'diffs': [
    {'key': {
      'elements': ['table1']
      }, 
      'from': {
        'type': 'ICEBERG_TABLE', 
        'id': '10df6e9b-890f-491e-821f-02dfeed3a847', 
        'metadataLocation': '/path/to/metadata/', 
        'snapshotId': 1, 
        'schemaId': 2, 
        'specId': 3, 
        'sortOrderId': 4
        }, 
        'to': None
    }], 
  'effectiveFromReference': {
      'type': 'BRANCH', 
      'name': 'test-branch3', 
      'hash': 'be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c'
      }, 
  'effectiveToReference': {
        'type': 'BRANCH', 
        'name': 'main', 
        'hash': '2e1cfa82b035c26cbbbdae632cea070514eb8b773f616aaeaf668e2f0be8f10d'
        }, 
  'hasMore': False
}
```
---

### get_reference_details(ref: str, fetch: Optional[str]=None)

This method retrieves the details of a reference.

**Parameters:**
- `ref`: The reference to query.
- `fetch`: Specifies how much extra information is to be retrieved from the server.

**Returns:**
- A JSON object containing the details of the reference.

**Usage**
```python
client.get_reference_details(ref="test-branch3",fetch="ALL")
```

**Response**
```python
{
  'reference': {
    'type': 'BRANCH', 
    'name': 'test-branch3', 
    'metadata': {
      'numCommitsAhead': 12, 
      'numCommitsBehind': 0, 
      'commitMetaOfHEAD': {
        'hash': 'be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c', 
        'committer': '', 
        'authors': ['authorName <authorName@example.com>'], 
        'allSignedOffBy': ['signedOffByName <signedOffBy@example.com>'], 
        'message': 'Example Commit Message', 
        'commitTime': '2023-07-02T15:03:28.152849839Z', 
        'authorTime': '2021-04-07T14:42:25.534748Z', 
        'allProperties': {'additionalprop1': ['xxx'], 
        'additionalprop2': ['yyy'], 
        'additionalprop3': ['zzz']
        }, 
      'parentCommitHashes': ['0e4a7eeb89cfef6aaecc72d94a8ae06391bad7a0e710ce1b591ad4d9facdc7e0']}, 
      'commonAncestorHash': '2e1cfa82b035c26cbbbdae632cea070514eb8b773f616aaeaf668e2f0be8f10d', 
      'numTotalCommits': 12
      }, 
    'hash': 'be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c'
    }
  }
```
---

### set_reference(ref: str, body: dict, ref_type: Optional[str]=None)

This method sets the hash for a reference to the hash of another reference.

**Parameters:**
- `ref`: The reference to update.
- `body`: The body containing the new hash.
- `ref_type`: The type of the reference.

**Returns:**
- A JSON object representing the set operation.

---

### delete_reference(ref: str, ref_type: Optional[str]="BRANCH")

This method deletes a reference.

**Parameters:**
- `ref`: The reference to delete.
- `ref_type`: The type of the reference (defaults to "BRANCH").

```python
client.delete_reference("test-branch2")
```

**Returns:**
- A JSON object representing the delete operation.

---

### get_several_contents(ref: str, keys: List[str], with_doc=False)

This method retrieves the contents of multiple keys in a reference.

**Parameters:**
- `ref`: The reference to query.
- `keys`: The keys to retrieve.
- `with_doc`: Whether to include the document in the response.

```python
client.get_several_contents("test-branch3", keys=["table1"])
```

**Returns:**
- A JSON object containing the contents of the keys.

```python
{
    'contents': [
        {
            'key': {'elements': ['table1']}, 
            'content': {
                'type': 'ICEBERG_TABLE', 
                'id': '10df6e9b-890f-491e-821f-02dfeed3a847', 
                'metadataLocation': '/path/to/metadata/', 
                'snapshotId': 1, 
                'schemaId': 2, 
                'specId': 3, 
                'sortOrderId': 4
                }
            }
        ], 
        'effectiveReference': {
            'type': 'BRANCH', 
            'name': 'test-branch3', 
            'hash': 'be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c'
            }}
```

---

### get_multiple_contents_post(ref: str, keys: List[str], with_doc: Optional[bool]=False)

This method retrieves the contents of multiple keys in a reference using a POST request.

**Parameters:**
- `ref`: The reference to query.
- `keys`: The keys to retrieve.
- `with_doc`: Whether to include the document in the response.

```python
client.get_multiple_contents_post("test-branch3", keys=["table1"], with_doc=True)
```

**Returns:**
- A JSON object containing the contents of the keys.

```python
{
    'contents': [], 
    'effectiveReference': {
        'type': 'BRANCH', 
        'name': 'test-branch3', 
        'hash': 'be4277d9393c0ae13434d904bbcb91d2ca0688e03f5dc581ced61428247d276c'
        }
}
```

---

### get_content(ref: str, key, with_doc=False)

This method retrieves the content of a key in a reference.

**Parameters:**
- `ref`: The reference to query.
- `key`: The key to retrieve.
- `with_doc`: Whether to include the document in the response.

```python
client.get_content(ref="test-branch3", key="table1", with_doc=False)
```

**Returns:**
- A JSON object containing the content of the key.

```python
{
    'content': {
        'type': 'ICEBERG_TABLE', 
        'id': '10df6e9b-890f-491e-821f-02dfeed3a847', 
        'metadataLocation': '/path/to/metadata/', 
        'snapshotId': 1, 
        'schemaId': 2, 
        'specId': 3, 
        'sortOrderId': 4
        }, 
    'effectiveReference': {
        'type': 'BRANCH', 
        'name': 'test-branch3', 
        'hash': 'e9f2b15f38fa3d083b51b5a26f6d654ada56eb81b3204e6a1a9d0c75aa343244'
        }
    }
```
---

### get_entries(ref, content=None, filter=None, key=None, max_key=None, max_records=None, min_key=None, page_token=None, prefix_key=None)

This method retrieves the entries of a reference.

**Parameters:**
- `ref`: The reference to query.
- `content`, `filter`, `key`, `max_key`, `max_records`, `min_key`, `page_token`, `prefix_key`: Various parameters to filter and limit the results.

**Returns:**
- A JSON object containing the entries of the reference.


```python
{
    'token': None, 
    'entries': [
        {
            'type': 'ICEBERG_TABLE', 
            'name': {
                'elements': ['table1']}, 
                'contentId': '10df6e9b-890f-491e-821f-02dfeed3a847', 
                'content': None
                }
        ], 
    'effectiveReference': {
        'type': 'BRANCH', 
        'name': 'test-branch3', 
        'hash': 'bbef45ace9c7a32b47da0e1ad2f6a42003651250406beb9b156af71c58c0c657'
        }, 
    'hasMore': False}
```

---

### get_commit_log(ref, fetch=None, filter=None, limit_hash=None, max_records=None, page_token=None)

This method retrieves the commit log of a reference.

**Parameters:**
- `ref`: The reference to query.
- `fetch`, `filter`, `limit_hash`, `max_records`, `page_token`: Various parameters to filter and limit the results.

**Returns:**
- A JSON object containing the commit log of the reference.

```python
{
    'token': None, 
    'logEntries': [
        {
            'commitMeta': {
                'hash': 'bbef45ace9c7a32b47da0e1ad2f6a42003651250406beb9b156af71c58c0c657', 
                'committer': '', 
                'authors': ['authorName <authorName@example.com>'], 
                'allSignedOffBy': ['signedOffByName <signedOffBy@example.com>'], 
                'message': 'Example Commit Message', 
                'commitTime': '2023-06-30T23:03:39.461768304Z', 
                'authorTime': '2021-04-07T14:42:25.534748Z', 
                'allProperties': {
                    'additionalprop1': ['xxx'], 
                    'additionalprop2': ['yyy'], 
                    'additionalprop3': ['zzz']
                    }, 
                'parentCommitHashes': ['3f52a463534cd31d312a65d61a35308b3124f9494e52892a16d1f6faa2543754']
                }, 
            'parentCommitHash': '3f52a463534cd31d312a65d61a35308b3124f9494e52892a16d1f6faa2543754', 
            'operations': None
        }, 
        {
            'commitMeta': {
                'hash': '3f52a463534cd31d312a65d61a35308b3124f9494e52892a16d1f6faa2543754', 
                'committer': '', 
                'authors': ['authorName <authorName@example.com>'], 
                'allSignedOffBy': ['signedOffByName <signedOffBy@example.com>'], 
                'message': 'Example Commit Message', 
                'commitTime': '2023-06-30T23:00:38.857124001Z', 
                'authorTime': '2021-04-07T14:42:25.534748Z', 
                'allProperties': {
                    'additionalprop1': ['xxx'], 
                    'additionalprop2': ['yyy'], 
                    'additionalprop3': ['zzz']}, 
                    'parentCommitHashes': ['2e1cfa82b035c26cbbbdae632cea070514eb8b773f616aaeaf668e2f0be8f10d']
                }, 
            'parentCommitHash': '2e1cfa82b035c26cbbbdae632cea070514eb8b773f616aaeaf668e2f0be8f10d', 
            'operations': None
        }], 
    'hasMore': False
    }
```