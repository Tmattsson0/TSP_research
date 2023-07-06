from amplify.amplify.client import FixstarsClient


def get_fixstars_client(time_limit):
    client = FixstarsClient()
    client.token = "e8YaqoJNdT5pM3kJjhXNXJW4yqgf25mW"
    client.parameters.timeout = time_limit  # Timeout is 5 seconds
    return client