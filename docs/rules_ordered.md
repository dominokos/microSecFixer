Invariants

    | 1 | No service that performs authorization should perform any other business functionality. |
    | 2 | No service that performs authentication should perform any other business functionality. |

Service creation

    | 3 | There should be a single service as entry point. |
    | 4 | There should be a single authorization service. |
    | 5 | There should be a single authentication service. |
    | 6 | There should be a single central logging subsystem. |
    | 7 | There should be a single service registry. |
    | 8 | There should be a single central secret store. |
        At least one
        | 9 | There should be a monitoring dashboard. |
        | 10 | There should be a message broker. |

Service stereotypes

    | 11 | All entry points should have a circuit breaker. | 
    | 12 | All entry points should have a load balancer. |
    | 13 | All entry points should perform authorization. |
    | 14 | All entry points should perform authentication. |
    | 15 | All services should perform logging. |
    | 16 | All services should sanitize logs. |
    | 17 | All service registries should have validation checks for incoming requests. |
        At least one
        | 18 | There should be a service limiting the number of login attempts. |

Flow creation

    | 19 | All services that perform logging should be connected to a message broker. |
    | 20 | All services should be connected to a monitoring dashboard. |

Flow stereotypes

    | 21 | All connections between services should be authorized. |
    | 22 | All connections between services should be authenticated. |
    | 23 | All connections between a service and an external entity should be encrypted. |
    | 24 | All connections between two services should be encrypted. |

Cleanup

    | 25 | No service that performs logging should be connected to a central logging subsystem. |
