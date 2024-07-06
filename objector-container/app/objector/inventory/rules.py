import rules


@rules.predicate
def location_is_owner(user, location):
    return rules.is_authenticated(user) is True and location.owner == user


@rules.predicate
def location_is_manager(user, location):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(location.management_group)).exists()
    )


@rules.predicate
def location_is_maintainer(user, location):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(location.maintenance_group)).exists()
    )


@rules.predicate
def object_is_owner(user, object):
    return rules.is_authenticated(user) and object.owner == user


@rules.predicate
def object_is_manager(user, object):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(object.management_group)).exists()
    )


@rules.predicate
def object_is_maintainer(user, object):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(object.maintenance_group)).exists()
    )


@rules.predicate
def sensor_is_object_owner(user, sensor):
    return rules.is_authenticated(user) and sensor.object.owner == user


@rules.predicate
def sensor_is_object_manager(user, sensor):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(sensor.object.management_group)).exists()
    )


@rules.predicate
def sensor_is_object_maintainer(user, sensor):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(sensor.object.maintenance_group)).exists()
    )


rules.add_perm("inventory.add_location", rules.is_staff)
rules.add_perm(
    "inventory.view_location",
    (location_is_owner | location_is_manager | location_is_maintainer),
)
rules.add_perm("inventory.change_location", location_is_owner | location_is_manager)
rules.add_perm("inventory.delete_location", location_is_owner | location_is_manager)

rules.add_perm("inventory.add_object", rules.is_staff)
rules.add_perm(
    "inventory.view_object",
    (object_is_owner | object_is_manager | object_is_maintainer),
)
rules.add_perm("inventory.change_object", object_is_owner | object_is_manager)
rules.add_perm("inventory.delete_object", object_is_owner)

rules.add_perm("inventory.add_sensor", rules.is_staff)
rules.add_perm(
    "inventory.view_sensor",
    (sensor_is_object_owner | sensor_is_object_manager | sensor_is_object_maintainer),
)
rules.add_perm("inventory.change_sensor", sensor_is_object_owner)
rules.add_perm("inventory.delete_sensor", sensor_is_object_owner)
