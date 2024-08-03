from extract_content_from_website import extract_website_content


def populate_sources(sources, num_elements):
    try:
        for i, source in enumerate(sources[:num_elements]):
            if not source:
                continue

            try:
                source['html'] = extract_website_content(source['link'])
                sources[i] = source
            except Exception as e:
                continue
    except Exception as e:
        print(f"Error in populate_sources: {e}")
        return sources

    return sources
