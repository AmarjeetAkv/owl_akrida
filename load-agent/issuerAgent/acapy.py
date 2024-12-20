import logging
from .base import BaseIssuer
import json
import os
import requests
import time

class AcapyIssuer(BaseIssuer):
        
        def get_invite(self, out_of_band=False):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                if out_of_band:
                        # Out of Band Connection 
                        # (ACA-Py v10.4 - only works with connections protocol, not DIDExchange) 
                        r = requests.post(
                                os.getenv("ISSUER_URL") + "/out-of-band/create-invitation?auto_accept=true", 
                                json={
                                "metadata": {}, 
                                "handshake_protocols": ["https://didcomm.org/didexchange/1.1"]
                                },
                                headers=headers
                        )
                else:
                        # Regular Connection
                        r = requests.post(
                                os.getenv("ISSUER_URL") + "/connections/create-invitation?auto_accept=true",
                                json={"metadata": {}, "my_label": "Test"},
                                headers=headers,
                        )

                        # Ensure the request worked
                        try:
                                try_var = r.json()["invitation_url"]
                        except Exception:
                                raise Exception("Failed to get invitation url. Request: ", r.json())
                        if r.status_code != 200:
                                raise Exception(r.content)

                r = r.json()

                # If OOB, need to grab connection_id
                if out_of_band:
                        invitation_msg_id = r['invi_msg_id']
                        g = requests.get(
                                os.getenv("ISSUER_URL") + "/connections",
                                params={"invitation_msg_id": invitation_msg_id},
                                headers=headers,
                        )
                        # Returns only one
                        connection_id = g.json()['results'][0]['connection_id']
                        r['connection_id'] = connection_id 
                
                return {
                        'invitation_url': r['invitation_url'], 
                        'connection_id': r['connection_id']
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
        


        def issue_credential_ver2_0(self, connection_id):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"
                
                issuer_did = os.getenv("CRED_DEF").split(":")[0]
                schema_parts = os.getenv("SCHEMA").split(":")
                payload = {
                        "auto_remove": True,
                        "comment": "Performance Issuance",
                        "connection_id": connection_id,
                        "credential_preview": {
                        "@type": "issue-credential/2.0/credential-preview",
                        "attributes": json.loads(os.getenv("CRED_ATTR")),
                        },
                        "filter": {
                        "indy": {
                                "cred_def_id": os.getenv("CRED_DEF"),
                                "issuer_did": issuer_did,
                                "schema_id": os.getenv("SCHEMA"),
                                "schema_issuer_did": schema_parts[0],
                                "schema_name": schema_parts[2],
                                "schema_version": schema_parts[3]
                        }
                        },
                        "trace": True,
                }
                r = requests.post(
                        os.getenv("ISSUER_URL") + "/issue-credential-2.0/send",
                        json=payload,
                        headers=headers
                )
                
                if r.status_code != 200:
                        raise Exception(r.content)

                r = r.json()
                return {
                        "connection_id": r["connection_id"], 
                        "cred_ex_id": r["cred_ex_id"]
                }


        def issue_non_revo_credential(self, connection_id):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"
                issuer_did = os.getenv("CRED_DEF_NR").split(":")[0]
                schema_parts = os.getenv("SCHEMA_NR").split(":")

                r = requests.post(
                        os.getenv("ISSUER_URL") + "/issue-credential/send",
                        json={
                                "auto_remove": True,
                                "comment": "Performance Issuance",
                                "connection_id": connection_id,
                                "cred_def_id": os.getenv("CRED_DEF_NR"),
                                "credential_proposal": {
                                "@type": "issue-credential/1.0/credential-preview",
                                "attributes": json.loads(os.getenv("CRED_ATTR_NR")),
                                },
                                "issuer_did": issuer_did,
                                "schema_id": os.getenv("SCHEMA_NR"),
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
        
        def delete_connection(self, connection_id):
                logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                url = os.getenv("ISSUER_URL") + "/connections/{conn_id}".format(conn_id=connection_id)

                r = requests.post(
                        url,
                        headers=headers,
                )

                # Log the response after deletion
                logging.info(f"The response after deletion is: {r.json()}")

                if r.status_code != 200:
                        raise Exception(r.content)

                return r.json()  # return the JSON response




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
                

        def revoke_non_revo_credential(self, connection_id, credential_exchange_id):
                headers = json.loads(os.getenv("ISSUER_HEADERS"))
                headers["Content-Type"] = "application/json"

                issuer_did = os.getenv("CRED_DEF_NR").split(":")[0]
                schema_parts = os.getenv("SCHEMA_NR").split(":")

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
