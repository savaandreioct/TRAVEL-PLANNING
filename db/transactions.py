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
