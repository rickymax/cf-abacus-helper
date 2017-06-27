Abacus Helper
===

A helper for CF service provider which using CF-Abacus.
To make service provider's life easier.


Building
---

Downloading CF CLI and setting up manifest

``` sh
./scripts/build.sh
```

Deploying to Cloud Foundry
---

``` sh
cf push
```


Usage
---

### Method: get
_HTTP request_:
```
GET /v1/helper/:service_instance_id
```

### JSON representation:
``` json
{
  "organization_id": "d92dfb6c-2395-4ee6-b7ba-18d002dbae0a",
  "space_id": "380cd390-2374-4524-bdd9-a0fa4082d450",
  "resource_id": [
    "iot-hub"
  ]
}
```
Fields:
* `"organization_id": "d92dfb6c-2395-4ee6-b7ba-18d002dbae0a"`
   GUID of the consumer's organization

* `"space_id": "380cd390-2374-4524-bdd9-a0fa4082d450"`
   GUID of the consumer's space (under organization)

* `"resource_id": ["iot-hub"]`
   Unique resource name which defined by the service provider
   Note: It's a feature tags provided by service instance
   Reference: [CF Service Instance Tags](https://docs.cloudfoundry.org/devguide/services/managing-services.html#instance-tags-update)
