# NessieV2Client

`NessieV2Client` is a class to interact with the Nessie V2 API. It includes methods to retrieve, create, and manipulate references (branches and tags), and their associated contents and commits.

---

## Class Initialization
`NessieV2Client(config: Dict)`

This initializes the class with a configuration dictionary. The configuration should include an endpoint, authentication details, SSL verification preference, and a default branch.

**Parameters:**
- `config`: A dictionary containing the configurations. 

---

## Class Methods

---

### setup_auth()

This method sets up the authentication based on the provided authentication type in the configuration. Supported types are 'none', 'bearer', 'aws', and 'basic'. 

**Returns:** 
- An authentication object for the requests.

---

### get_config()

This method sends a GET request to the `/config` endpoint to retrieve the configuration details.

**Returns:**
- A JSON object containing the configuration details.

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

---

### get_hash(name)

This method retrieves the hash of a given branch or tag.

**Parameters:**
- `name`: The name of the branch or tag.

**Returns:**
- The hash of the branch or tag.

---

### create_reference(name, ref_type="BRANCH", source_reference={"name":"main"})

This method creates a new branch or tag in the repository. 

**Parameters:**
- `name`: Name of the new branch or tag.
- `ref_type`: Type of the new reference ('BRANCH' or 'TAG').
- `source_reference`: Source reference data (should be a dictionary representing the reference object).

**Returns:**
- A JSON object representing the created reference.

---

### create_commit(operations, branch="main")

This method creates a new commit on a branch. 

**Parameters:**
- `operations`: The operations to be committed.
- `branch`: The branch on which to commit. Defaults to "main".

**Returns:**
- A JSON object representing the commit.

---

### create_merge(merge, branch="main")

This method merges changes into a branch.

**Parameters:**
- `merge`: The merge operation details.
- `branch`: The target branch. Defaults to "main".

**Returns:**
- A JSON object representing the merge.

---

### create_transplant(transplant, branch="main")

This method transplants changes onto a branch.

**Parameters:**
- `transplant`: The transplant operation details.
- `branch`: The target branch. Defaults to "main".

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

---

### get_commit_log(from_ref: str, to_ref: str, author: Optional[str]=None, committer: Optional[str]=None, max_records: Optional[int]=None, page_token: Optional[str]=None)

This method retrieves the commit log between two references.

**Parameters:**
- `from_ref`: The reference from which to start.
- `to_ref`: The reference to compare.
- `author`: Filter the results by author.
- `committer`: Filter the results by committer.
- `max_records`: The maximum number of records to return.
- `page_token`: Paging continuation token.

**Returns:**
- A JSON object containing the commit log between two references.

---

### get_value(branch: str, key: str)

This method retrieves a value from a branch.

**Parameters:**
- `branch`: The branch to query.
- `key`: The key of the value.

**Returns:**
- A JSON object containing the requested value.

---

### put_value(branch: str, key: str, value: dict)

This method inserts or updates a value in a branch.

**Parameters:**
- `branch`: The branch to update.
- `key`: The key of the value.
- `value`: The new value to insert or update.

**Returns:**
- A JSON object representing the put operation.

---

### delete_value(branch: str, key: str)

This method deletes a value from a branch.

**Parameters:**
- `branch`: The branch to update.
- `key`: The key of the value to delete.

**Returns:**
- A JSON object representing the delete operation.

---

### get_contents(branch: str, path: str, fetch: Optional[str]=None)

This method retrieves the contents of a path on a branch.

**Parameters:**
- `branch`: The branch to query.
- `path`: The path of the contents to retrieve.
- `fetch`: Specifies how much extra information is to be retrieved from the server.

**Returns:**
- A JSON object containing the requested contents.

---

### put_contents(branch: str, path: str, contents: dict)

This method inserts or updates the contents of a path on a branch.

**Parameters:**
- `branch`: The branch to update.
- `path`: The path of the contents to insert or update.
- `contents`: The new contents to insert or update.

**Returns:**
- A JSON object representing the put operation.

---

### delete_contents(branch: str, path: str)

This method deletes the contents of a path on a branch.

**Parameters:**
- `branch`: The branch to update.
- `path`: The path of the contents to delete.

**Returns:**
- A JSON object representing the delete operation.

---