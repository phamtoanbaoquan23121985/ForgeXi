# ForgeXi Authentication Architecture

ForgeXi separates authentication from agent reasoning, tools, trajectories, and evidence.

## Nebius AI Cloud
Nebius AI Cloud APIs support bearer access tokens. User access tokens can be obtained through the Nebius CLI/SDK. For service accounts, the documented flow is an authorized public key plus a short-lived RS256 JWT, exchanged through the Nebius IAM TokenExchange service for an access token. ForgeXi consumes only the resulting bearer credential and its expiry; private-key and JWT operations stay outside agent/evidence code.

## Token Factory
Current public Token Factory examples authenticate inference with a Token Factory API key. ForgeXi therefore declares Token Factory API-key auth as a distinct capability. It does not assume that an AI Cloud IAM token is accepted by Token Factory.

## Negotiation
Authentication is fail-closed. A runtime declares supported capabilities; ForgeXi prefers short-lived IAM when that capability is explicitly supported, otherwise uses the endpoint's explicitly declared supported mechanism. It never guesses authentication from a hostname and never silently falls back after an authentication failure.

## Secret boundary
Credential values are excluded from normalized responses and evidence. Credential objects redact their representation. User IDs, organization IDs, private keys, JWTs, API keys, and bearer tokens must not be written to benchmark artifacts or trajectories.
