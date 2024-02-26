from uuidGenerator import OpaqueId


def get_uuid_from_id(id, iso='fr'):
    return OpaqueId.generate_uuid(int(id), iso)


def get_id_from_uuid(uuid):
    return str(OpaqueId.uuid_to_id(uuid))
