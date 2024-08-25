Invariants

    | 10 | No service that performs authorization should perform any other business functionality. |
    | 11 | No service that performs authentication should perform any other business functionality. |
    | 19 | No service that performs logging should be connected to a central logging subsystem. |

Service creation

    | 1 | There should be a single service as entry point. |
    | 8 | There should be a single authorization service. |
    | 9 | There should be a single authentication service. |
    | 16 | There should be a single central logging subsystem. |
    | 23 | There should be a single service registry. |
    | 25 | There should be a single central secret store. |
        At least one
        | 20 | There should be a monitoring dashboard. |
        | 17 | There should be a message broker. |

Service stereotypes

    | 2 | All entry points should have a circuit breaker. | 
    | 3 | All entry points should have a load balancer. |
    | 4 | All entry points should perform authorization. |
    | 5 | All entry points should perform authentication. |
    | 15 | All services should perform logging. |
    | 22 | All services should sanitize logs. |
    | 24 | All service registries should have validation checks for incoming requests. |
        At least one
        | 12 | There should be a service limiting the number of login attempts. |

Flow creation

    | 18 | All services that perform logging should be connected to a message broker. |
    | 21 | All services should be connected to a monitoring dashboard. |

Flow stereotypes

    | 6 | All connections between services should be authorized. |
    | 7 | All connections between services should be authenticated. |
    | 13 | All connections between a service and an external entity should be encrypted. |
    | 14 | All connections between two services should be encrypted. |
