## FirebaseStaticSite

A service hosted on Firebase Hosting.

### Example Usage
```python
import launchflow as lf

website = lf.gcp.FirebaseStaticSite("my-website", static_directory="path/to/local/files")
```

### initialization

Creates a new Cloud Run service.

**Args:**
- `name (str)`: The name of the service.
- `static_directory (str)`: The directory of static files to serve. This should be a relative path from the project root where your `launchflow.yaml` is defined.
- `static_ignore (List[str])`: A list of files to ignore when deploying the service. This can be in the same syntax you would use for a `.gitignore`.
- `region (Optional[str])`: The region to deploy the service to.
- `domain (Optional[str])`: The custom domain to map to the service.
