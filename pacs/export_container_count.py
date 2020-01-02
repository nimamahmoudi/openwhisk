import time
import traceback

# source: https://github.com/prometheus/client_python
from prometheus_client import Gauge, start_http_server

import docker
docker_client = docker.from_env()


def get_container_counts():
    counts = {}
    for container in docker_client.containers.list():
        try:
            img = container.attrs['Config']['Image']
            if 'openwhisk' in img and 'action' in img:
                name = container.name.split('_')[-1]
                env = img.split('/')[-1].split(':')[0].replace('action', '').replace('-', '')
                tag = name + '-' + env
                if tag in counts:
                    counts[tag]['count'] += 1
                else:
                    counts[tag] = {
                        'count': 1,
                        'name': name,
                        'env': env,
                    }
        except Exception:
            traceback.print_exc()

    return counts

g = Gauge('pacs_container_count', 'A count for the number of containers running each function', ['tag', 'name', 'env'])

print('starting server...', end=' ')
start_http_server(8001)
print('done!')

while True:
    try:
        counts = get_container_counts()

        all_metrics = g._metrics.keys()
        # add 0 for apps that don't appear anymore
        for m in [m for m in all_metrics if m[0] not in counts]:
            counts[m[0]] = {
                'name': m[1],
                'env': m[2],
                'count': 0,
            }

        for k, v in counts.items():
            tag = k
            name = v['name']
            env = v['env']
            g.labels(tag=tag, name=name, env=env).set(v['count'])
    
    except Exception:
        traceback.print_exc()
    
    time.sleep(1)
    
