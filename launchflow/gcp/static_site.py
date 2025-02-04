from dataclasses import dataclass
from typing import List, Optional

from launchflow import exceptions
from launchflow.gcp.gcs import BackendBucket
from launchflow.gcp.service import GCPStaticService
from launchflow.models.enums import ServiceProduct
from launchflow.node import Inputs
from launchflow.resource import Resource
from launchflow.service import DNSOutputs, DNSRecord, StaticServiceOutputs


@dataclass
class StaticSiteInputs(Inputs):
    pass


# TODO: Add docs
class StaticSite(GCPStaticService):
    """A service hosted on Google Cloud Platform that serves static files.

    ### Example Usage
    ```python
    import launchflow as lf

    website = lf.gcp.StaticSite("my-website", static_directory="path/to/local/files")
    ```
    """

    product = ServiceProduct.GCP_STATIC_SITE.value

    def __init__(
        self,
        name: str,
        # static inputs
        static_directory: str,
        *,
        static_ignore: List[str] = [],
        wait_for_cdn_invalidation: bool = False,
        # backend bucket inputs
        region: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> None:
        """Creates a new Cloud Run service.

        **Args:**
        - `name (str)`: The name of the service.
        - `static_directory (str)`: The directory of static files to serve. This should be a relative path from the project root where your `launchflow.yaml` is defined.
        - `static_ignore (List[str])`: A list of files to ignore when deploying the service. This can be in the same syntax you would use for a `.gitignore`.
        - `region (Optional[str])`: The region to deploy the service to.
        - `domain (Optional[str])`: The custom domain to map to the service.
        """
        super().__init__(
            name=name,
            static_directory=static_directory,
            static_ignore=static_ignore,
        )
        self.region = region
        self.domain = domain
        self.wait_for_cdn_invalidation = wait_for_cdn_invalidation

        # TODO: make this configurable
        self._backend_bucket = BackendBucket(
            name=name,
            force_destroy=True,
            custom_domain=domain,
            main_page_suffix="index.html",
            not_found_page="404.html",
        )

    def inputs(self) -> StaticSiteInputs:
        return StaticSiteInputs()

    def resources(self) -> List[Resource]:
        return [self._backend_bucket]

    def outputs(self) -> StaticServiceOutputs:
        try:
            backend_bucket_outputs = self._backend_bucket.outputs()
        except exceptions.ResourceOutputsNotFound:
            raise exceptions.ServiceOutputsNotFound(service_name=self.name)

        service_url = f"http://{backend_bucket_outputs.cdn_ip_address}"
        dns_outputs = None

        if self.domain:
            service_url = f"https://{self.domain}"
            dns_outputs = DNSOutputs(
                domain=self.domain,
                dns_records=[
                    DNSRecord(
                        dns_record_value=backend_bucket_outputs.cdn_ip_address,
                        dns_record_type="A",
                    ),
                ],
            )

        service_outputs = StaticServiceOutputs(
            service_url=service_url,
            dns_outputs=dns_outputs,
        )
        service_outputs.gcp_id = backend_bucket_outputs.gcp_id

        return service_outputs
