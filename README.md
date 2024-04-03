# Logging Configuration

Sweater logging is meant to be a simple python package that allows for easy
configuration of python logging.  There are 2 configurations: dev and production.
By default, the dev configuration is used.  The production configuration is used
when one of the following conditions are met:

* The environment variable `ENV` is set to `prod`, `production`, or `staging`
* The environment variable `ENVIRONMENT` is set to `prod`, `production`, or `staging`
* The environment variable `JSON_LOGGING` is set (value is ignored)
* The `init()` function of `sweater_logging` is called with `json_logs=True`.


