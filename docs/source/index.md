# starlette-context

Middleware for Starlette that allows you to store and access the context data of a request. Can be used with logging so logs automatically use request headers such as x-request-id or x-correlation-id.

## Overview

starlette-context is a library that provides middleware components for the Starlette framework to maintain context data throughout the request-response cycle. It enables you to:

- Access request headers and metadata from anywhere in your application
- Propagate important identifiers like correlation IDs and request IDs
- Enrich your logs with request context information
- Store and retrieve custom data within a request's lifecycle

```{toctree}
---
maxdepth: 2
caption: Contents
---
quickstart
context
middleware
plugins
errors
testing
example
fastapi
contributing
license
changelog
```
