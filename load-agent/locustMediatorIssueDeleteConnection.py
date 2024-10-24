from locust import SequentialTaskSet, task, User, between
from locustClient import CustomClient
import time
import inspect
import json

import fcntl
import os
import signal

WITH_MEDIATION = os.getenv("WITH_MEDIATION")

class CustomLocust(User):
    abstract = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.client = CustomClient(self.host)

class UserBehaviour(SequentialTaskSet):
    def on_start(self):
        self.client.startup(withMediation=bool(WITH_MEDIATION))
        self.get_invite()
        self.accept_invite()
        self.delete_connection()

    def on_stop(self):
        self.client.shutdown()


    def get_invite(self):
        invite = self.client.issuer_getinvite()
        self.invite = invite


    def accept_invite(self):
        self.client.ensure_is_running()

        connection = self.client.accept_invite(self.invite['invitation_url'])
        self.connection = connection


    
    def delete_connection(self):
        self.client.delete_oob()

        
    @task
    def ping_mediator(self):
        self.client.ensure_is_running()

        self.client.ping_mediator()


class Issue(CustomLocust):
    tasks = [UserBehaviour]
    wait_time = between(float(os.getenv('LOCUST_MIN_WAIT',0.1)), float(os.getenv('LOCUST_MAX_WAIT',1)))
#    host = "example.com"
