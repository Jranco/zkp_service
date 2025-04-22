# ZKP verifier (Fiat-Shamir)

A demo, server-side application, acting as a verifier in a Fiat-Shamir interactive zero-knowledge verification scheme.

# Requirements

* Python >= 3.12.1
* Pythin Django >= 5.0.1
* Django channels >= 3.0.3
* Django daphne >= 3.0.2

# Prerequisites

### Setup database

```
python3 manage.py makemigrations
python3 manage.py migrate
```

# Configuration

// TODO

# API

The application provides three main apis fullfiling the ZKP requirements for a verifier.

## Registration (/register)

An HTTP-POST request performing new user registration.
Acts as a wrapper of the original registration payload, which is agnostic to the current scheme, and ships the unique ZKP public key for the specific device-user pair.

The request body:

```
{
  "protocolType": {The name of the `zero-knowledge` protocol},
  "payload": {The registration payload required by the target api},
  "userID": {Unique user identifier},
  "key": {
    "n": {N part of the `zero-knowledge` public key},
    "v": {V part of the `zero-knowledge` public key}
  }
}

```

The scheme is agnostic of the main registration payload of the main application.

## Authentication (/authenticate)

A Websocket connection performing user authentication.
Acts as a wrapper of the original authentication payload and performs the ZKP interactive verification. This way it asserts the device to be an eligible one that has already been registered directly (first time) or indirectly (binded via another registered device) for the specific user.

The first message's content:

```
{
  "protocolType": {The name of the `zero-knowledge` protocol},
  "payload": {The authentication payload required by the target api},
  "userID": {Unique user identifier},
  "key": {
    "n": {N part of the `zero-knowledge` public key},
    "v": {V part of the `zero-knowledge` public key}
  }
  "initiatingNum": {A random session identifier initiating the interactive verification challenge.}
}

```

## New device binding (/bindNewDevice)



# Usage

Running the server:

```
python3 manage.py runserver {YOUR_IP}:{YOUR_PORT}
```