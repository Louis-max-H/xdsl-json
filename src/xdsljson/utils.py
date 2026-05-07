import textwrap


def print_two_columns(
    left: str,
    right: str,
    width: int = 80,
    separator: str = " | ",
) -> None:
    """Affiche deux textes côte à côte dans deux colonnes de ``width`` caractères.

    Les lignes dont la longueur dépasse ``width`` sont repliées (wrappées).
    Les colonnes sont séparées par ``separator``.
    """

    def wrap(text: str) -> list[str]:
        wrapped: list[str] = []
        for line in text.splitlines() or [""]:
            if not line:
                wrapped.append("")
                continue
            wrapped.extend(
                textwrap.wrap(
                    line,
                    width=width,
                    drop_whitespace=False,
                    replace_whitespace=False,
                    expand_tabs=False,
                )
                or [""]
            )
        return wrapped

    left_lines = wrap(left)
    right_lines = wrap(right)

    nb_lines = max(len(left_lines), len(right_lines))
    left_lines.extend([""] * (nb_lines - len(left_lines)))
    right_lines.extend([""] * (nb_lines - len(right_lines)))

    for left_line, right_line in zip(left_lines, right_lines):
        print(f"{left_line:<{width}}{separator}{right_line:<{width}}")
