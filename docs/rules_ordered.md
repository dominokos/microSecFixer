Invariants

    | 1 | No service that performs authorization should perform any other business functionality. |
    | 2 | No service that performs authentication should perform any other business functionality. |
    | 3 | No service that performs logging should be connected to a central logging subsystem. |

Service creation

    | 4 | There should be a single service as entry point. |
    | 5 | There should be a single authorization service. |
    | 6 | There should be a single authentication service. |
    | 7 | There should be a single central logging subsystem. |
    | 8 | There should be a single service registry. |
    | 9 | There should be a single central secret store. |
        At least one
        | 10 | There should be a monitoring dashboard. |
        | 11 | There should be a message broker. |

Service stereotypes

    | 12 | All entry points should have a circuit breaker. | 
    | 13 | All entry points should have a load balancer. |
    | 14 | All entry points should perform authorization. |
    | 15 | All entry points should perform authentication. |
    | 16 | All services should perform logging. |
    | 17 | All services should sanitize logs. |
    | 18 | All service registries should have validation checks for incoming requests. |
        At least one
        | 19 | There should be a service limiting the number of login attempts. |

Flow creation

    | 20 | All services that perform logging should be connected to a message broker. |
    | 21 | All services should be connected to a monitoring dashboard. |

Flow stereotypes

    | 22 | All connections between services should be authorized. |
    | 23 | All connections between services should be authenticated. |
    | 24 | All connections between a service and an external entity should be encrypted. |
    | 25 | All connections between two services should be encrypted. |
