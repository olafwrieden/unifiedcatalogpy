def format_base_url(account_id: str) -> str:
    """
    Format the base URL for the Unified Catalog API.

    :param account_id: The guid of the Microsoft Purview account.
    :return: The formatted base URL.
    """
    return f"https://{account_id}-api.purview-service.microsoft.com/datagovernance"
