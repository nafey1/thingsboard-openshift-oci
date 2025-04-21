# Openshift microservices deployment scripts

This folder containing scripts and Kubernetes resources configurations to run ThingsBoard in Microservices mode on Openshift cluster.

You can find the deployment guide by the [**link**](https://thingsboard.io/docs/user-guide/install/cluster/openshift-cluster-setup/).

Use the **openshift-oci** installation in the folder, as the default one does not bring the MQTT and HTTP pods cleanly.

In order for the Thingsboard MQTT to work correctly, create a route for mqtt and modify the service **tb-mqtt-transport** and change the ServiceType from **ClusterIP** to **NodePort**. Modify the listener and use the Nodeport exposed by he service.

```yaml
kind: Route
apiVersion: route.openshift.io/v1
metadata:
  name: tb-route-mqtt-transport
  namespace: thingsboard
  annotations:
    openshift.io/host.generated: 'true'
spec:
  host: tb-route-mqtt-transport-thingsboard.apps.thingsboard.openshift.solutions
  path: /api/v1
  to:
    kind: Service
    name: tb-mqtt-transport
    weight: 100
  port:
    targetPort: mqtt
  tls:
    termination: edge
  wildcardPolicy: None
status:
  ingress:
    - host: tb-route-mqtt-transport-thingsboard.apps.thingsboard.openshift.solutions
      routerName: default
      conditions:
        - type: Admitted
          status: 'True'
      wildcardPolicy: None
      routerCanonicalHostname: apps.thingsboard.openshift.solutions
```
> Modify the host part to your own domain
Source: https://github.com/thingsboard/thingsboard/issues/3637
