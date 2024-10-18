import {
  AnonCredsCredentialFormatService,
  AnonCredsModule,
  AnonCredsProofFormatService,
  LegacyIndyCredentialFormatService,
  LegacyIndyProofFormatService,
  V1CredentialProtocol,
  V1ProofProtocol,
} from "@credo-ts/anoncreds";

import {
  IndyVdrAnonCredsRegistry,
  IndyVdrIndyDidResolver,
  IndyVdrModule,
  IndyVdrIndyDidRegistrar,
} from "@credo-ts/indy-vdr";

// var indySdk = require('indy-sdk')
import { AskarModule, AskarMultiWalletDatabaseScheme } from "@credo-ts/askar";
// import { ariesAskar } from '@hyperledger/aries-askar-react-native'
// import { AskarModule } from '@aries-framework/askar'

import {
  AutoAcceptCredential,
  AutoAcceptProof,
  DidsModule,
  ProofsModule,
  V2ProofProtocol,
  CredentialsModule,
  V2CredentialProtocol,
  ConnectionsModule,
  W3cCredentialsModule,
  KeyDidRegistrar,
  KeyDidResolver,
  CacheModule,
  InMemoryLruCache,
  WebDidResolver,
  HttpOutboundTransport,
  WsOutboundTransport,
  LogLevel,
  Agent,
  JsonLdCredentialFormatService,
  DifPresentationExchangeProofFormatService,
  MediationRecipientModule,
  MediatorPickupStrategy,
  ConnectionInvitationMessage,
  AgentEventTypes,
  CredentialEventTypes,
  ProofEventTypes,
  MediatorModule,
  DidCommMimeType,
  TransportEventTypes,
  TrustPingEventTypes,
  DidExchangeState,
  ConnectionEventTypes,
  DidRepository,
  CredentialState,
  ProofState,
  BasicMessageEventTypes,
} from "@credo-ts/core";
import { anoncreds } from "@hyperledger/anoncreds-nodejs";
import { ariesAskar } from "@hyperledger/aries-askar-nodejs";
import { indyVdr } from "@hyperledger/indy-vdr-nodejs";
import {
  agentDependencies,
  HttpInboundTransport,
  WsInboundTransport,
} from "@credo-ts/node";

var config = require("./config.js");
var deferred = require("deferred");
var process = require("process");

// console.log("config: ", config);
// console.log("deferred: ", deferred);
// console.log("process: ", process);

const characters =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

function generateString(length) {
  let result = "";
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }

  return result;
}

console.log("Genrate string wallet id", generateString(32));
console.log("Genrate string wallet key", generateString(32));

console.log("Test script is running");
console.log("test.ts file read successfully!!");
