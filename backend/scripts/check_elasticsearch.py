import requests

def is_elasticsearch_running(url="http://localhost:9200"):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            print("Elasticsearch is running at", url)
        else:
            print("Elasticsearch returned unexpected status code:", r.status_code)
    except requests.exceptions.ConnectionError:
        print("Elasticsearch is not running at", url)

if __name__ == "__main__":
    is_elasticsearch_running()
