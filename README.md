# mextmock

## Description

This project is a mock of an extension for the Marketplace platform.

This mock only subscribes to platform events related to the **Order** business object. It provides a filter to only receive events when the attribute status of the order is `Processing`.
It just acknowledges the event and dumps the event data to stdout.

