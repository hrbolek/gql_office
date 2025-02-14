import strawberry

from .EventGQLModel import EventMutations


@strawberry.federation.type(extend=True)
class Mutation(EventMutations):

    # from .FacilityGQLModel import (
    #     facility_insert,
    #     facility_update,
    #     facility_delete,
    # )

    # from .FacilityEventGQLModel import (
    #     facility_reservation_create,
    #     facility_reservation_update,
    #     facility_reservation_delete
    # )

    # from .FacilityTypeGQLModel import (
    #     facility_type_insert,
    #     facility_type_update,
    #     facility_type_delete
    # )
    pass