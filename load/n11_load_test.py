from locust import HttpUser, TaskSet, task, between

TEXTS = [
    "Nike",
    "Adidas",
    "erkek",
    "LG",
    "Huawei",
    "ZTE",
    "Samsung",
    "iPhone",
]

search_url = "/arama?q={query}"


class UserBehavior(TaskSet):

    @task
    def keyword(self):
        for word in TEXTS:
            self.client.get(search_url.format(query=word))


class AnonymousUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 10)
