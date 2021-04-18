To start the test app run

```
make up
```

The goal of this demo is to show these things:
- example setup of logging with Starlette-based app, though this lib is not focused on integrating logging but providing a context. Mostly for logging purposes.
- logging all requests and responses from the middleware
- manipulating context of the request-response cycle from view, which results in different logs depending on where the log is created
- how to use plugins that intercept relevant headers

Try this curl

```sh
curl --header "X-Request-ID: ffd391f9-5a76-46ab-8622-4e64b0616308" localhost:5000
```

You will see this request id in logs. That's because the middleware is using related plugin.
If no X-Request-ID is passed, it will create a new one.
