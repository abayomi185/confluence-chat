from os import environ


def process_llm_response(llm_response):
    sources = []
    for source in llm_response["source_documents"]:
        page_id = source.metadata["source"].split("page_")[-1].split(".txt")[0]
        sources.append(
            f"{environ['ATLASSIAN_URL']}/wiki/spaces/{environ['ATLASSIAN_SPACE']}/pages/{page_id}"
        )

    sources_str = ",\n".join(sources)

    return f"""
    {llm_response['result']}
    \nSources:
    {sources_str}
    """
