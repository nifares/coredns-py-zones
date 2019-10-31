# coredns-py-zones

Automated DNS zones generation to use in you local network using CoreDNS deployed on Kubernetes cluster

## Getting Started

```pip install -r requirements```
```cp zones.json.example zones.json```
if not running as a Jenkins job
```export BUILD_NUMBER=<a serial number to use in dns zone>```
to make coredns automatically reload zone files it needs to be different from previous one.
```python create-zone.py```
```kubectl apply -f manifests```

## Authors

* **Nifares** - *Initial work* - [Nifares](https://github.com/nifares)

## License
