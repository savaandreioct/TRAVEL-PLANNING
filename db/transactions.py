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


def get_user_by_token(rx, auth_token):
    query = """
    MATCH (n: Users {authToken: $auth_token}) RETURN n
    """
    result = rx.run(query, auth_token=auth_token)
    return result.single()


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


def create_visitor(tx, obj):
    query = """
        MERGE (s:Visitors {uuid: $uuid})
        ON CREATE SET s=$props
        ON MATCH SET s=$props
        RETURN s
        """
    result = tx.run(query, uuid=obj["uuid"], props=obj)
    return result.single()


def create_period(tx, obj):
    query = """
        MERGE (s:Periods {uuid: $uuid})
        ON CREATE SET s=$props
        ON MATCH SET s=$props
        RETURN s
        """
    result = tx.run(query, uuid=obj["uuid"], props=obj)
    return result.single()


def create_day(tx, obj):
    query = """
        MERGE (s:Days {uuid: $uuid})
        ON CREATE SET s=$props
        ON MATCH SET s=$props
        RETURN s
        """
    result = tx.run(query, uuid=obj["uuid"], props=obj)
    return result.single()


def create_baggage(tx, obj):
    query = """
        MERGE (s:Baggages {uuid: $uuid})
        ON CREATE SET s=$props
        ON MATCH SET s=$props
        RETURN s
        """
    result = tx.run(query, uuid=obj["uuid"], props=obj)
    return result.single()


def add_period_to_trip(tx, trip_id, period_id):
    query = """
        MATCH (t:Trips {uuid: $trip_id}), (u: Periods {uuid: $period_id})
        CREATE (t)-[r:HAS_PERIOD]->(u)
        """
    result = tx.run(query, trip_id=trip_id, period_id=period_id)
    return result.single()


def add_visitors_to_trip(tx, trip_id, user_id):
    query = """
        MATCH (t:Trips {uuid: $trip_id}), (v: Visitors {uuid: $user_id})
        CREATE (t)-[r:HAS_VISITORS]->(v)
        """
    result = tx.run(query, trip_id=trip_id, user_id=user_id)
    return result.single()


def add_days_to_period(tx, period_id, day_id):
    query = """
        MATCH (t:Periods {uuid: $period_id}), (v: Days {uuid: $day_id})
        CREATE (t)-[r:HAS_DAY]->(v)
        """
    result = tx.run(query, period_id=period_id, day_id=day_id)
    return result.single()


def add_baggage_to_visitor(tx, visitor_id, baggage_id):
    query = """
        MATCH (t:Visitors {uuid: $visitor_id}), (v: Baggages {uuid: $baggage_id})
        CREATE (t)-[r:HAS_BAGGAGE]->(v)
        """
    result = tx.run(query, visitor_id=visitor_id, baggage_id=baggage_id)
    return result.single()


def get_user_trips(tx, uuid):
    query = """
        MATCH (u:Users {uuid: $uuid})-[r:HAS_TRIP]->(n)
        RETURN n
        """
    result = tx.run(query, uuid=uuid)
    return list(result)


def get_trip_weather(tx, uuid):
    query = """
        MATCH (u:Trips {uuid: $uuid}) - [:HAS_PERIOD] -> (p) - [:HAS_DAY] -> (d) return d
        """
    result = tx.run(query, uuid=uuid)
    return list(result)


def get_trip_visitors(tx, uuid):
    query = """
        MATCH (t:Trips {uuid: $uuid})-[r:HAS_VISITORS]->(n)
        RETURN n
        """
    result = tx.run(query, uuid=uuid)
    return list(result)


def get_trip_info(rx, uuid):
    query = """
        MATCH (n:Trips {uuid: $uuid})
        RETURN n
        """
    result = rx.run(query, uuid=uuid)
    return result.single()


def get_visitor_baggage(tx, uuid):
    query = """
        MATCH (t:Baggages {uuid: $uuid}) 
        RETURN t
        """
    result = tx.run(query, uuid=uuid)
    return list(result)


def get_users(rx):
    query = """
    MATCH (n: Users) RETURN n
    """
    result = rx.run(query)
    return list(result)


def add_trip_to_user(tx, trip_id, user_id):
    query = """
    MATCH (t:Trips {uuid: $trip_id}), (u: Users {uuid: $user_id})
    CREATE (u)-[r:HAS_TRIP]->(t)
    """
    result = tx.run(query, trip_id=trip_id, user_id=user_id)
    return result.single()
