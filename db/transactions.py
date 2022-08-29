def get_all_nodes(rx):
    result = rx.run("MATCH (n) RETURN n")
    return list(result)


def register(tx, obj):
    query = """
        MERGE (s:Users {uuid: $uuid})
        ON CREATE SET s=$props
        ON MATCH SET s=$props
        """
    result = tx.run(query, uuid=obj["uuid"], props=obj)
    return result.single()


def check_user(rx, email):
    query = """
    MATCH (n: Users {email: $email}) RETURN n
    """
    result = rx.run(query, email=email)
    return list(result)


def login(rx, username, password):
    query = """
    MATCH (n: Users {username: $username, password: $password}) RETURN n
    """
    result = rx.run(query, username=username, password=password)
    return result.single()


def get_user(rx, username):
    query = """
    MATCH (n: Users {username: $username}) RETURN n
    """
    result = rx.run(query, username=username)
    return result.single()


def create_trip(tx, obj):
    query = """
        MERGE (s:Trips {uuid: $uuid})
        ON CREATE SET s=$props
        ON MATCH SET s=$props
        """
    result = tx.run(query, uuid=obj["uuid"], props=obj)
    return result.single()


def add_trip_to_user(tx, trip_id, user_id):
    query = """
        MATCH (t:Trips {uuid: $trip_id}), (u: Users {uuid: $user_id})
        CREATE (u)-[r:HAS_TRIP]->(t)
        """
    result = tx.run(query, trip_id=trip_id, user_id=user_id)
    return result.single()


def get_user_trips(tx, username):
    query = """
        MATCH (u:Users {username: $username})-[r:HAS_TRIP]->(n)
        RETURN n
        """
    result = tx.run(query, username=username)
    return list(result)
