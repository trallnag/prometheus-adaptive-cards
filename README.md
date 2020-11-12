# Prometheus Adaptive Cards

This project is on hold.

## PROJECT ON HOLD

After investing quite a few hours into this project I came to the realization
that it misses the target I set out to achieve. A simple opinionated generic
webhook handler that receives alert payloads from Prometheus Alertmanager,
processes the data and sends it off to a destination that accepts the Adaptive
Cards format. It should also support adding custom templates.

What I am about to end up with is a fairly complex app where a massive chunk
of code does not work on the actual templating but stuff like configuration
handling, route traversing, preprocessing, grouping and splitting of data,
generating target URLs from payload data and so on.

So this alone adds a lot of complexity. And if I now also want to add
customization of templating (for example with Jinja templates or straight up
Python script) it will become even messier.

And in the end I have another container that does nothing more than idle around
and wait for an occasional alert.

So for now this project is on hold. Nevertheless it contains good code I will
use for future projects. Especially the handling of the complex nested
configuration in YAML with Pydantic and Python Box turned out really nice.

## TODO

Consider going back to this project. Ideas to think about:

* Turn to project into a generic prometheus webhook proxy library that hands of
  	a set of preprocessed alert data sets to a to be implemented function and
  	sends the returned payloads to the respective targets.
* Make the project about a single defined target. For example MS Teams adaptive
  	cards. 
