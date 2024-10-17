from .base import BaseIssuer
import json
import os
import requests
import time

class AcapyIssuer(BaseIssuer):
        
        def get_invite(self, out_of_band=False):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                

              # Regular Connection
                r = requests.post(
                        os.getenv("ISSUER_URL") + "/connections/create-invitation?auto_accept=true",
                        json={"metadata": {}, "my_label": "Test"},
                        headers=headers,
                )
                print(f" reponse from regular connection {r.text}")
                try_var = r.json()["invitation_url"]
                try_var1 = r.json()["connection_id"]
                print(f" ivitation irl is {try_var}")
                print(f" conneciton id is {try_var1}")


                # Ensure the request worked
                try:
                        try_var = r.json()["invitation_url"]
                except Exception:
                        raise Exception("Failed to get invitation url. Request: ", r.json())
                if r.status_code != 200:
                        raise Exception(r.content)

                r = r.json()

               
                
                return {
                        'type': r['type'], 
                        'id': r['id'],
                        'label': r['label'], 
                        'recipientKeys': r['recipientKeys'],
                        'serviceEndpoint': r['serviceEndpoint']
                }

        def is_up(self):
                try:
                        headers = json.loads(os.getenv("ISSUER_HEADERS"))
                        headers["Content-Type"] = "application/json"
                        r = requests.get(
                                os.getenv("ISSUER_URL") + "/status",
                                json={"metadata": {}, "my_label": "Test"},
                                headers=headers,
                        )
                        if r.status_code != 200:
                                raise Exception(r.content)

                        r = r.json()
                except:
                        return False

                return True

        def issue_credential(self, connection_id):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                issuer_did = os.getenv("CRED_DEF").split(":")[0]
                schema_parts = os.getenv("SCHEMA").split(":")

                r = requests.post(
                        os.getenv("ISSUER_URL") + "/issue-credential/send",
                        json={
                                "auto_remove": True,
                                "comment": "Performance Issuance",
                                "connection_id": connection_id,
                                "cred_def_id": os.getenv("CRED_DEF"),
                                "credential_proposal": {
                                "@type": "issue-credential/1.0/credential-preview",
                                "attributes": json.loads(os.getenv("CRED_ATTR")),
                                },
                                "issuer_did": issuer_did,
                                "schema_id": os.getenv("SCHEMA"),
                                "schema_issuer_did": schema_parts[0],
                                "schema_name": schema_parts[2],
                                "schema_version": schema_parts[3],
                                "trace": True,
                        },
                        headers=headers,
                )
                if r.status_code != 200:
                        raise Exception(r.content)

                r = r.json()

                return {
                        "connection_id": r["connection_id"], 
                        "cred_ex_id": r["credential_exchange_id"]
                }

        def revoke_credential(self, connection_id, credential_exchange_id):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                issuer_did = os.getenv("CRED_DEF").split(":")[0]
                schema_parts = os.getenv("SCHEMA").split(":")

                time.sleep(1)

                r = requests.post(
                        os.getenv("ISSUER_URL") + "/revocation/revoke",
                        json={
                                "comment": "load test",
                                "connection_id": connection_id,
                                "cred_ex_id": credential_exchange_id,
                                "notify": True,
                                "notify_version": "v1_0",
                                "publish": True,
                        },
                        headers=headers,
                )
                if r.status_code != 200:
                        raise Exception(r.content)

        def send_message(self, connection_id, msg):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                r = requests.post(
                        os.getenv("ISSUER_URL") + "/connections/" + connection_id + "/send-message",
                        json={"content": msg},
                        headers=headers,
                )
                r = r.json()
