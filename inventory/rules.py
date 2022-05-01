import rules


@rules.predicate
def location_is_owner(user, location):
    return location.owner == user


@rules.predicate
def location_is_manager(user, location):
    return location.management_team is not None and rules.is_group_member(
        str(location.management_team)
    )


@rules.predicate
def location_is_maintainer(user, location):
    return location.maintenance_team is not None and rules.is_group_member(
        str(location.maintenance_team)
    )


@rules.predicate
def object_is_owner(user, object):
    return object.owner == user


@rules.predicate
def object_is_manager(user, object):
    return object.management_team is not None and rules.is_group_member(
        str(object.management_team)
    )


@rules.predicate
def object_is_maintainer(user, object):
    return object.maintenance_team is not None and rules.is_group_member(
        str(object.maintenance_team)
    )


@rules.predicate
def sensor_is_object_owner(user, obj):
    return obj.object.owner == user


@rules.predicate
def sensor_is_object_manager(user, obj):
    return obj.object.management_team is not None and rules.is_group_member(
        str(obj.object.management_team)
    )


@rules.predicate
def sensor_is_object_maintainer(user, obj):
    return obj.object.maintenance_team is not None and rules.is_group_member(
        str(obj.object.maintenance_team)
    )


rules.add_perm(
    "inventory.view_location",
    (location_is_owner | location_is_manager | location_is_maintainer),
)
rules.add_perm("inventory.change_location", location_is_owner | location_is_manager)
rules.add_perm("inventory.delete_location", location_is_owner | location_is_manager)
rules.add_perm(
    "inventory.view_object",
    (object_is_owner | object_is_manager | object_is_maintainer),
)
rules.add_perm("inventory.change_object", object_is_owner | object_is_manager)
rules.add_perm("inventory.delete_object", object_is_owner)
rules.add_perm("inventory.add_sensor", sensor_is_object_owner)
rules.add_perm(
    "inventory.view_sensor",
    (sensor_is_object_owner | sensor_is_object_manager | sensor_is_object_maintainer),
)
rules.add_perm("inventory.change_sensor", sensor_is_object_owner)
rules.add_perm("inventory.delete_sensor", sensor_is_object_owner)
