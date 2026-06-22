import sys
import os

services_dir = os.path.join(os.path.dirname(__file__), "services")
for svc in os.listdir(services_dir):
    svc_path = os.path.join(services_dir, svc)
    if os.path.isdir(svc_path):
        sys.path.insert(0, svc_path)
