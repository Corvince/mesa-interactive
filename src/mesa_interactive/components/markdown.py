import solara


def create_markdown(get_text):
    @solara.component
    def MarkDown(model):
        return solara.Markdown(get_text(model))

    return MarkDown
