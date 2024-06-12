import rules


@rules.predicate
def is_object_owner(user, object):
    return rules.is_authenticated(user) and object.object.owner == user


@rules.predicate
def is_object_manager(user, object):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(object.object.maintenance_group)).exists()
    )


@rules.predicate
def is_object_maintainer(user, object):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(object.object.maintenance_group)).exists()
    )


@rules.predicate
def is_sensor_object_owner(user, object):
    return rules.is_authenticated(user) and object.sensor.object.owner == user


@rules.predicate
def is_sensor_object_manager(user, object):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(object.object.maintenance_group)).exists()
    )


@rules.predicate
def is_sensor_object_maintainer(user, object):
    return (
        rules.is_authenticated(user)
        and user.groups.filter(name=str(object.object.maintenance_group)).exists()
    )


rules.add_perm("maintenance.add_task", rules.is_authenticated)
rules.add_perm(
    "maintenance.view_task",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm("maintenance.change_task", is_object_owner)
rules.add_perm("maintenance.delete_task", is_object_owner)

rules.add_perm("maintenance.add_journal", rules.is_authenticated)
rules.add_perm(
    "maintenance.view_journal",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm("maintenance.change_journal", is_object_owner)
rules.add_perm("maintenance.delete_journal", is_object_owner)

rules.add_perm(
    "maintenance.add_trigger",
    (is_sensor_object_owner | is_sensor_object_manager | is_sensor_object_maintainer),
)
rules.add_perm(
    "maintenance.view_trigger",
    (is_sensor_object_owner | is_sensor_object_manager | is_sensor_object_maintainer),
)
rules.add_perm("maintenance.change_trigger", is_sensor_object_owner)
rules.add_perm("maintenance.delete_trigger", is_sensor_object_owner)

rules.add_perm("maintenance.add_document", rules.is_authenticated)
rules.add_perm(
    "maintenance.view_document",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm("maintenance.change_document", is_object_owner)
rules.add_perm("maintenance.delete_document", is_object_owner)
