from bs4 import BeautifulSoup


def merge(
    path_to_template: str, path_to_content: str, path_to_output_directory: str = None
) -> str:
    """
    Merges a template with content and saves the result to a file if an output directory exists.
    In all cases the result of the merge is returned as a string.
    """
    episode_name = path_to_content.split("/")[-1]

    with open(path_to_template, "r") as html:
        template_markup = html.read()
    with open(path_to_content, "r") as html:
        content_markup = html.read()

    template_soup = BeautifulSoup(template_markup, "html.parser")
    content_soup = BeautifulSoup(content_markup, "html.parser")

    # replace the blank template article with the actual content article
    template_soup.find(attrs={"role": "article"}).replace_with(
        content_soup.find(attrs={"role": "article"})
    )

    for name in ["author", "episode", "date"]:
        header_meta = content_soup.find(attrs={"name": name})
        template_soup.head.insert(0, header_meta)

    if path_to_output_directory:
        with open(f"{path_to_output_directory}/{episode_name}", "w+") as file:
            file.write(str(template_soup))

    template_soup.smooth()

    return str(template_soup)
